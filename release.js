/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.1',
    build: 76,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Import unit customer — auto buat/update customer, tanpa duplikat.',
    changes: [
        { icon: 'fa-hospital', text: 'Import unit: customer otomatis dari Customer Name (Code boleh kosong)' },
        { icon: 'fa-arrows-rotate', text: 'Unit duplikat (Art No/SN) di-update, bukan ditambah ganda' },
        { icon: 'fa-tags', text: 'Product AVITUM/Hospital Care — normalisasi huruf besar-kecil' },
        { icon: 'fa-database', text: 'Simpan DB saat update unit atau customer baru dari import' }
    ]
};
