from nicegui             import ui
from ex4nicegui          import rxui
from ex4nicegui          import to_ref, ref_computed, effect

from pathlib             import Path
from reportlab.pdfbase   import _fontdata

class Watermark_viewmodel (rxui.ViewModel):
    text     = "POROTECH CONFIDENTIAL"
    color    = "#DD8888"
    font     = 0
    opacity  = 40
    rotation = 30
    rows     = 6
    cols     = 7

def watermark_setup(viewmodel : Watermark_viewmodel = None):
    font_dict     = { i : f for i, f in enumerate(_fontdata.standardFonts)}
    table_label   = lambda text : rxui.label(text).classes('font-bold text-right self-center')
    input_theme   = 'input-class="text-center"'
    

    with ui.grid(columns='70px 300px').classes('w-full gap-2 align-middle'):
        table_label('Text:')
        wm_text = rxui.input(
            value = viewmodel.text
        ).props('clearable;' + input_theme)

        table_label('Color:')
        wm_color = ui.color_input(
            value     = viewmodel.color, 
            on_change = lambda e : wm_color.style(f'background-color:{e.value}')
        ).style(f'background-color: {viewmodel.color};').props(input_theme)

        table_label('Font:')
        wm_font = rxui.select(
            options    = font_dict, 
            with_input = True,
        ).props(input_theme).bind_value(viewmodel.font)


        table_label('Opacity:')
        wm_opacity = rxui.number(
            value     = viewmodel.opacity, 
            step      = 5,
            min       = 5,
            max       = 100,
            suffix    = "%",
            precision = 0
        ).props(input_theme)

        table_label('Rotation:')
        wm_opacity = rxui.number(
            value     = viewmodel.rotation, 
            step      = 1,
            min       = 0,
            max       = 360,
            suffix    = "deg",
            precision = 0
        ).props(input_theme)

        table_label('Rows:')
        wm_opacity = rxui.number(
            value     = viewmodel.rows, 
            step      = 1,
            min       = 1,
            max       = 50,
            suffix    = "row",
            precision = 0
        ).props(input_theme)

        table_label('Columns:')
        wm_opacity = rxui.number(
            value     = viewmodel.cols, 
            step      = 1,
            min       = 1,
            max       = 50,
            suffix    = "col",
            precision = 0
        ).props(input_theme)




if __name__ in {"__main__", "__mp_main__"}:
    vm = Watermark_viewmodel()
    watermark_setup(vm)
    ui.run()