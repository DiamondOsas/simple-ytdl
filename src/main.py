import flet as ft
from src.yt.showdetails import get_video_details


def main(page: ft.Page):
    # Page configuration
    page.title = "Simple YTDL"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # UI Components
    logo_icon = ft.Icon(icon=ft.Icons.PLAY_CIRCLE_FILLED_OUTLINED, size=80, color=ft.Colors.RED)
    
    header_text = ft.Text(
        "Simple YouTube Downloader",
        size=32,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    sub_header = ft.Text(
        "Download your favorite videos easily",
        size=16,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER,
    )

    url_input = ft.TextField(
        label="Paste video URL",
        hint_text="https://www.youtube.com/watch?v=...",
        width=600,
        text_align=ft.TextAlign.LEFT,
        prefix_icon=ft.Icons.LINK,
        border_radius=10,
        bgcolor=ft.Colors.GREY_800,
    )

    def show_details_click(e):
        url = url_input.value
        if not url:
            page.show_snack_bar(ft.SnackBar(ft.Text("Please enter a URL"), open=True))
            return

        video_details = get_video_details(url)
        if video_details:
            page.go("/details")
            # This is a temporary way to pass data. In a real app, consider state management.
            page.session.set("video_details", video_details)
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Could not fetch video details. Check URL."), open=True))


    download_button = ft.Button(
        content=ft.Text("Show"),
        icon=ft.Icons.INFO,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=30),
            bgcolor=ft.Colors.RED,
            color=ft.Colors.WHITE,
        ),
        on_click=show_details_click,
    )

    # Main Layout
    main_container = ft.Column(
        controls=[
            logo_icon,
            header_text,
            sub_header,
            ft.Container(height=30),  # Spacer
            url_input,
            ft.Container(height=10),  # Spacer
            download_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Views
    def video_details_view(page: ft.Page):
        details = page.session.get("video_details")
        if not details:
            return ft.View(
                "/details",
                [
                    ft.AppBar(title=ft.Text("Video Details"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Text("No video details found. Please go back and try again."),
                    ft.ElevatedButton("Go Back", on_click=lambda e: page.go("/")),
                ]
            )
        
        title, thumbnail, creator, duration = details

        # Mock Download Button
        mock_download_button = ft.ElevatedButton(
            "Download (Mock)",
            icon=ft.Icons.DOWNLOAD,
            on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("Mock Download initiated!"), open=True)),
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
        )

        return ft.View(
            "/details",
            [
                ft.AppBar(title=ft.Text("Video Details"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.Column(
                    [
                        ft.Image(src=thumbnail, width=300, height=200, fit=ft.ImageFit.COVER) if thumbnail else ft.Container(),
                        ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Creator: {creator}" if creator else ""),
                        ft.Text(f"Duration: {duration} seconds" if duration else ""),
                        ft.Container(height=20),
                        mock_download_button,
                        ft.ElevatedButton("Go Back", on_click=lambda e: page.go("/")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Simple YTDL"), bgcolor=ft.colors.SURFACE_VARIANT),
                    main_container
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        if page.route == "/details":
            page.views.append(
                video_details_view(page)
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.run(main)
