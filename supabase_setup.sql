-- ============================================================
-- TMS ONLINE — Jalankan SEKALI di Supabase SQL Editor
-- Dashboard > SQL Editor > New query > Paste > Run
--
-- KEAMANAN v7.3.0+:
-- 1. Set write_secret setelah deploy (lihat komentar di bawah)
-- 2. Simpan nilai yang sama di GitHub Secret SYNC_SECRET + config.js syncSecret
-- 3. Tanpa write_secret = mode dev (update terbuka untuk anon)
-- ============================================================

-- 1. Tabel pusat data (semua user share 1 database via cloud)
CREATE TABLE IF NOT EXISTS public.tms_sync (
    id          INT PRIMARY KEY,
    db_version  BIGINT NOT NULL DEFAULT 1,
    db_data     JSONB NOT NULL DEFAULT '{}'::jsonb,
    write_secret TEXT,
    client_auth  TEXT,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Kolom auth untuk instalasi lama
ALTER TABLE public.tms_sync ADD COLUMN IF NOT EXISTS write_secret TEXT;
ALTER TABLE public.tms_sync ADD COLUMN IF NOT EXISTS client_auth TEXT;

-- 2. Aktifkan Realtime (update langsung ke semua user)
ALTER TABLE public.tms_sync REPLICA IDENTITY FULL;

DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.tms_sync;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- 3. Trigger: validasi secret saat UPDATE (jika write_secret diset)
CREATE OR REPLACE FUNCTION public.check_tms_write_auth()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.write_secret IS NOT NULL AND OLD.write_secret <> '' THEN
        IF NEW.client_auth IS DISTINCT FROM OLD.write_secret THEN
            RAISE EXCEPTION 'Unauthorized TMS sync write';
        END IF;
    END IF;
    NEW.client_auth := NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS tms_sync_auth ON public.tms_sync;
CREATE TRIGGER tms_sync_auth
    BEFORE UPDATE ON public.tms_sync
    FOR EACH ROW EXECUTE FUNCTION public.check_tms_write_auth();

-- 4. Izin akses untuk aplikasi web (anon key)
ALTER TABLE public.tms_sync ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "tms_anon_select" ON public.tms_sync;
DROP POLICY IF EXISTS "tms_anon_insert" ON public.tms_sync;
DROP POLICY IF EXISTS "tms_anon_update" ON public.tms_sync;

CREATE POLICY "tms_anon_select" ON public.tms_sync
    FOR SELECT TO anon USING (true);

CREATE POLICY "tms_anon_insert" ON public.tms_sync
    FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "tms_anon_update" ON public.tms_sync
    FOR UPDATE TO anon USING (true) WITH CHECK (true);

-- 5. SETUP PRODUCTION (jalankan manual setelah generate secret):
-- UPDATE public.tms_sync SET write_secret = 'GANTI-DENGAN-RANDOM-SECRET-PANJANG' WHERE id = 1;
-- Simpan secret yang sama di GitHub Secrets (SYNC_SECRET) dan config.js (syncSecret).

-- Selesai! Lanjut ke Atur_Cloud.bat lalu Jalankan_Setup.bat
