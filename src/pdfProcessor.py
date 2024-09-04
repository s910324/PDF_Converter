import os 
import pdfUtils           as pdf
from   misc               import Debugger
from   PyQt5.QtCore       import QObject, pyqtSignal, QCoreApplication



debug    = Debugger()

class PDFProcessor(QObject):
    percentage = pyqtSignal(float)
    fileError  = pyqtSignal()
    def __init__(self, parent = None):
        super(PDFProcessor, self).__init__(parent)

    def process(self, filePath, watermark = "SAMPLE", 
        font_name  = "Helvetica-Bold", font_size    = 25, 
        fill_color = '#DD5555',        fill_opacity = 0.15, 
        x = -500, y = 500, rotate = 30, row = 15, column = 15, row_pitch = None, column_pitch = None):
        
        if not(os.path.isfile(filePath)):
            self.fileError.emit()
            debug.print("File not exist or format error")
            return

        self.percentage.emit(1)
        QCoreApplication.processEvents()

        template = pdf.watermark_template(watermark, font_name, font_size, fill_color, fill_opacity, x, y, rotate, row, column, row_pitch, column_pitch)
        self.percentage.emit(2)
        QCoreApplication.processEvents()

        temp_path = pdf.file_to_PDF(filePath)
        self.percentage.emit(50)
        QCoreApplication.processEvents()

        output_name = pdf.apply_watermark(filename = temp_path, mask_stream = template)
        self.percentage.emit(95)
        QCoreApplication.processEvents()

        if not(filePath.lower().endswith("pdf")):
            pdf.remove_temp(temp_path)
        self.percentage.emit(100.0)
        QCoreApplication.processEvents()

        debug.print(f"Done, PDF out : {output_name}")





if __name__ == '__main__':

    debug.debug = True
    filePath    = r'.\example_file\Project Delorean optical transceiver 20240902-MTK.pptx'
    filePath    = r'.\example_file\POROTECH 8-inch GaN-on-Si display panel process design rule 20240711.docx'
    filePath    = r'.\example_file\POROTECH 8-inch GaN-on-Si display panel process design rule 20240711.pdf'
    watermark   = "POROTECH CONFIDENTIAL"

    p = PDFProcessor()
    p.percentage.connect(lambda v :debug.print(v) )
    p.process( filePath, watermark = watermark)
    