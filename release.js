/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.9',
    build: 74,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Service & Repair toolbar dirapikan + import batch unit customer.',
    changes: [
        { icon: 'fa-screwdriver-wrench', text: 'Toolbar Service & Repair dirapikan — tombol konsisten & terkelompok' },
        { icon: 'fa-file-import', text: 'Import Unit Excel + Template di halaman Service & Repair' },
        { icon: 'fa-user-shield', text: 'Batch import role matrix — Owner/SPV/Specialist penuh, TSF tools & backup' },
        { icon: 'fa-file-excel', text: 'Upload .xlsx — satu kolom per field' }
    ]
};
