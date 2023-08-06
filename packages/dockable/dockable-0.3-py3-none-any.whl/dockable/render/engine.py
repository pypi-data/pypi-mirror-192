from dockable.types import Context, Step, StepArgs

default = "dockable.raw"


def render_step(ctx: Context, step: dict, curr: str = default, default: str = default) -> list[str]:
    def resolve_dep(key: str) -> tuple[str, str]:
        if key.startswith("."):  # relative
            return curr, key[1:]
        elif "." in key:  # absolute
            mod, fnc = key.rsplit(".", 1)
            return mod, fnc
        else:  # default
            return default, key

    def invoke_step(curr: str, fnc: str, v: StepArgs) -> list[Step]:
        if curr not in ctx:
            raise ValueError(f"dockable module {curr} not found")
        if fnc not in ctx[curr]:
            raise ValueError(f"dockable module {curr} did not define {fnc}")
        match v:
            case dict() as d:
                return ctx[curr][fnc](**d)
            case list() as items:
                return ctx[curr][fnc](*items)
            case str() as s:
                return ctx[curr][fnc](s)

    def invoke(step: str, v: StepArgs) -> tuple[str, list[Step]]:
        c, fnc = resolve_dep(step)
        return c, invoke_step(c, fnc, v)

    data2 = [invoke(k, v) for k, v in step.items()]
    data3 = [render_steps(ctx, s, c) for c, s in data2]
    return [y for x in data3 for y in x]


def render_steps(ctx: Context, steps: list[Step], curr: str = default, default: str = default) -> list[str]:
    def _render(x: Step) -> list[str]:
        match x:
            case dict() as d:
                return render_step(ctx, d, curr=curr, default=default)
            case str() as s:
                return [s]

    data = [_render(x) for x in steps]
    return [y for x in data for y in x]
