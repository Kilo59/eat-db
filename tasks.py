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


@invoke.task
def build_image(ctx):
    """Build the docker image."""
    args = ["docker", "build", ".", "-t", "kilo59/eat-db"]
    cmd = " ".join(args)
    ctx.run(cmd)


@invoke.task
def container_run(ctx):
    """Run the latest docker image as a container."""
    args = ["docker", "run", "-p80:80", "kilo59/eat-db"]
    cmd = " ".join(args)
    ctx.run(cmd)
