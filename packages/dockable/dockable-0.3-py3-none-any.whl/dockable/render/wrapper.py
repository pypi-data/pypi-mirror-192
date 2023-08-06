from dockable.types import Context, Step

from . import engine


def render_image(ctx: Context, data: dict) -> str:
    meta_steps: list[Step] = [{k: v for k, v in data.items() if k not in ["steps", "name"]}]
    data2 = engine.render_steps(ctx, meta_steps, default="dockable.meta") + engine.render_steps(ctx, data["steps"])
    return "\n".join(data2)


def render(ctx: Context, data: dict) -> str:
    return "\n".join([render_image(ctx, x) for x in data["images"]])
