from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self, chunk_size=1000, separators=None):
        self.chunk_size = chunk_size
        self.separators = separators or ["\n\n", "\n", " ", ""]
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=200,
            separators=self.separators
        )
        self.chunks = []

    def split(self, text):
        chunks = self.splitter.split_text(text)
        return chunks