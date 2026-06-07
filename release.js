/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.3',
    build: 112,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Foto kondisi unit — tombol Ambil Foto langsung buka kamera HP.',
    changes: [
        { icon: 'fa-camera', text: 'Ambil Foto: capture kamera belakang HP (before & after repair)' },
        { icon: 'fa-images', text: 'Galeri: pilih banyak foto dari album' },
        { icon: 'fa-plus', text: 'Bisa ambil beberapa foto berturut dari kamera' }
    ]
};
