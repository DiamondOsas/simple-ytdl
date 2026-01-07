import flet as ft

def main(page):
    page.title = "Test App "
    hello = ft.Text("Type your note")
    box = ft.TextField()
    row1 = ft.Row(box)
    page.add(
        hello,
        row1
    ) 



if __name__ == "__main__":
    ft.run(main)