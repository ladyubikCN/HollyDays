import flet
import calendar
from datetime import datetime

class MiniRangeCalendar(flet.Container):
    def __init__(self, state, on_range_selected):
        super().__init__()
        self.state = state
        self.on_range_selected = on_range_selected # Funzione da chiamare quando il range è completo
        
        # Stato del calendario
        self.today = datetime.now().date()
        self.start_date = None
        self.end_date = None
        
        self.current_year = self.today.year
        self.current_month = self.today.month
        
        # Configurazione grafica del container esterno
        self.width = 320
        self.height = 340
        self.padding = 10
        self.bgcolor = flet.Colors.SURFACE_CONTAINER_HIGHEST
        self.border_radius = 12
        self.margin = flet.Margin(950, 210)
        
        # Griglia dei giorni (7 colonne per i giorni della settimana)
        self.giorni_grid = flet.GridView(
            runs_count=7,
            spacing=5,
            run_spacing=5,
            height=280,
            child_aspect_ratio=1.0
        )
        
        # Testo del month corrente
        self.month_text = flet.Text(weight=flet.FontWeight.BOLD)
        
        self.content = flet.Column([
            flet.Row([
                flet.IconButton(flet.Icons.CHEVRON_LEFT, on_click=self.previous_month),
                self.month_text,
                flet.IconButton(flet.Icons.CHEVRON_RIGHT, on_click=self.next_month),
            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN, height=30),
            # Riga dei giorni della settimana (L M M G V S D)
            flet.Row([
                flet.Text(g, size=11, weight=flet.FontWeight.BOLD, width=32, text_align=flet.TextAlign.CENTER) 
                for g in ["L", "M", "M", "G", "V", "S", "D"]
            ], alignment=flet.MainAxisAlignment.SPACE_AROUND, height=30),
            
            flet.Container(content=self.giorni_grid, height=220, width=300)
        ])
        
    def did_mount(self):
        # Disegna il month corrente solo quando il controllo è agganciato alla pagina
        self.draw_month(self.current_year, self.current_month)
    
    def gestisci_hover(self, e):
        e.control.style.bgcolor = flet.Colors.GREEN
        self.update()

    def draw_month(self, year, month):
        self.current_year = year
        self.current_month = month
        
        mesi_ita = ["", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        self.month_text.value = f"{mesi_ita[month]} {year}"
        
        self.giorni_grid.controls.clear()
        
        cal = calendar.Calendar(firstweekday=0)
        giorni_month = cal.monthdayscalendar(year, month)
        
        # Funzione factory interna per isolare il click di ogni singolo giorno in modo pulito
        def make_click_handler(d):
            return lambda e: self.manage_day_clic(d)
        
        for settimana in giorni_month:
            for giorno in settimana:
                if giorno == 0:
                    self.giorni_grid.controls.append(flet.Text(""))
                else:
                    data_corrente = datetime(year, month, giorno).date()
                    
                    bg = None
                    text_color = flet.Colors.ON_SURFACE
                    
                    if self.start_date and data_corrente == self.start_date:
                        bg = flet.Colors.PRIMARY 
                        text_color = flet.Colors.ON_PRIMARY
                    elif self.end_date and data_corrente == self.end_date:
                        bg = flet.Colors.PRIMARY 
                        text_color = flet.Colors.ON_PRIMARY
                    elif self.start_date and self.end_date and self.start_date < data_corrente < self.end_date:
                        bg = flet.Colors.PRIMARY_CONTAINER
                        text_color = flet.Colors.ON_PRIMARY_CONTAINER
                    
                    btn = flet.ElevatedButton(
                            str(giorno), # 💡 Il testo va passato come primo argomento posizionale!
                            style=flet.ButtonStyle(
                                bgcolor=bg,         # Applica il colore dinamico
                                color=text_color,   # Applica il colore del testo dinamico
                                shape=flet.RoundedRectangleBorder(radius=6),
                                padding=0 # 💡 Fondamentale: azzera il padding interno così i numeri a due cifre non vengono tagliati
                            ),
                            on_click=make_click_handler(data_corrente) # Usiamo on_tap del GestureDetector
                        )
                    self.giorni_grid.controls.append(btn)
        
        self.update()

    def manage_day_clic(self, data):
        print(f"Click su giorno: {data.strftime('%d/%m/%Y')}")
        
        if not self.start_date or self.end_date or data < self.start_date:
            self.start_date = data
            self.end_date = None
        else:
            self.end_date = data
            if self.on_range_selected:
                self.on_range_selected(self.start_date, self.end_date, self.state)
                
        self.draw_month(self.current_year, self.current_month)

    def previous_month(self, e):
        m = self.current_month - 1 if self.current_month > 1 else 12
        a = self.current_year if self.current_month > 1 else self.current_year - 1
        self.draw_month(a, m)

    def next_month(self, e):
        m = self.current_month + 1 if self.current_month < 12 else 1
        a = self.current_year if self.current_month < 12 else self.current_year + 1
        self.draw_month(a, m)