/**
 * TMS Observability — structured logging, error buffer, production diagnostics.
 */
(function (global) {
    'use strict';

    const TMS_LOG_MAX = 150;
    const TMS_LOG_KEY = 'tms_log_buf';

    function tmsLog(level, message, meta) {
        const entry = {
            t: new Date().toISOString(),
            level: level || 'info',
            message: String(message || ''),
            meta: meta || null
        };
        const fn = level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log';
        console[fn]('[TMS]', entry.message, entry.meta || '');
        try {
            const buf = JSON.parse(sessionStorage.getItem(TMS_LOG_KEY) || '[]');
            buf.push(entry);
            while (buf.length > TMS_LOG_MAX) buf.shift();
            sessionStorage.setItem(TMS_LOG_KEY, JSON.stringify(buf));
        } catch (e) { /* quota */ }
        return entry;
    }

    function tmsGetLogBuffer() {
        try {
            return JSON.parse(sessionStorage.getItem(TMS_LOG_KEY) || '[]');
        } catch (e) {
            return [];
        }
    }

    function tmsReportError(err, context) {
        const msg = err && err.message ? err.message : String(err);
        tmsLog('error', msg, { context: context || 'unknown', stack: err && err.stack });
    }

    function tmsInitObservability() {
        global.addEventListener('error', function (ev) {
            tmsReportError(ev.error || new Error(ev.message), 'window.onerror');
        });
        global.addEventListener('unhandledrejection', function (ev) {
            tmsReportError(ev.reason || new Error('unhandled rejection'), 'unhandledrejection');
        });
        tmsLog('info', 'TMS observability initialized', {
            version: (global.TMS_RELEASE && global.TMS_RELEASE.version) || 'unknown'
        });
    }

    global.tmsLog = tmsLog;
    global.tmsGetLogBuffer = tmsGetLogBuffer;
    global.tmsReportError = tmsReportError;
    global.tmsInitObservability = tmsInitObservability;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tmsInitObservability);
    } else {
        tmsInitObservability();
    }
})(typeof window !== 'undefined' ? window : globalThis);
