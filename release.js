/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.9',

    build: 131,

    date: '2026-06-07',

    title: 'Perbaikan Penting',

    summary: 'FIX: tombol Issue On-Site SPH kini bisa diklik (field required tersembunyi yang memblok submit).',

    changes: [

        { icon: 'fa-paper-plane', text: 'Issue On-Site SPH / Submit Quotation: tombol kini berfungsi (hapus required pada field tersembunyi)' },

        { icon: 'fa-eye', text: 'Angka QTY & HARGA baris SPH terlihat: kolom Qty dilebarkan + rata tengah, spinner disembunyikan' },

        { icon: 'fa-wrench', text: 'Lanjutan: </div> hilang di serviceDeliveryModal yang menelan 5 modal' },

        { icon: 'fa-shield-halved', text: 'Test anti-kambuh: keseimbangan <div> & required field tersembunyi' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

