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
    for sym in ('tmsEscHtml', 'hashPassword', 'cloneDbForCloudUpload', 'getTmsSyncSecret', 'tmsSafeDataUrl', 'sanitizeDbForRestore'):
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
    assert 'tmsRequirePerm' in js
    assert "tmsRequirePerm('DELETE_PERSONNEL'" in js


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


def test_release_version_7109():
    rel = (ROOT / 'release.js').read_text(encoding='utf-8')
    assert '7.10.9' in rel
    assert re.search(r"build:\s*131", rel)
    assert 'tms-cache-v131' in (ROOT / 'sw.js').read_text(encoding='utf-8')


def test_no_hidden_required_quote_details():
    """svc-quote-details selalu hidden; tak boleh dijadikan required (memblok submit)."""
    html = _html()
    assert "quoteDetails.setAttribute('required'" not in html
    assert "quoteDetails.removeAttribute('required')" in html


def test_number_input_spinner_hidden():
    html = _html()
    assert '.input-field[type="number"]' in html
    assert '-webkit-inner-spin-button' in html


def test_html_div_tags_balanced():
    """Cegah kambuhnya bug </div> hilang yang menyembunyikan modal."""
    html = _html()
    stripped = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    stripped = re.sub(r'<style\b[^>]*>.*?</style>', '', stripped, flags=re.DOTALL | re.IGNORECASE)
    stripped = re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)
    opens = len(re.findall(r'<div\b', stripped))
    closes = len(re.findall(r'</div>', stripped))
    assert opens == closes, f"<div> tidak seimbang: {opens} dibuka vs {closes} ditutup"


def test_service_modals_are_top_level():
    """Modal alur service harus anak langsung <body> (depth div 0), bukan tersarang di modal lain."""
    html = _html()
    lines = html.splitlines()
    depth = 0
    body_started = False
    modal_re = re.compile(r'<div id="([A-Za-z0-9_-]+)"[^>]*\bfixed inset-0')
    must_be_top = {
        'repairLocPickModal', 'handoverSignatureModal', 'reassignPjModal',
        'serviceDetailModal', 'serviceBulkBastModal', 'serviceDeliveryModal',
    }
    seen = {}
    for line in lines:
        if '<body' in line:
            body_started = True
        if not body_started:
            continue
        m = modal_re.search(line)
        if m and m.group(1) in must_be_top:
            seen[m.group(1)] = depth
        depth += len(re.findall(r'<div\b', line)) - len(re.findall(r'</div>', line))
    for name in must_be_top:
        assert seen.get(name) == 0, f"Modal {name} tidak di depth 0 (depth={seen.get(name)}) — tersarang di elemen tersembunyi"


def test_svc_debug_probe_present():
    html = _html()
    assert 'tmsSvcDebugLog' in html
    assert 'svcdebug=1' in html


def test_index_html_not_truncated():
    html = _html()
    assert len(html) > 900_000, 'index.html terlalu kecil — kemungkinan terpotong'
    for sym in (
        'function actionServiceTicket',
        'function runServiceTicketAction',
        'function initAppUI',
        'function openRepairLocPickModal',
        '</html>',
    ):
        assert sym in html
    assert html.rstrip().endswith('</html>')


def test_notification_xss_escaped():
    js = _js_bundle()
    block = js[js.find('function _checkNotificationsImpl'):js.find('function _checkNotificationsImpl') + 3500]
    assert 'const esc = typeof tmsEscHtml' in block
    assert 'esc(t.desc)' in block or 'esc(item.desc' in block


