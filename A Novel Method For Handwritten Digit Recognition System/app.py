import os
from flask import Flask,render_template,request,url_for ,flash
from recognizer import recognize
from werkzeug.utils import secure_filename 
app=Flask(__name__)



UPLOAD_FOLDER='static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) 
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
@app.route('/')
def main():
  return render_template('index.html')


@app.route('/predict',methods=['POST','GET'])
def predict():
  if request.method=="POST":
   
    file = request.files['photo'] 
    
          # if user does not select file, browser also 
          # submit an empty part without filename 
    if file.filename == '': 
      return render_template('recognize.html',not_found=True)
     
    if file and allowed_file(file.filename): 
      filename = secure_filename(file.filename) 
      #flash('file {} saved'.format(file.filename)) 
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
      
      best,img_name=recognize(file)
      
      
      return render_template('predict.html',best=best,img_name=img_name)
  else:
    return render_template('recognize.html')
if __name__=="__main__":
  app.run(debug=True)
