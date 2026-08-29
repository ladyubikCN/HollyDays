import flet
class AnchorMenu(flet.Container):

    barrier = None
    popup = None

    def __init__(self, page, main_control, submenu_control, open_on_focus, open_on_click):
        super().__init__()

        if open_on_focus:
            main_control.on_focus = lambda e: self.open_overlay(page)

        if open_on_click:
            main_control.on_click = lambda e: self.open_overlay(page)

        self.barrier = flet.Container(expand=True, bgcolor=flet.Colors.TRANSPARENT, on_click=lambda e:self.close_overlay(page))
        self.popup = submenu_control
            
        self.content = main_control

    def open_overlay(self, page):
        self.close_overlay(page)
        if self.barrier not in page.overlay:
            page.overlay.append(self.barrier)
        if self.popup not in page.overlay:
            page.overlay.append(self.popup)
        page.update()

    def close_overlay(self, page):
        if self.popup in page.overlay:
            page.overlay.remove(self.popup)
        if self.barrier in page.overlay:
            page.overlay.remove(self.barrier)
        if type(self.content).__name__ == "TextField":
            self.content.value = ""

        page.update()

    def update(self, page):
        self.close_overlay(page)
        self.open_overlay(page)