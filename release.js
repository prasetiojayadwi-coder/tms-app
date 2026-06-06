/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.9.2',
    build: 87,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Perbaikan daftar customer tidak muncul di HP.',
    changes: [
        { icon: 'fa-mobile-screen', text: 'Customer Master HP: selalu buka tab Customers saat masuk menu' },
        { icon: 'fa-list', text: 'Kartu customer & unit — area scroll tinggi cukup di layar kecil' },
        { icon: 'fa-circle-info', text: 'Tab Units: petunjuk jelas pilih customer di tab Customers dulu' }
    ]
};
