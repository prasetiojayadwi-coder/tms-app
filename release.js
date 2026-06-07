/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '7.6.0',
    build: 109,
    date: '2026-06-07',
    title: 'System Update Available',
    summary: 'Smart Fill prediktif — autocomplete Art Number & Description di SPH + form Service.',
    changes: [
        { icon: 'fa-wand-magic-sparkles', text: 'SPH lines: prediksi dari Art Number ATAU Description (master sparepart)' },
        { icon: 'fa-hospital', text: 'Daftar Service: autocomplete customer, art no, SN, nama unit' },
        { icon: 'fa-keyboard', text: 'Keyboard: Arrow Up/Down + Enter untuk pilih saran' },
        { icon: 'fa-bolt', text: 'Pilih saran → auto isi harga, art no, description' }
    ]
};
