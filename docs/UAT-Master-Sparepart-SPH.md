# UAT — Master Sparepart & SPH Module

| Field | Value |
|-------|-------|
| **Aplikasi** | TMS — Tool Management System |
| **Modul** | Master Sparepart, SPH Builder, SPH Log, Service & Repair |
| **Versi UAT** | v6.7.2 |
| **PRD Ref** | [PRD-Master-Sparepart-SPH.md](./PRD-Master-Sparepart-SPH.md) v1.4.1 |
| **Environment** | ☐ Staging · ☐ Production (GitHub Pages) |
| **URL** | https://prasetiojayadwi-coder.github.io/tms-app/ |
| **Tanggal UAT** | _______________ |
| **Tester** | _______________ |

### Legenda

| Simbol | Arti |
|--------|------|
| **P1** | Critical — wajib lulus |
| **P2** | High |
| **P3** | Medium |
| ☐ Pass · ☐ Fail · ☐ N/A | Hasil tes |
| **AC-xx** | Acceptance Criteria PRD |
| **T-xx** | Test Scenario PRD |

### Akun UAT (demo)

| Role | User | Password |
|------|------|----------|
| Owner | `owner` | `123` |
| SPV | `spv1` | `123` |
| TSF | `tsf1` | `123` |
| TS (field) | `ts1` | `123` |

---

## A. Sparepart Master

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-001 | AC-01 | P1 | SPV / TSF | ☐ Pass ☐ Fail |
| UAT-002 | AC-01 | P1 | SPV | ☐ Pass ☐ Fail |
| UAT-003 | AC-02 | P1 | SPV | ☐ Pass ☐ Fail |
| UAT-004 | AC-03 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-005 | AC-06 | P2 | SPV | ☐ Pass ☐ Fail |
| UAT-006 | AC-05, T-26 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-007 | AC-01 | P2 | SPV | ☐ Pass ☐ Fail |
| UAT-008 | AC-04 | P1 | TSF | ☐ Pass ☐ Fail |

### UAT-001 — Tambah sparepart baru

**Precondition:** Login sebagai SPV atau TSF. Menu **Sparepart Master** tersedia.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Buka Sparepart Master → **Add Sparepart** | Modal form terbuka |
| 2 | Isi Art Number `UAT-ART-001`, Description, Price `1500000`, Group Avitum, Status Active | Field terisi |
| 3 | Klik Save | Toast sukses; baris muncul di tabel |
| 4 | Cek stats Total / Active | Counter bertambah |

**Catatan:** _______________

---

### UAT-002 — Art Number duplikat ditolak

**Precondition:** `UAT-ART-001` sudah ada.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Add Sparepart dengan Art Number `UAT-ART-001` (case berbeda boleh dicoba) | Error validasi muncul |
| 2 | Tombol Save | Disabled / submit ditolak |

---

### UAT-003 — Batch import Excel

**Precondition:** File Excel dengan kolom: Art Number, Description, Price, Group, Status, Notes. Satu baris duplikat `UAT-ART-001`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Sparepart Master → Batch Import → upload file | Preview / proses import |
| 2 | Konfirmasi import | Baris baru masuk; duplikat di-skip |
| 3 | Lihat ringkasan | Error/skip count ditampilkan untuk baris duplikat |

---

### UAT-004 — Export CSV

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Klik Export CSV | File `TMS_Spareparts_Export.csv` terunduh |
| 2 | Buka file | Header + data sparepart lengkap |

---

### UAT-005 — Filter group

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Klik filter **Avitum** | Hanya sparepart group Avitum |
| 2 | Klik filter **Hospital Care** | Hanya group Hospital Care |
| 3 | Klik **All** | Semua group tampil |

---

### UAT-006 — Smart Fill: obsolete vs discontinued

**Precondition:** Sparepart `UAT-OBS-001` status **Obsolete**; `UAT-DISC-001` status **Discontinued** ada di master.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Buka Damage Quotation / SPH line → ketik `UAT-OBS-001` | Toast blocked; line tidak terisi |
| 2 | Ketik `UAT-DISC-001` | Warning toast; Description + Price terisi |

