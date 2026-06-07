/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.11',

    build: 133,

    date: '2026-06-07',

    title: 'Notifikasi SPH Log',

    summary: 'Menu SPH Log kini punya lonceng notifikasi saat ada SPH baru, hilang otomatis saat dibuka.',

    changes: [

        { icon: 'fa-bell', text: 'SPH Log: lonceng notifikasi muncul saat ada SPH terbaru, hilang setelah menu dibuka' },

        { icon: 'fa-rocket', text: 'Label versi + build permanen di sidebar (klik = lihat changelog)' },

        { icon: 'fa-paper-plane', text: 'Issue On-Site SPH: tombol berfungsi (lanjutan)' },

        { icon: 'fa-eye', text: 'Angka QTY & HARGA baris SPH terlihat jelas (lanjutan)' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

