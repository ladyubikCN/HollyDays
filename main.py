from view.main_view import show_full_page
import flet

def main():
    flet.app(show_full_page, view=flet.AppView.WEB_BROWSER, port=0)

main()