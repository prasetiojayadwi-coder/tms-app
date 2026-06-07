/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.7',
    build: 116,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Teknisi lapangan baru langsung aktif — SPV tidak perlu tunggu approval Direktur.',
    changes: [
        { icon: 'fa-user-check', text: 'Add Personnel role TS → status active langsung (bisa login)' },
        { icon: 'fa-bolt', text: 'SPV onboard Razif/Reza → langsung PJ & kerjakan tiket' },
        { icon: 'fa-shield', text: 'SPV/Owner/TSF/Specialist tetap butuh approval Direktur' }
    ]
};
