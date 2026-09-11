import flet
from .departure_flights import add_departure_flights_container
from .arrival_flights import add_arrival_flights_container
from .nights import add_nights_container
from .passengers import add_passengers_container
from .dates import add_dates
from .results_table import refresh_results
from .results_table import show_loading
from model.cache import Cache
import csv
from diskcache import Cache as DiskCache
from .selection_section import refresh_selected_departures
from .departure_flights import sync_departure_checks
from .selection_section import refresh_selected_arrivals
from .arrival_flights import sync_arrival_checks

cookies = DiskCache("./user_cookies")

def show_error(page, text):
    def close(e):
        error_dialog.open = False
        page.update()

    error_dialog = flet.AlertDialog(
        title=flet.Text("Errore!", color="red"),
        content=flet.Text(text),
        actions=[
            flet.TextButton("Chiudi", on_click=close)
        ],
        actions_alignment=flet.MainAxisAlignment.END,
    )

    page.overlay.append(error_dialog)
    error_dialog.open = True
    page.update()

def search_flights(e, state, page):
    show_loading()

    if cookies.get("credits_key"):
        state.credits_key = cookies.get("credits_key")

    if state.credits_key == "":
        show_error(page, "Inserisci la chiave nell'account")
        return

    if not state.credits_key in state.valid_keys:
        show_error(page, "Chiave non valida")
        return

    page.run_thread(do_search_work, e, state, page)

def do_search_work(e, state, page):
    f_cache = open("files/cache.csv", "r", encoding="utf-8")
    reader = csv.reader(f_cache)
    totale = sum(int(riga[2]) for riga in reader if riga[0] == state.credits_key)
    f_cache.close()
    if(totale >= 20):
        show_error(page, "Hai esaurito i crediti")
        return

    flights = state.find_flights_serpapi(state)
    cache = Cache()
    cache.save_research(state)

    refresh_results(flights, page)

def add_search_bar(page, state):
    search_bar_container = flet.Container()
    search_bar_container.bgcolor = page.theme.color_scheme.primary
    if page.width > 600:
        search_bar_container.padding = flet.Padding.only(left=80, top=30, right=80, bottom=30)
    else:
        search_bar_container.padding = flet.Padding.only(left=20, top=10, right=20, bottom=10)
    search_bar = flet.Column(expand=True, spacing=20)

    if page.width < 600: 
        filters = flet.Column(expand=True, spacing=0)
    else:
        filters = flet.Row(expand=True, spacing=0)
    
    departure_flights_container = add_departure_flights_container(page, state)
    arrival_flights_container = add_arrival_flights_container(page, state)
    dates_container = add_dates(page, state)
    nights_container = add_nights_container(page, state)
    passengers_container = add_passengers_container(page, state)

    filters.controls.append(departure_flights_container)    
    filters.controls.append(arrival_flights_container)    
    filters.controls.append(dates_container)

    if page.width > 600:
        filters.controls.append(nights_container)
        filters.controls.append(passengers_container)
    else:
        filters.controls.append(flet.Row([nights_container, passengers_container],
                                         spacing=0,
                                         expand=True))

    search_button = flet.ElevatedButton("Cerca", 
                                            bgcolor=page.theme.color_scheme.secondary, 
                                            color=page.theme.color_scheme.on_surface, 
                                            style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8), 
                                                                text_style=flet.TextStyle(weight=flet.FontWeight.BOLD, 
                                                                                        size=18),
                                                                    padding=flet.Padding.symmetric(horizontal=20)), 
                                            on_click=lambda e:search_flights(e, state, page))

    
    if page.width > 600:
        search_button.height = 54
        padding_top = 27
        padding_left = -10
    else:
        search_button.height = 40
        search_button.width = float("inf")
        search_button.expand = True
        padding_left=0
        padding_top = 5

    search_button_container = flet.Container(content=search_button,
                            expand=1, 
                            padding=flet.Padding(top=padding_top, left=padding_left),
                            bgcolor=flet.Colors.TRANSPARENT
                        ) 

    filters.controls.append(search_button_container)

    if page.width > 600:
        banner_font_size = 46
        icon_size = 36
    else:
        banner_font_size = 32
        icon_size = 24

    search_bar.controls.append(flet.Row(
                                [flet.Icon(flet.Icons.FLIGHT_TAKEOFF, 
                                           color=page.theme.color_scheme.secondary, 
                                           size=46), 
                                 flet.Column(
                                    [
                                        flet.Text("HollyDay...", 
                                                style=flet.TextStyle(font_family="Fredoka", 
                                                                     size=banner_font_size, 
                                                                     weight=flet.FontWeight.BOLD, 
                                                                     color=page.theme.color_scheme.on_primary)), 
                                        flet.Text("Free Your Holiday", 
                                                 style=flet.TextStyle(font_family="Fredoka", 
                                                                      size=int(banner_font_size / 2), 
                                                                      weight=flet.FontWeight.NORMAL, 
                                                                      color=page.theme.color_scheme.on_primary))
                                        ],
                                        spacing=0),
                                        flet.Container(expand=True),
                                        flet.PopupMenuButton(icon=flet.Icons.LANGUAGE, 
                                                             icon_color=page.theme.color_scheme.on_primary, 
                                                             icon_size=icon_size, 
                                                             tooltip="Lingua",
                                                             items=[
                                                                 flet.PopupMenuItem(
                                                                     content="Italiano",
                                                                     on_click=lambda e:change_language(state, "Italiano")
                                                                 )
                                                             ]),
                                        flet.PopupMenuButton(icon=flet.Icons.ACCOUNT_CIRCLE, 
                                                             icon_color=page.theme.color_scheme.on_primary, 
                                                             icon_size=icon_size, 
                                                             tooltip="Account",
                                                             items=[
                                                                 flet.PopupMenuItem(
                                                                     flet.TextField(
                                                                         password=True,
                                                                         can_reveal_password=True,
                                                                         on_change=lambda e:change_key(e,state),
                                                                     )
                                                                     
                                                                 )
                                                             ])
                                    ]))
    search_bar.controls.append(filters)
    if page.width > 600:
        search_bar.controls.append(flet.Text("Scegli e combina tutti gli aeroporti e tutti gli intervalli di date che vuoi!", 
                                         style=flet.TextStyle(color=page.theme.color_scheme.on_primary,
                                                              size=16)
                                        )
                               )
    else:
        search_bar.controls.append(flet.Text("Scegli e combina tutti gli aeroporti e tutti gli intervalli di date che vuoi!", 
                                                 style=flet.TextStyle(color=page.theme.color_scheme.on_primary,
                                                                      size=13),
                                                width=float("inf"),
                                                text_align=flet.TextAlign.CENTER                                 
                                            )
                                    )
    search_bar_container.content = search_bar

    state.subscribe_departure(lambda: refresh_selected_departures(state, page))
    state.subscribe_departure(lambda: sync_departure_checks(state))
    state.subscribe_arrival(lambda: refresh_selected_arrivals(state, page))
    state.subscribe_arrival(lambda: sync_arrival_checks(state))
    
    return search_bar_container

def change_language(state,lang):
    state.language = lang

def change_key(e, state):
    cookies.set("credits_key", e.control.value, expire=86400 * 30)
    state.credits_key = e.control.value


