/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.5.6',
    build: 108,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Fix kritis — konfirmasi on-site tidak hilang setelah klik (loadDB revert).',
    changes: [
        { icon: 'fa-bug', text: 'Bug fix: renderServiceTickets tidak timpa status setelah konfirmasi' },
        { icon: 'fa-bolt', text: 'Tombol On-Site: handler langsung tmsOnsitePickup(id)' },
        { icon: 'fa-cloud', text: 'Merge cloud: status tiket maju tidak di-rollback' },
        { icon: 'fa-user-check', text: 'Auto-align PJ jika nama Suci cocok di tiket' }
    ]
};
