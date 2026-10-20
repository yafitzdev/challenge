// A single Pi SDK session. The Python runner (run.py) owns staging and final evaluation.
import fs from 'node:fs';
import path from 'node:path';
import {
  createAgentSession, createExtensionRuntime, ModelRuntime,
  SessionManager, SettingsManager,
} from '@earendil-works/pi-coding-agent';
import { EnvHttpProxyAgent, setGlobalDispatcher } from 'undici';

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
const { session } = await createAgentSession({
  cwd: job.workspace, agentDir: state, modelRuntime,
  model: modelRuntime.getModel(provider, cfg.model), thinkingLevel: cfg.thinking,
  tools: cfg.tools, resourceLoader, sessionManager: SessionManager.inMemory(job.workspace),
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
const timer = setTimeout(() => {
  limit = 'migration_timeout';
  void session.abort();
}, cfg.migration_timeout_seconds * 1000);
session.subscribe((event) => {
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
try {
  await session.prompt(job.prompt);
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
    cost_usd: null, cost_note: 'Token usage only; no billing estimate.',
  });
  session.dispose();
  process.exitCode = completed ? 0 : 1;
}
