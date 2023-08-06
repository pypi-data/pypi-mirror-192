# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TabPane(Component):
    """A TabPane component.
TabPane

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- close_icon (string; optional):
    Customize close icon in TabPane's head. Only works while
    type=\"editable-card\".

- force_render (boolean; optional):
    Forced render of content in tabs, not lazy render after clicking
    on tabs.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; required):
    Show text in TabPane's head.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tab_key (string; required):
    TabPane's key."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_antd'
    _type = 'TabPane'
    @_explicitize_args
    def __init__(self, children=None, close_icon=Component.UNDEFINED, force_render=Component.UNDEFINED, tab_key=Component.REQUIRED, label=Component.REQUIRED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'close_icon', 'force_render', 'key', 'label', 'style', 'tab_key']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'close_icon', 'force_render', 'key', 'label', 'style', 'tab_key']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label', 'tab_key']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(TabPane, self).__init__(children=children, **args)
