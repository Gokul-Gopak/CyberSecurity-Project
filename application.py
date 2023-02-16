import os
from flask import Flask
from flask.templating import render_template
from flask import request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from dataProcessing import *
from Threads import *
from flask import send_file
import time 
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt'])
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
  return render_template('home.html')

def resultE():
    return render_template('Result.html')

def resultD():
    return render_template('resultD.html')

@app.route('/encrypt/')
def EncryptInput():
  Segment()
  gatherInfo()
  HybridCrypt()
  return resultE()

@app.route('/decrypt/')
def DecryptMessage():
  st=time.time()
  HybridDeCrypt()
  et=time.time()
  print(et-st)
  trim()
  st=time.time()
  Merge()
  et=time.time()
  print(et-st)
  return resultD()

def start():
  content = open('./Secured.txt','r')
  content.seek(0)
  first_char = content.read(1) 
  if not first_char:
    return render_template('Empty.html')
  else:
    return render_template('Option.html')


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/return-files-key/')
def return_files_key():
  try:
    return send_file('./Secured.txt',attachment_filename='Secured.txt',as_attachment=True)
  except Exception as e:
    return str(e)

@app.route('/return-files-data/')
def return_files_data():
  try:
    return send_file('./Output.txt',attachment_filename='Output.txt',as_attachment=True)
  except Exception as e:
    return str(e)


@app.route('/data/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return render_template('Nofile.html')
    file = request.files['file']
    if file.filename == '':
      return render_template('Nofile.html')
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Secured.txt'))
      return start()
       
    return render_template('Invalid.html')
    
if __name__ == '__main__':
  app.run(debug=True)