---

### UAT-007 — Edit & hapus sparepart (CRUD lengkap)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Edit sparepart `UAT-ART-001` → ubah Price | Save sukses; harga terupdate di tabel |
| 2 | Delete sparepart uji (bukan yang dipakai SPH aktif) | Konfirmasi → baris hilang; stats berkurang |

---

### UAT-008 — Smart Fill exact match (AC-04)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH line → ketik Art Number active yang ada di master | Description + unitPrice terisi otomatis |
| 2 | Ketik Art Number yang **tidak ada** | Tidak terisi / tidak ditemukan |

---

## B. SPH Builder — Single & Combined

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-010 | AC-07, T-04 | P1 | TSF | ☐ Pass ☐ Fail |
| UAT-011 | AC-09, AC-11 | P1 | TSF | ☐ Pass ☐ Fail |
| UAT-012 | AC-10, AC-15 | P1 | TSF | ☐ Pass ☐ Fail |
| UAT-013 | AC-12 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-014 | AC-08, T-05, T-19 | P1 | TSF | ☐ Pass ☐ Fail |
| UAT-015 | AC-07 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-016 | AC-08 | P2 | SPV | ☐ Pass ☐ Fail |

### UAT-010 — Damage Quotation (TSF single SPH)

**Precondition:** Service ticket TSF path, status **Diterima TSF** (`received_tsf`). Sparepart master terisi.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login TSF → Customer Service → tiket → **Damage Quotation** | Modal quotation terbuka |
| 2 | Pilih decision **Repairable** | Form SPH lines tampil |
| 3 | Add line → Smart Fill Art Number dari master | Description + harga terisi |
| 4 | Set qty = 2 | Subtotal = 2 × unit price |
| 5 | Isi Labor (mis. 500000) | Total terhitung otomatis |
| 6 | Cek **SPH Preview — Customer View** | Kolom: Art Number \| Description \| Harga saja |
| 7 | Submit | Toast SPH Issued; tiket status **Penawaran Dikirim** (`quoted`) |

---

### UAT-011 — Preview & qty subtotal

**Precondition:** Lanjutan UAT-010 atau quotation baru.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Ubah qty salah satu line | Subtotal & total berubah real-time |
| 2 | Preview customer table | Tidak menampilkan qty/subtotal ke customer |

---

### UAT-012 — Nomor SPH & quote auto

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Setelah SPH terbit → buka **SPH Log** | SPH No. format `SPH-YYMM-####` |
| 2 | Buka Service Detail tiket | `quoteDetails` terisi otomatis; `quotePrice` = total |

---

### UAT-013 — Upload dokumen SPH

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Saat buat SPH → attach file PDF/gambar | Upload berhasil |
| 2 | Service Detail → cek dokumen SPH | Link dokumen tersedia |

---

### UAT-014 — Combined SPH (≥2 unit, same customer)

**Precondition:** ≥2 tiket status `received_tsf`, **customer sama**, belum punya SPH.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Customer Service → tombol **Combined SPH** visible | Tombol muncul |
| 2 | Pilih ≥2 tiket (checkbox) → isi lines + labor | Form combined terbuka |
| 3 | Issue Combined SPH | 1 SPH No.; semua tiket → `quoted` |
| 4 | Cek `quotePrice` tiket 1 vs tiket 2 | Labor hanya di tiket pertama; tiket 2 = sparepart subtotal saja |

---

### UAT-015 — Validasi: SPH tanpa line item ditolak

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Damage Quotation → hapus semua line / kosongkan Art No. | — |
| 2 | Submit | Toast validation error; SPH tidak terbit |

---

### UAT-016 — Combined SPH button visibility

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Hanya 1 tiket eligible `received_tsf` | Tombol **Combined SPH** hidden |
| 2 | ≥2 tiket same customer eligible | Tombol **Combined SPH** visible |

---

