/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.9.1',
    build: 86,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Smart Search pada Customer Units — filter cepat per customer.',
    changes: [
        { icon: 'fa-magnifying-glass', text: 'Customer Units: smart search description, SN, art no, product, lokasi' },
        { icon: 'fa-filter', text: 'Subtitle menampilkan jumlah hasil filter vs total unit' },
        { icon: 'fa-mobile-screen', text: 'Pencarian aktif di tab Units HP setelah pilih customer' }
    ]
};
