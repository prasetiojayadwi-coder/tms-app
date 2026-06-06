/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.7',
    build: 82,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Perbaikan freeze Sparepart Master di HP + render cepat & UI toolbar mobile.',
    changes: [
        { icon: 'fa-bolt', text: 'Sparepart Master: render sekali (bukan loop innerHTML) — tidak freeze di HP' },
        { icon: 'fa-mobile-screen', text: 'HP hanya render kartu; desktop hanya tabel — hemat memori' },
        { icon: 'fa-list', text: 'Pagination 60 item + tombol Tampilkan Lagi untuk katalog besar' },
        { icon: 'fa-table-columns', text: 'Toolbar mobile Customer/Sparepart: class grid benar-benar aktif' }
    ]
};
