import flet
from datetime import datetime, timedelta
from model.cache import Cache

_table_rows = None
_results_container = None

def add_results_table(page):
    global _table_rows, _results_container

    header = flet.Container(content=flet.Row(
        controls=[
            flet.Text("Andata", expand=3, weight=flet.FontWeight.BOLD, text_align="center"),
            flet.Text("Ritorno", expand=3, weight=flet.FontWeight.BOLD, text_align="center"),
            flet.Text("Notti", expand=1, weight=flet.FontWeight.BOLD, text_align="center"),
            flet.Text("Prezzo", expand=1, weight=flet.FontWeight.BOLD, text_align="center"),
        ]
    ))
    header.bgcolor = page.theme.color_scheme.primary
    header.padding = 10

    # Avvolgiamo la tabella in una ListView o Column con scroll per evitare che esca dallo schermo
    _table_rows = flet.ListView(
        expand=True,
        spacing=0,
    )

    content = flet.Column(
        expand=True,
        spacing=0,
        controls=[
            header,
            flet.Container(content=_table_rows, bgcolor=page.theme.color_scheme.surface_container, expand=True)          # ListView(expand=True)
        ],
    )

    _results_container = flet.Container(expand=True, padding=flet.Padding.symmetric(horizontal=80), bgcolor=page.theme.color_scheme.primary)
    _results_container.content = content
    #_results_container.visible = False
    return _results_container

def refresh_results(flights, page):
    for outbound_flight, inbound_flight in flights:
        nights = (datetime.strptime(inbound_flight['departure_at'], "%Y-%m-%d %H:%M").date()
    - datetime.strptime(outbound_flight['departure_at'], "%Y-%m-%d %H:%M").date()).days
        times = datetime.strptime(outbound_flight['departure_at'], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M") + " - " + datetime.strptime(outbound_flight['arrival_at'], "%Y-%m-%d %H:%M").strftime("%H:%M")
        outbound_container = flet.Container(
                                flet.Row(controls=[
                                    flet.Image(outbound_flight['airline_logo'], 
                                               width=70, 
                                               height=70,
                                               fit="contain"),
                                    flet.Column([
                                        flet.Text(outbound_flight['origin_name'] + " - " + outbound_flight['destination_name']),
                                        flet.Text(times)],
                                        spacing=2,
                                        alignment=flet.MainAxisAlignment.CENTER,
                                        expand=True
                                    )]
                                ), expand=3)

        times = datetime.strptime(inbound_flight['departure_at'], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M") + " - " + datetime.strptime(inbound_flight['arrival_at'], "%Y-%m-%d %H:%M").strftime("%H:%M")
        inbound_container = flet.Container(
                                        flet.Row(controls=[
                                            flet.Image(inbound_flight['airline_logo'], 
                                               width=70, 
                                               height=70,
                                               fit="contain"),
                                            flet.Column([
                                                flet.Text(inbound_flight['origin_name'] + " - " + inbound_flight['destination_name']),
                                                flet.Text(times)],
                                                spacing=2,
                                                alignment=flet.MainAxisAlignment.CENTER,
                                                expand=True
                                            )]
                                        ), expand=3)

        row = flet.Container(
            padding=10,
            border=flet.Border.only(
                bottom=flet.BorderSide(1, flet.Colors.GREY_300)
            ),
            data={
                "price":outbound_flight['price'] + inbound_flight['price']
            },
            content=flet.Row(controls=[outbound_container, 
                                       inbound_container,
                                       flet.Text(str(nights), expand=1, text_align="center"),
                                       flet.Text(str(outbound_flight['price'] + inbound_flight['price']), weight=flet.FontWeight.BOLD, color=flet.Colors.GREEN_700, expand=1, text_align="center")
                                       ]
                            )
            )
        _table_rows.controls.append(row)
        
    # Rendiamo visibile la tabella e aggiorniamo la pagina
    _table_rows.controls.sort(
        key=lambda r: r.data["price"]
    )
    
    _table_rows.visible = True
    _results_container.visible = True
    page.update()

