import flet as ft
import inspect
import asyncio

async def main(page: ft.Page):
    with open("debug_output.txt", "w") as f:
        f.write(f"page.update is coroutine function? {inspect.iscoroutinefunction(page.update)}\n")
        f.write(f"page.add is coroutine function? {inspect.iscoroutinefunction(page.add)}\n")
        
        try:
            res = page.update()
            f.write(f"Result of page.update(): {res}\n")
            if inspect.isawaitable(res):
                f.write("Result is awaitable\n")
            else:
                f.write("Result is NOT awaitable\n")
        except Exception as e:
            f.write(f"Error calling page.update(): {e}\n")

    page.window_destroy()

if __name__ == "__main__":
    try:
        ft.run(target=main)
    except Exception as e:
        pass
