#!/usr/bin/env python3
"""Quick live deployment verification."""
import json
import re
import urllib.request

BASE = 'https://prasetiojayadwi-coder.github.io/tms-app/'


def fetch(path):
    return urllib.request.urlopen(BASE + path, timeout=90).read().decode('utf-8', 'replace')


def main():
    rel = fetch('release.js')
    sw = fetch('sw.js')
    html = fetch('index.html')
    deploy = fetch('config.deploy.js')
    ver = re.search(r"version:\s*'([^']+)'", rel)
    bld = re.search(r'build:\s*(\d+)', rel)
    cache = re.search(r'tms-cache-v(\d+)', sw)
    report = {
        'version': ver.group(1) if ver else None,
        'build': int(bld.group(1)) if bld else None,
        'cache': int(cache.group(1)) if cache else None,
        'sw_match': (bld and cache and bld.group(1) == cache.group(1)),
        'buildExcelBlob': 'function buildExcelBlob' in html,
        'template_xlsx': 'TMS_Template_Spareparts.xlsx' in html,
        'render_opt': 'ticketById' in html,
        'id_fix': '_lastAllocatedId' in html,
        'supabase_config': 'supabase.co' in deploy,
    }
    print(json.dumps(report, indent=2))
    ok = all([
        report['version'] == '6.7.6',
        report['sw_match'],
        report['buildExcelBlob'],
        report['template_xlsx'],
        report['supabase_config'],
    ])
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
