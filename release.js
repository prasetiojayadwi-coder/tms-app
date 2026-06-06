/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.2.0',
    build: 99,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Audit fix — keamanan password, XSS chat, sync stabil, CI QA gate.',
    changes: [
        { icon: 'fa-shield-halved', text: 'Password PBKDF2 — hash saat login/simpan, session tanpa password' },
        { icon: 'fa-lock', text: 'Production cloud: nonaktifkan akun default admin/teknisi' },
        { icon: 'fa-comment-slash', text: 'XSS: escape chat & history log; storage listener tunggal' },
        { icon: 'fa-user-gear', text: 'PJ tiket: match strict username/ID (bukan nama mirip)' }
    ]
};
