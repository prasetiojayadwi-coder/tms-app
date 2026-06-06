/**
 * TMS Cloud Configuration — TEMPLATE
 *
 * Cara setup:
 * 1. Salin file ini menjadi "config.js" di folder yang sama
 * 2. Isi URL dan Anon Key dari dashboard Supabase Anda
 * 3. Set syncSecret sama dengan write_secret di tabel tms_sync (production)
 * 4. Jangan commit config.js ke repository publik
 */
window.TMS_CONFIG = {
    supabase: {
        url: 'https://YOUR-PROJECT.supabase.co',
        anonKey: 'YOUR_SUPABASE_ANON_KEY'
    },
    syncSecret: ''
};
