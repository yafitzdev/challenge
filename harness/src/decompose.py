"""Decomposition: instead of one long session for the whole repository, the work is split into small requests.

1. Plan: a short session reads the Java repository and writes plan.json, one entry per Python module to create,
   with the Java file it ports and the modules it depends on. The harness adds every module the structure file
   lists and every module the public tests import, so the plan cannot leave out a module the tests need.
2. Modules: in dependency order, a fresh short session writes one module. Only that file is kept from the
   session; the modules it depends on already exist.
3. Retry (retry.py): a module whose public tests still fail is written again, up to `attempts` times.

Thesis: smaller requests mean less context, fewer hallucinations, better code.
"""
import json
import re
from pathlib import Path

from retry import PROMPTS, isolated_session, module_tests

PLAN_FILE = 'plan.json'
# With self_test, each module session also ports the Java unit test of its class and runs it. The test file is
# thrown away with the rest of the session's other files; it only gives the session a check where no public test
# covers the module (step 05: modules without public tests lost the most).
SELF_TEST = ('Also look for the Java unit test of this class in ../source/ (for example FooTest.java), port its '
             'cases to tests/scratch/test_this_module.py and run them as well; that file is only for your own '
             'check and is not kept.\n')


def listed_modules(structure_file):
    """Python files under src/ in the tree drawing of project_structure.txt (paths relative to candidate/)."""
    stack, modules = [], []
    for line in structure_file.read_text(encoding='utf-8', errors='replace').splitlines():
        match = re.search(r'[├└]── (.*)', line)
        if not match:
            continue
        depth = match.start() // 4
        name = match.group(1).split('#')[0].strip()
        if not name:
            continue
        stack[depth:] = [name.rstrip('/')]
        if stack[0] == 'src' and name.endswith('.py'):
            modules.append('/'.join(stack))
    return modules


def read_plan(candidate):
    try:
        plan = json.loads((candidate / PLAN_FILE).read_text(encoding='utf-8'))
        return [e for e in plan if isinstance(e, dict) and str(e.get('module', '')).startswith('src/')]
    except (OSError, ValueError, TypeError):
        return []


def order(entries):
    """Dependencies first; a cycle or an unknown dependency does not block (plan order then)."""
    by_module = {e['module']: e for e in entries}
    done, result = set(), []

    def visit(module, path):
        if module in done or module in path or module not in by_module:
            return
        for dep in by_module[module].get('depends_on') or []:
            visit(dep, path | {module})
        done.add(module)
        result.append(by_module[module])

    for e in entries:
        visit(e['module'], set())
    return result


def make_packages(candidate, planned):
    """Every package needs its __init__.py; an empty one is enough unless a session writes something else."""
    for entry in planned:
        folder = (candidate / entry['module']).parent
        folder.mkdir(parents=True, exist_ok=True)
        while folder != candidate and folder.name != 'src':
            (folder / '__init__.py').touch(exist_ok=True)
            folder = folder.parent


def decompose(config, workspace, output, run_agent):
    """Plan, then one session per module. Returns a record of what ran."""
    settings = config['decompose']
    candidate = workspace / 'candidate'
    session_config = {**config, 'max_assistant_turns': settings['max_assistant_turns'],
                      'migration_timeout_seconds': settings['timeout_seconds']}
    plan_config = {**session_config, 'max_assistant_turns': settings['plan_turns']}
    (output / 'plan').mkdir(parents=True)
    run_agent(plan_config, workspace, output / 'plan',
              (PROMPTS / 'task/decompose_plan.txt').read_text(encoding='utf-8'))
    planned = read_plan(candidate)
    # Modules the plan must not leave out: listed in project_structure.txt, or imported by a public test.
    known = {e['module'] for e in planned}
    listed = [m for m in listed_modules(candidate / 'project_structure.txt') if m not in known]
    planned += [{'module': m, 'java': None, 'depends_on': [], 'added_by_harness': True} for m in listed]
    make_packages(candidate, planned)
    # Only now, with the package folders in place, can a test's `from src.pkg import X` be told apart from a module.
    tests = module_tests(candidate)
    imported = [m for m in sorted(tests) if m not in {e['module'] for e in planned}]
    planned += [{'module': m, 'java': None, 'depends_on': [], 'added_by_harness': True} for m in imported]
    make_packages(candidate, planned)
    extra = listed + imported
    template = (PROMPTS / 'during_work/write_module.txt').read_text(encoding='utf-8')
    written = []
    # Package __init__.py files go last, so the classes they re-export already exist.
    ordered = order(planned)
    for entry in [e for e in ordered if not e['module'].endswith('__init__.py')] + \
                 [e for e in ordered if e['module'].endswith('__init__.py')]:
        module = entry['module']
        # An __init__.py needs its own session only when the plan lists what it imports or a test imports from it
        # (`from src.pkg import Name`); otherwise the empty one created above is enough.
        if module.endswith('__init__.py') and not (entry.get('java') or entry.get('depends_on') or module in tests):
            continue
        prompt = template.format(
            module=module, java=entry.get('java') or ('none: this is a package file; import and re-export the names the '
                                                      'tests import from this package' if module.endswith('__init__.py')
                                                      else 'find the Java class this module ports in ../source/'),
            done='\n'.join(f'- {m}' for m in written) or '- (none yet)',
            tests='\n'.join(f'- {t}' for t in tests.get(module, [])) or '- (no public test imports it directly)',
            self_test=SELF_TEST if settings.get('self_test') else '')
        name = module.removeprefix('src/').replace('/', '.')
        isolated_session(session_config, workspace, output / 'modules' / name, prompt, module, run_agent)
        written.append(module)
        print(f'module {module}: {"written" if (candidate / module).exists() else "missing"}', flush=True)
    return {'planned': len(planned), 'from_plan': len(known), 'added_by_harness': len(extra), 'modules': written}
