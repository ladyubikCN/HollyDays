import os
import flet
from view.main_view import show_full_page

def main():
    # Render assegna una porta dinamica tramite la variabile d'ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    
    # Usiamo flet.run invece di flet.app e ascoltiamo su host="0.0.0.0"
    flet.run(
        show_full_page, 
        view=flet.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=port
    )

if __name__ == "__main__":
    main()