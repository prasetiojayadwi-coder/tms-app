#!/usr/bin/env python3
"""Pemeriksaan kesehatan TMS — jalankan tanpa browser."""
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8080
BASE = f'http://localhost:{PORT}'
PASS = 0
FAIL = 0
WARN = 0


def ok(msg):
    global PASS
    PASS += 1
    print(f'  [OK]   {msg}')


def bad(msg):
    global FAIL
    FAIL += 1
    print(f'  [FAIL] {msg}')


def warn(msg):
    global WARN
    WARN += 1
    print(f'  [WARN] {msg}')


def fetch(path, timeout=8):
    return urllib.request.urlopen(f'{BASE}{path}', timeout=timeout)


def check_files():
    print('\n== File Proyek ==')
    required = [
        'index.html', 'manifest.json', 'sw.js', 'release.js', 'tms_pwa_icon.png',
        'Mulai_Server.bat', 'config.example.js', 'config.deploy.js',
        'Jalankan_Setup.bat', 'jalankan_setup.py', 'supabase_setup.sql',
    ]
    for name in required:
        p = ROOT / name
        if p.exists() and p.stat().st_size > 0:
            ok(f'{name} ({p.stat().st_size:,} bytes)')
        else:
            bad(f'{name} tidak ditemukan atau kosong')

    cfg = ROOT / 'config.js'
    example = ROOT / 'config.example.js'
    if cfg.exists():
        text = cfg.read_text(encoding='utf-8')
        if 'YOUR-PROJECT' in text or 'YOUR_SUPABASE_ANON_KEY' in text:
            warn('config.js masih berisi placeholder — isi kredensial Supabase')
        elif 'supabase.co' in text and 'anonKey' in text:
            ok('config.js terkonfigurasi')
        else:
            warn('config.js ada tetapi format tidak dikenali')
    elif example.exists():
        warn('config.js belum ada — jalankan Atur_Cloud.bat atau Setup_Config.bat')
    else:
        bad('config.example.js hilang, tidak bisa setup cloud sync')


