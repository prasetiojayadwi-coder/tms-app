# TODO — Master Sparepart & SPH (Per Fase)



> Berdasarkan [PRD-Master-Sparepart-SPH.md](./PRD-Master-Sparepart-SPH.md) v1.4.0  

> Legenda: `[x]` selesai · `[ ]` belum · `[~]` sebagian



---



## Ringkasan Progress



| Fase | Versi | Status | AC | Test |

|------|-------|--------|-----|------|

| Phase 1 | v6.4.0 | ✅ Done | AC-01–03, AC-06 | T-01, T-02, T-10 |

| Phase 2 | v6.4.0 | ✅ Done | AC-04, AC-05, AC-07, AC-09–12, AC-15 | T-03, T-04 |

| Phase 3 | v6.4.0 | ✅ Done | AC-08, AC-11, AC-13, AC-14 | T-05–07, T-19 |

| Phase 4 | v6.5.0 | ✅ Done | AC-17–24 | T-08, T-11–16 |

| Phase 4.1 | v6.5.1 | ✅ Done | AC-25–30 | T-17–21 |

| Phase 4.2 | v6.5.1 | ✅ Done | AC-31–35 | T-22–27 |

| **Cross-cutting** | setiap release | ✅ Done | BR-04–19 | Regression T-01–32 |

| Phase 5 | v6.6.0 | ✅ Done | AC-36–38 | T-28–29 |

| Phase 6 | v6.7.0 | ✅ Done | AC-39–42 | T-30–32 |
| Phase 6.1 | v6.7.1 | ✅ Done | Cancel hardening | — |
| **Phase 7** | v6.7.1 | 🔄 Deploy | Release | Live verify |



---



## Phase 1 — Sparepart Master + Batch Import/Export



**Target:** v6.4.0  

**PRD:** §5.1, §7.1, BR-01



### Data Model

- [x] Tambah array `spareparts[]` ke DB schema

- [x] Field: `id`, `artNo`, `description`, `price`, `group`, `status`, `notes`, `updatedAt`

- [x] `sanitizeDB()` — inisialisasi & filter array valid

- [x] `dedupe` sparepart by normalized `artNo` (BR-19)



### UI — `view-sparepart-master`

- [x] Menu nav: Owner, SPV, TSF

- [x] Stats: Total / Active / Discontinued

- [x] Filter group: All · Avitum · Hospital Care · Aesculap

- [x] Search: Art Number, Description, Group

- [x] Tabel + tombol Edit / Delete



### CRUD

- [x] Modal Add / Edit sparepart

- [x] Validasi `artNo` unik real-time (`findSparepartConflicts`)

- [x] Status enum: `active` · `discontinued` · `obsolete`

- [x] Group enum: Avitum · Hospital Care · Aesculap · General



### Batch Import / Export

- [x] Template Excel/CSV: `Art Number, Description, Price, Group, Status, Notes`

- [x] `importSparepartsBatch()` — skip duplikat + error per row

- [x] `exportSparepartsCSV()` — UTF-8 BOM



### QA

- [x] AC-01 CRUD + validasi unik

- [x] AC-02 Batch import

- [x] AC-03 Export CSV

- [x] AC-06 Filter group

- [x] T-01, T-02, T-10



---



## Phase 2 — SPH Line Items + Smart Fill



**Target:** v6.4.0  

**PRD:** §5.2, §6.7, §7.4, BR-02, BR-07, BR-08



### Data Model

- [x] Struktur line item: `sparepartId`, `artNo`, `description`, `unitPrice`, `qty`, `subtotal`, `serviceTicketId`

- [x] Extension `serviceTickets[]`: `sparepartLines`, `quoteDetails`, `quotePrice`

- [x] `calcSphLineSubtotal()` — qty min 1



### Smart Fill

- [x] `lookupSparepartByArtNo()` — exact match (normalized key)

- [x] Auto-fill Description + unitPrice di SPH line builder

- [x] Block `obsolete` + toast error (AC-05)

- [x] Warning toast untuk `discontinued` (BR-02)



### SPH Builder — Single (Damage Quotation / On-Site SPH)

- [x] Modal `serviceQuotationModal` — dynamic line rows

