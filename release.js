/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.1.0',
    build: 59,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Customer Service workflows, professional UI labels, and performance improvements are included in this release.',
    changes: [
        { icon: 'fa-language', text: 'Professional semi-English UI — menus, modals, buttons, and notifications standardized' },
        { icon: 'fa-hospital', text: 'Customer Master — manage hospitals/clients and linked equipment units in one place' },
        { icon: 'fa-wand-magic-sparkles', text: 'Smart Fill — auto-populate service forms from Customer, Unit, SN, Art No., and service history' },
        { icon: 'fa-clock-rotate-left', text: 'Damage / Service History panel with "Use Last Complaint" for faster ticket registration' },
        { icon: 'fa-shield-halved', text: 'Duplicate protection for customers, units, personnel, and active service tickets' },
        { icon: 'fa-bolt', text: 'Performance — debounced search, cached service history index, optimized renders' },
        { icon: 'fa-cloud', text: 'Cloud sync ready — Supabase realtime multi-user with setup scripts (Pasang_Cloud.bat)' },
        { icon: 'fa-bell', text: 'Update notification — you are now informed when a new version is available with a change summary' }
    ]
};
