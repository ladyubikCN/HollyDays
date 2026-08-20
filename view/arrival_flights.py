import flet
from .anchor_menu import AnchorMenu
from .selection_section import refresh_selected_arrivals

_arrivals_research_menu = None
_country_list = None
_airport_list = None
_countries_list_controls = []
_airports_list_controls = []

def show_country_list(page, state):
    global _country_list, _country_list_controls

    _country_list = flet.ListView(width=200, height=400, spacing=15, padding=flet.Padding.only(top=10))

    for country in state.selectable_arrival_countries:
        if country in state.airports and state.airports[country] != []:
            text = flet.Text(country[1] + " (" + country[0] + ")", data=country[1], on_tap=lambda e: add_arrival(e, state, page))
            _countries_list_controls.append(text)
            _country_list.controls.append(text)
    
    country_list_container = flet.Container(_country_list, bgcolor=page.theme.color_scheme.on_primary, border_radius=10, padding=flet.Padding.all(10))
    return country_list_container

def update_country_list(state):
    for control in _countries_list_controls:
            control.visible = control.data in state.selectable_arrival_countries.values()
                
    _country_list.update()

def show_airport_list(page, state):
    global _airport_list
    
    _airport_list = flet.ListView(width=300, height=400)
    all_selected_airports = [tup for tuple_list in state.airports.values() for tup in tuple_list]
    all_selected_airports = [
                v for v in sorted(all_selected_airports, key=lambda item: item[2])
            ]
    for airport in all_selected_airports:
        text = flet.Container(flet.Checkbox(airport[2] + " - " + airport[1] + " (" + airport[3] + ")", on_change=lambda e:add_arrival(e, state, page)), data=airport[3])
        _airport_list.controls.append(text)
        _airports_list_controls.append(text)

    airport_list_container = flet.Container(_airport_list, bgcolor=page.theme.color_scheme.on_primary, border_radius=10, padding=flet.Padding.all(10))

    return airport_list_container     

def update_airport_list(page, state):
    global _airports_list_controls
    
    selected_iata = {
        airport[3]
        for airports in state.selectable_arrival_airports.values()
        for airport in airports
    }
    
    for control in _airports_list_controls:
        control.visible = control.data in selected_iata
        
    _airport_list.update() 

def add_arrival(e, state, page):
    if e.control.value:
        state.add_arrival_airport(e.control.label)
    else:
        state.remove_arrival_airport(e.control.label)
        
    refresh_selected_arrivals(state, page)

def refresh_selectable_arrivals(e, state, page):
    state.filter_selectable_arrivals(e.control.value)
    update_country_list(state)
    update_airport_list(page, state)

def add_arrival_flights_container(page, state):
    global _arrivals_research_menu

    arrivals_container = flet.Container(padding=flet.Padding.only(right=2), bgcolor=flet.Colors.TRANSPARENT)
    arrival_column = flet.Column(expand=True)
    arrival_column.controls.append(flet.Text("Destinazioni", color=page.theme.color_scheme.on_primary, size=18, weight=flet.FontWeight.BOLD))
    arrivals_research = flet.TextField(hint_text="Paese, codice aeroporto o città", bgcolor=page.theme.color_scheme.surface_container, color=page.theme.color_scheme.on_surface, expand=True, on_focus=lambda e: _arrivals_research_menu.update(page), on_change=lambda e: refresh_selectable_arrivals(e, state, page))
    country_list_container = show_country_list(page, state)
    airport_list_container = show_airport_list(page, state)
    both_list_container = flet.Container(flet.Row([country_list_container, airport_list_container]), margin=flet.Margin(740, 210), width=950, height=420)
    _arrivals_research_menu = AnchorMenu(page, arrivals_research, both_list_container, False, True)
    arrival_column.controls.append(arrivals_research)
    arrivals_container.content = arrival_column
    arrivals_container.expand = 4
    
    return arrivals_container