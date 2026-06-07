/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.8',
    build: 117,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix: teknisi yang buat tiket otomatis jadi PJ & bisa langsung mengerjakan.',
    changes: [
        { icon: 'fa-user-pen', text: 'Daftar Unit oleh teknisi → PJ dipaksa ke diri sendiri (bukan dropdown)' },
        { icon: 'fa-link', text: 'registeredById/User — pembuat tiket selalu boleh mengerjakan' },
        { icon: 'fa-wrench', text: 'Heal tiket lama: PJ diselaraskan ke pembuat teknisi' }
    ]
};
