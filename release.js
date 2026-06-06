/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.7',
    build: 95,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Audit tombol — kartu HP selalu render, area sentuh 48px di semua menu.',
    changes: [
        { icon: 'fa-hand-pointer', text: 'Global: tmsCardsVisible — kartu HP tidak kosong saat zoom/font besar' },
        { icon: 'fa-mobile-screen', text: 'Customer, Units, Sparepart, Service — tombol kartu min 48px + type=button' },
        { icon: 'fa-shield-halved', text: 'QA: audit onclick dinamis + tms-card-btn wajib punya handler' }
    ]
};