## C. SPH Log & PO Sync

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-020 | AC-17, T-15 | P1 | SPV | ☐ Pass ☐ Fail |
| UAT-021 | AC-18, T-16 | P1 | TS / SPV | ☐ Pass ☐ Fail |
| UAT-022 | AC-19, T-06, T-14 | P1 | SPV | ☐ Pass ☐ Fail |
| UAT-023 | AC-20 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-024 | AC-22 | P2 | SPV | ☐ Pass ☐ Fail |
| UAT-025 | AC-33, T-25 | P3 | SPV | ☐ Pass ☐ Fail |
| UAT-026 | — | P2 | SPV | ☐ Pass ☐ Fail |
| UAT-027 | — | P2 | TSF | ☐ Pass ☐ Fail |

### UAT-020 — SPH muncul di SPH Log (Pending PO)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Buka menu **SPH Log** | Tabel SPH tampil |
| 2 | Cari SPH dari UAT-010 / UAT-014 | Row ada; status **Pending PO** (amber) |
| 3 | Filter **Pending PO** | Hanya SPH status `issued` |
| 4 | Stats bar | Counter Pending PO sesuai |

---

### UAT-021 — Input PO → SPH PO Received

**Precondition:** Tiket status `quoted` dengan `sphDocumentId`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login TS/SPV → tiket → **Input PO** | Modal PO; total penawaran ditampilkan |
| 2 | Isi PO No., Amount, Date; optional upload dokumen | Form valid |
| 3 | Submit | Toast PO Synced; tiket → **Perbaikan (PO)** (`po_issued`) |
| 4 | SPH Log | SPH status **PO Received**; PO No. tampil |

---

### UAT-022 — Combined SPH: PO di 1 tiket update semua

**Precondition:** Combined SPH dengan 3 tiket (UAT-014).

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Input PO hanya pada **1** dari 3 tiket | PO sync berhasil |
| 2 | Cek 2 tiket lainnya | Semua → `po_issued`; PO No. sama |
| 3 | SPH Log | 1 SPH → `po_received` |

---

### UAT-023 — Filter SPH Log

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Filter **PO Received** | Hanya SPH dengan PO |
| 2 | Filter **All** | Semua SPH |
| 3 | Search by PO number / customer | Hasil terfilter benar |

---

### UAT-024 — Badge path On-Site vs TSF

**Precondition:** Minimal 1 SPH On-Site dan 1 SPH TSF.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → kolom Path | Badge **On-Site** vs **TSF** benar |

---

### UAT-025 — Legacy PO (tiket tanpa SPH document)

**Precondition:** Tiket lama `quoted` tanpa `sphDocumentId` *(jika ada di data UAT)*.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Input PO pada tiket tersebut | Tiket → `po_issued` |
| 2 | SPH Log | Tidak ada perubahan pada SPH lain |

---

### UAT-026 — Upload dokumen PO

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Input PO → attach file PDF/gambar | Upload berhasil |
| 2 | Service Detail / SPH setelah PO | Dokumen PO tersimpan |

---

### UAT-027 — `showSphDetail` summary alert

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → klik **Detail** pada 1 SPH | Alert summary: SPH No., customer, path, status, total, PO |
| 2 | SPH dengan 1 tiket | Service Detail tiket terbuka otomatis |

---

## D. Jalur TSF Workshop (Full Flow)

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-030 | AC-29, T-21 | P1 | TS + TSF | ☐ Pass ☐ Fail |
| UAT-031 | AC-13, T-07 | P1 | TSF + TS | ☐ Pass ☐ Fail |
| UAT-032 | AC-25, T-17 | P1 | TSF + TS | ☐ Pass ☐ Fail |
| UAT-033 | AC-27, T-18 | P1 | TSF + TS | ☐ Pass ☐ Fail |
| UAT-034 | AC-30 | P1 | TS + TSF | ☐ Pass ☐ Fail |
| UAT-035 | T-20 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-036 | AC-14 | P1 | TS / SPV | ☐ Pass ☐ Fail |
| UAT-037 | AC-26 | P1 | TSF + TS | ☐ Pass ☐ Fail |
| UAT-038 | AC-28 | P1 | TSF + TS | ☐ Pass ☐ Fail |

