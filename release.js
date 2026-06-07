/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.5',

    build: 127,

    date: '2026-06-07',

    title: 'System Update Available',

    summary: 'Diagnostik modal: lacak openModal untuk Pilih Jalur Perbaikan (?svcdebug=1).',

    changes: [

        { icon: 'fa-bug', text: 'Log openModal: pastikan popup Pilih Jalur Perbaikan benar tampil (?svcdebug=1)' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