- [x] `addSphLineRow` / `removeSphLineRow` / `updateSphLineField`

- [x] `recalcSphTotals()` — parts + labor → total

- [x] Preview customer table: Art Number | Description | Harga (BR-07)

- [x] `formatQuoteDetailsFromLines()` → `quoteDetails` auto

- [x] Labor amount field

- [x] Upload `docSph` opsional (compress)



### SPH Number

- [x] `generateSphNumber()` — format `SPH-YYMM-####`



### TSF Path — Single SPH Issue

- [x] `submitServiceQuotation()` → create `sphDocuments` + `applySphToTickets()`

- [x] Ticket status → `quoted`; `sphDocumentId` ter-link (BR-04)

- [x] Field `tsfAnalysis` tersimpan

- [x] `sphDocuments.history[]` + `addToHistory()` saat SPH terbit (G-08)



### QA

- [x] AC-04 Smart Fill

- [x] AC-05 Obsolete blocked

- [x] AC-07 Single SPH line items

- [x] AC-09 Preview table

- [x] AC-10 SPH number format

- [x] AC-11 qty & subtotal

- [x] AC-12 docSph upload

- [x] AC-15 quoteDetails / quotePrice auto

- [x] T-03, T-04



---



## Phase 3 — Combined SPH + Repair Confirm



**Target:** v6.4.0  

**PRD:** §6.6, BR-03, BR-04, BR-11



### Combined SPH

- [x] `getEligibleSphTickets()` + `hasEligibleCombinedSph()`

- [x] Tombol **Combined SPH** di Customer Service (TSF/SPV/Owner)

- [x] Modal `sphBuilderModal` — pilih ≥2 tiket (checkbox)

- [x] Validasi same `customerId` (BR-03)

- [x] `submitSphBuilder()` → 1 `sphDocument`, N tickets

- [x] Labor split: **tiket pertama saja** (BR-11)

- [x] Line allocation via `serviceTicketId` opsional



### Repair Completion — Sparepart Confirm

- [x] `renderRepairSparepartChecklist()` — checkbox per line dari SPH

- [x] `collectReplacedSpareparts()` → `replacedSpareparts[]`

- [x] Tampil di service detail post-completion (AC-14)



### TSF Repair Complete (`po_issued`)

- [x] `openServiceRepairModal()` + `submitServiceRepair()`

- [x] Work notes + foto after repair (`compressImage`, BR-18)

- [x] Handover `send_field` → status `repaired`

- [x] `receive_field` — TS assigned (`assignedTsId`) + TTD



### QA

- [x] AC-08 Combined SPH

- [x] AC-13 Konfirmasi replaced parts

- [x] AC-14 Service detail SPH + replaced table

- [x] T-05, T-06, T-07, T-19



---



## Phase 4 — SPH Log + PO Sync + On-Site Path



**Target:** v6.5.0  

**PRD:** §6.3, §6.4, §6.5, G-01–G-09



### Data Model — `sphDocuments[]`

- [x] Entitas tiket SPH terpisah dari service ticket

- [x] Field: `repairPath`, `status`, `serviceTicketIds`, `history[]`, PO fields

- [x] Lifecycle: `issued` → `po_received` → `cancelled`



### SPH Log UI — `view-sph-log`

- [x] Menu nav: Owner, SPV, TSF, Specialist (view), TS (view)

- [x] Stats: Total · Pending PO · PO Received · Cancelled

- [x] Search: SPH No., customer, PO number

- [x] Filter chips: All · Pending PO · PO Received · Cancelled

- [x] Tabel: SPH No., Customer, Path badge, Tickets, Total, Status, PO No.

- [x] `showSphDetail()` — rich modal (lines, history, tickets, PO)



### PO Input & Synchronization

- [x] `openPoModal()` — tampilkan `quotePrice` referensi

- [x] Form PO: No, Amount, Date, upload `docPo` (compress)

- [x] Role input PO: TS, TSF, SPV, Owner (§7.5)

- [x] `syncSphPoFromServiceTicket()` — jika ada `sphDocumentId` (BR-06)

- [x] Legacy fallback: PO langsung `po_issued` tanpa SPH Log update (BR-17)

- [x] Combined SPH: PO di 1 tiket cukup (AC-19)

