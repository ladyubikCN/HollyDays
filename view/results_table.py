import flet
from datetime import datetime, timedelta
from model.cache import Cache
import requests
import base64
import sqlite3
from model.database import Database

_table_rows = None
_results_container = None
_loading_container = None
_logo_cache = {}

def add_results_table(page):
    global _table_rows, _results_container, _loading_container

    _table_rows = flet.ListView(
        expand=True,
        spacing=0,
    )

    _loading_container = flet.Container(expand=True, 
                                        bgcolor=page.theme.color_scheme.primary,
                                        alignment=flet.Alignment.CENTER)
    _progress_icon = flet.ProgressRing(color=page.theme.color_scheme.on_primary, 
                                       width=100, 
                                       height=100)
    _loading_container.content=_progress_icon
    _loading_container.visible = False

    _results_container = flet.Stack(controls=[_table_rows, _loading_container], 
                                    expand=True)
    
    return _results_container

def get_airline_logo(url):
    
    if not url:
        return None
    
    if url in _logo_cache:
        return _logo_cache[url]

    db = Database()
    logo = db.get_logo(url)
    if logo:
        _logo_cache[url] = logo
        return _logo_cache[url]
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # Converti i byte dell'immagine in Base64
            img_b64 = base64.b64encode(response.content).decode("utf-8")
            _logo_cache[url] = img_b64
            db.set_logo(url, img_b64)
            return img_b64
    except Exception:
        pass
    return None

def show_loading():
    _loading_container.visible = True
    _loading_container.update()

def refresh_results(flights, page):
    page.run_thread(lambda: update_table(flights, page))

def update_table(flights, page):

    for outbound_flight, inbound_flight in flights:
        nights = (datetime.strptime(inbound_flight['departure_at'], "%Y-%m-%d %H:%M").date()
    - datetime.strptime(outbound_flight['departure_at'], "%Y-%m-%d %H:%M").date()).days
        times = datetime.strptime(outbound_flight['departure_at'], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M") + " - " + datetime.strptime(outbound_flight['arrival_at'], "%Y-%m-%d %H:%M").strftime("%H:%M")
        outbound_logo = get_airline_logo(outbound_flight['airline_logo'])
        outbound_container = flet.Container(
                                flet.Row(controls=[
                                    flet.Image(outbound_logo, 
                                               width=45, 
                                               height=45,
                                               fit="contain"),
                                    flet.Column([
                                        flet.Text(outbound_flight['origin'] + " - " + outbound_flight['destination'], 
                                                  size=18, 
                                                  text_align=flet.TextAlign.CENTER,
                                                  weight=flet.FontWeight.BOLD, 
                                                  ),
                                        flet.Text(outbound_flight['origin_name'] + " - " + outbound_flight['destination_name'], 
                                                  size=12, 
                                                  text_align=flet.TextAlign.CENTER,
                                                  ),
                                        flet.Text(times, 
                                                  size=14, 
                                                  text_align=flet.TextAlign.CENTER,
                                                  )],
                                        spacing=2,
                                        alignment=flet.MainAxisAlignment.CENTER,
                                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                        expand=True
                                    )],
                                ), expand=3)

        times = datetime.strptime(inbound_flight['departure_at'], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M") + " - " + datetime.strptime(inbound_flight['arrival_at'], "%Y-%m-%d %H:%M").strftime("%H:%M")
        inbound_logo = get_airline_logo(inbound_flight['airline_logo'])
        inbound_container = flet.Container(
                                        flet.Row(controls=[
                                            flet.Image(inbound_logo, 
                                               width=45, 
                                               height=45,
                                               fit="contain"),
                                            flet.Column([
                                                flet.Text(inbound_flight['origin'] + " - " + inbound_flight['destination'], 
                                                            size=18, 
                                                            text_align=flet.TextAlign.CENTER,
                                                            weight=flet.FontWeight.BOLD, 
                                                            ),
                                                flet.Text(inbound_flight['origin_name'] + " - " + inbound_flight['destination_name'], 
                                                            size=12, 
                                                            text_align=flet.TextAlign.CENTER,
                                                            ),
                                                flet.Text(times, 
                                                            size=14, 
                                                            text_align=flet.TextAlign.CENTER,
                                                            )],
                                                spacing=2,
                                                alignment=flet.MainAxisAlignment.CENTER,
                                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                expand=True
                                            )]
                                        ), expand=3)

        row = flet.Container(
            data={
                "price":outbound_flight['price'] + inbound_flight['price']
            },
            content=flet.Row(controls=[outbound_container, 
                                       inbound_container,
                                       flet.Text(str(nights) + " notti", expand=1, text_align="center"),
                                       flet.Text(str(outbound_flight['price'] + inbound_flight['price']) + " €", weight=flet.FontWeight.BOLD, color=flet.Colors.GREEN_700, expand=1, text_align="center")
                                       ]
                            ),
            bgcolor=flet.Colors.WHITE,
            padding=20,
            margin=flet.Margin.only(bottom=12),
            border_radius=12,
            border=flet.Border.all(1, flet.Colors.GREY_300),
            shadow=flet.BoxShadow(
                blur_radius=4,
                spread_radius=0,
                color=flet.Colors.with_opacity(0.05, flet.Colors.BLACK),
                offset=flet.Offset(0,2)
            )
        )
        _table_rows.controls.append(row)
        
    # Rendiamo visibile la tabella e aggiorniamo la pagina
    _table_rows.controls.sort(
        key=lambda r: r.data["price"]
    )
    
    _loading_container.visible = False

    page.update()

