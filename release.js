/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.8',
    build: 73,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Batch import Excel — role matrix: Owner/SPV/Specialist penuh, TSF tools & backup saja.',
    changes: [
        { icon: 'fa-user-shield', text: 'Owner, Supervisor & Technical Specialist — batch import semua modul' },
        { icon: 'fa-warehouse', text: 'TSF — batch import hanya Special Tools & Unit Backup' },
        { icon: 'fa-file-excel', text: 'Upload wajib .xlsx — satu kolom per field di Excel' },
        { icon: 'fa-eye-slash', text: 'Tombol import per modul disesuaikan per role' }
    ]
};
