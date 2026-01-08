import flet as ft
from yt.showdetails import get_video_details
from yt.download import download_video

def main(page: ft.Page):
    # Page Configuration
    page.title = "Simple YouTube Downloader"
    page.theme_mode = ft.ThemeMode.DARK # Dark mode for YouTube-like feel
    page.padding = 20
    page.window_width = 600
    page.window_height = 800

    # Function to handle button click and show details
    def show_video_details(e):
        url = url_input.value
        if not url:
            # Show error if no URL is provided
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a YouTube URL first!"))
            page.snack_bar.open = True
            page.update()
            return

        # Disable button while processing (optional, but good UX)
        search_button.disabled = True
        page.update()

        # Fetch video details using the imported function
        print(url)
        details = get_video_details(url)
        
        # Re-enable button
        search_button.disabled = False

        if details:
            title, thumbnail, creator, duration, qualities = details

            # Create options for the dropdown menu based on available qualities
            quality_options = []
            for q in qualities:
                quality_options.append(ft.dropdown.Option(q))

            # Dropdown component
            quality_dropdown = ft.Dropdown(
                label="Quality",
                options=quality_options,
                value=quality_options[0].key if quality_options else None,
                border_radius=10,
                width=200
            )

            # Download handler
            def handle_download(e):
                quality = quality_dropdown.value
                if not quality:
                    return
                
                page.snack_bar = ft.SnackBar(ft.Text(f"Starting download: {title} ({quality})..."))
                page.snack_bar.open = True
                page.update()

                res = download_video(url, quality)
                
                if res:
                    page.snack_bar = ft.SnackBar(ft.Text("Download Finished!"))
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Download Failed."))
                page.snack_bar.open = True
                page.update()

            download_button = ft.FloatingActionButton(
                icon=ft.Icons.DOWNLOAD,
                content="Download",
                on_click=handle_download,
                bgcolor=ft.Colors.RED_600,
            )

            # Create a stylish card for the video details
            video_card = ft.Container(
                content=ft.Column([
                    # Video Thumbnail
                    ft.Image(
                        src=thumbnail,
                        width=400,
                        height=225,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.Border.all(10)
                    ),
                    # Video Title
                    ft.Text(f"Title: {title}", size=16, weight=ft.FontWeight.BOLD),
                    # Creator and Duration
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.GREY),
                        ft.Text(f"Channel: {creator}", color=ft.Colors.GREY),
                        ft.Icon(ft.Icons.TIMER, size=16, color=ft.Colors.GREY),
                        ft.Text(f"Duration: {duration}", color=ft.Colors.GREY),
                    ], spacing=10),
                    # Dropdown and Download Button
                    ft.Row([
                        quality_dropdown,
                        download_button
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ], spacing=10),
                padding=15,
                border=ft.Border.all(1, ft.Colors.GREY_800),
                border_radius=10,
                bgcolor=ft.Colors.GREY_900,
            )

            # Add to results and clear input
            results_column.controls.append(video_card)
            url_input.value = ""
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Could not get video details. Check URL."))
            page.snack_bar.open = True
            page.update()

    # --- UI Layout ---

    # Header: Icon and Title
    header = ft.Row(
        controls=[
            ft.Image(src="yticon.png", width=50, height=50), # Icon from assets
            ft.Text("Simple YouTube Downloader", size=24, weight=ft.FontWeight.BOLD),
            # ft.Text("Opensource", size=7, )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    # Input Area: Custom TextField and Button
    url_input = ft.TextField(
        label="YouTube Link",
        hint_text="Paste your video URL here",
        border_radius=15,
        expand=True,
        prefix_icon=ft.Icons.LINK # Visual cue
    )

    search_button = ft.Button(
        content="Show",
        icon=ft.Icons.SEARCH,
        on_click=show_video_details,
        height=50, # Match text field height
    )

    input_row = ft.Row(
        controls=[url_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Results Area: Scrollable list of cards
    results_column = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=20
    )

    # Add components to the page
    page.add(
        header,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacer
        input_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacer
        results_column
    )

if __name__ == "__main__":
    # Start the app, pointing to the 'assets' directory for images
    ft.run(main=main, before_main=None, name="Diamond", host=None, port=0, view=None, assets_dir="assets")
