import io

path = 'index.html'
with io.open(path, 'r', encoding='utf-8') as f:
    html = f.read()

assert (html.count('\n') + 1) > 15000, "file tampak terpotong"

# 1) CSS: kecilkan padding & sembunyikan spinner pada input number agar angka (QTY/HARGA) terlihat
css_old = """        .input-field {
            @apply w-full bg-white dark:bg-[#18181b] text-gray-900 dark:text-white border border-gray-300 dark:border-[#3f3f46] rounded-xl px-4 py-3.5 text-[0.875rem] font-semibold outline-none transition-all duration-300 shadow-sm dark:shadow-[inset_0_2px_4px_rgba(0,0,0,0.5)];
            appearance: none; -webkit-appearance: none;
        }"""
css_new = """        .input-field {
            @apply w-full bg-white dark:bg-[#18181b] text-gray-900 dark:text-white border border-gray-300 dark:border-[#3f3f46] rounded-xl px-4 py-3.5 text-[0.875rem] font-semibold outline-none transition-all duration-300 shadow-sm dark:shadow-[inset_0_2px_4px_rgba(0,0,0,0.5)];
            appearance: none; -webkit-appearance: none;
        }
        .input-field[type="number"] {
            padding-left: 0.5rem; padding-right: 0.5rem;
            -moz-appearance: textfield;
        }
        .input-field[type="number"]::-webkit-outer-spin-button,
        .input-field[type="number"]::-webkit-inner-spin-button {
            -webkit-appearance: none; margin: 0;
        }"""
c = html.count(css_old)
assert c == 1, f"anchor CSS ditemukan {c}x"
html = html.replace(css_old, css_new)

# 2) Lebarkan kolom Qty (sm:1 -> sm:2) dan rata-tengah angkanya
qty_old = """                        <div class="col-span-3 sm:col-span-1">
                            <label class="text-[8px] font-black uppercase text-gray-400">Qty</label>
                            <input type="number" min="1" class="input-field text-[11px] py-2" value="${line.qty || 1}" oninput="updateSphLineField('${containerId}', ${idx}, 'qty', this.value)">
                        </div>"""
qty_new = """                        <div class="col-span-3 sm:col-span-2">
                            <label class="text-[8px] font-black uppercase text-gray-400">Qty</label>
                            <input type="number" min="1" class="input-field text-[11px] py-2 text-center" value="${line.qty || 1}" oninput="updateSphLineField('${containerId}', ${idx}, 'qty', this.value)">
                        </div>"""
c = html.count(qty_old)
assert c == 1, f"anchor Qty ditemukan {c}x"
html = html.replace(qty_old, qty_new)

with io.open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(html)

print('OK: CSS number-input + lebar kolom Qty diperbaiki. lines:', html.count('\n') + 1)
