import flet
from .anchor_menu import AnchorMenu

_departures_research_menu = None
_airport_list = None
_airports_list_controls = []

def show_airport_list(page, state):

    global _airport_list

    if page.width > 600:
        _airport_list = flet.ListView(width=500, height=400)
    else:
        _airport_list = flet.ListView(width=(page.width - 60), height=200)
        
    all_selected_airports = [tup for tuple_list in state.airports.values() for tup in tuple_list]
    all_selected_airports = [
                v for v in sorted(all_selected_airports, key=lambda item: item[2])
            ]
    for airport in all_selected_airports:
        text = flet.Container(flet.Checkbox(airport[0] + " - " + airport[2] + " - " + airport[1] + " (" + airport[3] + ")", 
                                            visual_density=flet.VisualDensity.COMPACT, 
                                            on_change=lambda e: add_departure(e, state, page),
                                            label_style=flet.TextStyle(color=page.theme.color_scheme.primary),
                                            check_color=page.theme.color_scheme.secondary,
                                            border_side=flet.BorderSide(width=2, color=flet.Colors.OUTLINE),), 
                                            data=airport[3])
        _airport_list.controls.append(text)
        _airports_list_controls.append(text)

    if page.width > 600:
        airport_list_container = flet.Container(_airport_list, 
                                            bgcolor=page.theme.color_scheme.on_primary, 
                                            border_radius=10, 
                                            padding=flet.Padding.all(10),
                                            margin=flet.Margin(370, 210))
    else:
        airport_list_container = flet.Container(_airport_list, 
                                                bgcolor=page.theme.color_scheme.on_primary, 
                                                border_radius=10, 
                                                padding=flet.Padding.all(10),
                                                margin=flet.Margin(20, 130))

    return airport_list_container    

def update_airport_list(page, state):
    global _airports_list_controls

    selected_iata = {
        airport[3]
        for airports in state.selectable_departure_airports.values()
        for airport in airports
    }
    
    for control in _airports_list_controls:
        control.visible = control.data in selected_iata
        
    _airport_list.update()    
    

def add_departure(e, state, page):
    if e.control.value:
        state.add_departure_airport(e.control.label)
    else:
        state.remove_departure_airport(e.control.label)
    #refresh_selected_departures(state, page)
    state.filter_selectable_arrivals("")

def sync_departure_checks(state):
    for container in _airports_list_controls:
        checkbox = container.content
        checkbox.value = container.data in state.selected_departure_airports.keys()

    _airport_list.update()

def refresh_selectable_departures(e, state, page):
    state.filter_selectable_departures(e.control.value)
    update_airport_list(page, state)
    
# add the TextField for country/airport research
def add_departure_flights_container(page, state):
    global _departures_research_menu

    departures_container = flet.Container(padding=flet.Padding.only(right=2), 
                                          bgcolor=flet.Colors.TRANSPARENT)
    departures_column = flet.Column(expand=True)
    if page.width > 600:
        departures_column.controls.append(flet.Text("Partenze", 
                                                    color=page.theme.color_scheme.on_primary, 
                                                    size=18, 
                                                    weight=flet.FontWeight.BOLD))
        border_radius=flet.BorderRadius.only(
                                                top_left=0,
                                                top_right=0,
                                                bottom_left=0,
                                                bottom_right=0
                                            )
    else:
        border_radius=flet.BorderRadius.only(
                                                top_left=8,
                                                top_right=8,
                                                bottom_left=0,
                                                bottom_right=0
                                            )
    departures_research = flet.TextField(hint_text="Paese, codice aeroporto o città", 
                                         bgcolor=page.theme.color_scheme.surface_container, 
                                         color=page.theme.color_scheme.on_surface, 
                                         expand=True, 
                                         border_radius=border_radius,
                                         on_change=lambda e: refresh_selectable_departures(e, state, page))

    if page.width <= 600:
        departures_research.dense = True

    airport_list_container = show_airport_list(page, state)
    _departures_research_menu = AnchorMenu(page, 
                                           departures_research, 
                                           airport_list_container, 
                                           False, 
                                           True)
    departures_column.controls.append(_departures_research_menu)

    departures_container.content = departures_column
    if page.width > 600:
        departures_container.expand = 4
    else:
        departures_container.expand = True
    
    return departures_container



