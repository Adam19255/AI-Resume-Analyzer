// ===========================================================
// Loader and Progress Simulation
// ===========================================================
let progressInterval;
let progress = 0;

function startLoading() {
  const loader = document.getElementById("loader");
  const progressText = document.getElementById("progress-text");
  const progressFill = document.getElementById("progress-fill");

  loader.style.display = "flex";
  loader.classList.remove("fade-out");
  progress = 0;
  progressFill.style.width = "0%";
  progressText.textContent = "Analyzing your resume... 0%";

  progressInterval = setInterval(() => {
    if (progress < 90) {
      progress += Math.random() * 5;
      progressFill.style.width = progress.toFixed(0) + "%";
      progressText.textContent = `Analyzing your resume... ${progress.toFixed(0)}%`;
    }
  }, 300);
}

// ===========================================================
// Hide Loader Smoothly When Page Reloads (After Analysis)
// ===========================================================
window.addEventListener("load", () => {
  clearInterval(progressInterval);
  const loader = document.getElementById("loader");

  if (loader) {
    loader.classList.add("fade-out");
    setTimeout(() => {
      loader.style.display = "none";
      animateMetrics();
    }, 500);
  }
});

// ===========================================================
// Animated Metric Bars
// ===========================================================
function animateMetrics() {
  const metricBars = document.querySelectorAll(".metric-bar-fill");

  metricBars.forEach((bar) => {
    const value = parseFloat(bar.getAttribute("data-value"));
    if (!isNaN(value)) {
      let current = 0;
      const target = Math.min(value * 100, 100);
      const interval = setInterval(() => {
        if (current >= target) clearInterval(interval);
        else {
          current += 1;
          bar.style.width = current + "%";
          bar.textContent = current + "%";
        }
      }, 15);
    }
  });
}

// ===========================================================
// Toggle LLM Feedback
// ===========================================================
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("toggle-llm");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", async () => {
      toggleBtn.disabled = true;
      toggleBtn.textContent = "Toggling...";

      try {
        const res = await fetch("/toggle_llm", { method: "POST" });
        const data = await res.json();

        if (data.USE_LLM_FEEDBACK) {
          toggleBtn.textContent = "LLM Feedback: ON";
          toggleBtn.classList.remove("off");
        } else {
          toggleBtn.textContent = "LLM Feedback: OFF";
          toggleBtn.classList.add("off");
        }
      } catch {
        toggleBtn.textContent = "Error toggling!";
      } finally {
        toggleBtn.disabled = false;
      }
    });
  }

  // ===========================================================
  // Dynamic Weight Controls
  // ===========================================================
  ["similarity", "skill", "keyword", "section"].forEach((id) => {
    const range = document.getElementById(`w-${id}`);
    const valDisplay = document.getElementById(`val-${id}`);

    if (range && valDisplay) {
      range.addEventListener("input", () => {
        valDisplay.textContent = range.value;
      });
    }
  });

  const saveBtn = document.getElementById("save-weights");
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const weights = {
        similarity: parseFloat(document.getElementById("w-similarity").value),
        skill_coverage: parseFloat(document.getElementById("w-skill").value),
        keyword_density: parseFloat(document.getElementById("w-keyword").value),
        section_completeness: parseFloat(document.getElementById("w-section").value),
      };

      try {
        const res = await fetch("/update_weights", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(weights),
        });
        await res.json();
        alert("✅ Weights updated successfully!");
      } catch (err) {
        alert("❌ Failed to update weights. Check console.");
        console.error(err);
      }
    });
  }
});
