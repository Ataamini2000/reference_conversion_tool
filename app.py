from flask import Flask, request, render_template, send_file
import os
import tempfile
import logging

# Import functions from your existing script
from reference_conversion_tool import read_references, convert_to_endnote_format, write_endnote_file

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Ensure that a file was uploaded
        if 'reference_file' not in request.files:
            return "No file uploaded", 400

        input_file = request.files['reference_file']
        if input_file.filename == '':
            return "No selected file", 400
        
        input_format = request.form['input_format'].lower()

        # Read references from the uploaded file
        content = input_file.read().decode('utf-8')
        references = read_references(content, input_format)

        # Convert to EndNote XML
        endnote_xml = convert_to_endnote_format(references)

        # Save to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
        temp_file.write(endnote_xml.encode('utf-8'))
        temp_file.close()

        # Log success
        logging.info(f"Conversion successful. File saved at {temp_file.name}")
        
        # Send the file to the client
        return send_file(temp_file.name, as_attachment=True, download_name='output.xml')

    except Exception as e:
        # Log the error with detailed traceback
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
