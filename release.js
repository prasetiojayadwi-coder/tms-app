/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.8.8',
    build: 83,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'HP lebih ringan saat buka + sync realtime lebih cepat antar device.',
    changes: [
        { icon: 'fa-feather', text: 'Mode ringan HP: tanpa chart berat, font defer, view tersembunyi di-skip render' },
        { icon: 'fa-cloud-arrow-down', text: 'Realtime: poll 10s + heartbeat 12s di HP, reconnect otomatis' },
        { icon: 'fa-bolt', text: 'Update lite dari cloud — refresh tab aktif & badge tanpa popup berat' },
        { icon: 'fa-wifi', text: 'Sync saat online kembali + antar tab browser (storage event)' }
    ]
};
