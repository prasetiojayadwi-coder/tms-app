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
        RESTORE_DB: ['owner']
    };

    function tmsRequirePerm(permKey, actionLabel) {
        const roles = global.TMS_PERM && global.TMS_PERM[permKey];
        if (!roles) return global.tmsRequireRole ? global.tmsRequireRole(['owner'], actionLabel) : false;
        return global.tmsRequireRole ? global.tmsRequireRole(roles, actionLabel) : false;
    }

    global.tmsRequirePerm = tmsRequirePerm;
})(typeof window !== 'undefined' ? window : globalThis);
