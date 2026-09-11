import flet
from .mini_range_calendar import MiniRangeCalendar
from .selection_section import refresh_selected_dates
from .anchor_menu import AnchorMenu

def show_calendar(e, page, dates_picker):
    page.overlay.append(dates_picker)
    dates_picker.update()  # Aggiorna il calendario
    page.update()   # 💡 FONDAMENTALE: Aggiorna la colonna che lo contiene!

def add_dates(page, state):
    def date_range_selected(start_date, end_date, state):
        refresh_selected_dates(start_date, end_date, state, page)
        
    dates_container = flet.Container(padding=flet.Padding.only(right=2), 
                                     bgcolor=flet.Colors.TRANSPARENT)
    date_column = flet.Column(expand=True, spacing=0)
    if page.width > 600:
        date_column.controls.append(flet.Text("Date", 
                                              color=page.theme.color_scheme.on_primary, 
                                              size=18, 
                                              weight=flet.FontWeight.BOLD))

    dates_picker = MiniRangeCalendar(state, page, on_range_selected=date_range_selected)
    if page.width > 600:
        dates_button = flet.ElevatedButton("", 
                                        width=float("inf"), 
                                        height=55, 
                                        icon=flet.Icons.CALENDAR_MONTH,
                                        icon_color=page.theme.color_scheme.primary,
                                        bgcolor=page.theme.color_scheme.on_primary,
                                        margin=flet.Margin.only(top=9, right=3),
                                        style=flet.ButtonStyle(
                                            side=flet.BorderSide(
                                            width=1,
                                            color=page.theme.color_scheme.primary,
                                            )))
    else:
        dates_button = flet.ElevatedButton("", 
                                        width=float("inf"), 
                                        height=46, 
                                        icon=flet.Icons.CALENDAR_MONTH,
                                        icon_color=page.theme.color_scheme.primary,
                                        bgcolor=page.theme.color_scheme.on_primary,
                                        style=flet.ButtonStyle(
                                            side=flet.BorderSide(
                                            width=1,
                                            color=page.theme.color_scheme.primary,
                                            )))

    dates_research_menu = AnchorMenu(page, dates_button, dates_picker, False, True)

    date_column.controls.append(dates_research_menu)
    
    dates_container.content = date_column

    if page.width > 600:
        dates_container.expand = 3
    else:
        dates_container.expand = True

    return dates_container