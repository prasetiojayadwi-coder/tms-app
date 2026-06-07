/**

 * TMS Release manifest — bump version & changelog on every deploy.

 * Service Worker cache version (sw.js) should match `build`.

 */

window.TMS_RELEASE = {

    version: '7.10.7',

    build: 129,

    date: '2026-06-07',

    title: 'Perbaikan Penting',

    summary: 'FIX: tag </div> hilang yang menyembunyikan 5 modal (Mulai Pekerjaan, TTD, Detail, Alihkan PJ, BAST).',

    changes: [

        { icon: 'fa-wrench', text: 'FIX utama: </div> hilang di serviceDeliveryModal yang menelan 5 modal jadi tersembunyi' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: popup Pilih Jalur Perbaikan kini tampil normal' },

        { icon: 'fa-signature', text: 'TTD serah terima, Detail tiket, Alihkan PJ, BAST gabungan: kembali muncul' },

        { icon: 'fa-shield-halved', text: 'Tambah test anti-kambuh keseimbangan tag <div> HTML' },

        { icon: 'fa-play', text: 'Mulai Pekerjaan: dispatch klik langsung & anti-dobel (lanjutan)' },

        { icon: 'fa-shield-halved', text: 'XSS: timeline service, SPH detail, riwayat unit — semua teks di-escape' },

        { icon: 'fa-image', text: 'Tanda tangan & lampiran: hanya data:image/pdf yang valid' },

        { icon: 'fa-clock', text: 'Auto logout setelah 4 jam tidak aktif' },

        { icon: 'fa-database', text: 'Impor backup: password plain-text dihapus otomatis' },

        { icon: 'fa-people-arrows', text: 'PJ reassignment tetap — guard permission matrix diperkuat' }

    ]

};

