/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.4',
    build: 92,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Form Register Service — hapus Brand & Type, cukup Description + Art No + SN.',
    changes: [
        { icon: 'fa-file-invoice', text: 'Register Customer Unit Service: field Brand & Type dihapus' },
        { icon: 'fa-list', text: 'Daftar service, detail, PDF & WA pakai Description · Art · SN' },
        { icon: 'fa-file-excel', text: 'Export Excel service: kolom Merk/Model dihapus' }
    ]
};
