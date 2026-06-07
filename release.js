/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.5.0',
    build: 102,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Iterative audit 3 siklus — TMS_PERM matrix, integrity check, XSS inventori, render batch.',
    changes: [
        { icon: 'fa-shield-halved', text: 'js/tms-auth.js + js/tms-integrity.js — permission matrix & DB check' },
        { icon: 'fa-lock', text: 'Guard customer/sparepart/personel + password edit tidak tampilkan hash' },
        { icon: 'fa-bolt', text: 'Render SPV assets batch join + sync retry pintar (non-retryable skip)' },
        { icon: 'fa-comment-slash', text: 'XSS inventori & approval pakai tmsEscToolFields di seluruh tabel' }
    ]
};
