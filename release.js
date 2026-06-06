/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.2',
    build: 77,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Customer unit — kolom Description, tanpa Merk/Tipe, hapus terpilih atau semua.',
    changes: [
        { icon: 'fa-file-lines', text: 'Unit Name diganti Description (form, tabel, template Excel)' },
        { icon: 'fa-ban', text: 'Kolom Merk & Type dihapus dari unit customer' },
        { icon: 'fa-trash', text: 'Hapus Terpilih & Hapus Semua unit per customer' },
        { icon: 'fa-file-import', text: 'Import Excel tetap terima header lama Unit Name' }
    ]
};
