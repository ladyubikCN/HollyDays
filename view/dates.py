import flet
from .mini_range_calendar import MiniRangeCalendar
from .selection_section import refresh_selected_dates
from .anchor_menu import AnchorMenu
from .search_bar import refresh_cost

def show_calendar(e, page, dates_picker):
    page.overlay.append(dates_picker)
    dates_picker.update()  # Aggiorna il calendario
    page.update()   # 💡 FONDAMENTALE: Aggiorna la colonna che lo contiene!

def add_dates(page, state):
    def date_range_selected(start_date, end_date, state):
        refresh_selected_dates(start_date, end_date, state, page)
        refresh_cost(state)
        

    dates_container = flet.Container(padding=flet.Padding.only(right=2), bgcolor=flet.Colors.TRANSPARENT)
    date_column = flet.Column(expand=True, spacing=0)
    date_column.controls.append(flet.Text("Date", color=page.theme.color_scheme.on_primary, size=18, weight=flet.FontWeight.BOLD))
    dates_picker = MiniRangeCalendar(state, on_range_selected=date_range_selected)
    dates_button = flet.ElevatedButton("", 
                                       width=float("inf"), 
                                       height=55, 
                                       icon=flet.Icons.CALENDAR_MONTH,
                                       margin=flet.Margin.only(top=9, right=3),
                                       style=flet.ButtonStyle(
                                           side=flet.BorderSide(
                                           width=1,
                                           color=flet.Colors.WHITE,
                                        )))

    dates_research_menu = AnchorMenu(page, dates_button, dates_picker, False, True)
    '''dates_research_menu = flet.MenuBar(
        style=flet.MenuStyle(
            # Rende la barra trasparente così prende la forma del pulsante interno
            bgcolor=flet.Colors.TRANSPARENT,
            elevation=0,
        ),
        controls=[
            flet.SubmenuButton(
                # Questo è il testo del pulsante che l'utente vedrà a schermo
                content=flet.Text("Aggiungi Date", weight=flet.FontWeight.BOLD, expand=True),
                # Qui dentro inseriamo il tuo calendario come controllo del sottomenu
                controls=[
                    flet.Container(
                        content=dates_picker,
                        padding=5,
                        # Blocchiamo la larghezza per assicurarci che il sottomenu si apra delle dimensioni corrette
                        width=320, 
                    )
                ],
                style=flet.ButtonStyle(
                    shape=flet.RoundedRectangleBorder(radius=8),
                    # Puoi personalizzare i colori del "pulsante" qui
                    bgcolor=page.theme.color_scheme.surface_container,
                    color=page.theme.color_scheme.on_surface,
                ),
                expand=True
            ),
        ],
        expand=True
    )'''

    date_column.controls.append(dates_research_menu)
    
    dates_container.content = date_column
    dates_container.expand = 3
    
    return dates_container