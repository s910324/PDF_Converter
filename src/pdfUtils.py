import math
import os
from   pathlib              import Path
from   io                   import BytesIO
from   PyPDF2               import PdfWriter, PdfReader
from   reportlab.pdfgen     import canvas
from   reportlab.lib.units  import mm, inch
from   reportlab.lib.colors import Color
import comtypes.client
import logging

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger()


def watermark_template( 
    watermark    = "SAMPLE", font_name = "Helvetica-Bold", font_size = 25, fill_color = '#DD5555',
    fill_opacity = 0.15, rotate = 30, row = 6, column = 6, page_w = None, page_h = None):
    watermark        = watermark.replace("\\n", "\n")
    mask_stream      = BytesIO()
    row_pitch        = (page_h / (row    -1 )) if (row    > 1) else 0
    column_pitch     = (page_w / (column -1 )) if (column > 1) else 0
    x                = (page_w / 2)  - (column_pitch * column) / 2
    y                = (page_h / 2)  - (row_pitch    *    row) / 2
     
    page_size        = (page_w, page_w) 
    lines            = watermark.split("\n")
    text_length      = max([len(line) for line in lines])
    fr, fg, fb       = tuple(int(fill_color.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
    fill_color       = Color(fr, fg, fb, alpha = fill_opacity)
    rad              = math.radians(rotate)
    watermark_canvas = canvas.Canvas(mask_stream, pagesize = page_size)
    watermark_canvas.setFont(font_name, font_size)
    watermark_canvas.setFillColor(fill_color)
    watermark_canvas.saveState()
    watermark_canvas.rotate(rotate) 

    for r in range(int(row)):
        for c in range(int(column)):
            xi = x + column_pitch * (c  + ((r % 2) * 0.5))
            yi = y + row_pitch    * r

            for l, line in enumerate(lines):
                lsp = (l * font_size)
                xl  = xi
                yl  = yi - (l * font_size)
                xr  =   xl * math.cos(rad) + yl * math.sin(rad) + math.sin(rad) * lsp
                yr  = - xl * math.sin(rad) + yl * math.cos(rad)
                watermark_canvas.drawCentredString(xr, yr, line)
    watermark_canvas.restoreState()
    watermark_canvas.save()

    mask_stream.seek(0)
    return PdfReader(mask_stream)

def pdf_src(filename):
    src        = PdfReader(filename)
    pages      = len(src.pages)
    boxes      = [src.pages[i].mediabox for i in range(pages)]
    page_w     = max([box.width  for box in boxes])
    page_h     = max([box.height for box in boxes])
    return page_w, page_h

def apply_watermark(filename, mask, output_name = None, apply_front = True, apply_last = True):
    src         = PdfReader(filename)
    pages       = len(src.pages)
    output      = PdfWriter()
    pages       = len(src.pages)
    apply_front = (pages == 1  ) or apply_front
    apply_last  = (pages == 1  ) or apply_last
    start_page  = 0     if apply_front else 1
    end_page    = pages if apply_last  else pages-1
    mark_pages  = list(range(start_page, end_page, 1))

    for i in range(pages):
        page = src.pages[i]
        if i in mark_pages:
            page.merge_page(mask.pages[0])
        output.add_page(page)

    if not output_name:
        output_name = f"{os.path.splitext(filename)[0]}_watermark.pdf"

    with open(output_name, "wb") as output_stream:
        output.write(output_stream)
    return output_name



def file_to_PDF(filename, output_name = None):
    filename   = os.path.abspath(filename)
    type_check = filename.lower()

    log.debug(f"File input {filename}")
    if not(os.path.isfile(filename)) : return None
    if type_check.endswith("pdf") : return filename

    try:
        if not output_name:
            output_name = f"{os.path.splitext(filename)[0]}.pdf"

        log.debug(f"file output {output_name}")

        fmt    = 0
        app    = None
        opener = None
        if type_check.endswith(("ppt", "pptx")):
            fmt         = 32
            app         = comtypes.client.CreateObject("Powerpoint.Application", dynamic = True)
            app.Visible = 1
            opener      = app.Presentations
            log.debug(f"File opener : Powerpoint.Application")

        elif type_check.endswith(("doc", "docx")):
            fmt         =  17
            app         = comtypes.client.CreateObject("Word.Application", dynamic = True)
            app.Visible = 1
            opener      = app.Documents
            log.debug(f"File opener : Word.Application")

        log.debug(f"File opened")
        deck = opener.Open(filename)
        deck.SaveAs(output_name, fmt)
        deck.Close()
        
    except Exception as e:
        output_name = None
        log.debug(f"File open error: {e}")

    if app : app.Quit()

    log.debug(f"File saved as {output_name}")
    return output_name

def remove_temp(temp_path):
    try:
        os.remove(temp_path)
    except:
        pass


if __name__ == '__main__':
    filePath    = r'..\example_files\example.pptx'
    # filePath    = r'.\src\example_files\example.docx'
    # filePath    = r'.\src\example_files\example.pdf'
    watermark   = "SAMPLE\nSecond line"
    
    temp_path   = os.path.abspath(r"..\temp_files")
    temp_file   = os.path.join(temp_path, f"{Path(filePath).stem}.pdf" )
    out_path    = os.path.abspath(os.path.join(os.path.dirname(filePath), f"{Path(filePath).stem}.pdf" ))
    Path(temp_path).mkdir(parents=True, exist_ok=True)
    temp_file   = file_to_PDF(filePath, temp_file)
    w, h        = pdf_src(temp_file)
    template    = watermark_template(watermark = watermark, page_w = w, page_h = h)
    output_name = apply_watermark(filename = temp_file, mask = template, output_name = out_path)

    if not(filePath.lower().endswith("pdf")):
        remove_temp(temp_file)