### UAT-030 — TSF timeline: Pickup → Analisa → Terima TSF

**Precondition:** Tiket baru `repairLoc = TSF Workshop`, status Terdaftar.

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Pickup unit + TTD customer & teknisi | TS | Status **Dipegang Teknisi** |
| 2 | **Analisa Awal** + isi analisa + TTD kirim TSF | TS | Status **Kirim ke TSF** (`initial_analyzed`) |
| 3 | **Terima di TSF** + TTD | TSF | Status **Diterima TSF** (`received_tsf`) |

---

### UAT-031 — TSF repair lengkap (SPH → PO → Repair → BAST)

**Precondition:** Tiket TSF sudah `po_issued` (UAT-021).

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | **Selesai Perbaikan** — work notes + foto | TSF | Modal repair |
| 2 | Centang sparepart yang diganti | TSF | Checklist dari SPH lines |
| 3 | Submit + TTD kirim ke lapangan | TSF | Status **Kembali ke Lapangan** (`repaired`) |
| 4 | **Terima di Lapangan** + TTD | TS | Status **Siap Penyerahan** (`received_field`) |
| 5 | **Serahkan & BAST** + TTD customer | TS | Status **Selesai** (`completed`) |
| 6 | Service Detail | — | Tabel replaced spareparts tampil |

---

### UAT-032 — TSF Quick Repair (tanpa SPH/PO)

**Precondition:** Tiket `received_tsf`, **belum** ada SPH.

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Klik **Quick Repair** (bukan Damage Quotation) | TSF | Modal TSF Quick Repair + hint hijau |
| 2 | Isi work notes → submit + TTD | TSF | Tidak ada record baru di SPH Log |
| 3 | Lanjut terima lapangan + BAST | TS | Alur sampai `completed` |
| 4 | History tiket | — | Entri "TSF Quick Repair (tanpa SPH/PO)" |

---

### UAT-033 — Un-Repair (unit tidak bisa diperbaiki)

**Precondition:** Tiket `received_tsf`, belum SPH.

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Damage Quotation → **Not Repairable — Return Unit** | TSF | Form harga/SPH tersembunyi |
| 2 | Isi hasil inspeksi → submit + TTD | TSF | Tidak ada SPH; `toolStatus` unrepaired |
| 3 | Terima lapangan + BAST | TS | Pernyataan BAST menyebut **unrepaired** |

---

### UAT-034 — TTD tersimpan di Tanda Terima

**Precondition:** Tiket TSF path sudah melewati pickup, TSF, dan completed.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Klik **Tanda Terima** pada tiket | Modal receipt terbuka |
| 2 | Tab Pickup | TTD customer & teknisi tampil (jika sudah ditandatangani) |
| 3 | Tab TSF / Field / BAST | Tab aktif sesuai progres; TTD embedded |
| 4 | Print (Ctrl+P) | Layout cetak bersih (`print-svc-receipt`) |

---

### UAT-035 — Quick Repair tidak tersedia setelah SPH

**Precondition:** Tiket `received_tsf` sudah punya SPH (`quoted` atau lebih).

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Cek tombol di tiket `received_tsf` yang sudah SPH | **Quick Repair** tidak muncul / tidak applicable |
| 2 | Damage Quotation tidak bisa buat SPH kedua | SPH kedua ditolak |

---

### UAT-036 — Service Detail: SPH table + replaced parts (AC-14)

**Precondition:** Tiket `completed` setelah repair dengan sparepart dikonfirmasi.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Customer Service → **Track Status** / Service Detail | Modal/detail terbuka |
| 2 | Bagian penawaran | Tabel SPH: Art Number \| Description \| Harga |
| 3 | Bagian replaced parts | Tabel sparepart yang dikonfirmasi terpasang tampil |

---

### UAT-037 — TSF Quick Repair: rantai status (AC-26)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Setelah Quick Repair + TTD kirim | Status `repaired` (bukan `quoted`/`po_issued`) |
| 2 | TS terima di lapangan | Status `received_field` |
| 3 | BAST | Status `completed` |

