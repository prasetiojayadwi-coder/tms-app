/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.10',

    build: 132,

    date: '2026-06-07',

    title: 'Info Versi Aplikasi',

    summary: 'Versi aplikasi kini tampil permanen di sidebar — klik untuk lihat catatan pembaruan.',

    changes: [

        { icon: 'fa-rocket', text: 'Label versi + build tampil permanen di bawah tombol Log Out (klik = lihat changelog)' },

        { icon: 'fa-bell', text: 'Banner pembaruan otomatis muncul saat ada versi baru agar user tahu' },

        { icon: 'fa-paper-plane', text: 'Issue On-Site SPH / Submit Quotation: tombol berfungsi (lanjutan)' },

        { icon: 'fa-eye', text: 'Angka QTY & HARGA baris SPH terlihat jelas (lanjutan)' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

