/**
 * Scheme Sarthi - Interactive Client Script
 * Handles tabs switching, document checklist verification, income slider formatting, and tracking.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Income Slider formatting
    const incomeSlider = document.getElementById("incomeRange");
    const incomeDisplay = document.getElementById("incomeDisplay");
    
    if (incomeSlider && incomeDisplay) {
        incomeSlider.addEventListener("input", (e) => {
            const val = parseFloat(e.target.value);
            if (val >= 100000) {
                const lakhs = (val / 100000).toFixed(2);
                incomeDisplay.textContent = `₹${lakhs} Lakhs (₹${parseInt(val).toLocaleString('en-IN')})`;
            } else {
                incomeDisplay.textContent = `₹${parseInt(val).toLocaleString('en-IN')}`;
            }
        });
    }

    // 2. Tab switching logic inside Scheme cards
    document.querySelectorAll(".tab-btn").forEach(button => {
        button.addEventListener("click", () => {
            const schemeId = button.dataset.scheme;
            const tabTarget = button.dataset.tab;

            // Deactivate all sibling buttons
            const parent = button.closest(".scheme-card");
            parent.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
            parent.querySelectorAll(".tab-content").forEach(content => content.classList.remove("active"));

            // Activate clicked button and target tab
            button.classList.add("active");
            const targetEl = parent.querySelector(`#tab-${schemeId}-${tabTarget}`);
            if (targetEl) {
                targetEl.classList.add("active");
            }
        });
    });

    // 3. Document Checklist Progress Tracking
    document.querySelectorAll(".doc-checkbox").forEach(box => {
        box.addEventListener("change", (e) => {
            const parentList = e.target.closest(".doc-checklist");
            if (parentList) {
                const total = parentList.querySelectorAll(".doc-checkbox").length;
                const checked = parentList.querySelectorAll(".doc-checkbox:checked").length;
                const countBadge = parentList.closest(".tab-content").querySelector(".doc-count-badge");
                if (countBadge) {
                    countBadge.textContent = `${checked}/${total} Ready`;
                    if (checked === total) {
                        countBadge.className = "doc-count-badge badge-status badge-success";
                    } else {
                        countBadge.className = "doc-count-badge badge-status badge-warning";
                    }
                }
            }
        });
    });
});

/**
 * Initiates application tracking registration via API and redirects to tracker
 */
function initiateApplyAndTrack(schemeName, officialUrl) {
    const applicantName = prompt("Enter your Name for application tracking record:", "Student Applicant");
    if (!applicantName) return;

    fetch("/api/register_track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            scheme_name: schemeName,
            applicant_name: applicantName,
            state: "Karnataka"
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert(`Application Tracking ID generated!\n\nID: ${data.app_id}\n\nYou will now be redirected to the Official Government Portal (${officialUrl}) to complete your application.`);
            // Open official portal in new tab
            window.open(officialUrl, "_blank");
            // Redirect current page to tracker
            window.location.href = `/tracker?app_id=${data.app_id}`;
        }
    })
    .catch(err => {
        console.error("Tracking registration error:", err);
        window.open(officialUrl, "_blank");
    });
}
