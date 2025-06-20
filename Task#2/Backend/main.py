from flask import Flask, request, jsonify
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf_parser import PDFParser
from text_splitter import TextSplitter
from embedder import Embedder
from Db.qdrant_manager import QdrantManager
from qdrant_handler import QdrantHandler
from retrieval_chain import RetrievalChain

app = Flask(__name__)

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    reset_collection = request.form.get('reset_collection', 'true').lower() == 'true'
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Query text is required'}), 400

    if reset_collection:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        parser = PDFParser(file)
        text = parser.extract_text()
        splitter = TextSplitter(chunk_size=1000)
        splitted_text = splitter.split(text)
        embedder = Embedder()
        embeddings = embedder.generate_embeddings(splitted_text)

        qdrant_handler = QdrantHandler(collection_name="pdf_rag", embeddings=embeddings, QdrantManager=QdrantManager)
        qdrant_handler.delete_collection()
        qdrant_handler.add_embeddings()
    else:
        embedder = Embedder()
        qdrant_handler = QdrantHandler(collection_name="pdf_rag", embeddings=None, QdrantManager=QdrantManager)

    retrieval_chain = RetrievalChain(qdrant_handler=qdrant_handler)

    answer = retrieval_chain.generate_answer(
        query_text=query,
        embedder=embedder
    )

    return jsonify({
        'message': 'Operation completed successfully',
        'result': answer
    }), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)