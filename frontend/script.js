const API_BASE = "http://127.0.0.1:8001";

const singleLogInput = document.getElementById("singleLog");
const batchLogsInput = document.getElementById("batchLogs");

const analyzeSingleBtn = document.getElementById("analyzeSingleBtn");
const analyzeBatchBtn = document.getElementById("analyzeBatchBtn");
const clearSingleBtn = document.getElementById("clearSingleBtn");
const clearBatchBtn = document.getElementById("clearBatchBtn");

const resultBox = document.getElementById("resultBox");
const statusBadge = document.getElementById("statusBadge");

function setStatus(type, text) {
  statusBadge.className = `status ${type}`;
  statusBadge.textContent = text;
}

function toggleButtons(disabled) {
  analyzeSingleBtn.disabled = disabled;
  analyzeBatchBtn.disabled = disabled;
  clearSingleBtn.disabled = disabled;
  clearBatchBtn.disabled = disabled;
}

function showEmpty() {
  setStatus("idle", "Waiting");
  resultBox.innerHTML = `
    <div class="empty">
      <div>
        <div class="empty-icon">✨</div>
        <h3>No result yet</h3>
        <p>Run an analysis to see results here.</p>
      </div>
    </div>
  `;
}

function showLoading(text) {
  setStatus("loading", "Analyzing");
  resultBox.innerHTML = `
    <div class="loading-box">
      <p>⏳ ${text}</p>
    </div>
  `;
}

function showError(message) {
  setStatus("error", "Failed");
  resultBox.innerHTML = `
    <div class="error-box">
      <p>❌ ${message}</p>
    </div>
  `;
}

function showResult(data) {
  setStatus("success", "Completed");

  const confidence = ((data.confidence || 0) * 100).toFixed(2);

  resultBox.innerHTML = `
    <div class="result-grid">
      <div class="result-item">
        <span class="label">Issue Type</span>
        <div class="value issue">${data.issue_type || "N/A"}</div>
      </div>

      <div class="result-item">
        <span class="label">Confidence</span>
        <div class="value">${confidence}%</div>
      </div>

      <div class="result-item full">
        <span class="label">Root Cause</span>
        <div class="value">${data.root_cause || "N/A"}</div>
      </div>

      <div class="result-item full">
        <span class="label">Suggested Fix</span>
        <div class="value fix">${data.suggested_fix || "N/A"}</div>
      </div>

      <div class="result-item full">
        <span class="label">Reasoning</span>
        <div class="value reasoning">${data.reasoning || "N/A"}</div>
      </div>
    </div>
  `;
}

analyzeSingleBtn.addEventListener("click", async () => {
  const logText = singleLogInput.value.trim();

  if (!logText) {
    showError("Please enter a single log first.");
    return;
  }

  showLoading("Analyzing single log...");
  toggleButtons(true);

  const formData = new FormData();
  formData.append("log_text", logText);

  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (result.status === "success") {
      showResult(result.data);
    } else {
      showError(result.message || "Something went wrong.");
    }
  } catch (error) {
    showError("Could not connect to backend.");
  } finally {
    toggleButtons(false);
  }
});

analyzeBatchBtn.addEventListener("click", async () => {
  const batchText = batchLogsInput.value.trim();

  if (!batchText) {
    showError("Please enter batch logs first.");
    return;
  }

  const logs = batchText
    .split("\n")
    .map(line => line.trim())
    .filter(line => line);

  if (logs.length === 0) {
    showError("Please enter valid batch logs.");
    return;
  }

  showLoading("Analyzing batch logs...");
  toggleButtons(true);

  try {
    const response = await fetch(`${API_BASE}/analyze-batch`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ logs })
    });

    const result = await response.json();

    if (result.status === "success") {
      showResult(result.data);
    } else {
      showError(result.message || "Something went wrong.");
    }
  } catch (error) {
    showError("Could not connect to backend.");
  } finally {
    toggleButtons(false);
  }
});

clearSingleBtn.addEventListener("click", () => {
  singleLogInput.value = "";
  showEmpty();
});

clearBatchBtn.addEventListener("click", () => {
  batchLogsInput.value = "";
  showEmpty();
});

showEmpty();