from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)
client = MongoClient('mongodb+srv://maulanasyakhiya:X6Tx5vkB5TZUiCMo@cluster0.zsgjrxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    date = today.strftime('%Y-%m-%d')
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}'
    filesave_to = f'static/image/{filename}'
    file.save(filesave_to)
    
    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    profilesave_to = f'static/image/{profilename}'
    profile.save(profilesave_to)
    
    doc = {
        'profile': profilename,
        'file': filename,
        'title':title_receive,
        'content':content_receive,
        'date':date
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)