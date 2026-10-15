import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the FlowFoundry workspace", async () => {
  const response = await render("/workspace");
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>FlowFoundry — Intelligent Agent Orchestration<\/title>/i);
  assert.match(html, /Start a new workflow/i);
  assert.match(html, /ForgeMaster/i);
  assert.match(html, /Select actions/i);
  assert.match(html, /Specialist Agents/i);
  assert.match(html, /Reset session/i);
  assert.doesNotMatch(html, /Your site is taking shape|Building your site|codex-preview/i);
});

test("server-renders the working-session page", async () => {
  const response = await render("/session");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /Workflow in progress/i);
  assert.match(html, /ForgeMaster Live Feed/i);
  assert.match(html, /Athena/i);
  assert.match(html, /Themis/i);
  assert.match(html, /Hermes/i);
  assert.match(html, /3(?:<!-- -->)? agents complete/i);
});

test("server-renders About FlowFoundry as the home page", async () => {
  const response = await render();
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /About FlowFoundry/i);
  assert.match(html, /From an idea to coordinated action/i);
  assert.match(html, /You stay in control/i);
  assert.match(html, /Start a new workflow/i);
});

test("wires the browser workflow to the Python backend contract", async () => {
  const api = await readFile(new URL("../app/flowfoundry-api.ts", import.meta.url), "utf8");
  const intake = await readFile(new URL("../app/workspace/page.tsx", import.meta.url), "utf8");
  assert.match(api, /\/api\/sessions\/\$\{sessionId\}\/sources/);
  assert.match(api, /\/api\/sessions\/\$\{sessionId\}\/begin/);
  assert.match(intake, /await Promise\.all\(attachedFiles\.map/);
  assert.match(intake, /setWorkflowRun\(run\)/);
  assert.match(intake, /Local Simulation Mode/);
  assert.match(intake, /localSimulationSteps/);
  assert.doesNotMatch(intake, /Simulate ForgeMaster thinking/);
});

test("contains the deployable server entry and handover index", async () => {
  await access(new URL("../dist/server/index.js", import.meta.url));
  await access(new URL("../docs/00-HANDOVER-INDEX.md", import.meta.url));
  await access(new URL("../public/og.png", import.meta.url));
  await access(new URL("../public/flowfoundry-logo-modern-v1.png", import.meta.url));
  await access(new URL("../public/agent-portraits.png", import.meta.url));
  await access(new URL("../public/forgemaster-garcon.png", import.meta.url));
  await access(new URL("../public/forgemaster-default.png", import.meta.url));
  await access(new URL("../public/forgemaster-confused.png", import.meta.url));
  await access(new URL("../public/forgemaster-happy.png", import.meta.url));
  await access(new URL("../public/forgemaster-running.png", import.meta.url));
  await access(new URL("../public/forgemaster-investigating.png", import.meta.url));
  await access(new URL("../CLAUDE.md", import.meta.url));
  await access(new URL(".gitignore", projectRoot));
});
