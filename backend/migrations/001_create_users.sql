CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    google_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    avatar_url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Allow the backend service role to access this table
GRANT ALL ON TABLE public.users TO service_role;

-- Index for faster email lookups
CREATE INDEX IF NOT EXISTS idx_users_email
ON public.users(email);

CREATE INDEX IF NOT EXISTS idx_users_google_id
ON public.users(google_id);