---

### UAT-038 — Un-Repair: teks BAST unrepaired (AC-28)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Selesaikan alur Un-Repair sampai BAST | — |
| 2 | Baca pernyataan di modal BAST | Teks menyebut unit **tidak berhasil diperbaiki / unrepaired** |
| 3 | Tanda Terima tab Completed | Pernyataan unrepaired (bukan teks repaired) |

---

## E. Jalur On-Site

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-040 | AC-21, T-08, T-11 | P1 | SPV + TS | ☐ Pass ☐ Fail |
| UAT-041 | AC-23, T-09, T-13 | P1 | TS | ☐ Pass ☐ Fail |
| UAT-042 | AC-24, T-12 | P1 | TS | ☐ Pass ☐ Fail |
| UAT-043 | BR-14 | P2 | SPV | ☐ Pass ☐ Fail |
| UAT-044 | AC-32, T-24 | P2 | TS | ☐ Pass ☐ Fail |

### UAT-040 — Registrasi On-Site + On-Site SPH

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Registrasi service → Repair Location = **On-Site** | SPV | Tiket terbentuk |
| 2 | Pickup unit | TS (assigned) | Status `picked_up` |
| 3 | **On-Site SPH** → buat penawaran | TS | SPH Log: path **On-Site**; tiket `quoted` |
| 4 | Cek status tiket | — | Tidak pernah masuk `initial_analyzed` / `received_tsf` |

---

### UAT-041 — On-Site Quick Repair (tanpa SPH)

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Tiket onsite `picked_up` → **Quick Repair** | TS | Modal repair |
| 2 | Submit + BAST langsung | TS | Langsung `completed`; tidak ada SPH Log entry |
| 3 | SPH Log | — | Tidak bertambah untuk tiket ini |

---

### UAT-042 — On-Site SPH → PO → Repair & BAST

| Step | Aksi | Role | Expected Result |
|------|------|------|-----------------|
| 1 | Setelah On-Site SPH → Input PO | TS/SPV | `po_issued`; SPH `po_received` |
| 2 | **Repair & BAST** — konfirmasi sparepart | TS | `completed` |
| 3 | Service Detail | — | SPH table + replaced parts |

---

### UAT-043 — `repairLoc` On-Site: tidak ada status TSF

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Tiket On-Site dari registrasi sampai SPH | Tidak pernah muncul `initial_analyzed`, `received_tsf`, `repaired` |
| 2 | Cek Tanda Terima | Tab TSF & Field **disabled** |

---

### UAT-044 — Tanda Terima tab TSF (T-24)

**Precondition:** Tiket TSF path status ≥ `received_tsf`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Tanda Terima → tab **TSF Workshop** | Aktif; doc `STW/{noService}` |
| 2 | Tiket On-Site | Tab TSF disabled |

---

## F. Bulk BAST & Notifikasi

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-050 | AC-31, T-22 | P1 | TS | ☐ Pass ☐ Fail |
| UAT-051 | T-23 | P2 | TS | ☐ Pass ☐ Fail |
| UAT-052 | AC-34 | P2 | TS / SPV | ☐ Pass ☐ Fail |
| UAT-053 | AC-31 | P2 | TS | ☐ Pass ☐ Fail |
| UAT-054 | BR-16 | P2 | TS | ☐ Pass ☐ Fail |

### UAT-050 — BAST Gabungan (same customer)

**Precondition:** ≥2 tiket **same customer**, status `received_field`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Checkbox pilih ≥2 tiket → **BAST Gabungan** | Modal bulk terbuka |
| 2 | Isi catatan perbaikan per unit | Semua wajib terisi |
| 3 | TTD penyerah + penerima → submit | Semua tiket → `completed` |
| 4 | Cek `bulkBastId` | Sama di semua tiket (format `BAST-GBK-...`) |
| 5 | Tanda Terima tab Completed | Judul BAST Gabungan + tabel multi-unit |

---

