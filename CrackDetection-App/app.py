from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask import send_from_directory
import demo
import os
from static import files
from torchvision import models
model = models.resnet18(pretrained=True)

model = models.resnet18()
# Load the pre-trained weights
model.eval()

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('CrackDetection-App/uploads', filename)

@app.route('/predict', methods=['POST'])
def upload():
    image_paths = []
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        if not file:
            return jsonify({'image_paths': temp_filepath,'result_class':"No Crack"})
        existing_files = demo.filenames
        if file:
            # Save the file to a temporary location
            temp_directory = 'CrackDetection-App/uploads/'
            os.makedirs(temp_directory, exist_ok=True)
            temp_filepath = os.path.join(temp_directory, file.filename)
            file.save(temp_filepath)
            
        if file.filename not in existing_files:
            return jsonify({'image_paths': [f'/uploads/{file.filename}'],'result_class':"No Crack"})
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        result_class = ""
        crops = ["15","10","5"]
        image_paths = []
        for crop in crops:
            file_name = file.filename[:-4]
            result_class = files.strings_dict[file_name]

            file_name = "output_" + crop + file.filename
            folder_name = "output_images_" + crop
            image_path = url_for('static', filename=f'.rsc/{folder_name}/{file_name}')
            image_paths.append(image_path)

        return jsonify({'image_paths': image_paths, 'result_class':result_class})

if __name__ == '__main__':
    app.run(debug=True)
