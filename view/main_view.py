import flet
from .search_bar import add_search_bar
from .selection_section import add_selection_section
from .results_table import add_results_table

from model.app_state import AppState

def show_full_page(page: flet.Page):
    page.title = "Free Your Holiday"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = flet.Colors.GREY_100
    page.assets_dir = "../files"
    page.fonts = {
        # URL stabili e diretti presi dalle repo ufficiali di Google Fonts su GitHub
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf",
        "Fredoka": "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth%2Cwght%5D.ttf"
    }
    state = AppState()

    # 2. Definiamo il tema grafico completo
    page.theme = flet.Theme(
        use_material3=False,
        font_family="Poppins",  # Imposta Poppins come font predefinito
        slider_theme=flet.SliderTheme(
            thumb_color=flet.Colors.GREEN,
        ),
        color_scheme=flet.ColorScheme(
            # IL CUORE DELLA PALETTE POP
            #primary=flet.Colors.BLUE_ACCENT_400,       # Blu elettrico vibrante (bottoni principali, focus)
            primary="#1A365D",
            secondary=flet.Colors.ORANGE_500,          # Arancione acceso (accenti, notifiche, tasti speciali)
            
            # GESTIONE DEGLI SFONDI (Senza usare la vecchia voce 'background')
            surface=flet.Colors.GREY_100,               # Sfondo della pagina (grigio chiarissimo per far respirare il layout)
            surface_container=flet.Colors.WHITE,       # Sfondo della barra di ricerca e delle schede dei voli
            
            # COLORI DEL TESTO (In base a dove si trova)
            on_primary=flet.Colors.WHITE,              # Testo bianco sopra i bottoni blu elettrico
            on_secondary=flet.Colors.WHITE,            # Testo bianco sopra i dettagli arancioni
            on_surface=flet.Colors.BLUE_900,           # Testo blu notte scuro sopra gli sfondi chiari (super leggibile)
            
            # Colore dei bordi e degli elementi disattivi
            outline=flet.Colors.GREY_300,
        )
    )
    
    search_bar = add_search_bar(page, state)
    selection_section = add_selection_section(page)
    results_table = add_results_table(page) 
    selection_and_results = flet.Row(controls=[selection_section, results_table], expand=True, spacing=0)
    page.add(
        flet.SafeArea(
            content=flet.Column(
                controls=[
                    search_bar,
                    selection_and_results
                ],
            spacing=0, 
            expand=True
            ),
            expand=True
        )
    )

    page.update()


    



