(() => {
  const root = document.querySelector("#session-root");
  if (!root) return;

  const sessionData = JSON.parse(document.querySelector("#session-data").textContent);
  const minimumStateMs = Math.max(3500, Number(sessionData.minimum_state_ms) || 3500);
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const steps = [...document.querySelectorAll(".session-step")];
  const status = document.querySelector("#session-status");
  const statusCopy = status.querySelector("span");
  const fmImage = document.querySelector("#session-fm-image");
  const fmCopy = document.querySelector("#session-fm-copy");
  const progressFill = document.querySelector("#session-progress-fill");
  const progressCopy = document.querySelector("#session-progress-copy");
  const feed = document.querySelector("#session-feed");
  const typing = document.querySelector("#session-feed-typing");
  const actions = document.querySelector("#session-actions");
  const pause = document.querySelector("#session-pause");
  const cancel = document.querySelector("#session-cancel");
  const chatPanel = document.querySelector("#session-chat-panel");
  const chatArea = document.querySelector("#session-chat-area");
  const chatPlaceholder = document.querySelector("#session-chat-placeholder");
  const chatInput = document.querySelector("#session-chat-input");
  const chatMessage = document.querySelector("#session-chat-message");
  const chatSend = document.querySelector("#session-chat-send");
  const chatWfg = document.querySelector("#session-chat-wfg");
  const attentionLabel = document.querySelector("#session-attention-label");
  const fileInput = document.querySelector("#session-file-input");
  const fileList = document.querySelector("#session-files-list");
  const fileEmpty = document.querySelector("#session-files-empty");
  const fileCount = document.querySelector("#session-file-count");
  const masterDoc = document.querySelector("#session-master-doc");
  let workflowStatus = "running";
  let phase = 0;
  let timer = null;
  let attentionOpen = false;
  let attachedFiles = [];

  function setStatus(nextStatus, label) {
    workflowStatus = nextStatus;
    status.className = `session-status-badge ${nextStatus}`;
    statusCopy.textContent = label;
  }

  function updateProgress() {
    const completed = steps.filter((step) => step.classList.contains("complete")).length;
    progressFill.style.width = `${(completed / steps.length) * 100}%`;
    progressCopy.textContent = `${completed}/${steps.length} Agents complete`;
  }

  function setStep(index, nextStatus, output = "") {
    const step = steps[index];
    step.className = `session-step ${nextStatus}`;
    const badge = step.querySelector(".session-step-status");
    badge.className = `session-step-status ${nextStatus}`;
    badge.textContent = nextStatus === "in-progress" ? "In Progress" : nextStatus === "needs-input" ? "Input Required" : nextStatus === "complete" ? "✓ Complete" : "Waiting";
    const outputArea = step.querySelector(".session-step-output");
    if (output) {
      outputArea.hidden = false;
      outputArea.querySelector("p").textContent = output;
    }
    updateProgress();
  }

  function addFeed(text, done = false) {
    const item = document.createElement("div");
    item.className = `session-feed-item${done ? " done" : ""}`;
    item.innerHTML = `<i class="session-feed-dot${done ? " feed-done" : ""}"></i><p></p>${done ? '<span class="feed-check">✓</span>' : ""}`;
    item.querySelector("p").textContent = text;
    feed.insertBefore(item, typing);
    feed.scrollTop = feed.scrollHeight;
  }

  function markPreviousFeedDone() {
    [...feed.querySelectorAll(".session-feed-item:not(.typing)")].forEach((item) => item.classList.add("done"));
  }

  function scheduleNext() {
    window.clearTimeout(timer);
    if (workflowStatus !== "running") return;
    timer = window.setTimeout(runNextPhase, minimumStateMs);
  }

  function runNextPhase() {
    if (workflowStatus !== "running") return;
    markPreviousFeedDone();
    phase += 1;
    if (phase === 1) {
      setStep(0, "in-progress");
      addFeed("Athena (The Testing Mentor) has started reviewing your requirements...");
      scheduleNext();
    } else if (phase === 2) {
      setStep(0, "complete", steps[0].dataset.output);
      setStep(1, "in-progress");
      addFeed("Athena completed the review. Themis is drafting coverage from the reviewed requirements...");
      scheduleNext();
    } else if (phase === 3) {
      setStep(1, "complete", steps[1].dataset.output);
      setStep(2, "in-progress");
      addFeed("Themis completed the test coverage. Hermes is assembling the Master Document...");
      scheduleNext();
    } else if (phase === 4) {
      setStep(2, "needs-input");
      setStatus("investigating", "Investigating");
      fmImage.src = root.dataset.investigatingImage;
      fmImage.alt = "ForgeMaster is investigating";
      fmCopy.textContent = "Investigating Hermes request";
      addFeed("Hermes needs additional input. ForgeMaster is investigating and waiting for your response.");
      typing.querySelector("p").textContent = "Waiting for your response...";
      attentionOpen = true;
      actions.hidden = true;
      enableChatForAttention();
    }
  }

  function addChatMessage(from, text) {
    if (chatPlaceholder) chatPlaceholder.hidden = true;
    const message = document.createElement("div");
    message.className = `session-chat-msg ${from}`;
    if (from === "forgemaster") {
      const avatar = document.createElement("img");
      avatar.src = root.dataset.investigatingImage;
      avatar.alt = "ForgeMaster";
      avatar.className = "session-chat-avatar";
      message.append(avatar);
    }
    const copy = document.createElement("p");
    copy.textContent = text;
    message.append(copy);
    chatArea.append(message);
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  function enableChatForAttention() {
    chatPanel.classList.add("attention-open");
    attentionLabel.hidden = false;
    chatInput.classList.remove("disabled");
    chatMessage.disabled = false;
    chatSend.disabled = false;
    chatWfg.disabled = false;
    chatMessage.placeholder = "Reply to Hermes...";
    addChatMessage("forgemaster", sessionData.attention.question);
  }

  async function sendChat() {
    const message = chatMessage.value.trim();
    if (!message || chatMessage.disabled) return;
    addChatMessage("user", message);
    chatMessage.value = "";
    if (!attentionOpen) {
      window.setTimeout(() => addChatMessage("forgemaster", `I reviewed your question: “${message}” The current findings remain consistent with the Master Document.`), 900);
      return;
    }
    chatSend.disabled = true;
    const response = await fetch(root.dataset.responseUrl, {method: "POST", headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken}, body: JSON.stringify({response: message})});
    const payload = await response.json();
    if (payload.status !== "resumed") {
      addChatMessage("forgemaster", payload.message || "I still need a little more detail.");
      chatSend.disabled = false;
      return;
    }
    attentionOpen = false;
    actions.hidden = false;
    chatPanel.classList.remove("attention-open");
    attentionLabel.hidden = true;
    setStatus("running", "Running");
    fmImage.src = root.dataset.guidingImage;
    fmImage.alt = "ForgeMaster is supervising";
    fmCopy.textContent = "Supervising your workflow";
    setStep(2, "in-progress");
    typing.querySelector("p").textContent = "...";
    markPreviousFeedDone();
    addFeed("Your response was received. Hermes has resumed work.");
    addChatMessage("forgemaster", payload.acknowledgement);
    timer = window.setTimeout(() => completeWorkflow(payload), minimumStateMs);
  }

  function completeWorkflow(payload) {
    markPreviousFeedDone();
    setStep(2, "complete", payload.final_output || steps[2].dataset.output);
    setStatus("complete", "Complete");
    fmImage.src = root.dataset.completeImage;
    fmImage.alt = "ForgeMaster is happy";
    fmCopy.textContent = "Workflow complete";
    typing.hidden = true;
    masterDoc.hidden = false;
    addFeed("Hermes completed the summary.", true);
    addFeed(payload.completion_message, true);
    addChatMessage("forgemaster", "The workflow is complete. Ask me anything about the progress or results.");
    chatSend.disabled = false;
    actions.replaceChildren();
    actions.hidden = false;
    const download = document.createElement("button");
    download.type = "button";
    download.className = "session-btn download";
    download.textContent = "⬇ Download results";
    const fresh = document.createElement("a");
    fresh.className = "session-btn new session-nav-link";
    fresh.href = root.dataset.workspaceUrl;
    fresh.textContent = "＋ Start new workflow";
    actions.append(download, fresh);
  }

  function renderFiles() {
    fileList.replaceChildren();
    fileCount.textContent = `${attachedFiles.length} ${attachedFiles.length === 1 ? "file" : "files"}`;
    fileEmpty.hidden = attachedFiles.length > 0;
    fileList.hidden = attachedFiles.length === 0;
    attachedFiles.forEach((file, index) => {
      const row = document.createElement("div");
      row.className = "session-file-row";
      row.innerHTML = `<span class="session-file-icon">↗</span><div><strong></strong><small></small></div><button type="button" aria-label="Remove file">×</button>`;
      row.querySelector("strong").textContent = file.name;
      row.querySelector("small").textContent = `Working session · ${Math.max(1, Math.ceil(file.size / 1024))} KB`;
      row.querySelector("button").addEventListener("click", () => { attachedFiles.splice(index, 1); renderFiles(); });
      fileList.append(row);
    });
  }

  pause.addEventListener("click", () => {
    if (workflowStatus === "running") {
      window.clearTimeout(timer);
      setStatus("paused", "Paused");
      pause.className = "session-btn resume";
      pause.textContent = "▶ Resume workflow";
      return;
    }
    if (workflowStatus === "paused") {
      setStatus("running", "Running");
      pause.className = "session-btn pause";
      pause.textContent = "⏸ Pause workflow";
      scheduleNext();
    }
  });
  cancel.addEventListener("click", () => { window.location.href = root.dataset.workspaceUrl; });
  chatSend.addEventListener("click", () => { void sendChat(); });
  chatMessage.addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); void sendChat(); } });
  document.querySelector("#session-attach").addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => { attachedFiles.push(...fileInput.files); renderFiles(); fileInput.value = ""; });
  document.querySelectorAll("[data-scroll]").forEach((button) => button.addEventListener("click", () => document.querySelector("#session-steps").scrollBy({top: button.dataset.scroll === "up" ? -120 : 120, behavior: "smooth"})));
  document.querySelector("#session-feed-expand").addEventListener("click", (event) => { feed.classList.toggle("expanded"); event.currentTarget.textContent = feed.classList.contains("expanded") ? "Reduce ↙" : "Expand ↗"; });
  document.querySelectorAll(".session-download-files").forEach((button) => button.addEventListener("click", () => addFeed("No downloadable artifact has been generated in this local simulation.", true)));

  updateProgress();
  scheduleNext();
})();
