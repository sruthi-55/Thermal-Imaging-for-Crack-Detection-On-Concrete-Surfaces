from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import torch
from torchvision import models
from torchvision import transforms
model = models.resnet18(pretrained=True)
model = models.resnet18()

# Load the pre-trained weights
model.load_state_dict(torch.load('./basemodel.pth'))
model.eval()

app = Flask(__name__, static_url_path='/static', static_folder='static')

mean_nums = [0.485, 0.456, 0.406]
std_nums = [0.229, 0.224, 0.225]
## Define data augmentation and transforms
chosen_transforms = {'train': transforms.Compose([
        transforms.RandomResizedCrop(size=227),
        transforms.RandomRotation(degrees=10),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean_nums, std_nums)
]), 'val': transforms.Compose([
        transforms.Resize(227),
        transforms.CenterCrop(227),
        transforms.ToTensor(),
        transforms.Normalize(mean_nums, std_nums)
]),
}
idx_to_class = {0:'Negative', 1:'Positive'}
def predict(model, test_image, print_class = False):
     # it uses the model to predict on test_image...
    transform = chosen_transforms['val']

    test_image_tensor = transform(test_image)
    if torch.cuda.is_available(): # checks if we have a gpu available
        test_image_tensor = test_image_tensor.view(1, 3, 227, 227).cuda()
    else:
        test_image_tensor = test_image_tensor.view(1, 3, 227, 227)

    with torch.no_grad():
        model.eval()
        # Model outputs log probabilities
        # this computes the output of the model
        out = model(test_image_tensor)
        # this computes the probability of each classes.
        ps = torch.exp(out)
        # we choose the top class. That is, the class with highest probability
        topk, topclass = ps.topk(1, dim=1)
        class_name = idx_to_class[topclass.cpu().numpy()[0][0]]
        if print_class:
            print("Output class :  ", class_name)
    return class_name
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    image_paths = []
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        crops = ["15","10","5"]
        image_paths = []
        for crop in crops:
            file_name = "output_" + crop + file.filename
            folder_name = "output_images_" + crop
            image_path = url_for('static', filename=f'.rsc/{folder_name}/{file_name}')
            image_paths.append(image_path)

        return jsonify({'image_paths': image_paths})

if __name__ == '__main__':
    app.run(debug=True)
