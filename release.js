/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.1',
    build: 110,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Smart Fill Customer & Unit — searchable combobox untuk ribuan data.',
    changes: [
        { icon: 'fa-magnifying-glass', text: 'Load Master Data: cari customer by nama/kode (bukan dropdown panjang)' },
        { icon: 'fa-hospital', text: 'Customer Units: cari by nama, Art No, SN setelah customer dipilih' },
        { icon: 'fa-keyboard', text: 'Arrow + Enter untuk pilih; fokus unit tampilkan daftar singkat' },
        { icon: 'fa-bolt', text: 'Pilih customer/unit → form terisi otomatis' }
    ]
};
