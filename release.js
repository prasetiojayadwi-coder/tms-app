/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.6',
    build: 115,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Klarifikasi PJ — teknisi baru paham tiket mana yang boleh dikerjakan.',
    changes: [
        { icon: 'fa-filter', text: 'Filter Tiket Saya (PJ) untuk teknisi lapangan' },
        { icon: 'fa-user-lock', text: 'Label PJ: [nama] menggantikan Menunggu Giliran yang membingungkan' },
        { icon: 'fa-highlighter', text: 'Highlight emas pada baris tiket milik Anda (PJ)' },
        { icon: 'fa-circle-info', text: 'Banner penjelasan: hanya PJ yang ditunjuk SPV boleh mengerjakan' }
    ]
};
