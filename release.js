/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.4',
    build: 79,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Customer Master — Pilih Semua kembali di toolbar (mobile & desktop).',
    changes: [
        { icon: 'fa-check-double', text: 'Pilih Semua di toolbar Customer & Unit (tampil di HP)' },
        { icon: 'fa-table', text: 'Checkbox header tabel tetap ada & sinkron dengan toolbar' },
        { icon: 'fa-eye', text: 'Checkbox lebih terlihat di mode gelap' }
    ]
};
