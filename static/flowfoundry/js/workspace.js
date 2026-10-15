(() => {
  const root = document.querySelector(".enterprise-shell");
  if (!root) return;

  const staticRoot = "/static/flowfoundry/images/preview-forgemaster/";
  const minStateMs = 3500;
  const selectedActions = new Set();
  let preferredAgent = null;
  let wfg = false;
  let expanded = false;
  let files = [];

  const prompt = document.querySelector("#workflow-prompt");
  const panel = document.querySelector("#orchestration-panel");
  const expandControl = document.querySelector("#expand-composer");
  const chips = document.querySelector("#selected-action-chips");
  const count = document.querySelector("#selected-count");
  const preferred = document.querySelector("#preferred-agent");
  const wfgControl = document.querySelector("#wfg-control");
  const wfgIndicator = document.querySelector("#wfg-indicator");
  const begin = document.querySelector("#begin-workflow");
  const fileInput = document.querySelector("#context-files");
  const fileList = document.querySelector("#attached-file-list");
  const modal = document.querySelector("#fm-modal");
  const modalPanel = modal.querySelector(".fm-modal");
  const stateImage = document.querySelector("#fm-state-image");
  const modalTitle = document.querySelector("#fm-modal-title");
  const processing = document.querySelector("#fm-processing");
  const result = document.querySelector("#fm-result");
  const spinnerMessage = document.querySelector("#fm-spinner-message");
  const response = document.querySelector("#forgemaster-response");

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

  function renderActions() {
    count.textContent = `${selectedActions.size} selected`;
    chips.hidden = selectedActions.size === 0;
    chips.replaceChildren(...[...selectedActions].map(action => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.innerHTML = `${action}<span>×</span>`;
      chip.addEventListener("click", () => toggleAction(action));
      return chip;
    }));
    document.querySelectorAll("[data-action]").forEach(button => {
      const isSelected = selectedActions.has(button.dataset.action);
      button.classList.toggle("selected", isSelected);
      button.setAttribute("aria-pressed", String(isSelected));
      button.querySelector("i").textContent = isSelected ? "✓" : "+";
    });
  }

  function toggleAction(action) {
    selectedActions.has(action) ? selectedActions.delete(action) : selectedActions.add(action);
    renderActions();
  }

  function renderPreferredAgent() {
    preferred.hidden = !preferredAgent;
    preferred.querySelector("span").textContent = preferredAgent ? `Preferred Agent: ${preferredAgent.name}` : "";
    document.querySelectorAll(".agent-card").forEach(card => {
      const isSelected = card.dataset.agentId === preferredAgent?.id;
      card.classList.toggle("selected", isSelected);
      const button = card.querySelector("[data-select-agent]");
      if (!button || button.disabled) return;
      button.classList.toggle("selected-agent-control", isSelected);
      button.innerHTML = isSelected ? '<span class="selection-check">✓</span><span>Selected</span>' : 'Select Agent <span>→</span>';
    });
  }

  function renderFiles() {
    fileList.replaceChildren(...files.map((file, index) => {
      const chip = document.createElement("span");
      chip.className = "attached-file-chip";
      chip.append(document.createTextNode(file.name));
      const remove = document.createElement("button");
      remove.type = "button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove ${file.name}`);
      remove.addEventListener("click", () => { files.splice(index, 1); renderFiles(); });
      chip.append(remove);
      return chip;
    }));
  }

  function closeModal() {
    modal.hidden = true;
    result.hidden = true;
    result.replaceChildren();
  }

  function actionButton(label, className, handler) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.textContent = label;
    button.addEventListener("click", handler);
    return button;
  }

  function showClarification(question) {
    modalPanel.classList.remove("fm-modal-plan");
    processing.hidden = true;
    result.hidden = false;
    stateImage.src = `${staticRoot}robot-assistant-questioning.png`;
    stateImage.alt = "ForgeMaster has questions";
    modalTitle.textContent = "I am sorry but I have a few questions....";
    const explanation = document.createElement("p");
    explanation.className = "fm-explanation";
    explanation.textContent = question;
    const summary = document.createElement("div");
    summary.className = "fm-summary-box";
    summary.innerHTML = `<p><strong>What you wrote:</strong> ${prompt.value.trim() || "(nothing entered)"}</p>`;
    const retryTitle = document.createElement("p");
    retryTitle.className = "fm-try-again";
    retryTitle.textContent = "Let me try again";
    const retry = document.createElement("textarea");
    retry.className = "fm-clarification";
    retry.placeholder = "Provide more details about what you need...";
    const actions = document.createElement("div");
    actions.className = "fm-modal-actions";
    const resubmit = actionButton("Begin workflow →", "fm-approve-btn", () => {
      if (!retry.value.trim()) return;
      prompt.value = [prompt.value.trim(), `Clarification: ${retry.value.trim()}`].filter(Boolean).join("\n\n");
      void prepareWorkflow();
    });
    retry.addEventListener("input", () => { resubmit.disabled = !retry.value.trim(); });
    resubmit.disabled = true;
    actions.append(resubmit, actionButton("Go back to initial screen", "fm-approve-btn fm-back-btn-outline", closeModal));
    result.replaceChildren(explanation, summary, retryTitle, retry, actions);
  }

  function showPlan(payload) {
    modalPanel.classList.add("fm-modal-plan");
    processing.hidden = true;
    result.hidden = false;
    stateImage.src = `${staticRoot}robot-assistant-approved.png`;
    stateImage.alt = "ForgeMaster is ready";
    modalTitle.textContent = "Local simulation plan ready";
    const plan = document.createElement("div");
    plan.className = "fm-plan";
    const intro = document.createElement("p");
    intro.className = "fm-plan-intro";
    intro.textContent = payload.summary;
    plan.append(intro);
    payload.steps.forEach((step, index) => {
      const row = document.createElement("div");
      row.className = "fm-plan-step";
      row.innerHTML = `<span class="fm-step-num">${index + 1}</span><div><strong>${step.agent_name}</strong><p>${step.description}</p></div>`;
      plan.append(row);
    });
    if (payload.actions.length) {
      const actionsCopy = document.createElement("p");
      actionsCopy.className = "fm-plan-actions";
      actionsCopy.innerHTML = `<strong>Actions requested:</strong> ${payload.actions.join(", ")}`;
      plan.append(actionsCopy);
    }
    const classification = document.createElement("p");
    classification.className = "fm-plan-actions";
    classification.innerHTML = `<strong>Test classification:</strong> ${payload.test_classification}`;
    plan.append(classification);
    const modalActions = document.createElement("div");
    modalActions.className = "fm-modal-actions";
    modalActions.append(actionButton("Open working session →", "fm-approve-btn", () => { window.location.href = root.dataset.sessionUrl; }), actionButton("Close", "fm-back-btn", closeModal));
    result.replaceChildren(plan, modalActions);
    response.hidden = false;
    response.innerHTML = `<strong>ForgeMaster:</strong> ${payload.summary}`;
  }

  async function prepareWorkflow() {
    if (!prompt.value.trim()) {
      modal.hidden = false;
      showClarification("Your request is empty — I need you to describe what outcome you are looking for so I can identify the right specialists and build a workflow.");
      return;
    }
    const startedAt = Date.now();
    const wfgWasActive = wfg;
    modalPanel.classList.remove("fm-modal-plan");
    modal.hidden = false;
    processing.hidden = false;
    result.hidden = true;
    stateImage.src = `${staticRoot}robot-assistant-working.png`;
    stateImage.alt = "ForgeMaster is working";
    modalTitle.textContent = "ForgeMaster is working on your task!";
    spinnerMessage.textContent = "Identifying the right specialists...";
    const messageTimer = window.setTimeout(() => { spinnerMessage.textContent = "Building your workflow plan..."; }, 1800);
    if (wfg) {
      wfg = false;
      wfgControl.classList.remove("active");
      wfgControl.setAttribute("aria-pressed", "false");
      wfgIndicator.hidden = true;
      begin.firstChild.textContent = "Begin workflow";
    }
    try {
      const apiResponse = await fetch(root.dataset.prepareUrl, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
        body: JSON.stringify({
          objective: prompt.value,
          actions: [...selectedActions],
          preferred_agent: preferredAgent?.id || null,
          wfg_active: wfgWasActive,
        }),
      });
      const payload = await apiResponse.json();
      await sleep(Math.max(0, minStateMs - (Date.now() - startedAt)));
      if (!apiResponse.ok || payload.status === "error") throw new Error(payload.message || "FlowFoundry could not prepare the workflow.");
      payload.status === "clarification" ? showClarification(payload.question) : showPlan(payload);
    } catch (error) {
      await sleep(Math.max(0, minStateMs - (Date.now() - startedAt)));
      showClarification(error.message || "FlowFoundry could not prepare the workflow.");
    } finally {
      window.clearTimeout(messageTimer);
    }
  }

  document.querySelectorAll("[data-action]").forEach(button => button.addEventListener("click", () => toggleAction(button.dataset.action)));
  document.querySelectorAll("[data-select-agent]").forEach(button => button.addEventListener("click", () => {
    const card = button.closest(".agent-card");
    preferredAgent = preferredAgent?.id === card.dataset.agentId ? null : {id: card.dataset.agentId, name: card.dataset.agentName};
    renderPreferredAgent();
  }));
  preferred.querySelector("button").addEventListener("click", () => { preferredAgent = null; renderPreferredAgent(); });
  expandControl.addEventListener("click", () => {
    expanded = !expanded;
    panel.classList.toggle("expanded", expanded);
    expandControl.innerHTML = `${expanded ? "Reduce" : "Expand"} <span>${expanded ? "↙" : "↗"}</span>`;
    expandControl.setAttribute("aria-label", expanded ? "Reduce writing area" : "Expand writing area");
  });
  wfgControl.addEventListener("click", () => {
    wfg = !wfg;
    wfgControl.classList.toggle("active", wfg);
    wfgControl.setAttribute("aria-pressed", String(wfg));
    wfgIndicator.hidden = !wfg;
    begin.firstChild.textContent = wfg ? "GO" : "Begin workflow";
  });
  document.querySelector("#attach-context").addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => {
    [...fileInput.files].forEach(file => { if (!files.some(existing => existing.name === file.name && existing.size === file.size)) files.push(file); });
    fileInput.value = "";
    renderFiles();
  });
  begin.addEventListener("click", () => void prepareWorkflow());
  document.querySelector("#reset-session").addEventListener("click", () => {
    if (!window.confirm("Reset this session? Your prompt and all current selections will be cleared.")) return;
    prompt.value = "";
    selectedActions.clear();
    preferredAgent = null;
    files = [];
    wfg = false;
    response.hidden = true;
    wfgControl.classList.remove("active");
    wfgControl.setAttribute("aria-pressed", "false");
    wfgIndicator.hidden = true;
    begin.firstChild.textContent = "Begin workflow";
    renderActions(); renderPreferredAgent(); renderFiles();
  });
})();
