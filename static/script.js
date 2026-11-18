/**
 * ==========================================================
 *  Vehicle Fuel Efficiency Predictor — Frontend Logic
 * ==========================================================
 */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predict-form");
    const btn = document.getElementById("predict-btn");
    const btnText = document.getElementById("btn-text");
    const resultSection = document.getElementById("result-section");
    const resultValue = document.getElementById("result-value");
    const resultUnit = document.getElementById("result-unit");
    const resultBadge = document.getElementById("result-badge");
    const gaugeNeedle = document.getElementById("gauge-needle");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Collect form data
        const data = {
            Fuel_Type: document.getElementById("fuel-type").value,
            Engine_CC: parseInt(document.getElementById("engine-cc").value),
            Cylinders: parseInt(document.getElementById("cylinders").value),
            Gears: parseInt(document.getElementById("gears").value),
            Power_HP: parseInt(document.getElementById("power-hp").value),
            Transmission: document.getElementById("transmission").value,
            Body_Type: document.getElementById("body-type").value,
            Driving_Condition: document.getElementById("driving-condition").value,
        };

        // Validate
        for (const [key, val] of Object.entries(data)) {
            if (val === "" || val === null || (typeof val === "number" && isNaN(val))) {
                showError(`Please fill in: ${key.replace(/_/g, " ")}`);
                return;
            }
        }

        // Show loading state
        btn.classList.add("loading");
        btnText.textContent = "";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success) {
                showResult(result.prediction);
            } else {
                showError(result.error);
            }
        } catch (err) {
            showError("Connection error. Make sure the server is running.");
        } finally {
            btn.classList.remove("loading");
            btnText.textContent = "⚡ Predict Efficiency";
        }
    });

    function showResult(value) {
        resultSection.classList.add("visible");
        const card = resultSection.querySelector(".result-card");
        card.classList.remove("error");

        // Animate the number counting up
        animateValue(resultValue, 0, value, 800);
        resultUnit.textContent = "km/l";

        // Set efficiency badge
        let badgeText, badgeClass;
        if (value >= 20) {
            badgeText = "🌿 Excellent Efficiency";
            badgeClass = "badge-excellent";
        } else if (value >= 15) {
            badgeText = "👍 Good Efficiency";
            badgeClass = "badge-good";
        } else if (value >= 10) {
            badgeText = "⚠️ Average Efficiency";
            badgeClass = "badge-average";
        } else {
            badgeText = "🔴 Poor Efficiency";
            badgeClass = "badge-poor";
        }

        resultBadge.textContent = badgeText;
        resultBadge.className = "result-badge " + badgeClass;

        // Animate gauge needle (0-30 km/l mapped to -90deg to 90deg)
        const clamped = Math.min(Math.max(value, 0), 30);
        const angle = -90 + (clamped / 30) * 180;
        gaugeNeedle.style.transform = `translateX(-50%) rotate(${angle}deg)`;

        // Scroll to result
        resultSection.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function showError(message) {
        resultSection.classList.add("visible");
        const card = resultSection.querySelector(".result-card");
        card.classList.add("error");
        resultValue.textContent = "⚠";
        resultValue.style.fontSize = "2.5rem";
        resultUnit.textContent = "";
        resultBadge.textContent = message;
        resultBadge.className = "result-badge badge-poor";

        // Reset gauge
        gaugeNeedle.style.transform = `translateX(-50%) rotate(-90deg)`;

        setTimeout(() => {
            resultValue.style.fontSize = "";
        }, 3000);

        resultSection.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function animateValue(element, start, end, duration) {
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = start + (end - start) * eased;

            element.textContent = current.toFixed(1);

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }
});
