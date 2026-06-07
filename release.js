/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.5',
    build: 114,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Penguatan PJ — heal otomatis saat sync cloud & notifikasi login teknisi.',
    changes: [
        { icon: 'fa-cloud', text: 'Sanitize DB: relink PJ semua teknisi saat migrasi/sync cloud' },
        { icon: 'fa-bell', text: 'Login teknisi: toast jika penugasan PJ diselaraskan otomatis' },
        { icon: 'fa-shield', text: 'v7.6.4 fixes tetap: On-Site, user baru, auto-heal PJ' }
    ]
};
