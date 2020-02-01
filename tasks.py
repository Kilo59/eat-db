"""
tasks.py
~~~~~~~~
project invoke tasks
"""
import invoke


@invoke.task
def api(ctx, dev=True):
    """Start the FastAPI application."""
    args = ["uvicorn eat_db.api.main:APP"]
    if dev:
        args.append("--reload")
    cmd = " ".join(args)
    ctx.run(cmd)


@invoke.task
def sort(ctx, diff=False):
    """Sorts imports using isort tool."""
    args = ["isort", "-rc"]
    if diff:
        args.append("--diff")
    else:
        args.append("--atomic")
    args.append(".")
    cmd = " ".join(args)
    ctx.run(cmd)
