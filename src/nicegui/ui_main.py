from nicegui import ui
# from taskListView import task_list
from watermarkSetup import watermark_setup



with ui.grid(columns='1fr 5fr'):
	watermark_setup()
	ui.upload(
		multiple = True,

		on_upload=lambda e: ui.notify(f'Uploaded {e.name}')
	).classes("w-full")
	

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()