/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.9',
    build: 84,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Tombol seragam di seluruh app — netral elegan, delete merah, toolbar rapi.',
    changes: [
        { icon: 'fa-palette', text: 'Sistem tombol TMS: primary gelap, outline netral, layout toolbar grid' },
        { icon: 'fa-trash', text: 'Delete / bulk delete / kartu Delete — merah konsisten' },
        { icon: 'fa-table-columns', text: 'Toolbar Customer, Sparepart, Service, Assets — tata letak profesional' },
        { icon: 'fa-window-maximize', text: 'Modal Save/Import — warna seragam, footer rapi' }
    ]
};
