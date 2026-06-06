/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.4.0',
    build: 101,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Ultra audit hardening — auth guards, observability, backup aman, idle logout fix.',
    changes: [
        { icon: 'fa-shield-halved', text: 'Role guard: hapus aset, sparepart, customer, impor DB (owner only)' },
        { icon: 'fa-clock', text: 'Fix sesi idle — auto logout via handleLogout + structured logging' },
        { icon: 'fa-database', text: 'Backup/restore: ekspor tanpa password, impor dibatasi owner' },
        { icon: 'fa-chart-line', text: 'js/tms-observability.js — error buffer + sync retry fetch' }
    ]
};
