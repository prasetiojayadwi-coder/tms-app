"""Automated audit regression tests for TMS v7.3+."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _html() -> str:
    return (ROOT / 'index.html').read_text(encoding='utf-8')


def _js_bundle() -> str:
    html = _html()
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
    return js


def test_health_json_exists():
    data = json.loads((ROOT / 'health.json').read_text(encoding='utf-8'))
    assert data['status'] == 'ok'
    assert float(data['version'].split('.')[0]) >= 7


def test_security_module_loaded():
    html = _html()
    assert 'js/tms-security.js' in html
    assert 'js/tms-runtime.js' in html


def test_tms_security_exports():
    sec = (ROOT / 'js/tms-security.js').read_text(encoding='utf-8')
    for sym in ('tmsEscHtml', 'hashPassword', 'cloneDbForCloudUpload', 'getTmsSyncSecret'):
        assert sym in sec


def test_tms_runtime_exports():
    rt = (ROOT / 'js/tms-runtime.js').read_text(encoding='utf-8')
    for sym in ('tmsRequireRole', 'tmsRetryAsync', 'tmsInitRuntime', 'TMS_SESSION_IDLE_MS'):
        assert sym in rt


def test_csp_meta_present():
    assert 'Content-Security-Policy' in _html()


def test_pbkdf2_in_bundle():
    js = _js_bundle()
    assert 'async function hashPassword' in js or 'function hashPassword' in js
    assert 'verifyPassword' in js


def test_clone_db_for_cloud():
    js = _js_bundle()
    assert 'cloneDbForCloudUpload' in js
    assert 'cloneDbForCloudUpload(db)' in js


def test_sync_secret_payload():
    js = _js_bundle()
    assert 'client_auth' in js
    assert 'getTmsSyncSecret' in js


def test_session_without_password():
    js = _js_bundle()
    assert 'persistCurrentUserSession' in js
    assert 'delete safe.pass' in js or 'delete u.pass' in js


def test_role_guard_delete_personnel():
    js = _js_bundle()
    assert 'tmsRequireRole' in js
    assert "tmsRequireRole(['owner', 'spv']" in js


def test_single_storage_listener():
    js = _js_bundle()
    assert js.count("addEventListener('storage'") == 1
    assert 'handleStorageDbSync' in js


def test_xss_chat_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(m.text)' in js


def test_xss_history_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(h.m)' in js or 'tmsEscHtml(l.action)' in js


def test_xss_personnel_name_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(u.name)' in js


def test_xss_request_note_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(r.note)' in js


def test_service_ticket_resolver():
    js = _js_bundle()
    for fn in ('findServiceTicket', 'getDbUser', 'resolveTicketAssignedTsId', 'ticketPjMatchesCurrentUser'):
        assert f'function {fn}' in js


def test_service_global_click_binding():
    js = _js_bundle()
    assert 'bindServiceTicketGlobalActions' in js


def test_cloud_production_mode():
    js = _js_bundle()
    assert 'isCloudProductionMode' in js


def test_sync_retry():
    js = _js_bundle()
    assert 'tmsRetryAsync' in js


def test_supabase_write_trigger():
    sql = (ROOT / 'supabase_setup.sql').read_text(encoding='utf-8')
    assert 'check_tms_write_auth' in sql
    assert 'write_secret' in sql


def test_config_sync_secret_template():
    cfg = (ROOT / 'config.example.js').read_text(encoding='utf-8')
    assert 'syncSecret' in cfg


def test_release_version_73():
    rel = (ROOT / 'release.js').read_text(encoding='utf-8')
    assert '7.3' in rel


def test_pwa_files():
    assert (ROOT / 'manifest.json').exists()
    assert (ROOT / 'sw.js').exists()


def test_cek_sistem_script_exists():
    assert (ROOT / 'cek_sistem.py').exists()


def test_audit_score_script_exists():
    assert (ROOT / 'audit_score.py').exists()


def test_all_onclick_handlers_defined():
    html = _html()
    js = _js_bundle()
    func_defs = set(re.findall(r'function\s+([a-zA-Z_$][\w$]*)\s*\(', js))
    missing = []
    for m in re.finditer(r'onclick="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm and cm.group(1) not in func_defs:
            missing.append(cm.group(1))
    assert not missing, f'Missing handlers: {missing}'


def test_duplicate_protection_functions():
    js = _js_bundle()
    for fn in ('findPersonnelConflicts', 'validatePersonnelForm', 'sanitizeDatabase'):
        assert f'function {fn}' in js


def test_customer_master_views():
    html = _html()
    for cid in ('view-customer-master', 'view-customer-service', 'customerModal'):
        assert cid in html


def test_sparepart_pagination():
    js = _js_bundle()
    assert 'loadMoreSpareparts' in js
    assert '_renderSparepartMasterImpl' in js


def test_mobile_lite_update():
    js = _js_bundle()
    assert 'updateData({ lite:' in js
    assert 'isTmsMobileView' in js


def test_lazy_load_supabase():
    js = _js_bundle()
    assert 'ensureSupabaseClient' in js or 'loadTmsScript' in js


def test_merge_databases():
    js = _js_bundle()
    assert 'mergeDatabases' in js


def test_safe_save_local_storage():
    js = _js_bundle()
    assert 'safeSaveLocalStorage' in js


def test_batch_import_permissions():
    js = _js_bundle()
    assert 'BATCH_IMPORT_FULL_ROLES' in js


def test_excel_templates_defined():
    js = _js_bundle()
    assert 'TMS_Template_Spareparts.xlsx' in js


def test_service_pickup_action_global():
    js = _js_bundle()
    assert 'window.actionServiceTicket' in js or 'actionServiceTicket' in js


def test_repair_ticket_assignment():
    js = _js_bundle()
    assert 'repairTicketAssignmentForCurrentUser' in js


def test_tms_esc_attr_used():
    js = _js_bundle()
    assert 'tmsEscAttr' in js


def test_idle_session_timeout_constant():
    js = _js_bundle()
    assert 'TMS_SESSION_IDLE_MS' in js
    assert '30 * 60 * 1000' in js


def test_global_error_handler():
    js = _js_bundle()
    assert 'unhandledrejection' in js


def test_ci_workflow_qa_gate():
    wf = (ROOT / '.github/workflows/deploy-pages.yml').read_text(encoding='utf-8')
    assert 'cek_sistem.py' in wf


def test_sw_cache_version():
    sw = (ROOT / 'sw.js').read_text(encoding='utf-8')
    assert 'tms-cache-v' in sw


def test_required_project_files():
    for name in ('index.html', 'release.js', 'sw.js', 'supabase_setup.sql'):
        p = ROOT / name
        assert p.exists() and p.stat().st_size > 0


def test_audit_score_passes_threshold():
    r = subprocess.run(
        [sys.executable, str(ROOT / 'audit_score.py')],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_cek_sistem_no_fail():
    import os
    r = subprocess.run(
        [sys.executable, str(ROOT / 'cek_sistem.py')],
        cwd=str(ROOT),
        env={**os.environ, 'TMS_SKIP_SERVER': '1'},
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert '[FAIL]' not in r.stdout, r.stdout[-2000:]


def test_innerhtml_escape_ratio():
    js = _js_bundle()
    inner = len(re.findall(r'\.innerHTML', js))
    escaped = len(re.findall(r'tmsEscHtml\(', js))
    assert escaped >= 30
    assert escaped / max(inner, 1) >= 0.25


def test_delete_service_owner_only():
    js = _js_bundle()
    assert "currentUser.role !== 'owner'" in js


def test_get_current_user_hook():
    js = _js_bundle()
    assert '_tmsGetCurrentUser' in js


def test_update_data_raf_debounce():
    js = _js_bundle()
    assert '_updateDataQueued' in js
    assert 'requestAnimationFrame' in js


def test_sph_module_present():
    html = _html()
    assert 'view-sph-log' in html
    assert 'sphBuilderModal' in html


def test_tms_render_split_list():
    js = _js_bundle()
    assert 'tmsRenderSplitList' in js


def test_norm_inv_key_protection():
    js = _js_bundle()
    assert 'normInvKey' in js
    assert 'allocateUniqueId' in js


def test_customer_unit_import_upsert():
    js = _js_bundle()
    assert 'findCustomerUnitForUpsert' in js
    assert 'importCustomerUnitsBatch' in js


def test_sync_profile_mobile():
    js = _js_bundle()
    assert 'getTmsSyncProfile' in js
    assert 'startMobileSyncPoll' in js


def test_health_checks_list():
    data = json.loads((ROOT / 'health.json').read_text(encoding='utf-8'))
    assert 'pbkdf2-password' in data['checks']
    assert 'xss-escape' in data['checks']


def test_security_module_no_password_in_upload():
    sec = (ROOT / 'js/tms-security.js').read_text(encoding='utf-8')
    assert 'delete u.pass' in sec


def test_runtime_retry_max():
    rt = (ROOT / 'js/tms-runtime.js').read_text(encoding='utf-8')
    assert 'TMS_SYNC_MAX_RETRIES' in rt


def test_validate_personnel_escapes_errors():
    js = _js_bundle()
    assert 'tmsEscHtml(c.existing)' in js


def test_chat_user_name_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(u.name.split' in js


def test_service_duplicate_msg_escaped():
    js = _js_bundle()
    assert 'tmsEscHtml(dup.unitSn)' in js


def test_config_deploy_exists():
    assert (ROOT / 'config.deploy.js').exists()


def test_manifest_valid_json():
    json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))


def test_no_init_handover_canvas_legacy():
    js = _js_bundle()
    assert 'initHandoverCanvas' not in js


def test_build_service_ticket_row():
    js = _js_bundle()
    assert 'buildServiceTicketRow' in js


def test_tms_cards_visible():
    js = _js_bundle()
    assert 'tmsCardsVisible' in js
