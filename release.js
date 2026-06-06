/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.3',
    build: 78,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Customer Master — satu tombol Delete untuk customer & unit terpilih.',
    changes: [
        { icon: 'fa-trash', text: 'Unit: satu tombol Delete (centang lalu hapus)' },
        { icon: 'fa-hospital', text: 'Customer: centang + tombol Delete (hapus beserta unit)' },
        { icon: 'fa-check-double', text: 'Hapus ganda (Terpilih/Semua) dihilangkan' }
    ]
};
