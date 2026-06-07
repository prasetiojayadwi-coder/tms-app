/**
 * TMS Runtime — global error handler, session idle timeout, role guard, sync retry.
 */
(function (global) {
    'use strict';

    const TMS_SESSION_IDLE_MS = 30 * 60 * 1000;
    const TMS_SYNC_MAX_RETRIES = 3;
    let _lastActivity = Date.now();
    let _idleTimer = null;

    function tmsGetCurrentUser() {
        return typeof global._tmsGetCurrentUser === 'function' ? global._tmsGetCurrentUser() : null;
    }

    function tmsRequireRole(roles, actionLabel) {
        const u = tmsGetCurrentUser();
        const allowed = Array.isArray(roles) ? roles : [roles];
        if (u && allowed.indexOf(u.role) !== -1) return true;
        const label = actionLabel || 'Aksi ini';
        if (typeof global.showToast === 'function') {
            global.showToast('Akses Ditolak', label + ' memerlukan hak akses ' + allowed.join(' / ') + '.', 'error');
        }
        return false;
    }

    function tmsTouchActivity() {
        _lastActivity = Date.now();
    }

    function tmsResetIdleTimer() {
        if (_idleTimer) clearTimeout(_idleTimer);
        _idleTimer = setTimeout(function () {
            const u = tmsGetCurrentUser();
            if (!u) return;
            if (Date.now() - _lastActivity < TMS_SESSION_IDLE_MS) {
                tmsResetIdleTimer();
                return;
            }
            const doLogout = global.handleLogout || global.logout;
            if (typeof doLogout === 'function') {
                if (typeof global.showToast === 'function') {
                    global.showToast('Sesi Berakhir', 'Login ulang setelah tidak aktif 30 menit.', 'warning');
                }
                if (typeof global.tmsLog === 'function') {
                    global.tmsLog('warn', 'Session idle timeout — auto logout');
                }
                doLogout();
            }
        }, TMS_SESSION_IDLE_MS + 500);
    }

    function tmsInitRuntime() {
        ['click', 'keydown', 'touchstart', 'scroll'].forEach(function (ev) {
            document.addEventListener(ev, tmsTouchActivity, { passive: true, capture: true });
        });
        tmsResetIdleTimer();

        if (typeof global.tmsReportError !== 'function') {
            global.addEventListener('error', function (ev) {
                console.error('[TMS] Uncaught error:', ev.message, ev.filename, ev.lineno);
            });
            global.addEventListener('unhandledrejection', function (ev) {
                console.error('[TMS] Unhandled rejection:', ev.reason);
            });
        }
    }

    function tmsIsRetryableError(err) {
        if (!err) return false;
        const code = err.code || err.status || '';
        if (code === 'PGRST116' || code === 401 || code === 403 || code === '42501') return false;
        const msg = String(err.message || err).toLowerCase();
        return msg.includes('network') || msg.includes('fetch') || msg.includes('timeout')
            || msg.includes('failed') || msg.includes('econn') || code === 500 || code === 502 || code === 503;
    }

    async function tmsRetryAsync(fn, opts) {
        const max = (opts && opts.max) || TMS_SYNC_MAX_RETRIES;
        const baseDelay = (opts && opts.baseDelay) || 400;
        let lastErr;
        for (let attempt = 0; attempt < max; attempt++) {
            try {
                return await fn(attempt);
            } catch (err) {
                lastErr = err;
                if (!tmsIsRetryableError(err) || attempt >= max - 1) throw err;
                await new Promise(function (r) {
                    setTimeout(r, baseDelay * Math.pow(2, attempt));
                });
            }
        }
        throw lastErr;
    }

    global.TMS_SESSION_IDLE_MS = TMS_SESSION_IDLE_MS;
    global.tmsRequireRole = tmsRequireRole;
    global.tmsIsRetryableError = tmsIsRetryableError;
    global.tmsRetryAsync = tmsRetryAsync;
    global.tmsInitRuntime = tmsInitRuntime;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tmsInitRuntime);
    } else {
        tmsInitRuntime();
    }
})(typeof window !== 'undefined' ? window : globalThis);
