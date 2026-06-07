/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.10.0',
    build: 122,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Alihkan PJ tiket service — Owner/SPV/Spec dengan audit trail & tanpa reset alur TSF.',
    changes: [
        { icon: 'fa-people-arrows', text: 'Ganti PJ: Owner, SPV, Technical Specialist (tiket belum selesai)' },
        { icon: 'fa-clipboard-list', text: 'Alasan wajib + riwayat audit saat tiket sudah berjalan' },
        { icon: 'fa-route', text: 'Tiket Terdaftar: PJ baru pilih ulang jalur Lapangan/TSF' },
        { icon: 'fa-shield', text: 'Status/SPH/PO/TSF tidak di-reset — hanya penanggung jawab lapangan berganti' }
    ]
};
