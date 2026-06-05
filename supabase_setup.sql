-- ============================================================
-- TMS ONLINE — Jalankan SEKALI di Supabase SQL Editor
-- Dashboard > SQL Editor > New query > Paste > Run
-- ============================================================

-- 1. Tabel pusat data (semua user share 1 database via cloud)
CREATE TABLE IF NOT EXISTS public.tms_sync (
    id          INT PRIMARY KEY,
    db_version  BIGINT NOT NULL DEFAULT 1,
    db_data     JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Aktifkan Realtime (update langsung ke semua user)
ALTER TABLE public.tms_sync REPLICA IDENTITY FULL;

DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.tms_sync;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- 3. Izin akses untuk aplikasi web (anon key)
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

-- Selesai! Lanjut ke Atur_Cloud.bat lalu Online_Mudah.bat
