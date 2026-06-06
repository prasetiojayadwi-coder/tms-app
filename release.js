/**
 * TMS Release manifest — bump version & changelog on every deploy.
 * Service Worker cache version (sw.js) should match `build`.
 */
window.TMS_RELEASE = {
    version: '6.7.2',
    build: 67,
    date: '2026-06-06',
    title: 'System Update Available',
    summary: 'Login footer now shows the live app version from TMS_RELEASE.',
    changes: [
        { icon: 'fa-tag', text: 'Login footer version sync — displays current release (V6.7.2) from release.js' },
        { icon: 'fa-ban', text: 'Cancel SPH — reset toolStatus, role guard, and service notifications on revert' },
        { icon: 'fa-file-pdf', text: 'Export SPH to PDF — corporate layout for single and combined quotations' },
        { icon: 'fa-magnifying-glass', text: 'Partial Smart Fill — autocomplete Art Number with keyboard navigation' },
        { icon: 'fa-building', text: 'Combined SPH customer picker when multiple customers are eligible' },
        { icon: 'fa-location-dot', text: 'On-Site quotation modal — no Un-Repair option, path-specific labels' }
    ]
};