def test_pj_reassignment_flow():
    html = _html()
    js = _js_bundle()
    assert 'reassignPjModal' in html
    assert 'function canReassignServicePj' in js
    assert 'function openReassignPjModal' in js
    assert 'function submitReassignPj' in js
    assert 'PJ dialihkan dari' in js
    block = js[js.find('function submitReassignPj'):js.find('function getTicketPjName')]
    assert "s.status === 'registered'" in block
    assert 's.repairLoc = null' in block
    assert 'canReassignServiceTicket(s)' in js
    assert "tmsRequirePerm('REASSIGN_SERVICE_PJ'" in js
    open_block = js[js.find('function openReassignPjModal'):js.find('function openReassignPjModal') + 400]
    assert "tmsRequirePerm('REASSIGN_SERVICE_PJ'" in open_block
    auth = (ROOT / 'js/tms-auth.js').read_text(encoding='utf-8')
    assert 'REASSIGN_SERVICE_PJ' in auth


def test_session_idle_and_restore_hardening():
    js = _js_bundle()
    assert 'tmsInitSessionIdleWatch' in js
    assert 'sanitizeDbForRestore' in js
    assert 'tmsSafeDataUrl' in js
    integrity = (ROOT / 'js/tms-integrity.js').read_text(encoding='utf-8')
    assert 'ORPHAN_SERVICE_PJ' in integrity


def test_service_ticket_creator_roles():
    js = _js_bundle()
    assert 'function canCreateServiceTicket' in js
    assert 'function canActAsServicePj' in js
    assert "u.role === 'owner'" in js[js.find('function canCreateServiceTicket'):js.find('function canActAsServicePj')]
    assert 'isServiceSpecRole(u)' in js[js.find('function canCreateServiceTicket'):js.find('function canActAsServicePj')]
    reg_btn = js[js.find('function renderServiceTickets'):js.find('function renderServiceTickets') + 3500]
    assert 'canCreateServiceTicket(currentUser)' in reg_btn


def test_svc_ticket_btn_has_direct_onclick():
    js = _js_bundle()
    block = js[js.find('function svcTicketBtn'):js.find('function svcTicketBtn') + 800]
    # Buttons must invoke the direct dispatcher with embedded id/handler (no DOM/dataset dependency).
    assert "onclick=\"runSvcAction('" in block
    assert 'function runSvcAction' in js
    assert 'window.runSvcAction = runSvcAction' in js
    # Delegated fallback must NOT use capture-phase stopPropagation (which can swallow inline clicks).
    bind = js[js.find('function bindServiceTicketGlobalActions'):js.find('function bindServiceTicketGlobalActions') + 900]
    assert 'stopPropagation' not in bind
    assert "addEventListener('click'" in bind


def test_pj_pick_path_then_handover():
    html = _html()
    js = _js_bundle()
    assert 'repairLocPickModal' in html
    assert 'function openRepairLocPickModal' in js
    assert 'function submitRepairLocPickup' in js
    assert 'svc-repair-loc' not in html
    reg_block = js[js.find('async function submitServiceTicket'):js.find('async function submitServiceTicket') + 4500]
    assert 'repairLoc: null' in reg_block
    loc_block = js[js.find('function submitRepairLocPickup'):js.find('function actionServiceTicket')]
    assert 'openHandoverSignatureModal(id' in loc_block
    pickup_block = js[js.find('function actionServiceTicket'):js.find('function actionServiceTicket') + 3400]
    assert 'openRepairLocPickModal(id)' in pickup_block
    assert 'openHandoverSignatureModal(id, action)' in pickup_block
    assert 'executeWorkshopPickup' not in js


def test_pickup_via_handover_signature():
    js = _js_bundle()
    sig_block = js[js.find('function submitHandoverSignature'):js.find('function openAnalysisModal')]
    assert "action === 'pickup'" in sig_block
    assert 'signaturePickupGiver' in sig_block
    assert 'signaturePickupReceiver' in sig_block
    assert 'renderServiceTickets(true)' in sig_block
    handover_block = js[js.find('function openHandoverSignatureModal'):js.find('function submitHandoverSignature')]
    assert 'handoverOnsiteOnly' in handover_block
    assert 'handoverSigStep = 1' in handover_block


