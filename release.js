/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.1',

    build: 123,

    date: '2026-06-07',

    title: 'System Update Available',

    summary: 'Fix tombol Mulai Pekerjaan + hardening keamanan XSS, data URL, idle session.',

    changes: [

        { icon: 'fa-play', text: 'Fix: tombol Mulai Pekerjaan — onclick langsung + event binding awal' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

