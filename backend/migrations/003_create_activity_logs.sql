CREATE TABLE IF NOT EXISTS public.activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    task_id UUID NOT NULL
        REFERENCES public.tasks(id) ON DELETE CASCADE,

    user_id UUID
        REFERENCES public.users(id) ON DELETE SET NULL,

    action TEXT NOT NULL,

    details JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.activity_logs ENABLE ROW LEVEL SECURITY;

-- Backend service access
GRANT ALL ON TABLE public.activity_logs TO service_role;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_activity_logs_task_id
ON public.activity_logs(task_id);

CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id
ON public.activity_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at
ON public.activity_logs(created_at DESC);