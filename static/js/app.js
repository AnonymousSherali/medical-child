/* NeuroMonitor — umumiy interfeys skriptlari */
(function () {
    'use strict';

    var THEME_KEY = 'nm-theme';
    var root = document.documentElement;

    function storedTheme() {
        try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
    }

    function preferredTheme() {
        return storedTheme() ||
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }

    function applyTheme(theme) {
        root.setAttribute('data-bs-theme', theme);
        document.querySelectorAll('[data-theme-icon]').forEach(function (icon) {
            icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        });
    }

    /* ---------- Grafiklar ---------- */
    var chartBuilders = [];
    var chartInstances = [];

    function cssVar(name) {
        return getComputedStyle(root).getPropertyValue(name).trim();
    }

    function palette() {
        return {
            primary: '#2563eb',
            teal: '#14b8a6',
            danger: '#ef4444',
            warning: '#f59e0b',
            success: '#22c55e',
            violet: '#8b5cf6',
            text: cssVar('--bs-secondary-color') || '#6b7280',
            grid: cssVar('--bs-border-color') || '#e5e7eb'
        };
    }

    function baseOptions() {
        var c = palette();
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: c.text, usePointStyle: true, boxWidth: 8 } },
                tooltip: { padding: 10, cornerRadius: 8 }
            },
            scales: {
                x: { ticks: { color: c.text }, grid: { color: c.grid, drawBorder: false } },
                y: { ticks: { color: c.text }, grid: { color: c.grid, drawBorder: false }, beginAtZero: true }
            }
        };
    }

    /* Gorizontal me'yor chizig'i: options.plugins.nmRefLines = { lines: [{ value, label }] }.
       Dataset sifatida chizilgan chiziqdan farqli, bitta o'lchov bo'lganda ham ko'rinadi. */
    var refLinesPlugin = {
        id: 'nmRefLines',
        afterDatasetsDraw: function (chart, args, opts) {
            var lines = (opts && opts.lines) || [];
            var scale = chart.scales.y;
            var area = chart.chartArea;
            var ctx = chart.ctx;
            lines.forEach(function (line) {
                if (line.value === null || line.value === undefined || !scale) { return; }
                var y = scale.getPixelForValue(line.value);
                if (y < area.top - 1 || y > area.bottom + 1) { return; }
                ctx.save();
                ctx.strokeStyle = line.color || '#ef4444';
                ctx.fillStyle = line.color || '#ef4444';
                ctx.setLineDash([6, 4]);
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(area.left, y);
                ctx.lineTo(area.right, y);
                ctx.stroke();
                if (line.label) {
                    ctx.setLineDash([]);
                    ctx.font = '600 10px Inter, system-ui, sans-serif';
                    ctx.textAlign = 'right';
                    ctx.fillText(line.label, area.right - 2, y - 4);
                }
                ctx.restore();
            });
        }
    };
    var pluginRegistered = false;

    function renderCharts() {
        if (typeof Chart === 'undefined') { return; }
        if (!pluginRegistered) { Chart.register(refLinesPlugin); pluginRegistered = true; }
        chartInstances.forEach(function (chart) { chart.destroy(); });
        chartInstances = chartBuilders.map(function (build) {
            return build(palette(), baseOptions());
        }).filter(Boolean);
    }

    /* ---------- Toastlar ---------- */
    function showToasts() {
        if (typeof bootstrap === 'undefined') { return; }
        document.querySelectorAll('.toast[data-autoshow]').forEach(function (el) {
            bootstrap.Toast.getOrCreateInstance(el, { delay: 5000 }).show();
        });
    }

    /* ---------- Tasdiqlash oynasi ----------
       <form data-confirm="Matn" data-confirm-title="Sarlavha" data-confirm-ok="Ha">
       Brauzerning standart confirm() oynasi o'rniga chiroyli modal ishlatiladi. */
    function setupConfirm() {
        var modalEl = document.getElementById('nmConfirmModal');
        if (!modalEl || typeof bootstrap === 'undefined') { return; }
        var modal = new bootstrap.Modal(modalEl);
        var pendingForm = null;

        document.addEventListener('submit', function (event) {
            var form = event.target;
            if (!form.matches('[data-confirm]') || form.dataset.confirmed === '1') { return; }
            event.preventDefault();
            pendingForm = form;
            modalEl.querySelector('[data-confirm-title]').textContent =
                form.dataset.confirmTitle || 'Tasdiqlang';
            modalEl.querySelector('[data-confirm-text]').textContent = form.dataset.confirm;
            modalEl.querySelector('[data-confirm-ok]').textContent =
                form.dataset.confirmOk || 'Tasdiqlash';
            modal.show();
        });

        modalEl.querySelector('[data-confirm-ok]').addEventListener('click', function () {
            if (!pendingForm) { return; }
            pendingForm.dataset.confirmed = '1';
            modal.hide();
            pendingForm.submit();
        });
    }

    /* ---------- Formani ikki marta yuborishdan himoya ---------- */
    function setupSubmitGuard() {
        document.addEventListener('submit', function (event) {
            var form = event.target;
            if (event.defaultPrevented || form.method.toLowerCase() !== 'post') { return; }
            var button = form.querySelector('button[type="submit"]');
            if (button && !button.disabled) {
                window.setTimeout(function () {
                    button.disabled = true;
                    button.insertAdjacentHTML('afterbegin',
                        '<span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>');
                }, 0);
            }
        });
    }

    window.NM = {
        /* fn(palette, baseOptions) -> Chart. Mavzu o'zgarganda qayta chiziladi. */
        chart: function (fn) {
            chartBuilders.push(fn);
            if (document.readyState !== 'loading') { renderCharts(); }
        },
        readJSON: function (id) {
            var el = document.getElementById(id);
            return el ? JSON.parse(el.textContent) : null;
        }
    };

    applyTheme(preferredTheme());

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(preferredTheme());

        document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
            button.addEventListener('click', function () {
                var next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
                try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* saqlab bo'lmasa ham ishlayveradi */ }
                applyTheme(next);
                renderCharts();
            });
        });

        if (typeof bootstrap !== 'undefined') {
            document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
                new bootstrap.Tooltip(el);
            });
        }

        showToasts();
        setupConfirm();
        setupSubmitGuard();
        renderCharts();
    });
})();