### UAT-051 — BAST Gabungan ditolak (beda customer)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Pilih tiket dari 2 customer berbeda → BAST Gabungan | Toast error **Beda Customer** |

---

### UAT-052 — Notifikasi perubahan status

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Ubah status tiket (pickup / quoted / completed) | Notifikasi/badge di nav terupdate |
| 2 | Klik notifikasi | Navigasi ke service detail tiket |

---

### UAT-053 — Bulk BAST dari On-Site `picked_up`

**Precondition:** ≥2 tiket On-Site, same customer, status `picked_up` (setelah quick repair notes optional).

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Pilih tiket → BAST Gabungan | Modal terbuka (status onsite valid) |
| 2 | Selesaikan BAST | Semua → `completed` |

---

### UAT-054 — Bulk BAST ditolak (status tidak valid)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Pilih tiket status `quoted` / `po_issued` → BAST Gabungan | Toast error status tidak sesuai |

---

## G. Permission & Role

| ID | P | Hasil |
|----|---|-------|
| UAT-060 | P1 | ☐ Pass ☐ Fail |
| UAT-061 | P1 | ☐ Pass ☐ Fail |
| UAT-062 | P2 | ☐ Pass ☐ Fail |
| UAT-063 | — | P1 | TS | ☐ Pass ☐ Fail |
| UAT-064 | — | P2 | Owner | ☐ Pass ☐ Fail |

### UAT-060 — TSF tidak bisa registrasi service; bisa SPH TSF

| Role | Aksi | Expected |
|------|------|----------|
| TSF | Buat service ticket baru | Tidak ada akses / tombol tidak muncul |
| TSF | Damage Quotation di `received_tsf` | Berhasil |
| TS | On-Site SPH di `picked_up` (assigned) | Berhasil |
| TS | Damage Quotation di `received_tsf` | Tombol tidak untuk TS |

---

### UAT-061 — SPV: PO + SPH Log + Combined SPH

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login SPV | SPH Log, Combined SPH button visible (jika eligible) |
| 2 | Input PO | Berhasil |
| 3 | Sparepart Master CRUD | Berhasil |

---

### UAT-062 — Specialist: view only

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login Specialist | SPH Log dapat dibuka (read) |
| 2 | Coba tambah sparepart / buat SPH | Tidak ada akses tulis |

---

### UAT-063 — TS bukan assignee tidak bisa aksi

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login TS **bukan** `assignedTsId` tiket | Tombol Pickup / On-Site SPH / BAST tidak muncul |
| 2 | Login TS **assignee** | Tombol aksi muncul |

---

### UAT-064 — Owner: akses penuh smoke test

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login Owner | Sparepart Master, SPH Log, Customer Service, Combined SPH visible |
| 2 | Input PO + Bulk BAST | Berhasil |

---

## H. Phase 5 & 6 — PDF, Smart Fill, Cancel, UX (v6.7.0+)

| ID | AC | P | Role | Hasil |
|----|----|---|------|-------|
| UAT-072 | AC-38 | P1 | TSF / SPV | ☐ Pass ☐ Fail |
| UAT-073 | AC-36, T-28 | P1 | TSF / SPV | ☐ Pass ☐ Fail |
| UAT-074 | AC-37, T-29 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-075 | AC-39, T-30 | P1 | TSF / SPV | ☐ Pass ☐ Fail |
| UAT-076 | AC-40 | P2 | TSF | ☐ Pass ☐ Fail |
| UAT-077 | AC-41, T-31 | P1 | TS (on-site) | ☐ Pass ☐ Fail |
| UAT-078 | AC-42, T-32 | P2 | TSF / SPV | ☐ Pass ☐ Fail |
| UAT-079 | AC-39 | P2 | TS | ☐ Pass ☐ Fail |
| UAT-080 | AC-38 | P3 | TSF | ☐ Pass ☐ Fail |

### UAT-072 — SPH detail modal (bukan alert)

