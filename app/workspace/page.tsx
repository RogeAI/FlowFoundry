"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
 API_BASE,
 beginWorkflow as beginBackendWorkflow,
 createSession,
 deleteSource,
 resetSession,
 setActions,
 setPreferredAgent,
 setPrompt as setBackendPrompt,
 setWfg as setBackendWfg,
 uploadSource,
} from "../flowfoundry-api";
import { useWorkflowFiles } from "../workflow-files";

type Agent = { id:string; name:string; role:string; description:string; status:"Available"|"Busy"|"Unavailable"; portrait_index:number };
const agentPortraits: Record<string, string> = { athena: "/Athena.png", hermes: "/Hermes.png", themis: "/Themis.png", minerva: "/Minerva.png", apolo: "/Apolo.png" };
const shortcuts=["Summarize","Review requirements","Create testable scenarios","Design test cases","Identify gaps","Compare documents"];
const localSimulationSteps=[
 {agent_id:"athena",description:"Review the request, identify ambiguities, and confirm testable acceptance criteria."},
 {agent_id:"themis",description:"Draft test coverage from Athena's reviewed requirements and findings."},
 {agent_id:"hermes",description:"Consolidate the specialist outputs into a clear Master Document."},
];

export default function Home(){
 const router=useRouter();
 const [agents,setAgents]=useState<Agent[]>([]);
 const [wfg,setWfg]=useState(false),[prompt,setPrompt]=useState(""),[expanded,setExpanded]=useState(false);
 const [selectedAgent,setSelectedAgent]=useState<string|null>(null),[selectedActions,setSelectedActions]=useState<string[]>([]);
 const [forgeMasterSummary,setForgeMasterSummary]=useState<string|null>(null);
 const [executionMode,setExecutionMode]=useState<"checking"|"backend"|"local">("checking");
 const {files:attachedFiles,addFiles,removeFile,clearFiles,markUploaded,sessionId,setSessionId,workflowRun,setWorkflowRun}=useWorkflowFiles();
 const attachmentInputRef=useRef<HTMLInputElement|null>(null);
 const sessionRequested=useRef(false);

 type ModalState = "hidden"|"processing"|"outcomeA"|"outcomeB"|"error";
 const [modalState,setModalState]=useState<ModalState>("hidden");
 const [spinnerMessage,setSpinnerMessage]=useState(0);
 const [clarification,setClarification]=useState("");
 const [errorMessage,setErrorMessage]=useState("");
 const spinnerMessages=["Identifying the right specialists...","Building your workflow plan..."];
 const spinnerRef=useRef<ReturnType<typeof setInterval>|null>(null);
 const selected=useMemo(()=>agents.find(a=>a.id===selectedAgent),[selectedAgent,agents]);

 // Load agents and create session on mount
 useEffect(()=>{
  if(sessionRequested.current)return;
  sessionRequested.current=true;
  fetch(`${API_BASE}/api/agents`).then(r=>r.json()).then((data:Agent[])=>setAgents(data)).catch(()=>{
   // Fallback to static data if backend is unreachable
   setAgents([
    {id:"athena",name:"Athena",role:"The Testing Mentor",description:"Teaches you how to create test scenarios and manual test cases step by step. Covers requirements analysis, test approaches, coverage, and test data — aligned with ISTQB concepts.",status:"Available",portrait_index:0},
    {id:"hermes",name:"Hermes",role:"Information Intelligence Agent",description:"Transforms fragmented or mixed information into structured, evidence-aware intelligence. Surfaces meaningful insights, decisions, actions, risks, gaps, contradictions, and unresolved questions.",status:"Available",portrait_index:1},
    {id:"themis",name:"Themis",role:"Test Cases Creator",description:"Designs high-quality test assets from requirements, user stories, and handoff materials. Produces clear scenarios, test data, and manual test cases with atomic steps and measurable expected results.",status:"Available",portrait_index:2},
    {id:"minerva",name:"Minerva",role:"Test Strategy Advisor",description:"Guides you through creating and finalizing your Test Strategy — what's being tested, what could go wrong, how testing builds confidence, and what dependencies apply.",status:"Available",portrait_index:3},
    {id:"apolo",name:"Apolo",role:"Coming Soon",description:"This specialist is under development and will be available in a future release.",status:"Unavailable",portrait_index:4},
    {id:"agent6",name:"Agent 6",role:"Coming Soon",description:"This specialist is under development and will be available in a future release.",status:"Unavailable",portrait_index:5},
   ]);
  });
  createSession().then(s=>{setSessionId(s.id);setExecutionMode("backend");}).catch(()=>{
   setSessionId(null);
   setExecutionMode("local");
  });
 },[setSessionId]);

 const syncActions=(actions:string[])=>{
  if(!sessionId)return;
  setActions(sessionId,actions).catch(error=>setErrorMessage(error.message));
 };

 const toggleAction=(action:string)=>{
  setSelectedActions(c=>{const next=c.includes(action)?c.filter(i=>i!==action):[...c,action];syncActions(next);return next;});
 };

 const handleSelectAgent=(agentId:string|null)=>{
  setSelectedAgent(agentId);
  if(!sessionId)return;
  setPreferredAgent(sessionId,agentId).catch(error=>setErrorMessage(error.message));
 };

 const handleToggleWfg=()=>{
  const next=!wfg;setWfg(next);
 };

 const reset=()=>{
  if(!window.confirm("Reset this session? Your prompt and all current selections will be cleared."))return;
  setPrompt("");setWfg(false);setExpanded(false);setSelectedAgent(null);setSelectedActions([]);setForgeMasterSummary(null);setWorkflowRun(null);clearFiles();
  if(!sessionId)return;
  resetSession(sessionId).catch(error=>setErrorMessage(error.message));
 };

 const addAttachments=(files:FileList|null)=>{
  if(!files)return;
  const selectedFiles=Array.from(files);
  addFiles(selectedFiles,"Initial request");
  if(attachmentInputRef.current)attachmentInputRef.current.value="";
 };

 const removeAttachment=(id:string)=>{
  const item=attachedFiles.find(file=>file.id===id);
  removeFile(id);
  if(sessionId&&item?.sourceId)deleteSource(sessionId,item.sourceId).catch(error=>setErrorMessage(error.message));
 };

 const beginWorkflow=async(additionalContext="")=>{
  const objective=[prompt.trim(),additionalContext.trim()].filter(Boolean).join("\n\nClarification: ");
  if(!objective){setModalState("outcomeB");return;}
  setModalState("processing");
  setSpinnerMessage(0);
  spinnerRef.current=setInterval(()=>setSpinnerMessage(m=>(m+1)%spinnerMessages.length),1800);
  if(!sessionId){
   setExecutionMode("local");
   setWorkflowRun(null);
   setForgeMasterSummary("Local simulation plan ready: Athena will review the request, Themis will create test coverage, and Hermes will assemble the Master Document.");
   await new Promise(resolve=>setTimeout(resolve,700));
   if(spinnerRef.current)clearInterval(spinnerRef.current);
   if(wfg)setWfg(false);
   setClarification("");
   setModalState("outcomeA");
   return;
  }
  try{
   await setBackendPrompt(sessionId,objective);
   await setActions(sessionId,selectedActions);
   await setPreferredAgent(sessionId,selectedAgent);
   await setBackendWfg(sessionId,wfg);
   await Promise.all(attachedFiles.map(async item=>{
    const source=await uploadSource(sessionId,item.file);
    markUploaded(item.id,source.source_id);
   }));
   const run=await beginBackendWorkflow(sessionId);
   setWorkflowRun(run);
   setForgeMasterSummary(run.forgemaster_summary);
   if(wfg)setWfg(false);
   if(run.clarification_needed)setModalState("outcomeB");
   else if(run.specialist_error){setErrorMessage(`${run.specialist_error.summary} ${run.specialist_error.state_impact}`);setModalState("error");}
   else setModalState("outcomeA");
   setClarification("");
  }catch(error){
   setErrorMessage(error instanceof Error?error.message:"FlowFoundry could not start the workflow.");
   setModalState("error");
  }finally{
   if(spinnerRef.current)clearInterval(spinnerRef.current);
  }
 };

 const closeModal=()=>{
  if(spinnerRef.current)clearInterval(spinnerRef.current);
  setModalState("hidden");setClarification("");
 };

 const resubmitWithClarification=()=>{
  if(!clarification.trim())return;
  void beginWorkflow(clarification);
 };

 const agentLabel=(agentId:string|null)=>agents.find(agent=>agent.id===agentId)?.name??agentId??"ForgeMaster";

 return <main className="enterprise-shell">
  <header className="global-header">
   <div className="brand-art"><img className="brand-lockup" src="/flowfoundry-logo-modern-v1.png" alt="FlowFoundry" /></div>
   <nav className="global-nav" aria-label="Global navigation"><button className="current">Workspace</button><button>Activity</button><button>Agents</button><button>Governance</button><Link href="/">About</Link></nav>
   <div className="header-tools"><button className="header-icon" aria-label="Search">⌕</button><button className="header-icon" aria-label="Help">?</button><button className="user-menu" aria-label="Open user menu"><span>RN</span><div><strong>Roger</strong><small>Workspace owner</small></div><b>⌄</b></button></div>
  </header>
  <div className="application-body">
   <aside className="side-panel" aria-label="Workspace navigation">
    <button className="primary-create"><span>＋</span> New workflow</button><button className="reset-control" onClick={reset}><span>↻</span> Reset session</button>
    <div className="side-group"><span className="side-label">Workspace</span><button className="side-link active"><span>▦</span> Start</button><button className="side-link"><span>↺</span> History <b>12</b></button><button className="side-link"><span>◇</span> Saved</button></div>
    <div className="side-group"><span className="side-label">Recent sessions</span><button className="recent-link"><i className="recent-dot running"/><span>Checkout requirements<small>3 Agents · Running</small></span></button><button className="recent-link"><i className="recent-dot"/><span>SAP test scenarios<small>Yesterday</small></span></button><button className="recent-link"><i className="recent-dot"/><span>Automation review<small>12 Aug</small></span></button></div>
    <div className="side-footer"><span className="security-mark">✓</span><div><strong>Enterprise workspace</strong><small>Protected session context</small></div></div>
   </aside>
   <section className="main-workspace">
    <div className="page-heading"><div><span className="breadcrumb">Workspace / New workflow</span><h1>Start a new workflow</h1><p>Tell ForgeMaster what you need. It will assemble the right specialists, set the execution order, and supervise the work throughout.</p></div><div className={`system-state ${executionMode==="local"?"local-simulation":""}`}><i/> {executionMode==="local"?"Local Simulation Mode":executionMode==="checking"?"Checking local services":"Backend connected"}</div></div>
    {executionMode==="local"&&<div className="local-simulation-notice" role="status"><strong>Local Simulation Mode</strong><span>The external API is not connected. This workflow runs in your browser with three simulated Agents and is not a live integration test.</span></div>}
    <div className="workflow-guide" aria-label="How to begin">
     <div><span>1</span><p><strong>Describe the outcome</strong><small>Explain the result you need.</small></p></div><div><span>2</span><p><strong>Select useful actions</strong><small>Choose as many as needed.</small></p></div><div><span>3</span><p><strong>Add supporting context</strong><small>Attach relevant source material.</small></p></div><div><span>4</span><p><strong>Let ForgeMaster lead</strong><small>Agents and order are coordinated for you.</small></p></div>
    </div>
    {forgeMasterSummary&&<div className="forgemaster-response" role="status"><strong>ForgeMaster:</strong> {forgeMasterSummary}</div>}
    <section className={`orchestration-panel ${expanded?"expanded":""}`} aria-label="Start a request">
     <div className="panel-header"><div className="forgemaster-identity"><img className="forgemaster-mark" src="/forgemaster-garcon.png" alt="ForgeMaster" /><div><strong>ForgeMaster</strong><span>Orchestration and continuous supervision</span></div></div><span className="listening-state"><i/> Listening</span></div>
     <div className="request-builder">
      <div className="composer">
       <div className="composer-title"><label htmlFor="workflow-prompt">What would you like to achieve?</label><button onClick={()=>setExpanded(v=>!v)} aria-label={expanded?"Reduce writing area":"Expand writing area"}>{expanded?"Reduce":"Expand"} <span>{expanded?"↙":"↗"}</span></button></div>
       <textarea id="workflow-prompt" value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder="Describe the outcome, problem, or question in your own words..."/>
       {selectedActions.length>0&&<div className="selected-action-chips" aria-label="Selected actions">{selectedActions.map(action=><button key={action} onClick={()=>toggleAction(action)}>{action}<span>×</span></button>)}</div>}
       {selected&&<div className="preferred-agent"><span>Preferred Agent: {selected.name}</span><button onClick={()=>handleSelectAgent(null)} aria-label={`Remove ${selected.name}`}>×</button></div>}
       <div className="composer-footer">
        <div className="composer-actions">
         <input ref={attachmentInputRef} className="visually-hidden-file-input" type="file" multiple tabIndex={-1} aria-hidden="true" onChange={e=>addAttachments(e.target.files)} />
         <button className="secondary-control" onClick={()=>attachmentInputRef.current?.click()}><span>＋</span> Attach context</button>
         <button className={`secondary-control ${wfg?"active":""}`} onClick={handleToggleWfg} aria-pressed={wfg}><span>◷</span> WFG</button>{wfg&&<span className="wfg-indicator"><i/> WFG active · waiting for GO</span>}
        </div>
        <div className="attached-file-list" aria-live="polite" aria-label="Attached context files">
         {attachedFiles.map(item=><span className="attached-file-chip" key={item.id} title={item.file.type||item.file.name}>{item.file.name}<button onClick={()=>removeAttachment(item.id)} aria-label={`Remove ${item.file.name}`}>×</button></span>)}
        </div>
        <button className="begin-control" onClick={()=>void beginWorkflow()}>{wfg?"GO":"Begin workflow"}<span>→</span></button>
       </div>
      </div>
      <aside className="action-selector" aria-labelledby="actions-title">
       <div className="action-heading"><div><h2 id="actions-title">Select actions</h2><p><strong>{shortcuts.length} actions available</strong> · choose one or more</p></div><span>{selectedActions.length} selected</span></div>
       <div className="shortcut-grid">{shortcuts.map(action=>{const checked=selectedActions.includes(action);return <button key={action} onClick={()=>toggleAction(action)} className={checked?"selected":""} aria-pressed={checked}><i>{checked?"✓":"+"}</i><span>{action}</span></button>})}</div>
       <p className="order-note">ForgeMaster determines dependencies and execution order—not the order you select these actions.</p>
      </aside>
     </div>
    </section>
    <section className="agent-directory" aria-labelledby="agents-title">
     <div className="enterprise-section-heading directory-heading"><div className="section-title-row"><h2 id="agents-title">Specialist Agents</h2><span>{agents.length} specialists</span><p>Choose a preferred starting Agent, or let ForgeMaster decide.</p></div><div className="availability-legend"><span><i className="available"/>Available</span><span><i className="busy"/>Busy</span><span><i className="unavailable"/>Unavailable</span></div></div>
     <div className="agent-grid">{agents.map((agent)=>{const selectable=agent.status==="Available",isSelected=selectedAgent===agent.id,portrait=agentPortraits[agent.id];return <article key={agent.id} className={`agent-card ${agent.status.toLowerCase()} ${isSelected?"selected":""}`}><div className="agent-card-head">{portrait?<img className="agent-avatar" src={portrait} alt={agent.name}/>:<span className="agent-avatar agent-avatar-placeholder" role="img" aria-label={`${agent.name} portrait`}>?</span>}<div className="agent-identity"><h3>{agent.name}</h3><span className="agent-role">{agent.role}</span></div><span className="agent-status"><i/>{agent.status}</span></div><p>{agent.description}</p><button className={isSelected?"selected-agent-control":""} disabled={!selectable} onClick={()=>handleSelectAgent(isSelected?null:agent.id)}>{isSelected?<><span className="selection-check">✓</span><span>Selected</span></>:selectable?<>Select Agent<span>→</span></>:agent.status==="Busy"?"Selection disabled while busy":"Currently unavailable"}</button></article>})}</div>
    </section>
    <footer className="workspace-footer">ForgeMaster observes continuously and intervenes selectively throughout every workflow.</footer>
   </section>
  </div>

  {/* ForgeMaster Modal */}
  {modalState!=="hidden"&&<div className="fm-modal-overlay" role="dialog" aria-modal="true" aria-label="ForgeMaster response">
   <div className="fm-modal">

    {/* PROCESSING STATE */}
    {modalState==="processing"&&<>
     <div className="fm-modal-left">
      <Image className="fm-state-image" src="/forgemaster-default.png" alt="ForgeMaster is working" width={300} height={380} priority/>
     </div>
     <div className="fm-modal-right">
      <p className="fm-modal-title">ForgeMaster is working on your task!</p>
      <div className="fm-spinner"><div className="fm-spinner-ring"/></div>
      <p className="fm-spinner-message">{spinnerMessages[spinnerMessage]}</p>
     </div>
    </>}

    {/* OUTCOME A — Plan ready */}
    {modalState==="outcomeA"&&<>
     <div className="fm-modal-left">
      <Image className="fm-state-image" src="/forgemaster-happy.png" alt="ForgeMaster is ready" width={220} height={280} priority/>
     </div>
     <div className="fm-modal-right">
      <p className="fm-modal-title">{executionMode==="local"?"Local simulation plan ready":"ForgeMaster has completed the initial handoff"}</p>
      <div className="fm-plan">
       <p className="fm-plan-intro">{workflowRun?.forgemaster_summary||forgeMasterSummary||"ForgeMaster reviewed your request."}</p>
       {(workflowRun?.steps??(executionMode==="local"?localSimulationSteps:[])).map((step,index)=><div className="fm-plan-step" key={`${step.agent_id??"forgemaster"}-${index}`}><span className="fm-step-num">{index+1}</span><div><strong>{agentLabel(step.agent_id)}</strong><p>{step.description}</p></div></div>)}
       {workflowRun?.specialist_result&&<p className="fm-plan-actions"><strong>Hermes result:</strong> {workflowRun.specialist_result.summary}</p>}
       {selectedActions.length>0&&<p className="fm-plan-actions"><strong>Actions requested:</strong> {selectedActions.join(", ")}</p>}
       {executionMode==="local"&&<p className="fm-plan-actions"><strong>Test classification:</strong> Local UI simulation — no real Agent or external API execution.</p>}
      </div>
      <div className="fm-modal-actions">
       <button className="fm-approve-btn" onClick={()=>{closeModal();router.push("/session");}}>Open working session <span>→</span></button>
       <button className="fm-back-btn" onClick={closeModal}>Close</button>
      </div>
     </div>
    </>}

    {/* OUTCOME B — Needs more info */}
    {modalState==="outcomeB"&&<>
     <div className="fm-modal-left">
      <Image className="fm-state-image" src="/forgemaster-confused.png" alt="ForgeMaster has questions" width={300} height={380} priority/>
     </div>
     <div className="fm-modal-right">
      <p className="fm-modal-title">I am sorry but I have a few questions....</p>
      <p className="fm-explanation">{workflowRun?.clarification_question||(!prompt?.trim()?"Your request is empty — I need you to describe what outcome you are looking for so I can identify the right specialists and build a workflow.":"ForgeMaster needs more detail before assigning specialist work.")}</p>
      <div className="fm-summary-box">
       <p><strong>What you wrote:</strong> {prompt||"(nothing entered)"}</p>
       {selectedAgent&&selected&&<p><strong>Preferred Agent:</strong> {selected.name}</p>}
       {selectedActions.length>0&&<p><strong>Actions Selected:</strong> {selectedActions.join(", ")}</p>}
      </div>
      <p className="fm-try-again">Let me try again</p>
      <textarea className="fm-clarification" value={clarification} onChange={e=>setClarification(e.target.value)} placeholder="Provide more details about what you need..."/>
      <div className="fm-modal-actions">
       <button className="fm-approve-btn" onClick={resubmitWithClarification} disabled={!clarification.trim()}>Begin workflow <span>→</span></button>
       <button className="fm-approve-btn fm-back-btn-outline" onClick={closeModal}>Go back to initial screen</button>
      </div>
     </div>
    </>}

    {modalState==="error"&&<>
     <div className="fm-modal-left">
      <Image className="fm-state-image" src="/forgemaster-confused.png" alt="ForgeMaster could not continue" width={300} height={380} priority/>
     </div>
     <div className="fm-modal-right">
      <p className="fm-modal-title">ForgeMaster could not continue safely</p>
      <p className="fm-explanation">{errorMessage}</p>
      <div className="fm-modal-actions">
       <button className="fm-approve-btn fm-back-btn-outline" onClick={closeModal}>Return to the request</button>
      </div>
     </div>
    </>}

   </div>
  </div>}

 </main>;
}
