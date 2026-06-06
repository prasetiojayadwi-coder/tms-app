/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.3.0',
    build: 100,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Audit 8+ — modul keamanan, CSP, sync secret, 60+ tes otomatis, skor QA gate.',
    changes: [
        { icon: 'fa-shield-halved', text: 'Modul js/tms-security.js — PBKDF2, XSS escape, upload tanpa password' },
        { icon: 'fa-clock', text: 'Sesi idle 30 menit + role guard + CSP + sync write secret' },
        { icon: 'fa-rotate', text: 'Sync retry + cloneDbForCloudUpload + trigger Supabase auth' },
        { icon: 'fa-vial', text: 'audit_score.py + 60 pytest — CI gate skor >= 8/10' }
    ]
};
