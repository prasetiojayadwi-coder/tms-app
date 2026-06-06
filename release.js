/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.0',
    build: 88,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Review UI/UX menyeluruh — tampilan profesional, user-friendly di HP & desktop.',
    changes: [
        { icon: 'fa-mobile-screen', text: 'Service & Repair HP: kartu tiket + tombol alur mudah di-tap' },
        { icon: 'fa-palette', text: 'Tombol & ikon seragam — tms-icon-btn, tms-svc-btn, heading netral' },
        { icon: 'fa-list', text: 'Empty state jelas di Tools, Backup, Customer, Service' },
        { icon: 'fa-language', text: 'Placeholder & label konsisten (Bahasa Indonesia)' },
        { icon: 'fa-arrows-rotate', text: 'Tab Customer Master stabil saat rotate layar HP' }
    ]
};
