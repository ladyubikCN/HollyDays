import flet
from datetime import datetime

_credits_text = None
_departures_column = None
_arrivals_column = None
_dates_column = None
_nights_column = None
_passengers_column = None

def add_selection_section(page):
    global _credits_text
    global _departures_column
    global _arrivals_column
    global _dates_column
    global _nights_column
    global _passengers_column

    selection_container = flet.Container(width=360)
    selection_container.bgcolor = "#1A365D"
    selection_container.padding = flet.Padding.only(left=80, top=40, bottom=0, right=20)

    selection_items = flet.Column(expand=True, spacing = 20, scroll=flet.ScrollMode.AUTO)

    _credits_text = flet.Text("Crediti richiesti: 0", 
                              color=page.theme.color_scheme.primary, 
                              size=15, 
                              weight=flet.FontWeight.BOLD,
                              text_align=flet.TextAlign.CENTER)
    _credits_tooltip = flet.Text("Se ripeti la stessa ricerca entro un'ora sarà gratuita", 
                                  color=page.theme.color_scheme.primary, 
                                  size=12, 
                                  weight=flet.FontWeight.BOLD,
                                  text_align=flet.TextAlign.CENTER)
    _departures_column = flet.Column()
    _arrivals_column = flet.Column()
    _dates_column = flet.Column()
    _nights_column = flet.Column()
    _passengers_column = flet.Column()

    selection_items.controls.extend([flet.Container(content=flet.Column(
                                                        [_credits_text,
                                                         _credits_tooltip],
                                                         horizontal_alignment=flet.CrossAxisAlignment.CENTER, 
                                                    ), 
                                                    bgcolor=page.theme.color_scheme.secondary, 
                                                    alignment=flet.Alignment.CENTER,
                                                    margin=flet.Margin.only(bottom=20),
                                                    padding=10, border_radius=5),
                                     flet.Text("Partenze Selezionate", color=page.theme.color_scheme.on_primary, size=15, weight=flet.FontWeight.BOLD), 
                                     _departures_column, 
                                     flet.Text("Destinazioni Selezionate", color=page.theme.color_scheme.on_primary, size=15, weight=flet.FontWeight.BOLD),
                                     _arrivals_column, 
                                     flet.Text("Date Selezionate", color=page.theme.color_scheme.on_primary, size=15, weight=flet.FontWeight.BOLD),
                                     _dates_column, 
                                     flet.Text("Notti Selezionate", color=page.theme.color_scheme.on_primary, size=15, weight=flet.FontWeight.BOLD),
                                     _nights_column, 
                                     flet.Text("Passeggeri Selezionati", color=page.theme.color_scheme.on_primary, size=15, weight=flet.FontWeight.BOLD),
                                     _passengers_column])

    selection_container.content = selection_items

    return selection_container

def remove_departure(e, state):
    chip = e.control
    state.remove_departure_airport(chip.label.controls[0].value)


def refresh_selected_departures(state, page):
    _departures_column.controls.clear()
    
    for airport in state.selected_departure_airports:
        place_text = flet.Text(
                        state.selected_departure_airports[airport][0] + " - " + state.selected_departure_airports[airport][1] + " (" + airport + ")",
                        size=16,
                        color=page.theme.color_scheme.on_surface,
                    ) 

        name_text = flet.Text(
                        state.selected_departure_airports[airport][2],
                        size=10,
                        color=page.theme.color_scheme.on_surface,
                    )

        both_texts = flet.Column([place_text, name_text], spacing=0, horizontal_alignment=flet.CrossAxisAlignment.CENTER)
        
        chip = flet.Chip(
            both_texts,
            bgcolor=page.theme.color_scheme.surface_container,
            delete_icon=flet.Icon(
                flet.Icons.CLOSE,
                size=18,
            ),
            delete_icon_color=page.theme.color_scheme.on_surface,
            padding=flet.Padding.symmetric(horizontal=8, vertical=6),
            on_delete=lambda e: remove_departure(e, state),
            expand=True
        )
        _departures_column.controls.append(chip)
    _departures_column.update()

