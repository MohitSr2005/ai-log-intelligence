const API_BASE = "http://127.0.0.1:8001";

const singleLogInput = document.getElementById("singleLog");
const batchLogsInput = document.getElementById("batchLogs");

const analyzeSingleBtn = document.getElementById("analyzeSingleBtn");
const analyzeBatchBtn = document.getElementById("analyzeBatchBtn");
const clearSingleBtn = document.getElementById("clearSingleBtn");
const clearBatchBtn = document.getElementById("clearBatchBtn");
const runAnalysisBtn = document.getElementById("runAnalysisBtn");

const resultBox = document.getElementById("resultBox");
const statusBadge = document.getElementById("statusBadge");

const totalEvents = document.getElementById("totalEvents");
const anomalies = document.getElementById("anomalies");
const patterns = document.getElementById("patterns");
const responseTime = document.getElementById("responseTime");

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
      <h3>No result yet</h3>
      <p>Run an analysis to see backend prediction here.</p>
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
    <div class="result-card">
      <h2 class="issue-type">${data.issue_type || "Unknown"}</h2>

      <p><b>Confidence:</b> ${confidence}%</p>

      <div class="result-section">
        <h4>Root Cause</h4>
        <p>${data.root_cause || "N/A"}</p>
      </div>

      <div class="result-section">
        <h4>Suggested Fix</h4>
        <p>${data.suggested_fix || "N/A"}</p>
      </div>

      <div class="result-section">
        <h4>Reasoning</h4>
        <p>${data.reasoning || "N/A"}</p>
      </div>
    </div>
  `;
}

async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard`);
    const data = await res.json();

    totalEvents.textContent = data.total_events ?? 0;
    anomalies.textContent = data.anomalies_detected ?? 0;
    patterns.textContent = data.ai_patterns_found ?? 0;
    responseTime.textContent = data.avg_response_time ?? "0ms";
  } catch (err) {
    console.error("Dashboard backend not connected:", err);
  }
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
      loadDashboard();
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
      showResult(Array.isArray(result.data) ? result.data[0] : result.data);
      loadDashboard();
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

runAnalysisBtn.addEventListener("click", () => {
  loadDashboard();
});

showEmpty();
loadDashboard();