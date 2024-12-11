from flask import Flask, request, render_template, send_file
import os
import tempfile

# Import functions from your existing script
from reference_conversion_tool import read_references, convert_to_endnote_format, write_endnote_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Get uploaded file and input format
        input_file = request.files['reference_file']
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

        return send_file(temp_file.name, as_attachment=True, download_name='output.xml')
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)