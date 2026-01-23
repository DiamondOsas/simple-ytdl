import flet as ft


class FletAPP(ft.Page):
    def __init__(self):
        super().__init__()
        self.title = "Test App"
        self.theme_mode = ft.ThemeMode.LIGHT
        self.height = 500
        self.width = 500


if __name__ == "__main__":
    ft.run(main=FletAPP)