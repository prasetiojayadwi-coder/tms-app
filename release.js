/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.7.0',
    build: 119,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Lokasi perbaikan ditentukan Teknisi PJ saat pickup — bukan saat registrasi.',
    changes: [
        { icon: 'fa-map-location-dot', text: 'Repair Location: teknisi PJ pilih TSF Workshop atau On-Site saat Pickup Unit' },
        { icon: 'fa-file-invoice', text: 'Form Daftar Unit: hapus dropdown lokasi — cukup tentukan PJ' },
        { icon: 'fa-truck-pickup', text: 'Pickup 1-klik tetap berlaku setelah PJ memilih jalur' }
    ]
};
