from django import template
from django.conf import settings
import importlib

register = template.Library()
block_views = getattr(settings, "BLOCK_VIEWS", {})


def get_view_by_name(view_name):
    parts = view_name.split(".")
    module_name = str.join(".", parts[:-1])
    view_name = parts[-1]
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise AttributeError("Module '" + module_name + "' not found")
    view = getattr(module, view_name, None)
    if view is None:
        raise AttributeError("View '" + view_name + "' not defined in '" + module_name + "'")
    return view


class BlockNode(template.Node):
    def __init__(self, block_name):
        if block_name not in block_views.keys():
            raise AttributeError("Block '" + block_name + "' not registered")
        elif isinstance(block_views[block_name], str):
            self.block_view = get_view_by_name(block_views[block_name])
        else:
            self.block_view = block_views[block_name]

    def render(self, context):
        return self.block_view()


@register.tag(name="view_block")
def view_block(parser, token):
    block_name = str(token).split(" ")[-1].split("...")[0]
    return BlockNode(block_name)
