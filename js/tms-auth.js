/**
 * TMS Authorization — centralized permission matrix.
 */
(function (global) {
    'use strict';

    global.TMS_PERM = {
        MANAGE_PERSONNEL: ['owner', 'spv', 'tsf'],
        DELETE_PERSONNEL: ['owner', 'spv'],
        LOCK_PERSONNEL: ['owner', 'spv'],
        DELETE_ASSET: ['owner', 'tsf'],
        BULK_DELETE_ASSET: ['owner'],
        DELETE_SERVICE: ['owner'],
        MANAGE_CUSTOMER: ['owner', 'spv'],
        DELETE_SPAREPART: ['owner', 'spv', 'ts_spec', 'ts_spec_avitum', 'ts_spec_ais'],
        EXPORT_DB: ['owner', 'spv', 'tsf'],
        RESTORE_DB: ['owner'],
        REASSIGN_SERVICE_PJ: ['owner', 'spv', 'ts_spec', 'ts_spec_avitum', 'ts_spec_ais']
    };

    var TMS_SESSION_IDLE_MS = 4 * 60 * 60 * 1000;
    var _tmsIdleTimer = null;
    var _tmsIdleBound = false;

    function tmsTouchSessionActivity() {
        if (typeof global.sessionStorage !== 'undefined') {
            try { global.sessionStorage.setItem('tms_last_activity', String(Date.now())); } catch (e) {}
        }
        if (_tmsIdleTimer) clearTimeout(_tmsIdleTimer);
        _tmsIdleTimer = setTimeout(tmsSessionIdleExpired, TMS_SESSION_IDLE_MS);
    }

    function tmsSessionIdleExpired() {
        if (typeof global.tmsLog === 'function') global.tmsLog('info', 'Session idle timeout — logging out');
        if (typeof global.handleLogout === 'function') {
            global.handleLogout();
            if (typeof global.showToast === 'function') {
                global.showToast('Sesi Berakhir', 'Anda keluar otomatis karena tidak aktif.', 'warning');
            }
        }
    }

    function tmsInitSessionIdleWatch() {
        if (_tmsIdleBound) return;
        _tmsIdleBound = true;
        var events = ['click', 'keydown', 'touchstart', 'scroll'];
        events.forEach(function (ev) {
            global.addEventListener(ev, tmsTouchSessionActivity, { passive: true });
        });
        tmsTouchSessionActivity();
    }

    function tmsRequirePerm(permKey, actionLabel) {
        const roles = global.TMS_PERM && global.TMS_PERM[permKey];
        if (!roles) return global.tmsRequireRole ? global.tmsRequireRole(['owner'], actionLabel) : false;
        return global.tmsRequireRole ? global.tmsRequireRole(roles, actionLabel) : false;
    }

    global.tmsRequirePerm = tmsRequirePerm;
    global.TMS_SESSION_IDLE_MS = TMS_SESSION_IDLE_MS;
    global.tmsInitSessionIdleWatch = tmsInitSessionIdleWatch;
    global.tmsTouchSessionActivity = tmsTouchSessionActivity;
})(typeof window !== 'undefined' ? window : globalThis);