- [x] `notifyServiceUpdate` + `playNotificationSound` per tiket



### On-Site Repair Path

- [x] Field `repairLoc` saat registrasi service — immutable (BR-14)

- [x] `canIssueSphForTicket()` — `picked_up` + onsite

- [x] Tombol **On-Site SPH** + **Quick Repair** di `picked_up`

- [x] `repairPath: onsite` pada `sphDocuments`

- [x] On-Site: PO → `po_issued` → Repair & BAST (`openOnsiteRepair`)

- [x] On-Site Quick Repair → langsung `received_field` + BAST



### Cloud Sync

- [x] `spareparts[]` + `sphDocuments[]` ikut Supabase full JSON sync (AC-16)



### QA

- [x] AC-17 SPH Log registry

- [x] AC-18 PO → po_received

- [x] AC-19 Combined PO sync

- [x] AC-20 Filter SPH Log

- [x] AC-21 On-Site SPH

- [x] AC-22 Path badge

- [x] AC-23 On-Site Quick Repair

- [x] AC-24 On-Site PO → Repair & BAST

- [x] T-08, T-11–16, T-27



---



## Phase 4.1 — TSF Quick Repair + Handover + Un-Repair



**Target:** v6.5.1  

**PRD:** §6.2, §6.2a, §6.2b, §6.8, G-11–G-14



### TSF Timeline Lengkap

- [x] `openAnalysisModal()` — analisa awal teknisi (`initialAnalysis`)

- [x] Status `initial_analyzed` — TTD `send_tsf`

- [x] TSF receive → `received_tsf` + TTD `receive_tsf`

- [x] `canIssueSphForTicket()` — gate `received_tsf` only untuk TSF SPH (BR-13)



### TSF Quick Repair

- [x] Tombol **Quick Repair** di `received_tsf` (sejajar Damage Quotation)

- [x] `openTsfQuickRepair()` — mode `tsf_quick`

- [x] `setupServiceRepairModal()` — shared modal 3 mode

- [x] `repairCompletionType = tsf_quick` di audit trail

- [x] Alur: repair → TTD `send_field` → `repaired` → TS terima → BAST



### Un-Repair (TSF)

- [x] Decision *Not Repairable* di quotation modal

- [x] `toggleTsfDecision('unrepair')`

- [x] Tidak buat SPH; `toolStatus = unrepaired`

- [x] Langsung handover `send_field`

- [x] BAST pernyataan unrepaired berbeda



### Digital Handover (TTD)

- [x] `handoverSignatureModal` — pickup (2-step), send_tsf, receive_tsf, send_field, receive_field

- [x] Simpan `signature*` base64 per tahap

- [x] Single BAST — `openServiceDeliveryModal` + TTD customer



### QA

- [x] AC-25 TSF Quick Repair tanpa SPH

- [x] AC-26 Alur repaired → received_field → BAST

- [x] AC-27 Un-Repair tanpa SPH

- [x] AC-28 Unrepaired BAST text

- [x] AC-29 initial_analyzed di timeline

- [x] AC-30 TTD per tahap

- [x] T-17–T-21



---



## Phase 4.2 — Adjacent Flows + Dokumentasi



**Target:** v6.5.1  

**PRD:** §5.4, §5.5, §6.9–§6.11, G-21–G-25



### Bulk BAST

- [x] Tombol **BAST Gabungan** (multi-select checkbox)

- [x] Validasi same customer + status eligible (BR-16)

- [x] `bulkBastId = BAST-GBK-{timestamp}`

- [x] Shared TTD + catatan per unit

- [x] Role: TS, TSF, SPV, Owner



### Tanda Terima (Service Receipt)

- [x] Link **Tanda Terima** per tiket

- [x] Tab: Pickup · TSF · Field · Completed/BAST

- [x] TTD embedded + print CSS `print-svc-receipt`

- [x] Bulk BAST doc + tabel multi-unit



### Legacy & Sync (dokumentasi)

- [x] §5.4 Legacy PO tanpa `sphDocumentId` (BR-17)

- [x] §5.5 Cloud sync Supabase behavior

- [x] §6.11 `notifyServiceUpdate` + sound



