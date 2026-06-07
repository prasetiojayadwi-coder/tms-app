/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.5.1',
    build: 103,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix PJ tiket service — teknisi bisa pickup/perbaiki tiket baru & lama.',
    changes: [
        { icon: 'fa-user-gear', text: 'PJ tiket: utamakan username, auto-sync ID, dukung tiket legacy' },
        { icon: 'fa-truck-pickup', text: 'Pickup/On-Site/Analisa: perbaikan penugasan + pesan error jelas' },
        { icon: 'fa-rotate', text: 'sanitize & render: sync assignedTsUser/Name/Id konsisten' },
        { icon: 'fa-screwdriver-wrench', text: 'ensureServiceTicketPjReady sebelum setiap aksi tiket' }
    ]
};
