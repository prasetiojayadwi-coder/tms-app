/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.8',
    build: 96,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Perbaikan Pickup Unit — modal tanda tangan terbuka di PC & HP.',
    changes: [
        { icon: 'fa-truck-pickup', text: 'Service: fix ID tiket (Number) — Pickup/Konfirmasi On-Site buka modal' },
        { icon: 'fa-hand-pointer', text: 'Tombol aksi service — onclick langsung actionServiceTicket' },
        { icon: 'fa-shield-halved', text: 'findServiceTicket + openModal aman jika elemen hilang' }
    ]
};
