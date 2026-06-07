/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.2',
    build: 111,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Dropdown unit menampilkan Art Number, Description, dan SN.',
    changes: [
        { icon: 'fa-list', text: 'Saran unit: Art No — Description + baris SN (warna amber)' },
        { icon: 'fa-tag', text: 'Label terpilih: format Art — Description · SN xxx' },
        { icon: 'fa-magnifying-glass', text: 'Smart Fill customer & unit tetap seperti v7.6.1' }
    ]
};
