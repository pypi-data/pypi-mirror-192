# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdAccordionItem(Component):
    """An AntdAccordionItem component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- className (string; optional)

- collapsible (a value equal to: 'header', 'disabled'; optional)

- extra (a list of or a singular dash component, string or number; optional)

- forceRender (boolean; optional)

- key (string | number; required)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- showArrow (boolean; optional)

- style (dict; optional)

- title (a list of or a singular dash component, string or number; optional)"""
    _children_props = ['title', 'extra']
    _base_nodes = ['title', 'extra', 'children']
    _namespace = 'dmp_dash_components'
    _type = 'AntdAccordionItem'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.REQUIRED, collapsible=Component.UNDEFINED, title=Component.UNDEFINED, extra=Component.UNDEFINED, showArrow=Component.UNDEFINED, forceRender=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'collapsible', 'extra', 'forceRender', 'key', 'loading_state', 'showArrow', 'style', 'title']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'collapsible', 'extra', 'forceRender', 'key', 'loading_state', 'showArrow', 'style', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['key']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(AntdAccordionItem, self).__init__(children=children, **args)
