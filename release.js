/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.2.0',
    build: 60,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Product categories are now standardized to Avitum, Hospital Care, and Aesculap — legacy AIS/AES data migrates automatically.',
    changes: [
        { icon: 'fa-tags', text: 'Product categories standardized — Avitum, Hospital Care, and Aesculap only' },
        { icon: 'fa-arrows-rotate', text: 'Auto-migration — legacy AIS → Hospital Care and AES → Aesculap on sync and load' },
        { icon: 'fa-filter', text: 'Filters, dashboards, personnel products, and service forms aligned to the new categories' },
        { icon: 'fa-language', text: 'Professional semi-English UI — menus, modals, buttons, and notifications' },
        { icon: 'fa-hospital', text: 'Customer Master — hospitals/clients and linked equipment units in one place' },
        { icon: 'fa-wand-magic-sparkles', text: 'Smart Fill — auto-populate service forms from customer, unit, and service history' },
        { icon: 'fa-bell', text: 'Update notification — changelog summary shown when a new version is available' }
    ]
};
