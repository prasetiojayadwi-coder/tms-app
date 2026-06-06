/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.1.0',
    build: 98,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix klik Pickup — handler global + auto-repair PJ tiket untuk teknisi.',
    changes: [
        { icon: 'fa-hand-pointer', text: 'Service: klik global capture — tombol Pickup selalu jalan' },
        { icon: 'fa-user-gear', text: 'Auto-repair PJ by nama (Suci) jika ID tidak cocok' },
        { icon: 'fa-truck-pickup', text: 'Modal TTD z-500 + toast error jika form gagal buka' }
    ]
};
