/**
 * TMS Security module — XSS escape, password hashing, cloud upload sanitization.
 */
(function (global) {
    'use strict';

    const TMS_PBKDF2_ITERS = 100000;

    function tmsEscHtml(s) {
        if (s == null || s === '') return '';
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function tmsEscAttr(s) {
        return tmsEscHtml(s).replace(/`/g, '&#96;');
    }

    function isPasswordHashed(stored) {
        return typeof stored === 'string' && stored.startsWith('pbkdf2:');
    }

    function b64FromBytes(bytes) {
        let s = '';
        bytes.forEach(function (b) { s += String.fromCharCode(b); });
        return btoa(s);
    }

    function bytesFromB64(b64) {
        const bin = atob(b64);
        const out = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
        return out;
    }

    async function hashPassword(plain) {
        const p = String(plain || '');
        if (!p) return '';
        if (!global.crypto || !crypto.subtle) return p;
        const enc = new TextEncoder();
        const salt = crypto.getRandomValues(new Uint8Array(16));
        const key = await crypto.subtle.importKey('raw', enc.encode(p), 'PBKDF2', false, ['deriveBits']);
        const bits = await crypto.subtle.deriveBits(
            { name: 'PBKDF2', salt: salt, iterations: TMS_PBKDF2_ITERS, hash: 'SHA-256' },
            key,
            256
        );
        return 'pbkdf2:' + TMS_PBKDF2_ITERS + ':' + b64FromBytes(salt) + ':' + b64FromBytes(new Uint8Array(bits));
    }

    async function verifyPassword(plain, stored) {
        const p = String(plain || '').trim();
        const s = String(stored || '').trim();
        if (!p || !s) return false;
        if (!isPasswordHashed(s)) return p === s;
        if (!global.crypto || !crypto.subtle) return false;
        const parts = s.split(':');
        if (parts.length !== 4 || parts[0] !== 'pbkdf2') return false;
        const iterations = parseInt(parts[1], 10) || TMS_PBKDF2_ITERS;
        const salt = bytesFromB64(parts[2]);
        const expected = parts[3];
        const enc = new TextEncoder();
        const key = await crypto.subtle.importKey('raw', enc.encode(p), 'PBKDF2', false, ['deriveBits']);
        const bits = await crypto.subtle.deriveBits(
            { name: 'PBKDF2', salt: salt, iterations: iterations, hash: 'SHA-256' },
            key,
            256
        );
        return b64FromBytes(new Uint8Array(bits)) === expected;
    }

    function isCloudProductionMode() {
        const cfg = global.TMS_CONFIG || {};
        const sb = cfg.supabase || {};
        const url = sb.url || global.SUPABASE_URL || '';
        const key = sb.anonKey || global.SUPABASE_KEY || '';
        return !!(url && key && typeof location !== 'undefined' && location.protocol !== 'file:');
    }

    function getTmsSyncSecret() {
        const cfg = global.TMS_CONFIG || {};
        return String(cfg.syncSecret || cfg.supabase?.syncSecret || '').trim();
    }

    function tmsEscToolFields(t) {
        if (!t) return { noInv: '-', artNo: '-', desc: '-', merk: '-', sn: '-', tipe: '-' };
        return {
            noInv: tmsEscHtml(t.noInv || '-'),
            artNo: tmsEscHtml(t.artNo || '-'),
            desc: tmsEscHtml(t.desc || '-'),
            merk: tmsEscHtml(t.merk || '-'),
            sn: tmsEscHtml(t.sn || '-'),
            tipe: tmsEscHtml(t.tipe || '-')
        };
    }

    function cloneDbForCloudUpload(db) {
        const uploadDb = JSON.parse(JSON.stringify(db || {}));
        if (uploadDb.users) {
            Object.keys(uploadDb.users).forEach(function (k) {
                const u = uploadDb.users[k];
                if (u && typeof u === 'object') delete u.pass;
            });
        }
        return uploadDb;
    }

    var TMS_SAFE_DATA_URL_RE = /^data:(image\/(?:png|jpeg|jpg|gif|webp|svg\+xml)|application\/pdf);base64,[A-Za-z0-9+/=]+$/;

    function tmsSafeDataUrl(url) {
        if (!url || typeof url !== 'string') return '';
        var trimmed = url.trim();
        if (trimmed.length > 6 * 1024 * 1024) return '';
        return TMS_SAFE_DATA_URL_RE.test(trimmed) ? trimmed : '';
    }

    function sanitizeDbForRestore(db) {
        var restored = JSON.parse(JSON.stringify(db || {}));
        if (restored.users && typeof restored.users === 'object') {
            Object.keys(restored.users).forEach(function (k) {
                var u = restored.users[k];
                if (!u || typeof u !== 'object') return;
                if (u.pass && !isPasswordHashed(u.pass)) delete u.pass;
            });
        }
        return restored;
    }

    global.TMS_PBKDF2_ITERS = TMS_PBKDF2_ITERS;
    global.tmsEscHtml = tmsEscHtml;
    global.tmsEscAttr = tmsEscAttr;
    global.isPasswordHashed = isPasswordHashed;
    global.b64FromBytes = b64FromBytes;
    global.bytesFromB64 = bytesFromB64;
    global.hashPassword = hashPassword;
    global.verifyPassword = verifyPassword;
    global.isCloudProductionMode = isCloudProductionMode;
    global.getTmsSyncSecret = getTmsSyncSecret;
    global.cloneDbForCloudUpload = cloneDbForCloudUpload;
    global.tmsEscToolFields = tmsEscToolFields;
    global.tmsSafeDataUrl = tmsSafeDataUrl;
    global.sanitizeDbForRestore = sanitizeDbForRestore;
})(typeof window !== 'undefined' ? window : globalThis);
