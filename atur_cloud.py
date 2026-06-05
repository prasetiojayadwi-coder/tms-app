"""Simpan Anon Key Supabase ke config.js — cukup paste sekali."""
from pathlib import Path

URL = 'https://mezuatmcjqjxfsvepizv.supabase.co'

print()
key = input('Paste Anon Key di sini lalu tekan Enter:\n> ').strip().strip("'\"")

if not key:
    print('\n[ERROR] Key kosong. Ulangi dengan paste key dari Supabase.')
    raise SystemExit(1)

if not key.startswith('eyJ'):
    print('\n[PERINGATAN] Key biasanya diawali "eyJ". Pastikan Anda copy "anon public", bukan service_role.')
    lanjut = input('Lanjutkan simpan? (y/n): ').strip().lower()
    if lanjut != 'y':
        raise SystemExit(1)

content = f"""/**
 * TMS Cloud Configuration — dibuat otomatis oleh Atur_Cloud.bat
 */
window.TMS_CONFIG = {{
    supabase: {{
        url: '{URL}',
        anonKey: '{key}'
    }}
}};
"""

deploy_content = f"""/**
 * TMS Cloud — konfigurasi deploy online (GitHub Pages).
 */
window.TMS_CONFIG = {{
    supabase: {{
        url: '{URL}',
        anonKey: '{key}'
    }}
}};
"""

Path('config.js').write_text(content, encoding='utf-8')
Path('config.deploy.js').write_text(deploy_content, encoding='utf-8')
print('\n[OK] config.js + config.deploy.js berhasil disimpan!')
print('     Lokal  : jalankan Mulai_Server.bat')
print('     Online : push ke GitHub untuk update config.deploy.js')
print('     Badge "Cloud Live" (hijau) = cloud aktif.')