def test_technician_creator_is_pj():
    js = _js_bundle()
    assert 'function resolveServiceTicketAssignedTs' in js
    assert 'function applyServiceModalTsPicker' in js
    assert 'registeredById' in js
    assert 'registeredByUser' in js
    match = js[js.find('function ticketPjMatchesCurrentUser'):js.find('function syncTicketPjFields')]
    assert 'registeredById' in match
    assert 'registeredByUser' in match


def test_field_technician_instant_active():
    js = _js_bundle()
    assert "roleVal === 'ts'" in js
    assert 'langsung bisa login' in js
    block = js[js.find('async function submitTech'):js.find('async function submitTech') + 3500]
    assert "roleVal === 'ts'" in block
    assert "'active'" in block
    assert 'pending_approval' in block


def test_field_tech_creator_is_pj_only():
    js = _js_bundle()
    match = js[js.find('function ticketPjMatchesCurrentUser'):js.find('function formatServiceTicketActionFallback')]
    assert 'isServiceFieldUser(currentUser)' in match
    assert 'registeredById' in match
    relink = js[js.find('function relinkServiceTicketsForUser'):js.find('function healAllServiceTicketPj')]
    assert 'creatorFieldPj' in relink
    assert 'Mulai Pekerjaan' in js
    assert 'Saya kerjakan sendiri' in _html()
    assert 'function healServiceTicketsForCurrentUser' in js
    assert 'function relinkServiceTicketsForUser' in js
    assert 'function healAllServiceTicketPj' in js
    assert 'relinkServiceTicketsForUser(data)' in js
    assert 'relinkServiceTicketsForUser(targetUser)' in js
    assert 'relinkServiceTicketsForUser(u, target.serviceTickets)' in js
    assert 'Tiket diselaraskan' in js
    assert 'function formatServiceTicketActionFallback' in js
    assert 'filter-service-pj' in (ROOT / 'index.html').read_text(encoding='utf-8')
    assert 'Tiket Saya (PJ)' in (ROOT / 'index.html').read_text(encoding='utf-8')


def test_smart_fill_autocomplete():
    js = _js_bundle()
    assert 'function smartFillSphLineByDesc' in js
    assert 'function searchCustomersPartial' in js
    assert 'function searchCustomerUnitsPartial' in js
    assert 'function searchCustomersForPick' in js
    assert 'function searchCustomerUnitsForPick' in js
    assert 'svc-pick-customer-input' in js
    assert 'pickSvcMasterCustomer' in js
    assert 'SN:' in js
    assert "formatSvcUnitPickLabel(u, custId)" in js or 'function formatSvcUnitPickLabel' in js
    assert 'tms-suggest-dropdown' in js
    assert 'pickSphSuggestActive' in js
    assert 'onSvcCustNameInput' in js


def test_service_photo_camera_capture():
    js = _js_bundle()
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert 'function triggerServicePhotoPick' in js
    assert 'function onServicePhotoPicked' in js
    assert "setAttribute('capture', 'environment')" in js
    assert 'capture="environment"' in html
    assert "triggerServicePhotoPick('before','camera')" in html
    assert "triggerServicePhotoPick('after','camera')" in html


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


def test_observability_module():
    assert (ROOT / 'js/tms-observability.js').exists()
    js = _js_bundle()
    assert 'tmsReportError' in js
    assert 'tmsLog' in js


def test_idle_logout_uses_handle_logout():
    rt = (ROOT / 'js/tms-runtime.js').read_text(encoding='utf-8')
    assert 'handleLogout' in rt


def test_restore_database_owner_only():
    js = _js_bundle()
    assert "tmsRequirePerm('RESTORE_DB', 'Impor database')" in js


def test_backup_sanitizes_passwords():
    js = _js_bundle()
    assert 'cloneDbForCloudUpload(db)' in js
    idx = js.find('function backupDatabase')
    block = js[idx:idx + 400]
    assert 'cloneDbForCloudUpload' in block


def test_delete_asset_role_guard():
    js = _js_bundle()
    assert "tmsRequirePerm('DELETE_ASSET', 'Menghapus aset inventori')" in js


