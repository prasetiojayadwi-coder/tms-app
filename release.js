/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.7',
    build: 72,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Batch import Excel (.xlsx) — Owner only, satu kolom per field.',
    changes: [
        { icon: 'fa-user-shield', text: 'Batch import/update hanya akun Owner — sparepart, customer, tools, backup' },
        { icon: 'fa-file-excel', text: 'Upload wajib .xlsx — satu kolom per field di Excel' },
        { icon: 'fa-file-import', text: 'Template Excel untuk 5 modul batch import' },
        { icon: 'fa-eye-slash', text: 'Tombol Import/Template disembunyikan untuk non-Owner' }
    ]
};
