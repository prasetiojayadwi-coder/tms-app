/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.5',
    build: 80,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Perbaikan sync HP↔PC: sparepart tampil, unit yatim dibersihkan.',
    changes: [
        { icon: 'fa-mobile-screen', text: 'Sparepart Master: kartu mobile + sync cloud spareparts/SPH' },
        { icon: 'fa-arrows-rotate', text: 'Merge database sekarang gabung spareparts antar perangkat' },
        { icon: 'fa-broom', text: 'Unit tanpa customer (yatim) otomatis dibersihkan — statistik akurat' },
        { icon: 'fa-trash', text: 'Hapus customer/unit/sparepart tercatat untuk sync antar HP & PC' }
    ]
};
