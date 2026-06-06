/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.9.0',
    build: 85,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Toolbar Tools/Backup rapi + Sparepart Master hapus massal dengan checkbox.',
    changes: [
        { icon: 'fa-wrench', text: 'Special Tools & Unit Backup: judul, toolbar seragam, Pilih Semua' },
        { icon: 'fa-check-square', text: 'Sparepart Master: centang per item + Pilih Semua (HP & desktop)' },
        { icon: 'fa-trash', text: 'Tombol Delete merah — hapus banyak sparepart sekaligus' },
        { icon: 'fa-grip', text: 'Ikon aksi tabel Tools/Backup — tms-icon-btn konsisten' }
    ]
};
