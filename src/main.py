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
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # Initialize page data for session-like storage
    page.data = {}

    # UI Components
    logo_icon = ft.Icon(icon=ft.Icons.PLAY_CIRCLE_FILLED_OUTLINED, size=80, color=ft.Colors.RED)
    
    url_input = ft.TextField(
        label="Paste video URL",
        hint_text="https://www.youtube.com/watch?v=...",
        width=600,
        border_radius=10,
        bgcolor=ft.Colors.GREY_800,
    )

    async def show_details_click(e):
        url = url_input.value
        if not url:
            page.show_snack_bar(ft.SnackBar(ft.Text("Please enter a URL")))
            return

        video_details = get_video_details(url)
        
        if video_details:
            page.data["video_details"] = video_details
            await page.push_route("/details")
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Could not fetch details.")))

    download_button = ft.Button(
        content=ft.Text("Show"),
        icon=ft.Icons.VISIBILITY,
        on_click=show_details_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
    )

    async def go_home(e):
        await page.push_route("/")

    def video_details_view():
        details = page.data.get("video_details") if page.data else None
        title, thumbnail, creator, duration = details if details else ("Unknown", None, "Unknown", 0)

        return ft.View(
            route="/details",
            controls=[
                ft.AppBar(title=ft.Text("Video Details")),
                ft.Column(
                    [
                        ft.Image(src=thumbnail, width=300) if thumbnail else ft.Icon(icon=ft.Icons.IMAGE, size=100),
                        ft.Text(title, size=24, weight="bold"),
                        ft.Text(f"Creator: {creator}"),
                        ft.Button("Go Back", on_click=go_home),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Simple YTDL")),
                    logo_icon,
                    ft.Text("Simple YouTube Downloader", size=32, weight="bold"),
                    url_input,
                    download_button,
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        if page.route == "/details":
            page.views.append(video_details_view())
        await page.update()

    page.on_route_change = route_change
    await page.push_route(page.route)

if __name__ == "__main__":
    ft.run(main)
