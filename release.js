/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.6',
    build: 81,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Tampilan HP — toolbar & kartu tombol seragam, palet elegan monokrom.',
    changes: [
        { icon: 'fa-mobile-screen', text: 'Customer & Sparepart Master: grid toolbar rapi di HP' },
        { icon: 'fa-palette', text: 'Tombol seragam — primary gelap/terang, outline & ghost netral' },
        { icon: 'fa-layer-group', text: 'Aksi kartu mobile: Edit/Units/Delete tanpa warna-warni' },
        { icon: 'fa-chart-simple', text: 'Statistik & judul section: tone netral di mobile' }
    ]
};