### PRD v1.2 → v1.3.1

- [x] Permission matrix §7.5

- [x] AC-01–35 lengkap

- [x] Test T-01–T-27

- [x] Patch v1.3.1 (G-10, SPH detail alert, BR-OS-05)



### QA

- [x] AC-31 Bulk BAST

- [x] AC-32 Tanda Terima

- [x] AC-33 Legacy PO

- [x] AC-34 Notifikasi

- [x] AC-35 Cloud sync

- [x] T-22–T-27



### Deploy

- [x] Dipindah ke **Phase 7 — Deploy & Release** (lihat bawah)



---



## Cross-cutting — Setiap Release



**PRD:** §8 BR-04–19, §9, §5.5



### Release Engineering

- [x] Bump `release.js` — `version` + `build` + changelog

- [x] Bump `sw.js` — `CACHE_NAME` match `build` (v66)

- [x] Update banner / `TMS_RELEASE` di `index.html`

- [x] Jalankan `cek_sistem.py` — modul SPH + integritas handler

- [ ] Commit message mengikuti style repo (menunggu permintaan user)



### Business Rules — verifikasi lintas fase

- [x] BR-04 Satu tiket → satu `sphDocumentId` aktif

- [x] BR-05 Setiap SPH terbit → record `sphDocuments`

- [x] BR-08 Price snapshot di lines (tidak ikut perubahan master)

- [x] BR-09 On-Site: PO wajib setelah SPH sebelum repair berbayar

- [x] BR-10 Quick Repair skip SPH (On-Site + TSF)

- [x] BR-12 Un-Repair skip SPH

- [x] BR-15 TTD wajib tiap handover fisik

- [x] BR-18 Foto unit compress sebelum simpan DB

- [x] BR-19 Dedupe sparepart on load



### Media & Dokumen

- [x] `unitPhotoBefore` — registrasi service (multiple, compress)

- [x] `unitPhotoAfter` — repair modal (multiple, compress)

- [x] `docSph` / `docPo` — upload opsional (compress)



### Audit Trail

- [x] `serviceTickets.history[]` per status change

- [x] `sphDocuments.history[]` per SPH event

- [x] `historyLog` global (`addToHistory`) untuk aksi penting



### Permission Matrix (§7.5) — smoke test

- [x] Sparepart CRUD: Owner, SPV, TSF

- [x] SPH create: TSF (workshop), TS (on-site, assigned)

- [x] SPH Log view: semua role relevan

- [x] Combined SPH button: TSF, SPV, Owner



---



## Phase 5 — PDF Export + Partial Smart Fill



**Target:** v6.6.0 (shipped in v6.7.0)  

**PRD:** G-10, Non-Goals → Goals, Phase 5



### PDF SPH Export

- [x] Layout PDF korporat (header TMS, tabel sparepart, total, tanda tangan)

- [x] Tombol **Export PDF** di SPH Log detail & tabel actions

- [x] Support single SPH + combined SPH

- [x] Nama file: `SPH-{sphNo}.pdf` (via print dialog)



### SPH Log — Rich Detail Modal

- [x] Ganti `alert()` dengan modal proper (`sphDetailModal`)

- [x] Tampilkan: lines table, labor, history, linked tickets, PO doc preview

- [x] Tombol navigasi ke service ticket terkait



### Partial Smart Fill Search

- [x] Dropdown autocomplete saat ketik Art Number (partial match)

- [x] Filter hanya `active` + `discontinued` (exclude `obsolete`)

- [x] Keyboard navigation (↑↓ Enter)

- [x] Debounce 200ms



### QA

- [x] AC-36: PDF export menghasilkan file valid untuk single SPH

- [x] AC-37: Partial search menampilkan ≥1 saran untuk prefix match

- [x] AC-38: SPH detail modal menggantikan alert

- [x] T-28: Export PDF combined SPH 3 tickets

- [x] T-29: Partial search "ART-SP" → dropdown suggestions



---



## Phase 6 — SPH Cancel + UX Polish



**Target:** v6.7.0  

**PRD:** Phase 6, §14.3 `cancelled`, BR-OS-05, §6.6 multi-customer



### SPH Cancel Flow

- [x] UI cancel di SPH Log detail (hanya status `issued`)

