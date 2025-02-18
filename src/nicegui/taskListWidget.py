from nicegui import ui

def  taskListWidget(i, file_path):
	file_name = f'{file_path.split("\\")[-1]}'
	with ui.row():
		findex_label = ui.label("#{i}")
		with ui.column():
			fname_label  = ui.label(file_name)
			fprog_bar    = ui.linear_progress()
		rmv_button  = ui.button(color='orange-8', icon='delete', on_click=lambda: ui.notify('You clicked me!'))

if __name__ in {"__main__", "__mp_main__"}:
	taskListWidget("C:\\1feavrgbthnyj23.asd")
	ui.run()