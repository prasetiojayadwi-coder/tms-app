/**
 * TMS Integrity — lightweight DB consistency checks.
 */
(function (global) {
    'use strict';

    function normKey(v) {
        return String(v || '').trim().toLowerCase();
    }

    function getDbUserById(db, id) {
        if (id == null || id === '' || id === 0) return null;
        var users = db.users || {};
        var n = Number(id);
        if (!isNaN(n) && users[n]) return users[n];
        var sk = String(id);
        if (users[sk]) return users[sk];
        return Object.values(users).find(function (u) { return u && Number(u.id) === n; }) || null;
    }

    function runDbIntegrityCheck(db) {
        const issues = [];
        if (!db || typeof db !== 'object') {
            issues.push({ level: 'critical', code: 'DB_NULL', message: 'Database object missing' });
            return issues;
        }
        if (!db.users || typeof db.users !== 'object') {
            issues.push({ level: 'high', code: 'USERS_MISSING', message: 'db.users is missing or invalid' });
        }
        const users = Object.values(db.users || {});
        const seenUser = new Map();
        const seenNik = new Map();
        users.forEach(function (u) {
            if (!u) return;
            const uk = normKey(u.user);
            if (uk) {
                if (seenUser.has(uk)) issues.push({ level: 'medium', code: 'DUP_USER', message: 'Duplicate username: ' + uk });
                else seenUser.set(uk, u.id);
            }
            const nk = normKey(u.nik);
            if (nk) {
                if (seenNik.has(nk)) issues.push({ level: 'medium', code: 'DUP_NIK', message: 'Duplicate NIK: ' + nk });
                else seenNik.set(nk, u.id);
            }
        });
        (db.tools || []).forEach(function (t) {
            if (t.ownerId > 0 && !db.users[t.ownerId]) {
                issues.push({ level: 'low', code: 'ORPHAN_TOOL_OWNER', message: 'Tool ' + (t.noInv || t.id) + ' has orphan ownerId ' + t.ownerId });
            }
        });
        (db.demoUnits || []).forEach(function (t) {
            if (t.ownerId > 0 && !db.users[t.ownerId]) {
                issues.push({ level: 'low', code: 'ORPHAN_DEMO_OWNER', message: 'Demo ' + (t.noInv || t.id) + ' has orphan ownerId ' + t.ownerId });
            }
        });
        (db.serviceTickets || []).forEach(function (s) {
            if (!s) return;
            var pjId = s.assignedTsId;
            if (pjId != null && pjId !== '' && Number(pjId) > 0 && !getDbUserById(db, pjId)) {
                issues.push({ level: 'medium', code: 'ORPHAN_SERVICE_PJ', message: 'Service ticket ' + (s.noService || s.id) + ' has orphan assignedTsId ' + pjId });
            }
        });
        if (typeof db.version !== 'number' && typeof db.version !== 'string') {
            issues.push({ level: 'low', code: 'VERSION_MISSING', message: 'db.version not set' });
        }
        return issues;
    }

    function tmsRunIntegrityAndLog(db) {
        const issues = runDbIntegrityCheck(db);
        if (!issues.length) {
            if (typeof global.tmsLog === 'function') global.tmsLog('info', 'DB integrity check passed');
            return issues;
        }
        issues.forEach(function (i) {
            if (typeof global.tmsLog === 'function') global.tmsLog(i.level === 'critical' || i.level === 'high' ? 'warn' : 'info', 'Integrity: ' + i.message, i);
        });
        return issues;
    }

    global.runDbIntegrityCheck = runDbIntegrityCheck;
    global.tmsRunIntegrityAndLog = tmsRunIntegrityAndLog;
})(typeof window !== 'undefined' ? window : globalThis);
