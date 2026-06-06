/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.6',
    build: 94,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix Pickup Unit HP — onclick langsung + kartu selalu render, onsite tidak memblokir.',
    changes: [
        { icon: 'fa-hand-pointer', text: 'Pickup/Track: onclick langsung + window.runServiceTicketAction (fallback HP)' },
        { icon: 'fa-mobile-screen', text: 'Kartu service HP selalu di-render — tidak kosong saat deteksi layar salah' },
        { icon: 'fa-location-dot', text: 'On-Site Repair: tombol Konfirmasi On-Site + teks tanda tangan sesuai' }
    ]
};
