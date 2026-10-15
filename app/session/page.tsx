"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { deleteSource, uploadSource } from "../flowfoundry-api";
import { useWorkflowFiles } from "../workflow-files";

type AgentStep = {
 id: string;
 name: string;
 role: string;
 status: "waiting" | "in-progress" | "needs-input" | "complete";
 output?: string;
 portrait: string;
};

type AttentionRequest = {
 agentId: string;
 agentName: string;
 question: string;
};

const agentDetails: Record<string, {name:string;role:string;portrait:string}> = {
 athena: {name:"Athena",role:"The Testing Mentor",portrait:"/Athena.png"},
 hermes: {name:"Hermes",role:"Information Intelligence Agent",portrait:"/Hermes.png"},
 themis: {name:"Themis",role:"Test Cases Creator",portrait:"/Themis.png"},
 minerva: {name:"Minerva",role:"Test Strategy Advisor",portrait:"/Minerva.png"},
};

export default function SessionPage() {
 const router = useRouter();
 const {files: attachedFiles, addFiles, removeFile, clearFiles, markUploaded, sessionId, workflowRun, setWorkflowRun} = useWorkflowFiles();
 const [steps, setSteps] = useState<AgentStep[]>(()=>workflowRun?.steps.filter(step=>step.agent_id).map((step,index)=>{
  const agentId=step.agent_id as string;
  const details=agentDetails[agentId]??{name:agentId,role:"Specialist Agent",portrait:"/Hermes.png"};
  const completed=workflowRun.specialist_result?.agent_id===agentId;
  return {id:`${agentId}-${index}`,name:details.name,role:details.role,portrait:details.portrait,status:completed?"complete":"waiting",output:completed?workflowRun.specialist_result?.summary:undefined};
 })??[
  { id: "athena", name: "Athena", role: "The Testing Mentor", status: "waiting", portrait: "/Athena.png" },
  { id: "themis", name: "Themis", role: "Test Cases Creator", status: "waiting", portrait: "/Themis.png" },
  { id: "hermes", name: "Hermes", role: "Information Intelligence Agent", status: "waiting", portrait: "/Hermes.png" },
 ]);
 const [feed, setFeed] = useState<{text: string; done: boolean}[]>(()=>workflowRun?[{text:workflowRun.forgemaster_summary,done:true},...(workflowRun.specialist_result?[{text:workflowRun.specialist_result.summary,done:true}]:[])]:[{text:"ForgeMaster is preparing the workflow...",done:false}]);
 const [workflowStatus, setWorkflowStatus] = useState<"running" | "investigating" | "paused" | "complete">(workflowRun?"complete":"running");
 const [attentionRequest, setAttentionRequest] = useState<AttentionRequest | null>(null);
 const [attentionResolved, setAttentionResolved] = useState(false);
 const [chatMessage, setChatMessage] = useState("");
 const [chatHistory, setChatHistory] = useState<{from: string; text: string}[]>([]);
 const [scrollPos, setScrollPos] = useState(0);
 const attachmentInputRef = useRef<HTMLInputElement | null>(null);

 // Simulate workflow progression
 useEffect(() => {
  if (workflowRun) return;
  if (workflowStatus !== "running") return;

  if (attentionResolved) {
   const resumed = setTimeout(() => {
    setSteps(s => s.map(step => step.id === "hermes" ? {
     ...step,
     status: "complete",
     output: "Summary report assembled. 5 findings consolidated into actionable recommendations with priority rankings."
    } : step));
    setFeed(f => [...f.map(m => ({...m, done: true})), {text: "Hermes has completed the summary.", done: true}, {text: "All agents have finished. Your workflow is complete.", done: true}]);
    setWorkflowStatus("complete");
   }, 3000);
   return () => clearTimeout(resumed);
  }

  const t1 = setTimeout(() => {
   setSteps(s => s.map((step, i) => i === 0 ? { ...step, status: "in-progress" } : step));
   setFeed(f => [...f.map(m => ({...m, done: true})), {text: "Athena (SQA Mentor) has started reviewing your requirements...", done: false}]);
  }, 2000);

  const t2 = setTimeout(() => {
   setSteps(s => s.map((step, i) =>
    i === 0 ? { ...step, status: "complete", output: "Requirements reviewed. Found 3 ambiguities and 2 missing acceptance criteria. Recommendations prepared." } :
    i === 1 ? { ...step, status: "in-progress" } : step
   ));
   setFeed(f => [...f.map(m => ({...m, done: true})), {text: "Athena has completed the review. Passing findings to Themis...", done: true}, {text: "Themis (Test Cases Creator) is drafting coverage from the reviewed requirements...", done: false}]);
  }, 6000);

  const t3 = setTimeout(() => {
   setSteps(s => s.map((step, i) =>
    i === 1 ? { ...step, status: "complete", output: "Test coverage drafted across the confirmed requirements, ambiguities, and acceptance criteria." } :
    i === 2 ? { ...step, status: "in-progress" } : step
   ));
   setFeed(f => [...f.map(m => ({...m, done: true})), {text: "Themis has completed the test coverage. Passing outputs to Hermes...", done: true}, {text: "Hermes (Intelligence Summarizer) is assembling the Master Document...", done: false}]);
  }, 10000);

  const t4 = setTimeout(() => {
   const question = "Hermes needs clarification before completing the Master Document: which audience and level of detail should the final summary use?";
   setSteps(s => s.map(step => step.id === "hermes" ? { ...step, status: "needs-input" } : step));
   setFeed(f => [...f.map(m => ({...m, done: true})), {text: "Hermes needs additional input. ForgeMaster is investigating and waiting for your response.", done: false}]);
   setAttentionRequest({agentId: "hermes", agentName: "Hermes", question});
   setChatHistory(h => [...h, {from: "forgemaster", text: question}]);
   setWorkflowStatus("investigating");
  }, 14000);

  return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); };
 }, [workflowStatus, attentionResolved, workflowRun]);

 const completedCount = steps.filter(s => s.status === "complete").length;
 const progressPercent = steps.length ? (completedCount / steps.length) * 100 : 100;
 const chatAvailable = workflowStatus === "investigating" || workflowStatus === "complete";
 const forgeMasterImage = workflowStatus === "complete"
  ? "/forgemaster-happy.png"
  : workflowStatus === "investigating"
   ? "/forgemaster-investigating.png"
   : "/forgemaster-running.png";
 const forgeMasterAlt = workflowStatus === "complete"
  ? "ForgeMaster is happy"
  : workflowStatus === "investigating"
   ? "ForgeMaster is investigating"
   : "ForgeMaster is running";

 const sendChat = () => {
  if (!chatMessage.trim() || !chatAvailable) return;
  const msg = chatMessage.trim();
  setChatHistory(h => [...h, { from: "user", text: msg }]);
  setChatMessage("");

  if (workflowStatus === "investigating" && attentionRequest) {
   const agentName = attentionRequest.agentName;
   setSteps(s => s.map(step => step.id === attentionRequest.agentId ? { ...step, status: "in-progress" } : step));
   setFeed(f => [...f.map(m => ({...m, done: true})), {text: `Your response was received. ${agentName} has resumed work.`, done: false}]);
   setAttentionRequest(null);
   setAttentionResolved(true);
   setWorkflowStatus("running");
   setTimeout(() => {
    setChatHistory(h => [...h, { from: "forgemaster", text: `Thank you. I passed your response to ${agentName}, and the workflow is continuing.` }]);
   }, 700);
   return;
  }

  // Simulate ForgeMaster response
  setTimeout(() => {
   setChatHistory(h => [...h, { from: "forgemaster", text: `I checked with the relevant specialist. Regarding "${msg}" — the findings are consistent with what was documented in the Master Document. Would you like me to elaborate on a specific point?` }]);
  }, 1500);
 };

 const addAttachments = (files: FileList | null) => {
  if (!files) return;
  const selectedFiles = Array.from(files);
  addFiles(selectedFiles, "Working session");
  if (sessionId) {
   void Promise.all(selectedFiles.map(async file => {
    const id = `${file.name}-${file.size}-${file.lastModified}`;
    const source = await uploadSource(sessionId, file);
    markUploaded(id, source.source_id);
   })).then(() => setFeed(current => [...current, {text:"ForgeMaster added the new source files to this session.",done:true}])).catch(error => setFeed(current => [...current, {text:error instanceof Error?error.message:"The source upload failed.",done:false}]));
  }
  if (attachmentInputRef.current) attachmentInputRef.current.value = "";
 };

 const removeAttachment = (id: string) => {
  const item = attachedFiles.find(file => file.id === id);
  removeFile(id);
  if (sessionId && item?.sourceId) void deleteSource(sessionId, item.sourceId).catch(error => setFeed(current => [...current, {text:error.message,done:false}]));
 };

 const allAgents = [
  { name: "Athena", portrait: "/Athena.png" },
  { name: "Hermes", portrait: "/Hermes.png" },
  { name: "Themis", portrait: "/Themis.png" },
  { name: "Minerva", portrait: "/Minerva.png" },
  { name: "Apolo", portrait: "/Apolo.png" },
  { name: "Agent 6", portrait: null },
 ];

 return (
  <main className="enterprise-shell">
   <header className="global-header">
    <div className="brand-art"><img className="brand-lockup" src="/flowfoundry-logo-modern-v1.png" alt="FlowFoundry" /></div>
    <nav className="global-nav" aria-label="Global navigation"><button className="current">Workspace</button><button>Activity</button><button>Agents</button><button>Governance</button><Link href="/">About</Link></nav>
    <div className="header-tools"><button className="header-icon" aria-label="Search">⌕</button><button className="header-icon" aria-label="Help">?</button><button className="user-menu" aria-label="Open user menu"><span>RN</span><div><strong>Roger</strong><small>Workspace owner</small></div><b>⌄</b></button></div>
   </header>

   <div className="application-body">
    <aside className="side-panel" aria-label="Workspace navigation">
     <button className="primary-create" onClick={() => {clearFiles();setWorkflowRun(null);router.push("/");}}><span>＋</span> New workflow</button>
     <div className="side-group"><span className="side-label">Workspace</span><button className="side-link" onClick={() => router.push("/")}><span>▦</span> Start</button><button className="side-link"><span>↺</span> History <b>12</b></button><button className="side-link"><span>◇</span> Saved</button></div>
     <div className="side-group"><span className="side-label">Current session</span><button className="side-link active"><span>⚡</span> Active workflow</button></div>
     <div className="side-group"><span className="side-label" style={{marginTop:"16px"}}>&nbsp;</span><button className="side-link"><span>📝</span> My Saved Prompts</button><button className="side-link"><span>📁</span> My Saved Projects</button></div>
     <div className="side-footer"><span className="security-mark">✓</span><div><strong>Enterprise workspace</strong><small>Protected session context</small></div></div>
    </aside>

    <section className="main-workspace session-layout">
     {/* LEFT PANEL — Workflow content */}
     <div className="session-left">
      <div className="page-heading">
       <div>
        <span className="breadcrumb">Workspace / Active workflow</span>
        <h1>Workflow in progress</h1>
        <p>ForgeMaster is supervising the execution of your request.</p>
       </div>
      </div>

      {/* ForgeMaster supervision bar */}
      <div className="session-forgemaster-bar">
       <div className="session-fm-identity">
        <img className="session-fm-state-image" src={forgeMasterImage} alt={forgeMasterAlt} />
        <div>
         <strong>ForgeMaster</strong>
         <span>{workflowStatus === "complete" ? "Workflow complete" : workflowStatus === "investigating" ? `Investigating ${attentionRequest?.agentName ?? "an Agent"} request` : "Supervising your workflow"}</span>
        </div>
       </div>
       <div className="session-progress-area">
        <span className={`session-status-badge ${workflowStatus}`}><i />{workflowStatus === "running" ? "Running" : workflowStatus === "investigating" ? "Investigating" : workflowStatus === "paused" ? "Paused" : "Complete"}</span>
        <div className="session-progress">
         <div className="session-progress-bar"><div className="session-progress-fill" style={{ width: `${progressPercent}%` }} /></div>
         <span>{completedCount}/{steps.length} agents complete</span>
        </div>
       </div>
      </div>

      {/* Workflow Plan */}
      <div className="session-plan-panel">
       <h2>Workflow Plan</h2>
       <div className="session-steps-container">
        <div className="session-steps">
        {steps.map((step) => (
          <div key={step.id} className={`session-step ${step.status}`}>
           <div className="session-step-header">
            <img className="agent-avatar" src={step.portrait} alt={step.name} />
            <div className="session-step-info">
             <strong>{step.name}</strong>
             <span>{step.role}</span>
            </div>
            <span className={`session-step-status ${step.status}`}>
             {step.status === "waiting" && "Waiting"}
             {step.status === "in-progress" && "In Progress"}
             {step.status === "needs-input" && "Input Required"}
             {step.status === "complete" && "✓ Complete"}
            </span>
           </div>
           {step.output && (
            <div className="session-step-output">
             <p>{step.output}</p>
             <button className="session-download-files" aria-label={`Download ${step.name} files`}><Image src="/Download-files.png" alt="" width={24} height={24} /><span>Download Files</span></button>
            </div>
           )}
          </div>
         ))}
        </div>
        {steps.length > 2 && <div className="session-scroll-arrows">
         <button onClick={() => setScrollPos(Math.max(0, scrollPos - 1))}>▲</button>
         <button onClick={() => setScrollPos(Math.min(steps.length - 2, scrollPos + 1))}>▼</button>
        </div>}
       </div>

       {/* Master Document */}
       {workflowStatus === "complete" && (
        <div className="session-master-doc">
         <strong>Master Document</strong>
         <button className="session-download-files" aria-label="Download master file"><Image src="/Download Master.png" alt="" width={24} height={24} /><span>Download master file</span></button>
        </div>
       )}
      </div>

      {/* Workflow Files */}
      <section className="session-files-panel" aria-labelledby="workflow-files-title">
       <div className="session-files-header">
        <div><h2 id="workflow-files-title">Workflow Files</h2><p>Files available to this workflow</p></div>
        <span>{attachedFiles.length} {attachedFiles.length === 1 ? "file" : "files"}</span>
       </div>
       {attachedFiles.length > 0 ? (
        <div className="session-files-list" aria-live="polite">
         {attachedFiles.map(item => <div className="session-file-row" key={item.id}>
          <span className="session-file-icon">↗</span>
          <div><strong>{item.file.name}</strong><small>{item.addedFrom} · {Math.max(1,Math.ceil(item.file.size/1024))} KB</small></div>
          <button onClick={() => removeAttachment(item.id)} aria-label={`Remove ${item.file.name}`}>×</button>
         </div>)}
        </div>
       ) : <p className="session-files-empty">No files attached to this workflow yet.</p>}
      </section>

      {/* Action buttons */}
      <div className="session-actions">
       {workflowStatus === "running" && (
        <>
         <button className="session-btn pause" onClick={() => setWorkflowStatus("paused")}>⏸ Pause workflow</button>
         <button className="session-btn cancel" onClick={() => router.push("/")}>✕ Cancel workflow</button>
        </>
       )}
       {workflowStatus === "paused" && (
        <>
         <button className="session-btn resume" onClick={() => setWorkflowStatus("running")}>▶ Resume workflow</button>
         <button className="session-btn cancel" onClick={() => router.push("/")}>✕ Cancel workflow</button>
        </>
       )}
       {workflowStatus === "complete" && (
        <>
         <button className="session-btn download">⬇ Download results</button>
         <button className="session-btn new" onClick={() => router.push("/")}>＋ Start new workflow</button>
        </>
       )}
      </div>

      {/* ForgeMaster Live Feed */}
      <div className="session-feed-panel">
       <div className="session-feed-header"><h2>ForgeMaster Live Feed</h2><button className="session-expand-btn">Expand ↗</button></div>
       <div className="session-feed">
        {feed.map((msg, i) => (
         <div key={i} className={`session-feed-item ${msg.done ? "done" : ""}`}>
          <i className={`session-feed-dot ${msg.done ? "feed-done" : ""}`} />
          <p>{msg.text}</p>
          {msg.done && <span className="feed-check">✓</span>}
         </div>
        ))}
        {(workflowStatus === "running" || workflowStatus === "investigating") && (
         <div className="session-feed-item typing">
          <i className="session-feed-dot" />
          <p className="typing-indicator">{workflowStatus === "investigating" ? "Waiting for your response..." : "..."}</p>
         </div>
        )}
       </div>
      </div>
     </div>

     {/* RIGHT PANEL — Agent selection + Chat */}
     <div className="session-right">
      {/* Select an Agent — grayed out phase 2 */}
      <div className="session-agent-select disabled">
       <h3>Select an Agent <span className="coming-soon">Coming soon</span></h3>
       <div className="session-agent-portraits">
        {allAgents.map((agent) => (
         <span className="session-agent-tooltip" data-agent-name={agent.name} key={agent.name}>
          {agent.portrait
           ? <img className="agent-avatar disabled-avatar" src={agent.portrait} alt={agent.name} />
           : <span className="agent-avatar agent-avatar-placeholder disabled-avatar" role="img" aria-label={agent.name}>?</span>}
         </span>
        ))}
       </div>
      </div>

      {/* Chat area */}
      <div className={`session-chat-panel ${workflowStatus === "investigating" ? "attention-open" : ""}`}>
       <h3>ForgeMaster {workflowStatus === "investigating" && <span className="session-attention-label">Input required · {attentionRequest?.agentName}</span>}</h3>
       <div className="session-chat-area">
        {!chatAvailable && chatHistory.length === 0 && (
         <p className="session-chat-disabled">Chat available once workflow completes.</p>
        )}
        {workflowStatus === "complete" && chatHistory.length === 0 && (
         <p className="session-chat-welcome">I&apos;m supervising your workflow. Ask me anything about the progress or results.</p>
        )}
        {chatHistory.map((msg, i) => (
         <div key={i} className={`session-chat-msg ${msg.from}`}>
          {msg.from === "forgemaster" && <img src="/ForgeMaster_Icon_4.png" alt="ForgeMaster" style={{ width: "24px", height: "24px", borderRadius: "50%", objectFit: "cover" }} />}
          <p>{msg.text}</p>
         </div>
        ))}
       </div>
       <div className={`session-chat-input ${!chatAvailable ? "disabled" : ""}`}>
        <textarea
         rows={3}
         placeholder={workflowStatus === "investigating" ? `Reply to ${attentionRequest?.agentName ?? "ForgeMaster"}...` : "Ask ForgeMaster..."}
         value={chatMessage}
         onChange={e => setChatMessage(e.target.value)}
         onKeyDown={e => {if(e.key === "Enter" && !e.shiftKey){e.preventDefault();sendChat();}}}
         disabled={!chatAvailable}
        />
        <div className="session-chat-controls">
         <input ref={attachmentInputRef} className="visually-hidden-file-input" type="file" multiple tabIndex={-1} aria-hidden="true" onChange={e => addAttachments(e.target.files)} />
         <button className="session-chat-attach" onClick={() => attachmentInputRef.current?.click()}>＋ Attach context</button>
         <button className="session-chat-wfg" disabled={!chatAvailable}>◷ WFG</button>
         <button className="session-chat-send" onClick={sendChat} disabled={!chatAvailable}>SEND</button>
        </div>
       </div>
      </div>
     </div>
    </section>
   </div>
  </main>
 );
}
