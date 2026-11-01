/**
 * Health360: Dynamic Healthcare Analytics Engine
 * Manages real-time multi-dimensional filter interaction, KPI updates,
 * and high-performance Plotly rendering.
 */

document.addEventListener('DOMContentLoaded', function () {
    initFilters();
    initTooltips();
    window.addEventListener('resize', debounceResize);
});

// Cache current chart instances
let activeCharts = {};

function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Filter Form Handler
 */
function initFilters() {
    const filterForm = document.getElementById('global-filter-form');
    if (!filterForm) return;

    filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        applyCurrentFilters();
    });

    const resetBtn = document.getElementById('btn-reset-filters');
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            filterForm.reset();
            applyCurrentFilters();
        });
    }

    // Auto-apply on change if requested
    const autoSelects = filterForm.querySelectorAll('select');
    autoSelects.forEach(sel => {
        sel.addEventListener('change', function () {
            applyCurrentFilters();
        });
    });
}

/**
 * Collect filter payload and request updated metrics & charts from backend
 */
function applyCurrentFilters() {
    const filterForm = document.getElementById('global-filter-form');
    if (!filterForm) return;

    const formData = new FormData(filterForm);
    const filterPayload = {};

    formData.forEach((val, key) => {
        filterPayload[key] = val;
    });

    // Show loading indicators on KPIs
    showKpiLoading();

    // Send AJAX request to Flask endpoint
    fetch('/api/filter-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(filterPayload)
    })
    .then(response => {
        if (!response.ok) throw new Error('Network error filtering data');
        return response.json();
    })
    .then(data => {
        updateKPIs(data.kpis);
        updateCharts(data.charts);
        updateActiveFilterTags(filterPayload);
        if (data.insights_summary) {
            updateQuickInsights(data.insights_summary);
        }
    })
    .catch(err => {
        console.error('Error applying filters:', err);
    });
}

/**
 * Update KPI values smoothly with animated count-up
 */
function updateKPIs(kpis) {
    if (!kpis) return;

    animateValue('kpi-total-patients', kpis.total_patients, 0);
    animateValue('kpi-avg-bp', kpis.avg_bp, 2, ' mmHg');
    animateValue('kpi-avg-bmi', kpis.avg_bmi, 1, ' kg/m²');
    animateValue('kpi-avg-risk', kpis.avg_risk_score, 1, '/100');
    
    // Disease counts & percentages
    const hdElem = document.getElementById('kpi-heart-disease');
    if (hdElem) {
        hdElem.innerHTML = `${kpis.heart_disease_count.toLocaleString()} <span class="badge bg-danger-subtle text-danger ms-1 fs-6">${kpis.heart_disease_pct}%</span>`;
    }

    const diabElem = document.getElementById('kpi-diabetes');
    if (diabElem) {
        diabElem.innerHTML = `${kpis.diabetes_count.toLocaleString()} <span class="badge bg-warning-subtle text-warning ms-1 fs-6">${kpis.diabetes_pct}%</span>`;
    }

    const strokeElem = document.getElementById('kpi-stroke');
    if (strokeElem) {
        strokeElem.innerHTML = `${kpis.stroke_count.toLocaleString()} <span class="badge bg-info-subtle text-info ms-1 fs-6">${kpis.stroke_pct}%</span>`;
    }

    const fatigueElem = document.getElementById('kpi-fatigue');
    if (fatigueElem) {
        fatigueElem.innerHTML = `${kpis.fatigue_count.toLocaleString()} <span class="badge bg-secondary-subtle text-secondary ms-1 fs-6">${kpis.fatigue_pct}%</span>`;
    }

    const recPill = document.getElementById('filter-record-count');
    if (recPill) {
        recPill.textContent = `${kpis.total_patients.toLocaleString()} Patients Filtered`;
    }
}

/**
 * Update Plotly Charts using Plotly.react for 60fps instant transitions
 */
function updateCharts(charts) {
    if (!charts) return;

    const chartMapping = {
        'chart_exercise_donut': 'container-exercise-donut',
        'chart_bp_by_age': 'container-bp-by-age',
        'chart_alcohol_smoking': 'container-alcohol-smoking',
        'chart_bmi_hd_rate': 'container-bmi-hd-rate',
        'chart_hd_vs_diabetes': 'container-hd-vs-diabetes',
        'chart_age_pie': 'container-age-pie',
        'chart_heatmap': 'container-heatmap',
        'chart_age_fatigue': 'container-age-fatigue'
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    for (const [chartKey, containerId] of Object.entries(chartMapping)) {
        const container = document.getElementById(containerId);
        if (container && charts[chartKey]) {
            const chartData = charts[chartKey];
            Plotly.react(container, chartData.data, chartData.layout, config);
            activeCharts[containerId] = true;
        }
    }
}

/**
 * Display active filter badges with quick remove buttons
 */
function updateActiveFilterTags(filters) {
    const container = document.getElementById('active-filters-container');
    if (!container) return;

    container.innerHTML = '';
    let hasActive = false;

    for (const [key, val] of Object.entries(filters)) {
        if (val && val !== 'All') {
            hasActive = true;
            const tag = document.createElement('span');
            tag.className = 'badge bg-light text-dark border me-1 mb-1 p-2 font-monospace';
            tag.innerHTML = `<strong>${formatFilterKey(key)}:</strong> ${val} <i class="bi bi-x-circle ms-1 cursor-pointer text-danger" onclick="clearSpecificFilter('${key}')"></i>`;
            container.appendChild(tag);
        }
    }

    const clearAllBtn = document.getElementById('btn-clear-all-tags');
    if (clearAllBtn) {
        clearAllBtn.style.display = hasActive ? 'inline-block' : 'none';
    }
}

function clearSpecificFilter(key) {
    const filterForm = document.getElementById('global-filter-form');
    if (!filterForm) return;

    const elem = filterForm.elements[key];
    if (elem) {
        elem.value = 'All';
        applyCurrentFilters();
    }
}

function formatFilterKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Number animation helper
 */
function animateValue(id, endValue, decimals = 0, suffix = '') {
    const obj = document.getElementById(id);
    if (!obj) return;
    obj.innerHTML = `${Number(endValue).toFixed(decimals).toLocaleString()}${suffix}`;
}

function showKpiLoading() {
    // Subtle indicator without layout shift
    const recPill = document.getElementById('filter-record-count');
    if (recPill) {
        recPill.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span> Updating...';
    }
}

function updateQuickInsights(summary) {
    const box = document.getElementById('quick-insight-banner');
    if (box && summary) {
        box.textContent = summary;
    }
}

let resizeTimeout;
function debounceResize() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        for (const containerId of Object.keys(activeCharts)) {
            const container = document.getElementById(containerId);
            if (container) {
                Plotly.Plots.resize(container);
            }
        }
    }, 200);
}
