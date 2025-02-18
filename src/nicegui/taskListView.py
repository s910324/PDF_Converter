from nicegui import ui

def  task_list():

	ui.upload(
		multiple = True,

		on_upload=lambda e: ui.notify(f'Uploaded {e.name}')
	).classes('max-w-full')


if __name__ in {"__main__", "__mp_main__"}:
	taskListView()
	ui.run()