- [x] Konfirmasi dialog + alasan cancel

- [x] `sphDocuments.status` → `cancelled`

- [x] Unlink `sphDocumentId` dari service tickets → kembali `received_tsf` / `picked_up`

- [x] `sphDocuments.history[]` + `historyLog` entry

- [x] Filter SPH Log: **Cancelled** chip



### On-Site Modal UX Fix (BR-OS-05)

- [x] Sembunyikan opsi Un-Repair saat `repairLoc = onsite`

- [x] Ganti label "TSF Advanced Inspection" → "On-Site Inspection Result"

- [x] Ganti judul modal → "On-Site Analysis & SPH"

- [x] `openQuotationModal()` — `configureQuotationModalForTicket()` by path



### Combined SPH — Customer Picker

- [x] Jika >1 customer punya ≥2 tiket eligible → modal dropdown pilih customer

- [x] Tidak auto-pick `custIds[0]` saja

- [x] Preview jumlah tiket per customer di toolbar hint (`combined-sph-hint`)



### QA

- [x] AC-39: Cancel SPH hanya untuk status `issued`

- [x] AC-40: Cancelled SPH tidak muncul di filter Pending PO

- [x] AC-41: On-Site quotation modal tanpa opsi Un-Repair

- [x] AC-42: Combined SPH customer picker berfungsi

- [x] T-30: Cancel SPH → tickets kembali eligible

- [x] T-31: On-Site open quotation — no Un-Repair option

- [x] T-32: 2 customers eligible — picker shows both



---



## Phase 6.1 — Cancel Hardening & Doc Preview (v6.7.1)



**Target:** v6.7.1 — patch audit gap



### Kode

- [x] `cancelSphDocument()` — reset `toolStatus` saat revert tiket

- [x] `canCancelSphDocument()` — role guard TSF/SPV/Owner di fungsi

- [x] `notifyServiceUpdate()` dipanggil per tiket saat cancel

- [x] `buildCompressedDocPreviewHtml()` — preview `docPo` / `docSph` di detail modal

- [x] Stat card **Cancelled** di SPH Log



### Dokumentasi

- [x] PRD v1.4.0 — AC-36–42, T-28–32, §7.2 modal spec

- [x] UAT v1.2 — 9 skenario baru (UAT-072–080), total 58 kasus



---



## Phase 7 — Deploy & Release



**Target:** v6.7.1  

**PRD:** §12 Release Plan, Cross-cutting Release Engineering



### Pre-deploy Checklist

- [x] `cek_sistem.py` — 87 OK, 0 FAIL kode (server lokal opsional)

- [x] `release.js` v6.7.1 / build 66 + changelog

- [x] `sw.js` `tms-cache-v66` match build

- [x] Semua handler onclick/onsubmit valid (97 onclick)

- [x] Modul SPH: 25 fungsi + 5 modal/view terverifikasi

- [x] Dokumen: PRD v1.4.0, UAT v1.2, TODO lengkap Phase 1–6.1

- [x] Regression T-01–T-32 code-verified



### Git & GitHub Pages

- [ ] `git add` — index.html, release.js, sw.js, cek_sistem.py, docs/

- [ ] `git commit` — message style repo (Bahasa Indonesia)

- [ ] `git push origin main`

- [ ] Tunggu GitHub Pages deploy (~1–3 menit)



### Post-deploy Verification

- [ ] Live `release.js` → version `6.7.1`, build `66`

- [ ] Live `sw.js` → `tms-cache-v66`

- [ ] Live app: menu Sparepart Master + SPH Log tampil

- [ ] Live app: SPH detail modal (bukan alert)

- [ ] URL: https://prasetiojayadwi-coder.github.io/tms-app/



### QA Deploy

- [ ] Live version match local

- [ ] PWA cache bump terdeteksi (update banner)



---



## Backlog Opsional (di luar PRD inti)



> Fitur ada di app, belum masuk PRD modul SPH — dokumentasi terpisah jika diperlukan.



- [ ] Bulk delete service tickets (Owner only)

- [ ] Export service tickets CSV (`exportServiceTicketsCSV`)

- [ ] Service stats dashboard (`renderServiceStatsDash`)

