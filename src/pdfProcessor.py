import os
import pdfUtils           as pdf
from   pathlib            import Path
from   misc               import Debugger
from   PyQt5.QtCore       import QObject, pyqtSignal, QCoreApplication



debug    = Debugger()

class PDFProcessor(QObject):
    finished   = pyqtSignal(str)
    percentage = pyqtSignal(float)
    fileError  = pyqtSignal()
    def __init__(self, parent = None):
        super(PDFProcessor, self).__init__(parent)

    def process(self, **kwards):
        filePath    = kwards.pop('filePath')
        parent_path = Path(os.path.realpath(__file__)).parent.parent.absolute()
        temp_path   = os.path.abspath(os.path.join(parent_path, "temp_files"))
        temp_file   = os.path.join( temp_path, f"{Path(filePath).stem}.pdf" )
        out_path    = os.path.abspath(os.path.join(os.path.dirname(filePath), f"{Path(filePath).stem}.pdf" ))
        Path(temp_path).mkdir(parents=True, exist_ok=True)
        
        if not(os.path.isfile(filePath)):
            self.fileError.emit()
            debug.print("File not exist or format error")
            return

        self.percentage.emit(5)
        QCoreApplication.processEvents()

        temp_file = pdf.file_to_PDF(filePath, temp_file)
        self.percentage.emit(60)
        QCoreApplication.processEvents()

        w, h      = pdf.pdf_src(temp_file)
        self.percentage.emit(70)
        QCoreApplication.processEvents()

        
        kwards    = kwards | {"page_w" : w, "page_h" : h}
        template  = pdf.watermark_template(**kwards)
        self.percentage.emit(80)
        QCoreApplication.processEvents()

        output_name = pdf.apply_watermark(filename = temp_file, mask = template, output_name = out_path)
        self.percentage.emit(95)
        QCoreApplication.processEvents()

        if not(filePath.lower().endswith("pdf")):
            pdf.remove_temp(temp_file)
        self.percentage.emit(100.0)
        self.finished.emit(output_name)
        QCoreApplication.processEvents()

        debug.print(f"Done, PDF out : {output_name}")





if __name__ == '__main__':

    debug.debug = True
    filePath    = r'..\example_files\example.pptx'
    # filePath    = r'.\src\example_files\example.docx'
    # filePath    = r'.\src\example_files\example.pdf'
    watermark   = "POROTECH \nCONFIDENTIAL"

    p = PDFProcessor()
    p.percentage.connect(lambda v :debug.print(v) )
    p.process( filePath = filePath, watermark = watermark, row = 4, column = 4)
    