def test_delete_sparepart_role_guard():
    js = _js_bundle()
    assert "tmsRequirePerm('DELETE_SPAREPART'" in js


def test_toggle_user_lock_role_guard():
    js = _js_bundle()
    assert "tmsRequirePerm('LOCK_PERSONNEL', 'Mengunci/membuka akun personel')" in js


def test_sync_fetch_retry():
    js = _js_bundle()
    assert 'tmsRetryAsync(fetchCloud' in js or 'tmsRetryAsync(fetchCloud' in js.replace('\n', ' ')
    assert 'fetchCloud' in js


def test_tms_esc_tool_fields():
    sec = (ROOT / 'js/tms-security.js').read_text(encoding='utf-8')
    assert 'tmsEscToolFields' in sec


def test_tms_auth_module():
    assert (ROOT / 'js/tms-auth.js').exists()
    js = _js_bundle()
    assert 'TMS_PERM' in js
    assert 'tmsRequirePerm' in js


def test_tms_integrity_module():
    assert (ROOT / 'js/tms-integrity.js').exists()
    js = _js_bundle()
    assert 'tmsRunIntegrityAndLog' in js
    assert 'runDbIntegrityCheck' in js


def test_submit_tech_perm_guard():
    js = _js_bundle()
    assert "tmsRequirePerm('MANAGE_PERSONNEL', 'Menyimpan data personel')" in js


def test_edit_personnel_no_hash_in_password_field():
    js = _js_bundle()
    assert 'isPasswordHashed(u.pass)' in js


def test_inventory_render_uses_esc_tool_fields():
    js = _js_bundle()
    assert 'const tf = tmsEscToolFields(t)' in js


def test_customer_manage_perm_guard():
    js = _js_bundle()
    assert "tmsRequirePerm('MANAGE_CUSTOMER'" in js


def test_spv_assets_batch_render():
    js = _js_bundle()
    assert 'sc.innerHTML = filtered.map(t =>' in js


def test_sync_retry_smart():
    rt = (ROOT / 'js/tms-runtime.js').read_text(encoding='utf-8')
    assert 'tmsIsRetryableError' in rt


def test_session_restore_validates_user():
    html = _html()
    assert 'syncCurrentUserFromDb();' in html
    assert 'if (!currentUser) return;' in html


def test_health_audit_cycles():
    data = json.loads((ROOT / 'health.json').read_text(encoding='utf-8'))
    assert data.get('auditCycles', 0) >= 3


def test_service_pj_sync_functions():
    js = _js_bundle()
    for fn in ('syncTicketPjFields', 'ensureServiceTicketPjReady', 'isActiveFieldTsUser'):
        assert f'function {fn}' in js


def test_service_pj_username_priority():
    js = _js_bundle()
    block = js[js.find('function resolveTicketAssignedTsId'):js.find('function resolveTicketAssignedTsId') + 1200]
    assert 'assignedTsUser' in block
    assert block.find('assignedTsUser') < block.find('getU(s.assignedTsId)')


def test_pickup_shows_login_username_hint():
    js = _js_bundle()
    assert 'Anda login sebagai' in js or 'assignedTsUser' in js


def test_service_pj_strict_designated_technician():
    js = _js_bundle()
    match = js[js.find('function ticketPjMatchesCurrentUser'):js.find('function syncTicketPjFields')]
    assert 'resolveTicketAssignedTsId(s)' in match
    assert 'assignedTsUser' in match
    assert 'Number(resolved) === uid' in match
    assert 'handoverOnsiteOnly' in js
    resolve = js[js.find('function resolveTicketAssignedTsId'):js.find('function syncCurrentUserFromDb')]
    assert 'userConflict' in resolve
    assert 'byName.length === 1' in resolve
    assert 'canActAsServicePj(assignedTs)' in js
    assert 'creatorFieldPj' in js


def test_onsite_repair_pj_guard():
    js = _js_bundle()
    idx = js.find('function openOnsiteRepair')
    block = js[idx:idx + 500]
    assert 'isAssignedServiceTs' in block