**Precondition:** Minimal 1 SPH di SPH Log.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → klik **Detail** | Modal `sphDetailModal` terbuka (bukan `alert`) |
| 2 | Periksa isi modal | Lines table, labor, history, linked tickets terlihat |
| 3 | Klik salah satu linked ticket | Modal tutup; Service Detail tiket terbuka |

---

### UAT-073 — Export PDF SPH (single & combined)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH single → klik **PDF** di tabel | Tab print terbuka; judul `SPH-{no}`; tabel lines + total |
| 2 | Combined SPH 3 tiket → Export PDF | 3 baris service ticket + semua lines + total |
| 3 | Save as PDF dari dialog print | File dapat disimpan |

---

### UAT-074 — Partial Smart Fill autocomplete

**Precondition:** Sparepart master punya item prefix `ART-SP`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Buka Damage Quotation / SPH builder → Add line | Field Art Number tersedia |
| 2 | Ketik `ART-SP` (min 2 karakter) | Dropdown saran muncul setelah ~200ms |
| 3 | Tekan ↓ lalu Enter | Line terisi artNo, description, harga |
| 4 | Coba sparepart `obsolete` | Tidak muncul di dropdown; exact match diblokir |

---

### UAT-075 — Cancel SPH (issued only)

**Precondition:** SPH status Pending PO (`issued`); tiket terkait `quoted`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → Detail → **Cancel SPH** | Prompt alasan + konfirmasi |
| 2 | Isi alasan → confirm | SPH status → Cancelled; toast sukses |
| 3 | Cek service ticket terkait | `sphDocumentId` hilang; status `received_tsf` atau `picked_up`; `toolStatus` cleared |
| 4 | Cek tombol SPH di tiket | On-Site/TSF SPH dapat dibuat lagi |

---

### UAT-076 — Filter & stat Cancelled

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → filter **Pending PO** | SPH `cancelled` tidak muncul |
| 2 | Filter **Cancelled** | Hanya SPH cancelled |
| 3 | Periksa stat card | Counter **Cancelled** sesuai jumlah |

---

### UAT-077 — On-Site quotation tanpa Un-Repair

**Precondition:** Service ticket `repairLoc=onsite`, status `picked_up`.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Klik **On-Site SPH** | Modal judul "On-Site Analysis & SPH" |
| 2 | Periksa form | Opsi Un-Repair / TSF Decision **tidak** tampil |
| 3 | Label inspection | "On-Site Inspection Result" (bukan TSF Advanced) |

---

### UAT-078 — Combined SPH customer picker

**Precondition:** ≥2 customer berbeda, masing-masing punya ≥2 tiket eligible (`received_tsf`).

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Customer Service → perhatikan hint toolbar | Menampilkan jumlah tiket per customer |
| 2 | Klik **Combined SPH** | Modal pilih customer (bukan auto-pick customer pertama) |
| 3 | Pilih customer B → Continue | `sphBuilderModal` hanya tiket customer B |

---

### UAT-079 — Cancel SPH ditolak untuk role TS

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Login sebagai `ts1` | Role TS |
| 2 | Buka SPH detail `issued` | Tombol Cancel SPH **tidak** tampil |
| 3 | (Opsional) Panggil `cancelSphDocument` via console | Toast "Not Allowed" |

---

### UAT-080 — Preview dokumen PO/SPH di detail modal

**Precondition:** SPH punya `docSph` atau PO punya `docPo` (gambar/PDF).

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | SPH Log → Detail SPH dengan attachment | Preview gambar atau embed PDF terlihat |
| 2 | SPH tanpa attachment | Tidak ada blok preview kosong/error |

---

## I. Cloud Sync (multi-device)

| ID | AC | P | Hasil |
|----|----|---|-------|
| UAT-070 | AC-16, AC-35, T-27 | P2 | ☐ Pass ☐ Fail |
| UAT-071 | BR-18 | P3 | TS | ☐ Pass ☐ Fail |

### UAT-070 — SPH & sparepart sync antar perangkat

