/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.5',
    build: 93,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix tombol Pickup & Track tidak bisa diklik di HP — Service & Repair.',
    changes: [
        { icon: 'fa-mobile-screen', text: 'Service HP: tombol Pickup Unit & Track pakai event delegation + area sentuh 48px' },
        { icon: 'fa-hand-pointer', text: 'Perbaikan match teknisi PJ (assignedTsId) — tidak gagal karena tipe data' },
        { icon: 'fa-signature', text: 'Fix struktur HTML modal tanda tangan pickup' }
    ]
};
