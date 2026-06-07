/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.9',
    build: 118,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix Pickup Unit — teknisi lapangan tidak perlu TTD PIC untuk mulai kerja.',
    changes: [
        { icon: 'fa-truck-pickup', text: 'Pickup TSF Workshop: 1 klik langsung (tanpa modal TTD PIC)' },
        { icon: 'fa-file-signature', text: 'TTD PIC opsional via menu Tanda Terima' },
        { icon: 'fa-shield', text: 'Status pickup tidak revert setelah simpan' }
    ]
};
