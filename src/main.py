import flet as ft
from yt.showdetails import get_video_details

def main(page):
    def show_video_details(e):
        url = box.value
        if not url:
            return

        details = get_video_details(url)
        
        if details:
            title, thumbnail, creator, duration = details

            # Create controls to display details
            items.controls.append(
                ft.Column([
                    ft.Image(src=thumbnail, width=300, repeat=ft.ImageRepeat.NO_REPEAT, fit=ft.BoxFit.CONTAIN),
                    ft.Text(f"Title: {title}", weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"Channel: {creator}"),
                    ft.Text(f"Duration: {duration}"),
                ], spacing=5)
            )
            box.value = ""
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Could not get video details. Check URL."))
            page.snack_bar.open = True
            page.update()

    page.title = "Simple Youtube Downloder"   
    hello = ft.Text("Type your Item")
    items = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    box = ft.TextField(expand=True)
    button  = ft.Button("Show", on_click=show_video_details)
    row1 = ft.Row(controls=[box, button])


    page.add(
        hello,
        row1,
        items
    ) 



if __name__ == "__main__":
    ft.run(main)