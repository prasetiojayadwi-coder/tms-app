/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.3',
    build: 68,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'UAT bugfixes — unique ID allocation and owner account stability.',
    changes: [
        { icon: 'fa-bug', text: 'Fix allocateUniqueId() — monotonic IDs prevent combined SPH PO sync missing tickets' },
        { icon: 'fa-user-shield', text: 'Fix owner account (direktur) removed by duplicate phone sanitize' },
        { icon: 'fa-clipboard-check', text: 'UAT pack v1.3 — 56 Pass automated via uat_sph_runner.py' },
        { icon: 'fa-ban', text: 'Cancel SPH — reset toolStatus, role guard, and service notifications on revert' },
        { icon: 'fa-file-pdf', text: 'Export SPH to PDF — corporate layout for single and combined quotations' },
        { icon: 'fa-magnifying-glass', text: 'Partial Smart Fill — autocomplete Art Number with keyboard navigation' }
    ]
};
