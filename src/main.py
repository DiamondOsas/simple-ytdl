import flet as ft
# Assuming your local module exists
try:
    from yt.showdetails import get_video_details
except ImportError:
    # Placeholder for testing if module is missing
    def get_video_details(url): return ["Title", None, "Creator", 120]

async def main(page: ft.Page):
    page.title = "Simple YTDL"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.colors.RED)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # Initialize page data for session-like storage
    page.data = {}

    # UI Components
    logo_icon = ft.Icon(icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED, size=80, color=ft.colors.RED)
    
    url_input = ft.TextField(
        label="Paste video URL",
        hint_text="https://www.youtube.com/watch?v=...",
        width=600,
        border_radius=10,
        bgcolor=ft.colors.GREY_800,
    )

    async def show_details_click(e):
        url = url_input.value
        if not url:
            page.open(ft.SnackBar(ft.Text("Please enter a URL")))
            return

        video_details = get_video_details(url)
        
        if video_details:
            page.data["video_details"] = video_details
            page.go("/details")
        else:
            page.open(ft.SnackBar(ft.Text("Could not fetch details.")))

    download_button = ft.Button(
        "Show",
        icon=ft.icons.VISIBILITY,
        on_click=show_details_click,
        style=ft.ButtonStyle(bgcolor=ft.colors.RED, color=ft.colors.WHITE),
    )

    def video_details_view():
        details = page.data.get("video_details") if page.data else None
        title, thumbnail, creator, duration = details if details else ("Unknown", None, "Unknown", 0)

        return ft.View(
            "/details",
            [
                ft.AppBar(title=ft.Text("Video Details")),
                ft.Column(
                    [
                        ft.Image(src=thumbnail, width=300) if thumbnail else ft.Icon(ft.icons.IMAGE, size=100),
                        ft.Text(title, size=24, weight="bold"),
                        ft.Text(f"Creator: {creator}"),
                        ft.Button("Go Back", on_click=lambda _: page.go("/")),
                    ],
                    horizontal_alignment="center",
                )
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )

    async def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Simple YTDL")),
                    logo_icon,
                    ft.Text("Simple YouTube Downloader", size=32, weight="bold"),
                    url_input,
                    download_button,
                ],
                vertical_alignment="center",
                horizontal_alignment="center",
            )
        )
        if page.route == "/details":
            page.views.append(video_details_view())
        await page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.run(main)
