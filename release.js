/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.1',
    build: 66,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'SPH cancel hardening, doc preview in detail modal, and Phase 5–6 documentation sync.',
    changes: [
        { icon: 'fa-ban', text: 'Cancel SPH — reset toolStatus, role guard, and service notifications on revert' },
        { icon: 'fa-file-image', text: 'SPH detail modal — embedded preview for PO and SPH attachments' },
        { icon: 'fa-chart-simple', text: 'SPH Log — Cancelled stat counter added' },
        { icon: 'fa-file-pdf', text: 'Export SPH to PDF — corporate layout for single and combined quotations' },
        { icon: 'fa-magnifying-glass', text: 'Partial Smart Fill — autocomplete Art Number with keyboard navigation' },
        { icon: 'fa-building', text: 'Combined SPH customer picker when multiple customers are eligible' },
        { icon: 'fa-location-dot', text: 'On-Site quotation modal — no Un-Repair option, path-specific labels' }
    ]
};
