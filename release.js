/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.6',
    build: 71,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Template & export Excel (.xlsx) — satu kolom per field, tanpa CSV.',
    changes: [
        { icon: 'fa-file-excel', text: 'Download template .xlsx — Art Number, Description, Price, Group, Status, Notes di kolom terpisah' },
        { icon: 'fa-file-import', text: 'Import hanya Excel (.xlsx) — buka langsung di Excel, isi per kolom' },
        { icon: 'fa-file-export', text: 'Export sparepart, tools, service, log — format Excel bukan CSV' },
        { icon: 'fa-folder-open', text: 'Folder templates/ — 5 file .xlsx referensi' }
    ]
};
