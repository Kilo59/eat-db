"""
tasks.py
~~~~~~~~
project invoke tasks
"""
import invoke


@invoke.task
def api(ctx, dev=True):
    """Start the FastAPI application."""
    args = ["uvicorn eat_db.api.main:app"]
    if dev:
        args.append("--reload")
    cmd = " ".join(args)
    ctx.run(cmd)
