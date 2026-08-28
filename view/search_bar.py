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
from threading import Timer

_search_timer = None

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
    global _search_timer

    if _search_timer is not None:
        _search_timer.cancel()

        _search_timer = Timer(0.5, do_actual_search, args=[state, page])
        _search_timer.start()

def do_actual_search(state, page):
    show_loading()

    if cookies.get("credits_key"):
        state.credits_key = cookies.get("credits_key")

    if state.credits_key == "":
        show_error(page, "Inserisci la chiave nell'account")
        return

    if not state.credits_key in state.valid_keys:
        show_error(page, "Chiave non valida")
        return
    
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
    search_bar_container.padding = flet.Padding.only(left=80, top=30, right=80, bottom=30)
    
    search_bar = flet.Column(expand=True, spacing=20)
    filters_row = flet.Row(expand=True, spacing=0)
    
    departure_flights_container = add_departure_flights_container(page, state)
    arrival_flights_container = add_arrival_flights_container(page, state)
    dates_container = add_dates(page, state)
    nights_container = add_nights_container(page, state)
    passengers_container = add_passengers_container(page, state)

    filters_row.controls.append(departure_flights_container)    
    filters_row.controls.append(arrival_flights_container)    
    filters_row.controls.append(dates_container)
    filters_row.controls.append(nights_container)
    filters_row.controls.append(passengers_container)
    filters_row.controls.append(flet.Container(
                                    flet.Row(
                                        [flet.ElevatedButton(
                                            "Cerca", 
                                            bgcolor=page.theme.color_scheme.secondary, 
                                            color=page.theme.color_scheme.on_surface, 
                                            style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8), 
                                                                text_style=flet.TextStyle(weight=flet.FontWeight.BOLD, 
                                                                                        size=18),
                                                                    padding=flet.Padding.symmetric(horizontal=20)), 
                                            height=54,
                                            on_click=lambda e:search_flights(e, state, page)
                                        )]
                                    ), 
                                    expand=1, 
                                    padding=flet.Padding(top=27, left=-10),
                                    bgcolor=flet.Colors.TRANSPARENT
                                ))
    
    search_bar.controls.append(flet.Row(
                                [flet.Icon(flet.Icons.FLIGHT_TAKEOFF, color=page.theme.color_scheme.secondary, size=46), 
                                 flet.Column(
                                    [
                                        flet.Text("HollyDay...", 
                                                style=flet.TextStyle(font_family="Fredoka", 
                                                                     size=46, 
                                                                     weight=flet.FontWeight.BOLD, 
                                                                     color=page.theme.color_scheme.on_primary)), 
                                        flet.Text("Free Your Holiday", 
                                                 style=flet.TextStyle(font_family="Fredoka", 
                                                                      size=23, 
                                                                      weight=flet.FontWeight.NORMAL, 
                                                                      color=page.theme.color_scheme.on_primary))
                                        ],
                                        spacing=0),
                                        flet.Container(expand=True),
                                        flet.PopupMenuButton(icon=flet.Icons.LANGUAGE, 
                                                             icon_color=page.theme.color_scheme.on_primary, 
                                                             icon_size=36, 
                                                             tooltip="Lingua",
                                                             items=[
                                                                 flet.PopupMenuItem(
                                                                     content="Italiano",
                                                                     on_click=lambda e:change_language(state, "Italiano")
                                                                 )
                                                             ]),
                                        flet.PopupMenuButton(icon=flet.Icons.ACCOUNT_CIRCLE, 
                                                             icon_color=page.theme.color_scheme.on_primary, 
                                                             icon_size=36, 
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
    search_bar.controls.append(filters_row)
    search_bar_container.content = search_bar
    
    return search_bar_container

def change_language(state,lang):
    state.language = lang

def change_key(e, state):
    cookies.set("credits_key", e.control.value, expire=86400 * 30)
    state.credits_key = e.control.value


