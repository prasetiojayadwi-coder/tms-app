/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.0',
    build: 75,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Optimasi performa — startup lebih ringan, render lebih cepat.',
    changes: [
        { icon: 'fa-bolt', text: 'Excel & Supabase lazy-load — tidak dimuat saat buka halaman login' },
        { icon: 'fa-bell', text: 'Notifikasi di-debounce — badge cepat, list hanya saat panel dibuka' },
        { icon: 'fa-table', text: 'Render Service Tickets dioptimasi (single-pass HTML)' },
        { icon: 'fa-feather', text: 'Font Awesome async + font weight dikurangi' }
    ]
};