def remove_arrival(e, state):
    chip = e.control
    state.remove_arrival_airport(chip.label.controls[0].value)

def refresh_selected_arrivals(state, page):
    _arrivals_column.controls.clear()
    for airport in state.selected_arrival_airports:
        place_text = flet.Text(
                            state.selected_arrival_airports[airport][0] + " - " + state.selected_arrival_airports[airport][1] + " (" + airport + ")",
                            size=16,
                            color=page.theme.color_scheme.on_surface,
                        ) 

        name_text = flet.Text(
                                state.selected_arrival_airports[airport][2],
                                size=10,
                                color=page.theme.color_scheme.on_surface,
                            )
        
        both_texts = flet.Column([place_text, name_text], spacing=0, horizontal_alignment=flet.CrossAxisAlignment.CENTER)

        chip = flet.Chip(
                    both_texts,
                    bgcolor=page.theme.color_scheme.surface_container,
                    delete_icon=flet.Icon(
                        flet.Icons.CLOSE,
                        size=18,
                    ),
                    delete_icon_color=page.theme.color_scheme.on_surface,
                    padding=flet.Padding.symmetric(horizontal=8, vertical=6),
                    on_delete=lambda e: remove_arrival(e, state),
                    expand=True
                )
        
        _arrivals_column.controls.append(chip)

    _arrivals_column.update()

def remove_selected_dates(e, state):
    chip = e.control
    if chip in _dates_column.controls:
        _dates_column.controls.remove(chip)
    start_date = datetime.strptime(chip.label.value.split("-")[0], "%d/%m/%y").date()
    end_date = datetime.strptime(chip.label.value.split("-")[1], "%d/%m/%y").date()
    state.remove_selected_dates(start_date, end_date)

def refresh_selected_dates(start_date, end_date, state, page):
    state.add_selected_dates(start_date, end_date)
    _dates_column.controls.clear()
    for date_couple in state.selected_dates:
        text = flet.Text(
                            date_couple[0].strftime('%d/%m/%y') + "-" + date_couple[1].strftime('%d/%m/%y'),
                            size=16,
                            color=page.theme.color_scheme.on_surface,
                        ) 
        
        chip = flet.Chip(
                    text,
                    bgcolor=page.theme.color_scheme.surface_container,
                    delete_icon=flet.Icon(
                        flet.Icons.CLOSE,
                        size=18,
                    ),
                    delete_icon_color=page.theme.color_scheme.on_surface,
                    padding=flet.Padding.symmetric(horizontal=8, vertical=2),
                    on_delete=lambda e: remove_selected_dates(e, state),
                )
        
        _dates_column.controls.append(chip)   
    _credits_text.value = "Crediti richiesti: " + str(len(state.valid_date_couples))

def refresh_selected_nights(state, page):
    _nights_column.controls.clear()
    text = flet.Text("Da " + str(int(state.selected_nights_min)) + " a " + str(int(state.selected_nights_max)) + " notti",
                     size=16,
                     color=page.theme.color_scheme.on_surface,
                    )
    chip = flet.Container(
                        content=text,
                        bgcolor=page.theme.color_scheme.surface_container,
                        padding=flet.Padding.symmetric(horizontal=8, vertical=2),
                        border_radius=8, 
                    )
    _nights_column.controls.append(chip)

    _credits_text.value = "Crediti richiesti: " + str(len(state.valid_date_couples))

def refresh_selected_passengers(state, page):
    _passengers_column.controls.clear()
    text = flet.Text(str(int(state.selected_passengers)) + " passeggeri",
                     size=16,
                     color=page.theme.color_scheme.on_surface,
                    )
    chip = flet.Container(
                            content=text,
                            bgcolor=page.theme.color_scheme.surface_container,
                            padding=flet.Padding.symmetric(horizontal=8, vertical=2),
                            border_radius=8, 
                        )
    _passengers_column.controls.append(chip)        