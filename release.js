/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.8',

    build: 130,

    date: '2026-06-07',

    title: 'Perbaikan Tampilan',

    summary: 'FIX: angka QTY/HARGA di baris SPH kini terlihat (padding & spinner number dirapikan).',

    changes: [

        { icon: 'fa-eye', text: 'Angka QTY & HARGA di baris SPH kini terlihat: kolom Qty dilebarkan + rata tengah' },

        { icon: 'fa-sliders', text: 'Input number: padding dikecilkan & panah spinner disembunyikan agar angka tak terpotong' },

        { icon: 'fa-wrench', text: 'Lanjutan: </div> hilang di serviceDeliveryModal yang menelan 5 modal' },

        { icon: 'fa-shield-halved', text: 'Test anti-kambuh keseimbangan tag <div> HTML' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

