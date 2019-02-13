import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, flash, render_template, session, send_from_directory
from PIL import Image
import numpy as np
import imageio
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import datasets, models, transforms

UPLOAD_FOLDER = "static/images/uploads/"
ALLOWED_EXTENSIONS = set(['png','jpg', 'jpeg', 'gif'])

device = torch.device('cpu')

model = models.resnet50(pretrained=False).to(device)
model.fc = nn.Sequential(
    nn.Linear(2048, 128),
    nn.ReLU(inplace=True),
    nn.Linear(128, 2)).to(device)
model.load_state_dict(torch.load('models/cva_weights_second_model.h5', map_location='cpu'))
model.eval()

data_transforms = {
        'train':
        transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()]),
    'validation':
        transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])}



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class global_file():
    name = ''

@app.route("/")
def viz_page():
    #opens home page
    with open("templates/home.html", 'r') as viz_file:
        return viz_file.read()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No file!'
        if file and allowed_file(file.filename):
            global data_transforms
            global model
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img = Image.open(file)
            resized = torch.stack([data_transforms['validation'](img).to(device)])
            pred_logits_tensor = model(resized)
            pred_probs = F.softmax(pred_logits_tensor, dim=1).cpu().data.numpy()
            if pred_probs[0][0] > .50:
                result = 'not sweet'
                prob = '{:.0f}%'.format(100*pred_probs[0][0])
            else:
                result = 'sweet'
                prob = '{:.0f}%'.format(100*pred_probs[0][1])
            return render_template('is_it_sweet.html', filename=UPLOAD_FOLDER + filename,
                                  result=result, prob=prob)
#            if ypred == 1:
#                return redirect(url_for('success'))
#            else:
#                return redirect(url_for('failure'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

#@app.route('/success')
#def success():
#    filename = global_file.name
#    return render_template('success.html', filename=filename)

#@app.route('/failure')
#def failure():
#    filename = global_file.name
#    return render_template('fail.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
