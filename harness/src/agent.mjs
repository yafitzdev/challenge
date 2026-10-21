// A single Pi SDK session. The Python runner (run.py) owns staging and final evaluation.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import {
  createAgentSession, createExtensionRuntime, ModelRuntime,
  SessionManager, SettingsManager,
} from '@earendil-works/pi-coding-agent';
import { EnvHttpProxyAgent, setGlobalDispatcher } from 'undici';
import { Type } from 'typebox';

// Pi's CLI routes HTTP through HTTPS_PROXY, but the SDK does not, so do it here.
// Needed in the cloud, where a proxy adds the API key; no effect when no proxy is set.
if (process.env.HTTPS_PROXY || process.env.https_proxy) setGlobalDispatcher(new EnvHttpProxyAgent());

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
// Every text the harness sends to a model lives in harness/prompts/.
const PROMPTS = new URL('../prompts/', import.meta.url);
const prompt = (name) => fs.readFileSync(new URL(`${name}.txt`, PROMPTS), 'utf8').replace(/\n$/, '');
const checkOnly = process.argv.includes('--check');
const cfg = job.config;
// run.py passes the key for the config's provider as MODEL_API_KEY.
const key = process.env.MODEL_API_KEY;
if (!checkOnly && !key) throw new Error('MODEL_API_KEY is missing');
// Keep the credential in this process, not in shell-tool environments.
delete process.env.MODEL_API_KEY;
const provider = cfg.provider || 'deepseek';
// DeepSeek needs its own thinking format; other OpenAI-compatible providers use the default.
const compat = provider === 'deepseek'
  ? { thinkingFormat: 'deepseek', supportsDeveloperRole: false, maxTokensField: 'max_tokens' }
  : { supportsDeveloperRole: false, maxTokensField: 'max_tokens' };
