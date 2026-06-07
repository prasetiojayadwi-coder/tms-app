/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.3',

    build: 125,

    date: '2026-06-07',

    title: 'System Update Available',

    summary: 'Perbaikan tuntas tombol Mulai Pekerjaan — dispatch klik langsung & anti-dobel.',

    changes: [

        { icon: 'fa-play', text: 'Mulai Pekerjaan: tombol panggil aksi langsung (tanpa delegasi rapuh)' },

        { icon: 'fa-hand-pointer', text: 'Hapus capture+stopPropagation yang bisa menelan klik' },

        { icon: 'fa-bolt', text: 'Guard anti-dobel diperpendek 350ms agar klik berulang tetap responsif' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

