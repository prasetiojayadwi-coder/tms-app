/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.5',
    build: 70,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'CSV template Excel Indonesia — satu kolom per field (delimiter titik koma).',
    changes: [
        { icon: 'fa-file-csv', text: 'Template import/export CSV pakai delimiter ; — satu kolom per field di Excel Indonesia' },
        { icon: 'fa-file-import', text: 'Import CSV auto-detect ; atau , — berlaku sparepart, customer, tools, backup' },
        { icon: 'fa-folder-open', text: 'Folder templates/ — 5 file CSV referensi siap unduh' },
        { icon: 'fa-gauge-high', text: 'Render sparepart & SPH log dioptimasi — batch DOM write' },
        { icon: 'fa-clipboard-check', text: 'UAT-004 verifikasi template semicolon + parse CSV' }
    ]
};
