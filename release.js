/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.0.2',
    build: 90,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Audit render semua menu — cegah daftar kosong di HP.',
    changes: [
        { icon: 'fa-shield-halved', text: 'Helper tmsRenderSplitList — kartu HP & tabel desktop aman di semua menu' },
        { icon: 'fa-bug', text: 'Fix Service & Repair HP: kartu tiket selalu render (sama seperti bug Customer)' },
        { icon: 'fa-cloud-arrow-down', text: 'Buka menu kosong otomatis sync cloud (customer, sparepart, service, SPH, tools)' },
        { icon: 'fa-list', text: 'Empty state konsisten di Customer, Units, Sparepart, Service, SPH Log' }
    ]
};
