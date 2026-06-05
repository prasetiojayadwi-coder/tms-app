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

Path('config.js').write_text(content, encoding='utf-8')
print('\n[OK] config.js berhasil disimpan!')
print('     Jalankan Mulai_Server.bat lalu login.')
print('     Badge "Cloud Live" (hijau) = berhasil.')
