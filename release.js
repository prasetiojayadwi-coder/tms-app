/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.3.0',
    build: 61,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Batch Excel import for Customer Master, Special Tools, and Backup Units — plus a mobile-friendly Customer Master layout.',
    changes: [
        { icon: 'fa-file-import', text: 'Batch Excel import — upload .xlsx/.csv with one field per column for customers, units, tools, and backup units' },
        { icon: 'fa-download', text: 'Downloadable import templates with correct column headers for each module' },
        { icon: 'fa-mobile-screen', text: 'Customer Master mobile UI — tab switcher, card layout, and larger touch targets on phone' },
        { icon: 'fa-tags', text: 'Product categories — Avitum, Hospital Care, and Aesculap with auto-migration' },
        { icon: 'fa-hospital', text: 'Customer Master linked to Customer Service & Repair workflows' },
        { icon: 'fa-bell', text: 'Update notification with changelog summary on new releases' }
    ]
};
