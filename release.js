/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.2',

    build: 124,

    date: '2026-06-07',

    title: 'System Update Available',

    summary: 'Hardening notifikasi XSS + guard PJ modal + anti-truncation QA gate.',

    changes: [

        { icon: 'fa-bell', text: 'Notifikasi dashboard: escape semua field user-generated' },

        { icon: 'fa-shield', text: 'Guard permission REASSIGN_SERVICE_PJ di openReassignPjModal' },

        { icon: 'fa-vial', text: 'QA gate: deteksi index.html terpotong (regression Mulai Pekerjaan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