def check_html_integrity():
    print('\n== Integritas Kode HTML/JS ==')
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    scripts = [
        m.group(1) for m in re.finditer(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', html, re.I)
        if not m.group(1).strip().startswith('tailwind.config')
    ]
    js = '\n'.join(scripts)
    func_defs = set(re.findall(r'function\s+([a-zA-Z_$][\w$]*)\s*\(', js))

    onclick_calls = set()
    for m in re.finditer(r'onclick="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm:
            onclick_calls.add(cm.group(1))
    missing_onclick = sorted(onclick_calls - func_defs)
    if missing_onclick:
        bad(f'Handler onclick tanpa fungsi: {", ".join(missing_onclick)}')
    else:
        ok(f'Semua {len(onclick_calls)} handler onclick valid')

    onsubmit_ok = True
    for m in re.finditer(r'onsubmit="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm and cm.group(1) not in func_defs:
            bad(f'Handler onsubmit tanpa fungsi: {cm.group(1)}')
            onsubmit_ok = False
    if onsubmit_ok:
        ok('Semua handler onsubmit valid')

    missing_event = []
    for attr in ('onchange', 'oninput', 'onkeyup'):
        for m in re.finditer(attr + r'="([^"]+)"', html):
            cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
            if cm and cm.group(1) not in func_defs:
                missing_event.append(f'{attr}:{cm.group(1)}')
    if missing_event:
        bad(f'Handler event tanpa fungsi: {", ".join(sorted(set(missing_event)))}')
    else:
        ok('Semua handler onchange/oninput/onkeyup valid')

    tabs = set(re.findall(r"switchTab\('([^']+)'\)", html))
    views = set(re.findall(r'id="view-([^"]+)"', html))
    missing_views = sorted(tabs - views)
    if missing_views:
        bad(f'Tab tanpa view: {", ".join(missing_views)}')
    else:
        ok(f'Semua {len(tabs)} tab navigasi punya view')

    if 'initHandoverCanvas' in js:
        warn('Kode legacy initHandoverCanvas masih ada')
    else:
        ok('Kode legacy handover canvas sudah dibersihkan')

    for fn in ('sanitizeDatabase', 'allocateUniqueId', 'normInvKey', 'findPersonnelConflicts', 'validatePersonnelForm', 'findBackupUnitConflicts', 'validateBackupUnitForm', 'findCustomerConflicts', 'validateCustomerForm', 'findCustomerUnitConflicts', 'validateCustomerUnitForm'):
        if f'function {fn}' in js:
            ok(f'Proteksi duplikat: {fn} ada')
        else:
            bad(f'Proteksi duplikat hilang: {fn}')

    for cid in ('view-customer-master', 'customerModal', 'customerUnitModal'):
        if cid in html:
            ok(f'Master Data Customer: {cid} ada')
        else:
            bad(f'Master Data Customer: {cid} hilang')

    for fn in ('renderCustomerMaster', 'debouncedRenderCustomerMaster', 'populateServiceCustomerSelects', 'onPickServiceCustomer', 'onPickServiceUnit', 'getUnitServiceHistory', 'buildServiceHistoryIndex', 'openServiceModalForUnit', 'smartFillServiceByCustomerName', 'applyLastServiceComplaint'):
        if f'function {fn}' in js:
            ok(f'Master Data Customer: {fn} ada')
        else:
            bad(f'Master Data Customer: {fn} hilang')

    if 'view-customer-service' in html:
        ok('Service & Repair: view-customer-service ada')
    else:
        bad('Service & Repair: view-customer-service hilang')

    svc_m = re.search(r'id="view-customer-service"[\s\S]*?<!-- Service Status', html)
    svc_block = svc_m.group(0) if svc_m else ''
    if svc_block and 'Import Unit Excel' in svc_block and "openBatchImportModal('customer-unit')" in svc_block:
        ok('Service & Repair: Import Unit Excel di toolbar')
    else:
        bad('Service & Repair: Import Unit Excel di toolbar hilang')
    if svc_block and 'Template Unit' in svc_block and "downloadBatchTemplate('customer-unit')" in svc_block:
        ok('Service & Repair: Template Unit di toolbar')
    else:
        bad('Service & Repair: Template Unit di toolbar hilang')
    if svc_block and svc_block.count('data-batch-type="customer-unit"') >= 2:
        ok('Service & Repair: batch unit punya data-batch-type')
    else:
        bad('Service & Repair: data-batch-type customer-unit tidak lengkap')
    if 'function renderServiceTickets' in js and 'syncBatchImportButtons()' in js.split('function renderServiceTickets')[1][:800]:
        ok('Service & Repair: syncBatchImportButtons di renderServiceTickets')
    else:
        bad('Service & Repair: syncBatchImportButtons tidak dipanggil saat render')
    if 'function importCustomerUnitsBatch' in js and 'findCustomerUnitConflicts' in js.split('importCustomerUnitsBatch')[1][:1200]:
        ok('Service & Repair: importCustomerUnitsBatch + proteksi duplikat')
    else:
        bad('Service & Repair: importCustomerUnitsBatch tidak lengkap')

    for cid in ('view-sparepart-master', 'view-sph-log', 'sphBuilderModal', 'sphDetailModal', 'sphCustomerPickModal'):
        if cid in html:
            ok(f'Modul SPH: {cid} ada')
        else:
            bad(f'Modul SPH: {cid} hilang')

    for fn in ('buildExcelBlob', 'downloadExcelFile', 'downloadBatchTemplate', 'canBatchImport', 'canBatchImportType', 'isExcelXlsxFile', 'syncBatchImportButtons'):
        if f'function {fn}' in js:
            ok(f'Excel batch import: {fn} ada')
        else:
            bad(f'Excel batch import: {fn} hilang')

    if 'BATCH_IMPORT_FULL_ROLES' in js and 'BATCH_IMPORT_TSF_TYPES' in js and 'data-batch-type' in html:
        ok('Batch import: Owner/SPV/Specialist penuh, TSF hanya tool & demo')
    else:
        bad('Matrix permission batch import tidak ditemukan')

    if "accept=\".xlsx" in html and '.xls"' not in html.split('batch-import-file')[1][:120] if 'batch-import-file' in html else False:
        ok('Upload batch hanya menerima .xlsx')
    elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in html:
        ok('Upload batch hanya menerima .xlsx')
    else:
        warn('Accept file batch import perlu dicek manual')

    if 'TMS_Template_Spareparts.xlsx' in js and 'aoa_to_sheet' in js:
        ok('Template sparepart Excel (.xlsx) — satu kolom per field')
    else:
        bad('Template sparepart Excel (.xlsx) tidak ditemukan di kode')

    templates_dir = ROOT / 'templates'
    for name in (
        'TMS_Template_Spareparts.xlsx', 'TMS_Template_Customers.xlsx',
        'TMS_Template_Customer_Units.xlsx', 'TMS_Template_Special_Tools.xlsx',
        'TMS_Template_Backup_Units.xlsx',
    ):
        p = templates_dir / name
        if p.exists() and p.stat().st_size > 500:
            ok(f'File template: {name}')
        else:
            warn(f'File template belum ada atau kosong: {name}')

    for fn in (
        'lookupSparepartByArtNo', 'searchSparepartsPartial', 'smartFillSphLine', 'showSphArtSuggestions',
        'renderSphLog', 'showSphDetail', 'exportSphPdf', 'cancelSphDocument', 'openSphBuilderModal',
        'confirmSphCustomerPick', 'getCombinedSphCustomerGroups', 'openTsfQuickRepair',
        'configureQuotationModalForTicket', 'syncSphPoFromServiceTicket', 'canIssueSphForTicket',
        'canCancelSphDocument', 'buildCompressedDocPreviewHtml', 'syncLoginFooterVersion',
    ):
        if f'function {fn}' in js:
            ok(f'Modul SPH: {fn} ada')
        else:
            bad(f'Modul SPH: {fn} hilang')

    if 'flt-sph-cancelled' in html and 'sph-stat-cancelled' in html:
        ok('Modul SPH: filter + stat Cancelled ada')
    else:
        bad('Modul SPH: filter/stat Cancelled hilang')

    if 'id="login-footer-version"' in html and 'syncLoginFooterVersion()' in js:
        ok('Footer login: versi dinamis dari TMS_RELEASE')
    else:
        bad('Footer login: syncLoginFooterVersion atau login-footer-version hilang')

    if 'function showSphDetail' in js and 'alert(`SPH' not in js:
        ok('Modul SPH: showSphDetail pakai modal (bukan alert)')
    elif 'alert(`SPH' in js:
        bad('Modul SPH: showSphDetail masih pakai alert()')

    release_text = (ROOT / 'release.js').read_text(encoding='utf-8')
    sw_text = (ROOT / 'sw.js').read_text(encoding='utf-8')
    build_match = re.search(r"build:\s*(\d+)", release_text)
    cache_match = re.search(r"tms-cache-v(\d+)", sw_text)
    if build_match and cache_match and build_match.group(1) == cache_match.group(1):
        ok(f'Versi cache SW match release build v{build_match.group(1)}')
    elif build_match and cache_match:
        bad(f'Versi cache SW tidak match: release build {build_match.group(1)} vs sw {cache_match.group(1)}')
    else:
        warn('Tidak bisa verifikasi match release.js / sw.js build')

    for cid in ['sig-canvas', 'handover-sig-canvas-giver', 'handover-sig-canvas-receiver']:
        if cid in html:
            ok(f'Canvas {cid} ada')
        else:
            bad(f'Canvas {cid} hilang')

    for bad_cls in ('bg-red-650', 'text-red-650', 'text-gray-505', 'text-gray-750', 'bg-gray-150', 'bg-lux-850', 'border-gray-150', 'border-lux-850'):
        if bad_cls in html:
            warn(f'Class CSS tidak valid: {bad_cls}')

    if 'release.js' in html and 'TMS_RELEASE' in (ROOT / 'release.js').read_text(encoding='utf-8'):
        ok('Sistem update: release.js + TMS_RELEASE ada')
    elif 'release.js' not in html:
        warn('release.js tidak direferensikan di index.html')

    if 'release.js' in sw_text:
        ok('Service Worker cache mencakup release.js')
    else:
        warn('release.js belum ada di CORE_ASSETS sw.js')

    if 'mezuatmcjqjxfsvepizv' in html or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' in html:
        bad('Kredensial Supabase masih tertanam di index.html')
    elif 'config.js' in html:
        ok('Kredensial Supabase dipisah ke config.js')
    else:
        warn('config.js tidak direferensikan di index.html')


def _dup_keys(items, field):
    seen = {}
    dups = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        val = (item.get(field) or '').strip().lower()
        if not val or val == '-':
            continue
        if val in seen:
            dups.append(val)
        else:
            seen[val] = item.get('id')
    return dups


def audit_cloud_duplicates():
    import re
    import json as jsonlib
    cfg = ROOT / 'config.js'
    if not cfg.exists():
        cfg = ROOT / 'config.deploy.js'
    if not cfg.exists():
        warn('Tidak bisa audit duplikat cloud — config tidak ada')
        return
    text = cfg.read_text(encoding='utf-8')
    url_m = re.search(r"url:\s*['\"]([^'\"]+)['\"]", text)
    key_m = re.search(r"anonKey:\s*['\"]([^'\"]+)['\"]", text)
    if not url_m or not key_m:
        warn('Format config tidak dikenali — lewati audit duplikat cloud')
        return
    base, key = url_m.group(1).strip(), key_m.group(1).strip()
    req = urllib.request.Request(
        f'{base.rstrip("/")}/rest/v1/tms_sync?select=db_data&id=eq.1',
        headers={'apikey': key, 'Authorization': f'Bearer {key}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            rows = jsonlib.loads(r.read().decode('utf-8', 'replace'))
    except Exception as e:
        warn(f'Audit duplikat cloud gagal: {e}')
        return
    if not rows:
        ok('Cloud kosong — tidak ada duplikat')
        return
    data = rows[0].get('db_data') or {}
    tools = data.get('tools') or []
    demos = data.get('demoUnits') or []
    inv_dups = _dup_keys(tools + demos, 'noInv')
    sn_dups = _dup_keys(tools + demos, 'sn')
    demo_art_dups = _dup_keys(demos, 'artNo')
    svc_active = [s for s in (data.get('serviceTickets') or []) if s.get('status') not in ('completed', 'cancelled', 'returned_cust')]
    svc_sn_dups = _dup_keys(svc_active, 'unitSn')
    if inv_dups:
        warn(f'Duplikat No. Inventaris di cloud: {len(inv_dups)} ({", ".join(inv_dups[:3])}...)')
    else:
        ok('Cloud: tidak ada duplikat No. Inventaris')
    if sn_dups:
        warn(f'Duplikat Serial Number di cloud: {len(sn_dups)} ({", ".join(sn_dups[:3])}...)')
    else:
        ok('Cloud: tidak ada duplikat Serial Number aset')
    if demo_art_dups:
        warn(f'Duplikat Art Number unit backup di cloud: {len(demo_art_dups)}')
    else:
        ok('Cloud: tidak ada duplikat Art Number unit backup')
    if svc_sn_dups:
        warn(f'Duplikat SN service aktif di cloud: {len(svc_sn_dups)}')
    else:
        ok('Cloud: tidak ada duplikat SN service aktif')

    users = list((data.get('users') or {}).values())
    user_dups = _dup_keys([{'id': u.get('id'), 'noInv': u.get('user', '')} for u in users if isinstance(u, dict)], 'noInv')
    nik_dups = _dup_keys([{'id': u.get('id'), 'noInv': u.get('nik', '')} for u in users if isinstance(u, dict)], 'noInv')
    email_dups = _dup_keys([{'id': u.get('id'), 'noInv': u.get('email', '')} for u in users if isinstance(u, dict)], 'noInv')
    if user_dups:
        warn(f'Duplikat username personel di cloud: {len(user_dups)}')
    else:
        ok('Cloud: tidak ada duplikat username personel')
    if nik_dups:
        warn(f'Duplikat NIK personel di cloud: {len(nik_dups)}')
    else:
        ok('Cloud: tidak ada duplikat NIK personel')
    if email_dups:
        warn(f'Duplikat email personel di cloud: {len(email_dups)}')
    else:
        ok('Cloud: tidak ada duplikat email personel')

    cust_code_dups = _dup_keys(data.get('customers') or [], 'code')
    cust_sn_dups = _dup_keys(data.get('customerUnits') or [], 'unitSn')
    if cust_code_dups:
        warn(f'Duplikat kode customer di cloud: {len(cust_code_dups)}')
    else:
        ok('Cloud: tidak ada duplikat kode customer')
    if cust_sn_dups:
        warn(f'Duplikat SN unit customer di cloud: {len(cust_sn_dups)}')
    else:
        ok('Cloud: tidak ada duplikat SN unit customer')


def check_cloud():
    print('\n== Cloud / Online ==')
    deploy = ROOT / 'config.deploy.js'
    if deploy.exists() and 'supabase.co' in deploy.read_text(encoding='utf-8'):
        ok('config.deploy.js siap untuk GitHub Pages')
    else:
        bad('config.deploy.js tidak valid')

    live_base = 'https://prasetiojayadwi-coder.github.io/tms-app/'
    try:
        with urllib.request.urlopen(live_base + 'config.deploy.js', timeout=12) as r:
            body = r.read().decode('utf-8', 'replace')
            if r.status == 200 and 'supabase.co' in body:
                ok('Aplikasi online: config.deploy.js HTTP 200')
            else:
                warn(f'Aplikasi online tidak normal (HTTP {r.status})')
    except Exception as e:
        warn(f'Tidak bisa cek deploy online: {e}')

    release_local = (ROOT / 'release.js').read_text(encoding='utf-8')
    local_ver = re.search(r"version:\s*'([^']+)'", release_local)
    local_build = re.search(r'build:\s*(\d+)', release_local)
    try:
        with urllib.request.urlopen(live_base + 'release.js', timeout=15) as r:
            live_rel = r.read().decode('utf-8', 'replace')
        live_ver = re.search(r"version:\s*'([^']+)'", live_rel)
        live_build = re.search(r'build:\s*(\d+)', live_rel)
        with urllib.request.urlopen(live_base + 'sw.js', timeout=15) as r:
            live_sw = r.read().decode('utf-8', 'replace')
        live_cache = re.search(r'tms-cache-v(\d+)', live_sw)
        if local_ver and live_ver and local_ver.group(1) == live_ver.group(1):
            ok(f'Live release.js: v{live_ver.group(1)} match lokal')
        elif live_ver:
            warn(f'Live v{live_ver.group(1)} tidak match lokal v{local_ver.group(1) if local_ver else "?"}')
        if live_build and live_cache and live_build.group(1) == live_cache.group(1):
            ok(f'Live sw.js: tms-cache-v{live_cache.group(1)} match build')
        elif live_cache:
            warn(f'Live cache v{live_cache.group(1)} tidak match build {live_build.group(1) if live_build else "?"}')
        with urllib.request.urlopen(live_base + 'index.html', timeout=90) as r:
            live_html = r.read().decode('utf-8', 'replace')
        if 'TMS_Template_Spareparts.xlsx' in live_html and 'buildExcelBlob' in live_html:
            ok('Live index.html: template Excel .xlsx aktif')
        else:
            warn('Live index.html: fitur template Excel belum terdeteksi')
        if 'Import Unit Excel' in live_html and "openBatchImportModal('customer-unit')" in live_html:
            ok('Live index.html: batch import unit di Service & Repair')
        else:
            warn('Live index.html: batch import unit Service belum terdeteksi')
    except Exception as e:
        warn(f'Tidak bisa verifikasi live release: {e}')

    audit_cloud_duplicates()


def check_server():
    print('\n== Server Lokal ==')
    try:
        r = fetch('/index.html')
        body = r.read()
        if r.status == 200 and len(body) > 100_000:
            ok(f'index.html dilayani ({len(body):,} bytes)')
        else:
            bad(f'index.html tidak normal (status {r.status})')
    except urllib.error.URLError:
        bad(f'Server tidak berjalan di {BASE}')
        warn('Jalankan Mulai_Server.bat terlebih dahulu, lalu ulangi cek ini')
        return

    for path in ['config.js', 'manifest.json', 'sw.js', 'release.js', 'tms_pwa_icon.png']:
        try:
            r = fetch('/' + path)
            r.read()
            ok(f'{path} HTTP {r.status}')
        except Exception as e:
            bad(f'{path}: {e}')


def check_git():
    print('\n== Git / GitHub ==')
    git = r'C:\Program Files\Git\cmd\git.exe'
    if not Path(git).exists():
        warn('Git tidak ditemukan — lewati pemeriksaan GitHub')
        return

    def git_run(*args):
        r = subprocess.run([git, *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return r.stdout.strip(), r.returncode

    remote, _ = git_run('remote', 'get-url', 'origin')
    if remote:
        ok(f'Remote: {remote}')
    else:
        bad('Remote origin tidak dikonfigurasi')
        return

    tracked, _ = git_run('ls-files')
    tracked_set = set(tracked.splitlines()) if tracked else set()
    if 'config.js' in tracked_set:
        bad('KRITIS: config.js ter-track di git — kredensial bisa bocor ke GitHub')
    else:
        ok('config.js tidak ter-track')

    _, ignore_code = git_run('check-ignore', '-v', 'config.js')
    if ignore_code == 0:
        ok('.gitignore melindungi config.js')
    elif Path('.gitignore').exists():
        warn('.gitignore ada tetapi config.js belum ter-ignore')

    if 'config.example.js' not in tracked_set:
        warn('config.example.js belum di-commit ke GitHub')

    status, _ = git_run('status', '-sb')
    if any(line.startswith('??') for line in status.splitlines()[1:]):
        warn('Ada file baru yang belum di-commit')
    if ' M ' in f' {status} ' or '\n M ' in status:
        warn('Ada perubahan lokal yang belum di-commit')

    remote_html, rc = git_run('show', 'origin/main:index.html')
    if rc == 0:
        if 'mezuatmcjqjxfsvepizv' in remote_html or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' in remote_html:
            bad('KRITIS: GitHub origin/main masih memuat kredensial di index.html — perlu push perbaikan')
        else:
            ok('GitHub origin/main bebas kredensial hardcoded')


def main():
    print('========================================')
    print('  TMS — Pemeriksaan Kesehatan Sistem')
    print('========================================')
    check_files()
    check_html_integrity()
    check_git()
    check_cloud()
    check_server()
    print('\n========================================')
    print(f'  Hasil: {PASS} OK | {WARN} peringatan | {FAIL} gagal')
    print('========================================')
    if FAIL:
        sys.exit(1)


if __name__ == '__main__':
    main()
