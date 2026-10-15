export const API_BASE =
 process.env.NEXT_PUBLIC_FLOWFOUNDRY_API_URL ?? "http://localhost:8000";

export type WorkflowStepResponse = {
 agent_id: string | null;
 description: string;
 depends_on: string[];
};

export type SpecialistResult = {
 agent_id: string;
 status: string;
 summary: string;
 findings: Record<string, unknown>[];
 risks: string[];
 unresolved_questions: string[];
 recommended_follow_up: string[];
};

export type SpecialistError = {
 category: string;
 summary: string;
 retryable: boolean;
 state_impact: string;
 technical_reference_id: string;
};

export type WorkflowRunResponse = {
 id: string;
 session_id: string;
 workflow_type: string;
 status: string;
 steps: WorkflowStepResponse[];
 forgemaster_summary: string;
 clarification_needed: boolean;
 clarification_question: string | null;
 specialist_result: SpecialistResult | null;
 specialist_error: SpecialistError | null;
};

type SessionResponse = { id: string; wfg_active: boolean };

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
 const response = await fetch(`${API_BASE}${path}`, init);
 const payload = await response.json().catch(() => null);
 if (!response.ok) {
  const detail = payload && typeof payload.detail === "string"
   ? payload.detail
   : `FlowFoundry backend returned ${response.status}.`;
  throw new Error(detail);
 }
 return payload as T;
}

const jsonPatch = (body: unknown): RequestInit => ({
 method: "PATCH",
 headers: { "Content-Type": "application/json" },
 body: JSON.stringify(body),
});

export const createSession = () => requestJson<SessionResponse>("/api/sessions", { method: "POST" });

export const setPrompt = (sessionId: string, prompt: string) =>
 requestJson<SessionResponse>(`/api/sessions/${sessionId}/prompt`, jsonPatch({ prompt }));

export const setActions = (sessionId: string, actions: string[]) =>
 requestJson<SessionResponse>(`/api/sessions/${sessionId}/actions`, jsonPatch({ actions }));

export const setPreferredAgent = (sessionId: string, agentId: string | null) =>
 requestJson<SessionResponse>(`/api/sessions/${sessionId}/agent`, jsonPatch({ agent_id: agentId }));

export const setWfg = (sessionId: string, active: boolean) =>
 requestJson<SessionResponse>(`/api/sessions/${sessionId}/wfg`, jsonPatch({ active }));

export async function uploadSource(sessionId: string, file: File) {
 const form = new FormData();
 form.append("file", file, file.name);
 return requestJson<{ source_id: string }>(`/api/sessions/${sessionId}/sources`, {
  method: "POST",
  body: form,
 });
}

export const beginWorkflow = (sessionId: string) =>
 requestJson<WorkflowRunResponse>(`/api/sessions/${sessionId}/begin`, { method: "POST" });

export const resetSession = (sessionId: string) =>
 requestJson<SessionResponse>(`/api/sessions/${sessionId}`, { method: "DELETE" });

export async function deleteSource(sessionId: string, sourceId: string) {
 const response = await fetch(
  `${API_BASE}/api/sessions/${sessionId}/sources/${encodeURIComponent(sourceId)}`,
  { method: "DELETE" },
 );
 if (!response.ok) throw new Error("FlowFoundry could not remove the session source.");
}
