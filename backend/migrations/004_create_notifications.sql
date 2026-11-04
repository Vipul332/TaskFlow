CREATE TABLE IF NOT EXISTS public.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    task_id UUID NOT NULL
        REFERENCES public.tasks(id) ON DELETE CASCADE,

    recipient_id UUID NOT NULL
        REFERENCES public.users(id) ON DELETE CASCADE,

    type TEXT NOT NULL
        CHECK (type IN ('TASK_ASSIGNED', 'TASK_COMPLETED')),

    status TEXT NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'SENT', 'FAILED')),

    sent_at TIMESTAMPTZ,
    error_message TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;

-- Backend service access
GRANT ALL ON TABLE public.notifications TO service_role;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_notifications_recipient_id
ON public.notifications(recipient_id);

CREATE INDEX IF NOT EXISTS idx_notifications_task_id
ON public.notifications(task_id);

CREATE INDEX IF NOT EXISTS idx_notifications_status
ON public.notifications(status);

CREATE INDEX IF NOT EXISTS idx_notifications_created_at
ON public.notifications(created_at DESC);