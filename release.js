/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.5.5',
    build: 107,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix kritis On-Site — satu klik langsung konfirmasi tanpa modal TTD.',
    changes: [
        { icon: 'fa-bolt', text: 'On-Site: klik KONFIRMASI langsung aktifkan tiket (tanpa modal)' },
        { icon: 'fa-user-shield', text: 'Sync user aman — tidak logout saat klik aksi tiket' },
        { icon: 'fa-signature', text: 'Canvas TTD: koordinat touch/mouse diperbaiki' },
        { icon: 'fa-hand-pointer', text: 'Tombol aksi: anti double-click, handler tunggal' }
    ]
};
