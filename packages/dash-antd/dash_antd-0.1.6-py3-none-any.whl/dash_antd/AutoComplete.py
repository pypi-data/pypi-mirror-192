# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AutoComplete(Component):
    """An AutoComplete component.
Alert component for feedback.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allow_clear (boolean; default False):
    Show clear button.

- auto_focus (boolean; default False):
    If get focus when component mounted.

- backfill (boolean; default False):
    If backfill selected item the input when using keyboard.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- default_active_first_option (boolean; default True):
    Whether active first option by default.

- default_open (boolean; optional):
    Initial open state of dropdown.

- default_value (string; optional):
    Initial selected option.

- disabled (boolean; default False):
    Whether disabled select.

- dropdown_match_select_width (number; default True):
    Determine whether the dropdown menu and the select input are the
    same width. Default set min-width same as input. Will ignore when
    value less than select width. False will disable virtual scroll.

- filter_option (boolean; default True):
    If True, filter options by input, if function, filter options
    against it. The function will receive two arguments, inputValue
    and option, if the function returns True, the option will be
    included in the filtered set; Otherwise, it will be excluded.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- n_blur (number; default 0):
    Called when leaving the component.

- n_change (number; default 0):
    Called when selecting an option or changing an input value.

- n_clear (number; default 0):
    Called when a option is selected. param is option's value and
    option instance.

- n_dropdown_visible_change (number; default 0):
    Call when dropdown open.

- n_focus (number; default 0):
    Called when entering the component.

- n_search (number; default 0):
    Called when searching items.

- n_select (number; default 0):
    Called when a option is selected. param is option's value and
    option instance.

- not_found_content (string; default 'Not Found'):
    Specify content to show when no result matches.

- open (boolean; optional):
    Controlled open state of dropdown.

- options (list of dicts; optional):
    Select options. Will get better perf than jsx definition.

    `options` is a list of dicts with keys:

    - label (string; required)

    - value (string; required)

- placeholder (string; optional):
    The placeholder of input.

- popup_class_name (string; optional):
    The className of dropdown menu.

- status (a value equal to: 'error', 'warning'; optional):
    Set validation status.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- value (string; optional):
    Selected option."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_antd'
    _type = 'AutoComplete'
    @_explicitize_args
    def __init__(self, children=None, allow_clear=Component.UNDEFINED, auto_focus=Component.UNDEFINED, backfill=Component.UNDEFINED, default_active_first_option=Component.UNDEFINED, default_open=Component.UNDEFINED, default_value=Component.UNDEFINED, disabled=Component.UNDEFINED, popup_class_name=Component.UNDEFINED, dropdown_match_select_width=Component.UNDEFINED, filter_option=Component.UNDEFINED, not_found_content=Component.UNDEFINED, open=Component.UNDEFINED, options=Component.UNDEFINED, placeholder=Component.UNDEFINED, status=Component.UNDEFINED, value=Component.UNDEFINED, n_blur=Component.UNDEFINED, n_change=Component.UNDEFINED, n_dropdown_visible_change=Component.UNDEFINED, n_focus=Component.UNDEFINED, n_search=Component.UNDEFINED, n_select=Component.UNDEFINED, n_clear=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'allow_clear', 'auto_focus', 'backfill', 'class_name', 'default_active_first_option', 'default_open', 'default_value', 'disabled', 'dropdown_match_select_width', 'filter_option', 'key', 'n_blur', 'n_change', 'n_clear', 'n_dropdown_visible_change', 'n_focus', 'n_search', 'n_select', 'not_found_content', 'open', 'options', 'placeholder', 'popup_class_name', 'status', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'allow_clear', 'auto_focus', 'backfill', 'class_name', 'default_active_first_option', 'default_open', 'default_value', 'disabled', 'dropdown_match_select_width', 'filter_option', 'key', 'n_blur', 'n_change', 'n_clear', 'n_dropdown_visible_change', 'n_focus', 'n_search', 'n_select', 'not_found_content', 'open', 'options', 'placeholder', 'popup_class_name', 'status', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AutoComplete, self).__init__(children=children, **args)
