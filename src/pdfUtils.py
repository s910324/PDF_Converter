
import os
from   io                   import BytesIO
from   PyPDF2               import PdfWriter, PdfReader
from   reportlab.pdfgen     import canvas
from   reportlab.lib.units  import mm, inch
from   reportlab.lib.colors import Color
import comtypes.client

def watermark_template( 
    watermark = "SAMPLE", 
    font_name = "Helvetica-Bold", font_size    = 25, 
    color     = '#DD5555',        fill_opacity = 0.15, 
    x = -500, y = 500, rotate = 30, row = 15, column = 15, row_pitch = None, column_pitch = None):

    row_pitch        = row_pitch    or int(font_size * 4) 
    column_pitch     = column_pitch or int(len(watermark) * font_size * 1.5) 
    fr, fg, fb       = tuple(int(color.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4))
    fill_color       = Color(fr, fg, fb, alpha = fill_opacity)
    mask_stream      = BytesIO()
    pagesize         = (20 * inch, 10 * inch) 
    watermark_canvas = canvas.Canvas(mask_stream, pagesize = pagesize)
    watermark_canvas.setFont(font_name, font_size)
    watermark_canvas.setFillColor(fill_color)
    watermark_canvas.rotate(rotate) 

    for r in range(row):
        for c in range(column):
            xi = x + column_pitch * (c  + ((r % 2) * 0.5))
            yi = y - row_pitch    * r
            watermark_canvas.drawString(xi, yi, watermark)
    watermark_canvas.rotate(-rotate) 
    watermark_canvas.save()

    mask_stream.seek(0)
    return mask_stream

def apply_watermark(filename, mask_stream, output_name = None, apply_front = False, apply_last = True):

    mask       = PdfReader(mask_stream)
    src        = PdfReader(filename)
    output     = PdfWriter()
    pages      = len(src.pages)
    start_page = 0     if apply_front else 1
    end_page   = pages if apply_last  else pages-1
    mark_pages = list(range(start_page, end_page, 1))

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

    application = None

    type_chek = filename.lower()

    if type_chek.endswith("ppt"):
        application = "Powerpoint"

    elif type_chek.endswith("pptx"):
        application = "Powerpoint"

    elif type_chek.endswith("doc"):
        application = "Word"

    elif type_chek.endswith("docx"):
        application = "Word"

    elif type_chek.endswith("pdf"):
        return filename

    else:
        return None

    try:
        filename = os.path.abspath(filename)
        if not output_name:
            output_name = f"{os.path.splitext(filename)[0]}.pdf"

        if   application == "Powerpoint":
            app  = comtypes.client.CreateObject("Powerpoint.Application", dynamic = True)
            app.Visible = 1
            deck = app.Presentations.Open(filename)
            deck.SaveAs(output_name, 32)

        elif application == "Word":
            app  = comtypes.client.CreateObject("Word.Application", dynamic = True)
            app.Visible = 1
            deck = app.Documents.Open(filename)
            deck.SaveAs(output_name, 17)
        deck.Close()

    except:
        output_name = None

    app.Quit()
    return output_name

def remove_temp(temp_path):
    try:
        os.remove(temp_path)
    except:
        pass


if __name__ == '__main__':
    filePath    = r'.\example_file\Project Delorean optical transceiver 20240902-MTK.pptx'
    filePath    = r'.\example_file\POROTECH 8-inch GaN-on-Si display panel process design rule 20240711.docx'
    filePath    = r'.\example_file\POROTECH 8-inch GaN-on-Si display panel process design rule 20240711.pdf'
    watermark   = "POROTECH CONFIDENTIAL"


    template    = watermark_template(watermark = watermark)
    temp_path   = file_to_PDF(filePath)
    output_name = apply_watermark(filename = temp_path, mask_stream = template)

    if not(filePath.lower().endswith("pdf")):
        remove_temp(temp_path)
