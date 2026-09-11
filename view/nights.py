import flet
from .selection_section import refresh_selected_nights

_min_nights_text = None
_max_nights_text = None

def show_nights(e, state, page):
      state.selected_nights_min = e.control.start_value
      state.selected_nights_max = e.control.end_value
      refresh_selected_nights(state, page)
    
def add_night_from(state, page):
    state.selected_nights_min += 1
    state.compute_valid_dates()
    _min_nights_text.value = state.selected_nights_min
    refresh_selected_nights(state, page)

def remove_night_from(state, page):
    state.selected_nights_min -= 1
    state.compute_valid_dates()
    _min_nights_text.value = state.selected_nights_min
    refresh_selected_nights(state, page)

def add_night_to(state,page):
    state.selected_nights_max += 1
    state.compute_valid_dates()
    _max_nights_text.value = state.selected_nights_max
    refresh_selected_nights(state, page)

def remove_night_to(state, page):
    state.selected_nights_max -= 1
    state.compute_valid_dates()
    _max_nights_text.value = state.selected_nights_max
    refresh_selected_nights(state, page)

def add_nights_container(page, state):
    global _min_nights_text, _max_nights_text

    if page.width > 600:
        nights_container = flet.Container(padding=flet.Padding.only(right=2), 
                                        expand=True, 
                                        bgcolor=flet.Colors.TRANSPARENT)
    else:
        nights_container = flet.Container(expand=True, 
                                          bgcolor=flet.Colors.TRANSPARENT)
    
    nights_column = flet.Column(spacing=0, tight=True, expand=True)
    if page.width > 600:
        nights_column.controls.append(flet.Text("Notti", color=page.theme.color_scheme.on_primary, size=18, weight=flet.FontWeight.BOLD))
        nights_row_min = flet.Row(expand=True, margin=flet.Margin.only(top=10))
        nights_row_min.controls.append(flet.Text("Min", margin=flet.Margin.only(right=4), color=page.theme.color_scheme.on_primary))
        nights_row_min.controls.append(flet.ElevatedButton("-", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, style=flet.ButtonStyle(alignment=flet.Alignment.CENTER), on_click=lambda e:remove_night_from(state, page)))
        _min_nights_text = flet.Text("2", color=page.theme.color_scheme.on_primary)
        nights_row_min.controls.append(_min_nights_text)
        nights_row_min.controls.append(flet.ElevatedButton("+", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, on_click=lambda e:add_night_from(state, page)))
        nights_column.controls.append(nights_row_min)
        nights_row_max = flet.Row(expand=True, margin=flet.Margin.only(top=0))
        nights_row_max.controls.append(flet.Text("Max", color=page.theme.color_scheme.on_primary))
        nights_row_max.controls.append(flet.ElevatedButton("-", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, style=flet.ButtonStyle(alignment=flet.Alignment.CENTER), on_click=lambda e:remove_night_to(state, page)))
        _max_nights_text = flet.Text("4", color=page.theme.color_scheme.on_primary)
        nights_row_max.controls.append(_max_nights_text)
        nights_row_max.controls.append(flet.ElevatedButton("+", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, on_click=lambda e:add_night_to(state, page)))
        nights_column.controls.append(nights_row_max)
        nights_container.expand = 2
    else:
        nights_column = flet.TextField(hint_text="Notti", 
                                                 bgcolor=page.theme.color_scheme.surface_container, 
                                                 color=page.theme.color_scheme.on_surface, 
                                                 expand=True, 
                                                 on_change=print("Nights"),
                                                 border_radius=flet.BorderRadius.only(
                                                                                        top_left=0,
                                                                                        top_right=0,
                                                                                        bottom_left=8,
                                                                                        bottom_right=0
                                                                                    ),
                                                 dense=True)
         
    nights_container.content=nights_column

    return nights_container