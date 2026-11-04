CREATE TABLE IF NOT EXISTS public.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(200) NOT NULL,
    description TEXT,

    creator_id UUID NOT NULL
        REFERENCES public.users(id) ON DELETE CASCADE,

    assignee_id UUID
        REFERENCES public.users(id) ON DELETE SET NULL,

    status TEXT NOT NULL DEFAULT 'TODO'
        CHECK (status IN ('TODO', 'IN_PROGRESS', 'COMPLETED')),

    priority TEXT NOT NULL DEFAULT 'MEDIUM'
        CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),

    due_date TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;

-- Backend service access
GRANT ALL ON TABLE public.tasks TO service_role;

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_tasks_creator_id
ON public.tasks(creator_id);

CREATE INDEX IF NOT EXISTS idx_tasks_assignee_id
ON public.tasks(assignee_id);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON public.tasks(status);

CREATE INDEX IF NOT EXISTS idx_tasks_created_at
ON public.tasks(created_at DESC);