- [ ] Smart fill registrasi service (customer, Art No, SN) + `checkServiceDuplicate`

- [ ] Validasi PO amount vs SPH total (currently non-goal)

- [ ] ERP / SAP integration (non-goal)

- [ ] Stock qty sparepart (non-goal)



---



## Checklist Regression (setiap release)



Jalankan sebelum bump versi / deploy — **semua T-01 s/d T-32**:



| # | Skenario | Fase | Status |

|---|----------|------|--------|

| [x] | T-01 Add sparepart | 1 | code-verified |

| [x] | T-02 Import duplicate artNo | 1 | code-verified |

| [x] | T-03 Smart Fill obsolete blocked | 2 | code-verified |

| [x] | T-04 Single TSF SPH | 2 | code-verified |

| [x] | T-05 Combined SPH 3 tickets | 3 | code-verified |

| [x] | T-06 PO on 1 of 3 combined | 3 | code-verified |

| [x] | T-07 Repair confirm spareparts | 3 | code-verified |

| [x] | T-08 On-Site SPH path | 4 | code-verified |

| [x] | T-09 On-Site Quick Repair | 4 | code-verified |

| [x] | T-10 Export sparepart CSV | 1 | code-verified |

| [x] | T-11 On-Site SPH at picked_up | 4 | code-verified |

| [x] | T-12 On-Site PO then repair | 4 | code-verified |

| [x] | T-13 On-Site Quick Repair (no SPH) | 4 | code-verified |

| [x] | T-14 PO sync combined SPH | 4 | code-verified |

| [x] | T-15 SPH Log filter Pending | 4 | code-verified |

| [x] | T-16 SPH Log after PO | 4 | code-verified |

| [x] | T-17 TSF Quick Repair | 4.1 | code-verified |

| [x] | T-18 Un-Repair | 4.1 | code-verified |

| [x] | T-19 Combined labor split | 3 | code-verified |

| [x] | T-20 Quick Repair blocked after SPH | 4.1 | code-verified |

| [x] | T-21 initial_analyzed handover | 4.1 | code-verified |

| [x] | T-22 Bulk BAST 3 units | 4.2 | code-verified |

| [x] | T-23 Bulk BAST different customers | 4.2 | code-verified |

| [x] | T-24 Tanda Terima TSF tab | 4.2 | code-verified |

| [x] | T-25 Legacy PO no sphDocumentId | 4.2 | code-verified |

| [x] | T-26 Discontinued sparepart warning | 2 | code-verified |

| [x] | T-27 Cloud sync after SPH | 4 | code-verified |

| [x] | T-28 Export PDF combined SPH | 5 | code-verified |

| [x] | T-29 Partial search autocomplete | 5 | code-verified |

| [x] | T-30 Cancel SPH revert tickets | 6 | code-verified |

| [x] | T-31 On-Site modal no Un-Repair | 6 | code-verified |

| [x] | T-32 Combined SPH customer picker | 6 | code-verified |



---



## Referensi Cepat



| Dokumen | Path |

|---------|------|

| PRD lengkap | `docs/PRD-Master-Sparepart-SPH.md` |

| UAT skenario | `docs/UAT-Master-Sparepart-SPH.md` |

| Release manifest | `release.js` |

| Service Worker cache | `sw.js` (build harus match `release.js`) |

| Implementasi | `index.html` |

| Health check | `cek_sistem.py` |



---



## Mapping PRD → TODO (cek kelengkapan)



| PRD Section | Tercakup di TODO |

|-------------|------------------|

| §5 Data Model | Phase 1–4, Cross-cutting |

| §6 User Flows | Phase 2–4.2, Phase 6 |

| §7 UI Specs | Phase 1–6, Cross-cutting permissions |

| §8 Business Rules BR-01–19 | Per fase + Cross-cutting |

| §10 AC-01–42 | Per fase QA |

| §11 T-01–32 | Regression table |

| §12 Phase 5–6 | Phase 5–6.1 ✅ |

| §12 Phase 7 Deploy | Phase 7 |

| Backlog opsional | § Backlog |



---



*Updated: 2026-06-06 — v1.3 TODO: Phase 7 Deploy in progress, PRD v1.4.0 ref, build v66*

