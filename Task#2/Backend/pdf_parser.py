import PyPDF2

class PDFParser:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
    
    def extract_text(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_file)
        extracted_text = ""
        
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""
        
        return extracted_text