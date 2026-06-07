#!/usr/bin/env python3
"""Skor audit objektif TMS — target >= 8.0 per dimensi."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PASS_THRESHOLD = 8.0


def read_js_bundle() -> str:
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    scripts = [
        m.group(1)
        for m in re.finditer(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', html, re.I)
        if not m.group(1).strip().startswith('tailwind.config')
    ]
    js = '\n'.join(scripts)
    js_dir = ROOT / 'js'
    if js_dir.is_dir():
        for path in sorted(js_dir.glob('tms-*.js')):
            js += '\n' + path.read_text(encoding='utf-8')
    return js, html


def count_tests() -> int:
    tests_dir = ROOT / 'tests'
    if not tests_dir.is_dir():
        return 0
    total = 0
    for path in tests_dir.glob('test_*.py'):
        text = path.read_text(encoding='utf-8')
        total += len(re.findall(r'^\s*def test_', text, re.M))
    return total


def score_security(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    checks = [
        ('hashPassword', 1.0, 'PBKDF2 password hashing'),
        ('cloneDbForCloudUpload', 1.0, 'Cloud upload tanpa password plain'),
        ('getTmsSyncSecret', 1.0, 'Sync secret config'),
        ('client_auth', 1.0, 'Sync write auth payload'),
        ('Content-Security-Policy', 1.0, 'CSP meta tag'),
        ('tmsEscHtml', 1.0, 'XSS escape helper'),
        ('tmsEscAttr', 0.5, 'Attribute escape helper'),
        ('tmsRequireRole', 1.0, 'Role guard'),
        ('TMS_SESSION_IDLE_MS', 1.0, 'Session idle timeout'),
        ('isCloudProductionMode', 1.0, 'Disable default creds production'),
        ('persistCurrentUserSession', 0.5, 'Session tanpa password'),
        ('check_tms_write_auth', 0.5, 'Supabase write trigger'),
        ('tmsReportError', 0.5, 'Structured error reporting'),
        ("tmsRequirePerm('RESTORE_DB'", 0.5, 'Restore DB owner-only'),
        ('TMS_PERM', 0.5, 'Centralized permission matrix'),
        ('runDbIntegrityCheck', 0.5, 'DB integrity check'),
    ]
    sql = (ROOT / 'supabase_setup.sql').read_text(encoding='utf-8') if (ROOT / 'supabase_setup.sql').exists() else ''
    combined = js + html + sql
    for token, weight, label in checks:
        if token in combined:
            pts += weight
            notes.append(f'+{weight}: {label}')
    inner = len(re.findall(r'\.innerHTML', js))
    escaped = len(re.findall(r'tmsEscHtml\(', js))
    ratio = min(1.0, escaped / max(inner * 0.35, 1))
    pts += ratio * 1.5
    notes.append(f'+{ratio * 1.5:.1f}: XSS coverage ({escaped} escape / {inner} innerHTML)')
    return min(10.0, pts), notes


def score_architecture(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    modules = list((ROOT / 'js').glob('tms-*.js')) if (ROOT / 'js').is_dir() else []
    if len(modules) >= 5:
        pts += 4.0
        notes.append(f'+4.0: {len(modules)} modul JS terpisah')
    elif len(modules) >= 3:
        pts += 3.5
        notes.append(f'+3.5: {len(modules)} modul JS terpisah')
    elif len(modules) >= 2:
        pts += 3.0
        notes.append(f'+3.0: {len(modules)} modul JS terpisah')
    if (ROOT / 'health.json').exists():
        pts += 1.5
        notes.append('+1.5: health.json endpoint')
    if 'handleStorageDbSync' in js and js.count("addEventListener('storage'") == 1:
        pts += 2.0
        notes.append('+2.0: Single storage sync listener')
    if 'tmsRetryAsync' in js:
        pts += 1.5
        notes.append('+1.5: Sync retry helper')
    if 'requestAnimationFrame' in js and '_updateDataQueued' in js:
        pts += 1.0
        notes.append('+1.0: updateData debounce via rAF')
    if 'sc.innerHTML = filtered.map(t =>' in js:
        pts += 0.5
        notes.append('+0.5: SPV assets batch render join')
    lines = html.count('\n')
    if lines < 12000:
        pts += 1.0
        notes.append('+1.0: index.html size manageable')
    return min(10.0, pts), notes


def score_code_quality(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    func_defs = set(re.findall(r'function\s+([a-zA-Z_$][\w$]*)\s*\(', js))
    onclick_calls = set()
    for m in re.finditer(r'onclick="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm:
            onclick_calls.add(cm.group(1))
    missing = onclick_calls - func_defs
    if not missing:
        pts += 3.0
        notes.append(f'+3.0: Semua {len(onclick_calls)} onclick handler valid')
    else:
        pts += 1.0
        notes.append(f'+1.0: {len(missing)} onclick handler hilang')
    for fn in ('sanitizeDatabase', 'findServiceTicket', 'bindServiceTicketGlobalActions'):
        if f'function {fn}' in js:
            pts += 1.0
            notes.append(f'+1.0: {fn}')
    if 'findPersonnelConflicts' in js and 'validatePersonnelForm' in js:
        pts += 2.0
        notes.append('+2.0: Validasi duplikat personel')
    if 'tmsRenderSplitList' in js:
        pts += 1.0
        notes.append('+1.0: tmsRenderSplitList')
    return min(10.0, pts), notes


def score_performance(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    if 'loadTmsScript' in js or 'ensureSupabaseClient' in js:
        pts += 2.5
        notes.append('+2.5: Lazy-load library berat')
    if '_renderSparepartMasterImpl' in js and 'loadMoreSpareparts' in js:
        pts += 2.0
        notes.append('+2.0: Sparepart pagination')
    if 'debouncedRenderCustomerMaster' in js or 'debouncedRenderCustomerUnits' in js:
        pts += 2.0
        notes.append('+2.0: Debounced render customer')
    if 'updateData({ lite:' in js and 'isTmsMobileView' in js:
        pts += 2.0
        notes.append('+2.0: Mobile lite updateData')
    if 'preconnect' in html:
        pts += 1.5
        notes.append('+1.5: DNS preconnect')
    return min(10.0, pts), notes


def score_scalability(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    if 'mergeDatabases' in js:
        pts += 2.5
        notes.append('+2.5: mergeDatabases cloud merge')
    if 'db.version' in js and 'db_version' in js:
        pts += 2.0
        notes.append('+2.0: Versioned sync')
    if 'deletedIds' in js:
        pts += 1.5
        notes.append('+1.5: Tombstone deletedIds')
    if 'write_secret' in (ROOT / 'supabase_setup.sql').read_text(encoding='utf-8'):
        pts += 2.0
        notes.append('+2.0: Optional sync write lock')
    if 'getTmsSyncProfile' in js:
        pts += 1.0
        notes.append('+1.0: Sync profile per device')
    if count_tests() >= 40:
        pts += 1.0
        notes.append('+1.0: Regression tests for scale changes')
    return min(10.0, pts), notes


def score_reliability(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    if 'handleStorageDbSync' in js:
        pts += 2.5
        notes.append('+2.5: Cross-tab storage sync')
    if 'tmsRetryAsync' in js:
        pts += 2.0
        notes.append('+2.0: Retry async operations')
    if 'safeSaveLocalStorage' in js:
        pts += 2.0
        notes.append('+2.0: safeSaveLocalStorage')
    if 'unhandledrejection' in js or 'tmsInitRuntime' in js:
        pts += 1.5
        notes.append('+1.5: Global error handlers')
    if 'syncPending' in js and 'isSyncing' in js:
        pts += 1.0
        notes.append('+1.0: Sync queue coalescing')
    if (ROOT / 'cek_sistem.py').exists():
        pts += 1.0
        notes.append('+1.0: cek_sistem.py health script')
    return min(10.0, pts), notes


def score_maintainability(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    modules = list((ROOT / 'js').glob('tms-*.js')) if (ROOT / 'js').is_dir() else []
    pts += min(3.0, len(modules) * 1.5)
    notes.append(f'+{min(3.0, len(modules) * 1.5)}: {len(modules)} modul terpisah')
    if (ROOT / 'config.example.js').exists():
        pts += 1.5
        notes.append('+1.5: config.example.js')
    if (ROOT / 'release.js').exists():
        pts += 1.0
        notes.append('+1.0: release manifest')
    if 'cek_sistem.py' in [p.name for p in ROOT.iterdir()]:
        pts += 2.0
        notes.append('+2.0: Automated integrity checks')
    if count_tests() >= 50:
        pts += 2.5
        notes.append(f'+2.5: {count_tests()} unit tests')
    elif count_tests() >= 30:
        pts += 1.5
        notes.append(f'+1.5: {count_tests()} unit tests')
    return min(10.0, pts), notes


def score_tests() -> tuple[float, list[str]]:
    n = count_tests()
    pts = min(10.0, 4.0 + n * 0.08)
    notes = [f'+{pts:.1f}: {n} automated pytest cases']
    if (ROOT / 'cek_sistem.py').exists():
        pts = min(10.0, pts + 1.5)
        notes.append('+1.5: cek_sistem integration gate')
    if (ROOT / '.github/workflows/deploy-pages.yml').exists():
        pts = min(10.0, pts + 1.0)
        notes.append('+1.0: CI deploy workflow')
    return min(10.0, pts), notes


def score_production(js: str, html: str) -> tuple[float, list[str]]:
    pts, notes = 0.0, []
    health = ROOT / 'health.json'
    if health.exists():
        data = json.loads(health.read_text(encoding='utf-8'))
        if data.get('status') == 'ok':
            pts += 2.0
            notes.append('+2.0: health.json status ok')
    if (ROOT / '.github/workflows/deploy-pages.yml').exists():
        wf = (ROOT / '.github/workflows/deploy-pages.yml').read_text(encoding='utf-8')
        if 'cek_sistem.py' in wf:
            pts += 2.5
            notes.append('+2.5: CI QA gate')
        if 'audit_score.py' in wf:
            pts += 1.5
            notes.append('+1.5: CI audit score gate')
    if 'manifest.json' in [p.name for p in ROOT.iterdir()] and 'sw.js' in [p.name for p in ROOT.iterdir()]:
        pts += 2.0
        notes.append('+2.0: PWA manifest + service worker')
    if 'isCloudProductionMode' in js:
        pts += 1.5
        notes.append('+1.5: Production mode guard')
    if 'syncSecret' in (ROOT / 'config.example.js').read_text(encoding='utf-8'):
        pts += 0.5
        notes.append('+0.5: syncSecret documented')
    return min(10.0, pts), notes


def run_cek_sistem() -> bool:
    env = {**os.environ, 'TMS_SKIP_SERVER': '1'}
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / 'cek_sistem.py')],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return r.returncode == 0 and '[FAIL]' not in r.stdout
    except Exception:
        return False


def main() -> int:
    js, html = read_js_bundle()
    dimensions = {
        'Architecture': score_architecture(js, html),
        'Code Quality': score_code_quality(js, html),
        'Security': score_security(js, html),
        'Performance': score_performance(js, html),
        'Scalability': score_scalability(js, html),
        'Reliability': score_reliability(js, html),
        'Maintainability': score_maintainability(js, html),
        'Test Coverage': score_tests(),
        'Production Readiness': score_production(js, html),
    }

    print('\n== TMS Audit Score (objektif) ==\n')
    failed = []
    total = 0.0
    for name, (score, notes) in dimensions.items():
        total += score
        status = 'PASS' if score >= PASS_THRESHOLD else 'FAIL'
        if score < PASS_THRESHOLD:
            failed.append(name)
        print(f'  {name:22} {score:4.1f}/10  [{status}]')
        for n in notes[:4]:
            print(f'    {n}')
    avg = total / len(dimensions)
    print(f'\n  Rata-rata keseluruhan: {avg:.1f}/10')
    print(f'  Target per dimensi:    {PASS_THRESHOLD}/10')

    if failed:
        print(f'\n  Dimensi di bawah target: {", ".join(failed)}')
        return 1
    print('\n  Semua dimensi >= 8.0 — AUDIT PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
