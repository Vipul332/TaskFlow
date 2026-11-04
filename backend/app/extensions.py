from supabase import create_client

supabase_client = None


def init_extensions(app):
    global supabase_client

    supabase_url = app.config.get("SUPABASE_URL")
    supabase_key = app.config.get("SUPABASE_SERVICE_ROLE_KEY")

    if supabase_url and supabase_key:
        supabase_client = create_client(
            supabase_url,
            supabase_key
        )

        app.logger.info("Supabase client initialized")
    else:
        app.logger.info("Supabase credentials not configured yet")