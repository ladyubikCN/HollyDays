import flet
from .selection_section import refresh_selected_passengers

def add_passenger(state, page):
    state.selected_passengers += 1
    refresh_selected_passengers(state, page)

def remove_passenger(state, page):
    state.selected_passengers -= 1
    refresh_selected_passengers(state, page)

def add_passengers_container(page, state):
    passengers_container = flet.Container(padding=flet.Padding.only(right=2), expand=True, bgcolor=flet.Colors.TRANSPARENT, margin=flet.Margin.only(top=-13))
    passengers_column = flet.Column(expand=True)
    passengers_column.controls.append(flet.Text("Passeggeri", color=page.theme.color_scheme.on_primary, size=18, weight=flet.FontWeight.BOLD))
    passengers_row = flet.Row(expand=True, margin=flet.Margin.only(top=10))
    passengers_row.controls.append(flet.ElevatedButton("-", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, style=flet.ButtonStyle(alignment=flet.Alignment.CENTER), on_click=lambda e:remove_passenger(state, page)))
    passengers_row.controls.append(flet.Text("1", color=page.theme.color_scheme.on_primary,))
    passengers_row.controls.append(flet.ElevatedButton("+", width=40, bgcolor=page.theme.color_scheme.on_primary, color=page.theme.color_scheme.primary, on_click=lambda e:add_passenger(state, page)))
    passengers_column.controls.append(passengers_row)
    passengers_container.expand = 2
    passengers_container.content=passengers_column

    return passengers_container