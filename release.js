/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.1',
    build: 89,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Perbaikan kritis — daftar customer kosong di HP.',
    changes: [
        { icon: 'fa-bug', text: 'Fix: kartu customer HP terhapus setelah render — daftar & pesan kosong tampil' },
        { icon: 'fa-cloud-arrow-down', text: 'Buka Customer Master otomatis tarik data cloud jika lokal kosong' },
        { icon: 'fa-mobile-screen', text: 'Kartu customer selalu di-render di HP (tidak bergantung deteksi viewport)' }
    ]
};
