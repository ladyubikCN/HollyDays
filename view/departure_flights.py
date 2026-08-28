import flet
from .anchor_menu import AnchorMenu
from .selection_section import refresh_selected_departures

_departures_research_menu = None
_country_list = None
_airport_list = None
_countries_list_controls = []
_airports_list_controls = []

def show_country_list(page, state):
    global _country_list

    _country_list = flet.ListView(width=200, height=400, spacing=15, padding=flet.Padding.only(top=10))
    for country in state.selectable_departure_countries.items():
        if country in state.airports and state.airports[country] != []:
            text = flet.Text(country[1] + " (" + country[0] + ")", data=country[1])
            _countries_list_controls.append(text)
            _country_list.controls.append(text)

    country_list_container = flet.Container(_country_list, 
                                            bgcolor=page.theme.color_scheme.on_primary, 
                                            border_radius=10, 
                                            padding=flet.Padding.all(10))

    return country_list_container

def update_country_list(state):

    for control in _countries_list_controls:
        if control.data in state.selectable_departure_countries.values():
            control.visible = True
        else:
            control.visible = False
            
    _country_list.update()

def show_airport_list(page, state):

    global _airport_list

    _airport_list = flet.ListView(width=500, height=400)
    all_selected_airports = [tup for tuple_list in state.airports.values() for tup in tuple_list]
    all_selected_airports = [
                v for v in sorted(all_selected_airports, key=lambda item: item[2])
            ]
    for airport in all_selected_airports:
        text = flet.Container(flet.Checkbox(airport[0] + " - " + airport[2] + " - " + airport[1] + " (" + airport[3] + ")", 
                                            visual_density=flet.VisualDensity.COMPACT, 
                                            on_change=lambda e: add_departure(e, state, page)), 
                                            data=airport[3])
        _airport_list.controls.append(text)
        _airports_list_controls.append(text)

    airport_list_container = flet.Container(_airport_list, 
                                            bgcolor=page.theme.color_scheme.on_primary, 
                                            border_radius=10, 
                                            padding=flet.Padding.all(10),
                                            margin=flet.Margin(370, 210))

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
    refresh_selected_departures(state, page)
    state.filter_selectable_arrivals("")

def refresh_selectable_departures(e, state, page):
    state.filter_selectable_departures(e.control.value)
    #update_country_list(state)
    update_airport_list(page, state)
    
# add the TextField for country/airport research
def add_departure_flights_container(page, state):
    global _departures_research_menu

    departures_container = flet.Container(padding=flet.Padding.only(right=2), bgcolor=flet.Colors.TRANSPARENT)
    departures_column = flet.Column(expand=True)
    departures_column.controls.append(flet.Text("Partenze", color=page.theme.color_scheme.on_primary, size=18, weight=flet.FontWeight.BOLD))
    departures_research = flet.TextField(hint_text="Paese, codice aeroporto o città", bgcolor=page.theme.color_scheme.surface_container, color=page.theme.color_scheme.on_surface, expand=True, on_focus=lambda e: _departures_research_menu.update(page), on_change=lambda e: refresh_selectable_departures(e, state, page))
    country_list_container = show_country_list(page, state)
    airport_list_container = show_airport_list(page, state)
    both_list_container = flet.Container(flet.Row([country_list_container, airport_list_container]), margin=flet.Margin(370, 210), width=450, height=420)
    #_departures_research_menu = AnchorMenu(page, departures_research, both_list_container, False, True)
    _departures_research_menu = AnchorMenu(page, departures_research, airport_list_container, False, True)
    departures_column.controls.append(_departures_research_menu)

    departures_container.content = departures_column
    departures_container.expand = 4
    
    return departures_container