**Precondition:** Supabase sync aktif; 2 browser/device login akun berbeda yang sama-sama punya akses.

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Device A: tambah sparepart + issue SPH | Data tersimpan |
| 2 | Device B: refresh / tunggu sync | Sparepart & SPH muncul di SPH Log |
| 3 | Device A: input PO | Device B melihat SPH → PO Received |

---

### UAT-071 — Foto kondisi unit (before / after)

| Step | Aksi | Expected Result |
|------|------|-----------------|
| 1 | Registrasi service → upload foto before | Foto tersimpan; tidak error ukuran |
| 2 | Repair complete → upload foto after | Foto tersimpan di tiket |

---

## J. Coverage Matrix — AC vs UAT

| AC | UAT ID | AC | UAT ID |
|----|--------|----|--------|
| AC-01 | 001, 002, 007 | AC-19 | 022 |
| AC-02 | 003 | AC-20 | 023 |
| AC-03 | 004 | AC-21 | 040 |
| AC-04 | 008 | AC-22 | 024 |
| AC-05 | 006 | AC-23 | 041 |
| AC-06 | 005 | AC-24 | 042 |
| AC-07 | 010, 015, 040 | AC-25 | 032 |
| AC-08 | 014, 016 | AC-26 | 037 |
| AC-09 | 011 | AC-27 | 033 |
| AC-10 | 012 | AC-28 | 038 |
| AC-11 | 011 | AC-29 | 030 |
| AC-12 | 013 | AC-30 | 034 |
| AC-13 | 031 | AC-31 | 050, 053 |
| AC-14 | 036 | AC-32 | 034, 043, 044 |
| AC-15 | 012 | AC-33 | 025 |
| AC-16 | 070 | AC-34 | 052 |
| AC-17 | 020 | AC-35 | 070 |
| AC-18 | 021 | AC-36 | 073 |
| AC-38 | 072, 080 | AC-37 | 074 |
| AC-39 | 075, 079 | AC-40 | 076 |
| AC-41 | 077 | AC-42 | 078 |

*Semua AC-01 s/d AC-42 memiliki ≥1 UAT ID.*

---

## K. Ringkasan Hasil UAT

| Seksi | Total | Pass | Fail | N/A |
|-------|-------|------|------|-----|
| A. Sparepart Master | 8 | | | |
| B. SPH Builder | 7 | | | |
| C. SPH Log & PO | 8 | | | |
| D. Jalur TSF | 9 | | | |
| E. Jalur On-Site | 5 | | | |
| F. Bulk BAST & Notif | 5 | | | |
| G. Permission | 5 | | | |
| H. Phase 5 & 6 | 9 | | | |
| I. Cloud Sync & Media | 2 | | | |
| **TOTAL** | **58** | | | |

### Kriteria Kelulusan UAT

| Kriteria | Syarat |
|----------|--------|
| **Lulus modul** | Semua **P1** (30 kasus) = Pass |
| **Lulus bersyarat** | P1 Pass + P2 Fail ≤ 2 dengan workaround terdokumentasi |
| **Gagal** | Ada P1 Fail tanpa fix plan |

### Defect Log

| Defect ID | UAT ID | Deskripsi | Severity | Status |
|-----------|--------|-----------|----------|--------|
| DEF-001 | | | | Open |
| DEF-002 | | | | |

---

## L. Sign-off

| Peran | Nama | Tanda Tangan | Tanggal |
|-------|------|--------------|---------|
| Business Owner | | | |
| SPV / Operations | | | |
| TSF Lead | | | |
| QA / Tester | | | |
| IT / Developer | | | |

**Keputusan UAT:** ☐ **APPROVED** · ☐ **APPROVED WITH CONDITIONS** · ☐ **REJECTED**

**Catatan:** _______________________________________________

---

## Referensi

| Dokumen | Path |
|---------|------|
| PRD | `docs/PRD-Master-Sparepart-SPH.md` |
| TODO per fase | `docs/TODO-Master-Sparepart-SPH-Phased.md` |
| Release | `release.js` (v6.7.2) |

---

*UAT Pack v1.2.1 — 2026-06-06 — 58 skenario, 100% AC-01–42 covered, release ref v6.7.2*
