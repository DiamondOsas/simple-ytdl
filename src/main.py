import flet as ft
from yt.showdetails import get_video_details

def main(page):
    def send_item(e):
        items.controls.append(ft.Text(box.value))
        box.value = ""
        page.update()

    page.title = "TO DO LIST"   
    hello = ft.Text("Type your Item")
    items = ft.Column()
    box = ft.TextField()
    button  = ft.Button("Save", on_click=send_item)
    row1 = ft.Row(controls=[box, button])


    page.add(
        hello,
        items,
        row1
    ) 



if __name__ == "__main__":
    ft.run(main)