/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.4',
    build: 113,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix teknisi baru — Konfirmasi On-Site & penugasan PJ otomatis diselaraskan.',
    changes: [
        { icon: 'fa-location-dot', text: 'Fix: tombol Konfirmasi On-Site tidak terblokir handler global' },
        { icon: 'fa-link', text: 'relinkServiceTicketsForUser — PJ tiket otomatis ke ID user baru' },
        { icon: 'fa-user-check', text: 'Heal PJ saat login, daftar personel, approve, & buka Service' },
        { icon: 'fa-id-badge', text: 'Teknisi baru otomatis jabatan Technical Service + ID numerik' },
        { icon: 'fa-eye', text: 'Label PJ jika teknisi bukan penanggung jawab tiket' }
    ]
};
