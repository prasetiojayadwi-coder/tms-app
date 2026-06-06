/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.3',
    build: 91,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Import Excel 2000+ unit — SN unik per alat, bukan per Art Number saja.',
    changes: [
        { icon: 'fa-file-excel', text: 'Fix import unit: Art Number sama + SN berbeda = unit terpisah (bukan overwrite)' },
        { icon: 'fa-database', text: 'Fix sanitize: tidak lagi hapus ribuan unit duplikat art no' },
        { icon: 'fa-mobile-screen', text: 'Import besar: toast total unit + peringatan jika penyimpanan HP penuh' },
        { icon: 'fa-cloud-arrow-up', text: 'Setelah import ulang Excel, data sync ke cloud untuk tampil di HP' }
    ]
};
