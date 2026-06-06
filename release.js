/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.9',
    build: 97,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix teknisi PJ — Suci dan akun TS lain bisa mengerjakan tiket yang ditugaskan.',
    changes: [
        { icon: 'fa-user-gear', text: 'Service: getDbUser + resolveTicketAssignedTsId — cocokkan PJ by ID/nama/username' },
        { icon: 'fa-database', text: 'sanitizeDatabase perbaiki assignedTsId tiket lama otomatis' },
        { icon: 'fa-truck-pickup', text: 'Login TS sync ID + isAssignedServiceTs diperkuat' }
    ]
};
