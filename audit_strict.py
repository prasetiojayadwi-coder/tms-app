#!/usr/bin/env python3
"""Strict system audit — performance benchmarks + integrity checks."""
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8765
BASE = f'http://localhost:{PORT}/index.html'
OUT = ROOT / 'docs' / 'audit-strict-results.json'

BENCH = '''
() => {
    const results = {};
    const bench = (name, fn) => {
        const t0 = performance.now();
        const out = fn();
        results[name] = { ms: Math.round((performance.now() - t0) * 100) / 100, out };
    };
    loadDB();
    const nSp = 500, nSvc = 200, nSph = 100;
    const now = new Date().toISOString();
    for (let i = 0; i < nSp; i++) {
        db.spareparts.push({ id: 900000 + i, artNo: 'BENCH-SP-' + i, description: 'Bench', price: 1000, group: 'Avitum', status: 'active', notes: '', updatedAt: now });
    }
    for (let i = 0; i < nSvc; i++) {
        db.serviceTickets.push({ id: 800000 + i, noService: 'BENCH-SVC-' + i, customerId: 1, status: 'received_tsf', repairLoc: 'tsf', history: [] });
    }
    for (let i = 0; i < nSph; i++) {
        db.sphDocuments.push({ id: 700000 + i, sphNo: 'SPH-BENCH-' + i, customerId: 1, lines: [], status: 'issued', repairPath: 'tsf', serviceTicketIds: [], createdAt: now, updatedAt: now, history: [] });
    }

    bench('allocateUniqueId_x100', () => {
        const ids = new Set();
        for (let i = 0; i < 100; i++) ids.add(allocateUniqueId());
        return { unique: ids.size === 100 };
    });
    bench('searchSparepartsPartial', () => searchSparepartsPartial('BENCH').length);
    bench('sanitizeDatabase', () => { sanitizeDatabase(db); return true; });
    bench('JSON.stringify_db', () => JSON.stringify(db).length);
    bench('renderSparepartMaster', () => { renderSparepartMaster(); return document.getElementById('spareparts-container')?.children.length; });
    bench('renderSphLog', () => { renderSphLog(); return document.getElementById('sph-log-container')?.children.length; });
    bench('getEligibleSphTickets', () => getEligibleSphTickets().length);
    bench('hasEligibleCombinedSph', () => hasEligibleCombinedSph());

    const jsonLen = JSON.stringify(db).length;
    results._meta = {
        spareparts: db.spareparts.length,
        serviceTickets: db.serviceTickets.length,
        sphDocuments: db.sphDocuments.length,
        jsonBytes: jsonLen,
        jsonMB: Math.round(jsonLen / 1024 / 1024 * 100) / 100,
        indexHtmlNote: 'monolith ~974KB parse on first load'
    };
    return results;
}
'''

THRESHOLDS = {
    'allocateUniqueId_x100': 500,
    'searchSparepartsPartial': 50,
    'sanitizeDatabase': 200,
    'JSON.stringify_db': 300,
    'renderSparepartMaster': 150,
    'renderSphLog': 150,
    'getEligibleSphTickets': 30,
    'hasEligibleCombinedSph': 30,
}


async def main():
    from playwright.async_api import async_playwright

    server = subprocess.Popen(
        [sys.executable, '-m', 'http.server', str(PORT), '--directory', str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    report = {'benchmarks': {}, 'bottlenecks': [], 'bugs': [], 'ok': []}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            t0 = time.perf_counter()
            await page.goto(BASE, wait_until='load', timeout=120000)
            load_ms = round((time.perf_counter() - t0) * 1000)
            report['pageLoadMs'] = load_ms

            await page.wait_for_function('() => typeof loadDB === "function"', timeout=120000)
            parse_ms = round((time.perf_counter() - t0) * 1000)
            report['jsReadyMs'] = parse_ms

            data = await page.evaluate(BENCH)
            report['benchmarks'] = data
            report['meta'] = data.pop('_meta', {})

            for key, limit in THRESHOLDS.items():
                ms = data.get(key, {}).get('ms', 9999)
                if ms > limit:
                    report['bottlenecks'].append(f'{key}: {ms}ms > threshold {limit}ms')
                else:
                    report['ok'].append(f'{key}: {ms}ms OK')

            if data.get('allocateUniqueId_x100', {}).get('out', {}).get('unique') is False:
                report['bugs'].append('allocateUniqueId produced duplicates in rapid x100 call')

            if report['meta'].get('jsonMB', 0) > 4:
                report['bottlenecks'].append(f"DB JSON {report['meta']['jsonMB']}MB — mendekati localStorage limit 5MB")

            if load_ms > 8000:
                report['bottlenecks'].append(f'Page load {load_ms}ms — index.html monolith heavy')

            # Live version
            live = await browser.new_page()
            await live.goto('https://prasetiojayadwi-coder.github.io/tms-app/index.html', wait_until='load', timeout=120000)
            ver = await live.evaluate('() => window.TMS_RELEASE?.version')
            report['liveVersion'] = ver
            await browser.close()
    finally:
        server.terminate()

    OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('=== STRICT AUDIT ===')
    print(f"Page load: {report.get('pageLoadMs')}ms | JS ready: {report.get('jsReadyMs')}ms")
    print(f"Live: {report.get('liveVersion')}")
    print(f"DB bench: {report.get('meta')}")
    print('\nBenchmarks:')
    for k, v in report.get('benchmarks', {}).items():
        print(f"  {k}: {v.get('ms')}ms")
    if report['bugs']:
        print('\nBUGS:', *report['bugs'], sep='\n  ')
    if report['bottlenecks']:
        print('\nBOTTLENECKS:', *report['bottlenecks'], sep='\n  ')
    else:
        print('\nNo benchmark threshold violations')
    print(f'\nOK ({len(report["ok"])}):', ', '.join(report['ok'][:5]), '...')
    print(f'\nWritten: {OUT}')
    return 1 if report['bugs'] else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
