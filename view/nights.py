import flet
from .selection_section import refresh_selected_nights

_min_nights_text = None
_max_nights_text = None
_bottom_sheet = None
nights_column = None

def show_nights(e, state, page):
    state.selected_nights_min = e.control.start_value
    state.selected_nights_max = e.control.end_value
    refresh_selected_nights(state, page)
    if page.width < 600:
        nights_column.content = "Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max)+ " notti"
    
def add_night_from(state, page):
    state.selected_nights_min += 1
    state.compute_valid_dates()
    _min_nights_text.value = state.selected_nights_min
    refresh_selected_nights(state, page)
    if page.width < 600:
        nights_column.content = "Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max)+ " notti"

def remove_night_from(state, page):
    state.selected_nights_min -= 1
    state.compute_valid_dates()
    _min_nights_text.value = state.selected_nights_min
    refresh_selected_nights(state, page)
    if page.width < 600:
        nights_column.content = "Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max)+ " notti"

def add_night_to(state,page):
    state.selected_nights_max += 1
    state.compute_valid_dates()
    _max_nights_text.value = state.selected_nights_max
    refresh_selected_nights(state, page)
    if page.width < 600:
        nights_column.content = "Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max)+ " notti"

def remove_night_to(state, page):
    state.selected_nights_max -= 1
    state.compute_valid_dates()
    _max_nights_text.value = state.selected_nights_max
    refresh_selected_nights(state, page)
    if page.width < 600:
        nights_column.content = "Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max)+ " notti"
    

def add_nights_container(page, state):
    global _min_nights_text, _max_nights_text, _bottom_sheet, nights_column

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
                                       value="Da " + str(state.selected_nights_min) + " a " + str(state.selected_nights_max) + " notti",
                                        bgcolor=page.theme.color_scheme.surface_container, 
                                        color=page.theme.color_scheme.on_surface, 
                                        expand=True, 
                                        on_focus=lambda e:open_night_filters(page),
                                        border_radius=flet.BorderRadius.only(
                                                                            top_left=0,
                                                                            top_right=0,
                                                                            bottom_left=8,
                                                                            bottom_right=0
                                                                        ),
                                        dense=True, read_only=True)

        __container = flet.Container(margin=flet.Margin.all(20))

        _max_nights_text = flet.Text(state.selected_nights_max, 
                                    expand=1,
                                    text_align=flet.TextAlign.CENTER)
        _min_nights_text = flet.Text(state.selected_nights_max, 
                                    expand=1,
                                    text_align=flet.TextAlign.CENTER)
        __container.content = flet.Column([
                                    flet.Text("Notti",
                                              width=float("inf"),
                                              text_align=flet.TextAlign.CENTER, 
                                              margin=flet.Margin.only(bottom=30),
                                              weight=flet.FontWeight.BOLD),
                                    flet.Row([flet.Text("Min", expand=3), 
                                            flet.ElevatedButton("-", 
                                                                expand=1,
                                                                on_click=lambda e:remove_night_from(state, page)), 
                                            _min_nights_text, 
                                            flet.ElevatedButton("+", 
                                                                expand=1, 
                                                                on_click=lambda e:add_night_from(state, page))],
                                            alignment=flet.CrossAxisAlignment.CENTER
                                            ),
                                    flet.Row([flet.Text("Max", expand=3), 
                                            flet.ElevatedButton("-", 
                                                                expand=1,
                                                                on_click=lambda e: remove_night_to(state, page)), 
                                            _max_nights_text, 
                                            flet.ElevatedButton("+", 
                                                                expand=1,
                                                                on_click=add_night_to(state,page))],
                                            alignment=flet.CrossAxisAlignment.CENTER
                                            ),
                                    flet.Container(expand=True),
                                    flet.ElevatedButton("OK", 
                                                        on_click=lambda e:close_night_filters(page), 
                                                        width=float("inf"),
                                                        )])
    
        _bottom_sheet = flet.BottomSheet(__container)
        _bottom_sheet.open = False
        page.overlay.append(_bottom_sheet)
         
    nights_container.content=nights_column

    return nights_container

def open_night_filters(page):    
    _bottom_sheet.open = True
    page.update()

def close_night_filters(page):
    _bottom_sheet.open = False
    page.update()
    