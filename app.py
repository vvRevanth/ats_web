from flask import Flask, request, jsonify
from PyPDF2 import PdfFileReader
import os

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfFileReader(pdf_file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
        return text
    except Exception as e:
        return str(e)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    
    pdf_file = request.files['pdf_file']
    
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(pdf_file)
        return jsonify({'text': text})
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