const redact = (text) => (key ? text.replaceAll(key, '[REDACTED]') : text);
const save = (name, value) => fs.writeFileSync(path.join(job.output, name), redact(JSON.stringify(value, null, 2)));
const state = path.join(job.output, 'pi-state');
fs.mkdirSync(state, { recursive: true });
const modelRuntime = await ModelRuntime.create({
  authPath: path.join(state, 'auth.json'), modelsPath: null,
  modelsStorePath: path.join(state, 'models.json'),
  allowModelNetwork: false, refreshOnCreate: false,
});
modelRuntime.registerProvider(provider, {
  baseUrl: cfg.base_url, api: 'openai-completions',
  models: [{
    id: cfg.model, name: cfg.model, reasoning: true, input: ['text'],
    contextWindow: 1000000, maxTokens: cfg.max_output_tokens,
    // No price estimate: actual token usage is reported separately.
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    compat,
  }],
});
await modelRuntime.setRuntimeApiKey(provider, key || 'offline-check-only');
const resourceLoader = {
  getExtensions: () => ({ extensions: [], errors: [], runtime: createExtensionRuntime() }),
  getSkills: () => ({ skills: [], diagnostics: [] }),
  getPrompts: () => ({ prompts: [], diagnostics: [] }),
  getThemes: () => ({ themes: [], diagnostics: [] }),
  getAgentsFiles: () => ({ agentsFiles: [] }),
  getSystemPrompt: () => prompt('system'),
  getSystemPromptSource: () => undefined,
  getAppendSystemPrompt: () => [], getAppendSystemPromptSources: () => [],
  extendResources: () => {}, reload: async () => {},
};
// With start_in_candidate, the agent's tools start where the code goes, so relative paths land in candidate/.
const agentCwd = cfg.start_in_candidate ? path.join(job.workspace, 'candidate') : job.workspace;
// Custom tools: each runs one harness script and returns its text. Like the agent's shell commands, they get no
// network when the sandbox asks for it.
const runScript = (name, args) => {
  const cmd = [...job[name], ...args];
  const net = process.env.HARNESS_NO_NETWORK ? ['unshare', '--net'] : [];
  try {
    return execFileSync(net[0] || cmd[0], [...net.slice(1), ...(net.length ? cmd : cmd.slice(1))],
      { encoding: 'utf8', timeout: 180000, maxBuffer: 10 * 1024 * 1024 });
  } catch (e) {
    return `${name} failed: ${String(e.stdout || '')}${String(e.stderr || e.message).slice(-1500)}`;
  }
};
const textResult = (text) => ({ content: [{ type: 'text', text }], details: {} });
const CUSTOM_TOOLS = {
  // Step 07: a test tool that returns a short structured report instead of raw pytest output (per-file counts, one
  // line per failure, missing modules with the file to create). See run_tests.py.
  run_tests: {
    name: 'run_tests', label: 'run tests',
    description: 'Run pytest on the Python project the way the evaluation does (from candidate/, with candidate/ and ' +
      'candidate/src on PYTHONPATH) and get a short report: passed/failed per test file, the first error line of ' +
      'each failing test, and modules the tests cannot import. Default: all of public_tests/.',
    parameters: Type.Object({
      path: Type.Optional(Type.String({ description: 'Test file or folder, relative to candidate/ (default public_tests)' })),
    }),
    execute: async (_id, params) => textResult(runScript('run_tests', [params.path || 'public_tests'])),
  },
  // Step 08: the Java API of a class, and what a Python module still lacks of it. See java_tools.py.
  java_api: {
    name: 'java_api', label: 'Java API',
    description: 'Find the Java file of a class in ../source/ and list its non-private constructors, methods, fields, ' +
      'constants and enum values, each with the Python name to use. For a nested type, pass Outer.Inner.',
    parameters: Type.Object({ class_name: Type.String({ description: 'Java class name, e.g. WGS84Point or PhoneNumber.Type' }) }),
    execute: async (_id, params) => textResult(runScript('java_tools', ['api', params.class_name])),
  },
  port_check: {
    name: 'port_check', label: 'port check',
    description: 'Compare a Python module with the Java class it ports and list every non-private Java constructor, ' +
      'method or constant that has no Python counterpart yet. Checks names only, not behavior.',
    parameters: Type.Object({ module: Type.String({ description: 'Module path relative to candidate/, e.g. src/geohash/wgs84point.py' }) }),
    execute: async (_id, params) => textResult(runScript('java_tools', ['check', params.module])),
  },
};
const customTools = cfg.tools.filter(t => t in CUSTOM_TOOLS).map(t => CUSTOM_TOOLS[t]);
// Every session (main, module, push and retry) is told about the custom tools it has.
const toolHints = customTools.map(t => prompt(`during_work/${t.name}_hint`)).join('\n');
const { session } = await createAgentSession({
  cwd: agentCwd, agentDir: state, modelRuntime,
  model: modelRuntime.getModel(provider, cfg.model), thinkingLevel: cfg.thinking,
  tools: cfg.tools, customTools, resourceLoader, sessionManager: SessionManager.inMemory(agentCwd),
  settingsManager: SettingsManager.inMemory({
    compaction: { enabled: cfg.compaction },
    retry: { enabled: false, provider: { maxRetries: cfg.automatic_retries } },
    cacheWarming: 'off', shellPath: job.bash,
  }),
});
save('session-config.json', {
  model: session.model, thinking: session.thinkingLevel, tools: session.getActiveToolNames(),
  system_prompt: session.systemPrompt, node: process.version, check_only: checkOnly,
});
if (checkOnly) {
  session.dispose();
  console.log('Pi SDK initialized; no model request sent.');
  process.exit(0);
}
let turns = 0;
let limit = null;
let error = null;
const started = Date.now();
const startTimer = (ms) => setTimeout(() => {
  limit = 'migration_timeout';
  void session.abort();
}, ms);
let timer = startTimer(cfg.migration_timeout_seconds * 1000);
// With loop_breaker, a tool call that fails N times with the same output and no file written in between gets a
// harness note. Re-running a failing test after an edit is normal work, so any successful write or edit resets it.
const callArgs = new Map();
const failures = new Map();
const loopNotes = [];
session.subscribe((event) => {
  if (cfg.loop_breaker && event.type === 'tool_execution_start') callArgs.set(event.toolCallId, event.args);
  if (cfg.loop_breaker && event.type === 'tool_execution_end' && !event.isError
      && ['write', 'edit'].includes(event.toolName)) failures.clear();
  if (cfg.loop_breaker && event.type === 'tool_execution_end' && event.isError) {
    const call = `${event.toolName} ${JSON.stringify(callArgs.get(event.toolCallId))}`;
    // Timings like "in 0.02s" differ between otherwise identical outputs.
    const output = JSON.stringify(event.result?.content || '').replace(/[0-9]+\.[0-9]+s/g, '');
    const key = `${call}\n${output}`;
    const count = (failures.get(key) || 0) + 1;
    failures.set(key, count);
    if (count % cfg.loop_breaker === 0) {
      loopNotes.push({ at_turn: turns, count, call: call.slice(0, 300) });
      void session.steer(prompt('during_work/loop_breaker',
        { tool: event.toolName, count, call: call.slice(0, 300), cwd: agentCwd }));
    }
  }
  // Completed messages plus tool lifecycle are enough to reconstruct the run.
  if (event.type !== 'message_update' && event.type !== 'tool_execution_update') {
    fs.appendFileSync(path.join(job.output, 'events.jsonl'), redact(JSON.stringify(event)) + '\n');
  }
  if (event.type === 'message_end' && event.message.role === 'assistant') {
    turns++;
    console.log(`Assistant turn ${turns}: ${event.message.stopReason}`);
    if (turns >= cfg.max_assistant_turns && event.message.stopReason === 'toolUse') {
      limit = 'assistant_turn_limit';
      void session.abort();
    }
  }
});
// With resume_after_errors, a session that ends on a provider error or on the output limit (a reply cut off at
// max_output_tokens, which ends the Pi session) is sent on, up to that many times. Baseline: one output-limit end
// left a repo with no code (results/00_baseline/README.md).
const resumes = [];
const RESUME_PROMPTS = { error: 'during_work/provider_error', length: 'during_work/output_limit' };
// Not a lever, so it is on for every config: when the provider is rate-limited (HTTP 429), wait and send the agent
// on. The wait does not count against the session's time limit. Gemini through OpenRouter was rate-limited upstream
// even with one agent at a time (results/03_weak_baseline/).
const rateLimitWaits = [];
let pausedMs = 0;
const RATE_LIMIT_WAITS_SECONDS = [30, 60, 90, 120, 180];
const sendPrompt = async (text) => {
  await session.prompt(text);
  while (!limit && rateLimitWaits.length < RATE_LIMIT_WAITS_SECONDS.length) {
    const last = session.messages.filter(m => m.role === 'assistant').at(-1);
    if (last?.stopReason !== 'error' || !String(last.errorMessage).includes('429')) return;
    const wait = RATE_LIMIT_WAITS_SECONDS[rateLimitWaits.length];
    rateLimitWaits.push({ at_turn: turns, wait_seconds: wait });
    console.log(`Rate-limited at turn ${turns}: waiting ${wait} s`);
    clearTimeout(timer);
    const left = cfg.migration_timeout_seconds * 1000 - (Date.now() - started - pausedMs);
    await new Promise(resolve => setTimeout(resolve, wait * 1000));
    pausedMs += wait * 1000;
    timer = startTimer(Math.max(left, 1000));
    await session.prompt(prompt('during_work/provider_error'));
  }
};
try {
  // With rules, every session also gets a fixed rule sheet (step 09, a prompt file named by the config).
  const extra = [toolHints, cfg.rules ? prompt(cfg.rules) : ''].filter(Boolean).join('\n\n');
  await sendPrompt(extra ? `${job.prompt}\n\n${extra}` : job.prompt);
  while (resumes.length < (cfg.resume_after_errors || 0) && !limit && turns < cfg.max_assistant_turns) {
    const last = session.messages.filter(m => m.role === 'assistant').at(-1);
    const reason = last?.stopReason;
    if (!(reason in RESUME_PROMPTS)) break;
    resumes.push({ at_turn: turns, reason, error: last.errorMessage ? String(last.errorMessage).slice(0, 200) : null });
    console.log(`Resume ${resumes.length} at turn ${turns}: ${reason}`);
    if (reason === 'error') await new Promise(resolve => setTimeout(resolve, 2000 * 2 ** (resumes.length - 1)));
    await sendPrompt(prompt(RESUME_PROMPTS[reason]));
  }
} catch (e) {
  error = redact(String(e));
} finally {
  clearTimeout(timer);
  const messages = session.messages;
  save('messages.json', messages);
  const assistant = messages.filter(m => m.role === 'assistant');
  const usage = {};
  for (const m of assistant) {
    for (const [name, value] of Object.entries(m.usage || {})) {
      if (typeof value === 'number') usage[name] = (usage[name] || 0) + value;
    }
  }
  const last = assistant.at(-1);
  const completed = !error && !limit && last?.stopReason === 'stop';
  save('agent-result.json', {
    completed, error: error || last?.errorMessage || null, limit, assistant_turns: turns,
    elapsed_seconds: (Date.now() - started) / 1000, usage,
    requested_model: cfg.model, returned_model: last?.model || null,
    last_stop_reason: last?.stopReason || null,
    resumes, loop_notes: loopNotes, rate_limit_waits: rateLimitWaits,
    cost_usd: null, cost_note: 'Token usage only; no billing estimate.',
  });
  session.dispose();
  process.exitCode = completed ? 0 : 1;
}
