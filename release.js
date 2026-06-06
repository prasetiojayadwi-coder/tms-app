/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.4',
    build: 69,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Render performance — sparepart master & SPH log load faster at scale.',
    changes: [
        { icon: 'fa-gauge-high', text: 'Optimize renderSparepartMaster — batch DOM write (500+ rows under 150ms)' },
        { icon: 'fa-gauge-high', text: 'Optimize renderSphLog — Map lookup + single innerHTML assign' },
        { icon: 'fa-clipboard-check', text: 'Strict audit — audit_strict.py benchmarks pass, 0 bottlenecks' },
        { icon: 'fa-bug', text: 'Fix allocateUniqueId() — monotonic IDs prevent combined SPH PO sync missing tickets' },
        { icon: 'fa-user-shield', text: 'Fix owner account (direktur) removed by duplicate phone sanitize' },
        { icon: 'fa-clipboard-check', text: 'UAT Phase 2 UI — 24 Pass via uat_sph_ui_runner.py' }
    ]
};
