/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.5.4',
    build: 106,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix Konfirmasi On-Site — teknisi PJ bisa langsung kerjakan tiket tanpa TTD PIC dulu.',
    changes: [
        { icon: 'fa-location-dot', text: 'On-Site: satu langkah — teknisi PJ tanda tangan & mulai kerja' },
        { icon: 'fa-user-check', text: 'PJ ketat: hanya username/ID teknisi yang ditunjuk SPV' },
        { icon: 'fa-hand-pointer', text: 'Tombol Pickup/On-Site: onclick langsung + sync user dari DB' },
        { icon: 'fa-signature', text: 'Modal TTD on-site: tidak wajib PIC customer di langkah pertama' }
    ]
};
