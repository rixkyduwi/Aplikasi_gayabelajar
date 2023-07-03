from flask import Flask, flash, render_template,jsonify, redirect, request, url_for,session
from flask_mysqldb import MySQL
app = Flask(__name__)
from functools import wraps
import random
import string
from time import time
import time
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import joblib 

ALLOWED_EXTENSIONS = set(['xlsx'])
def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# time sesion
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="wis tak omongi ora rahasia"
    ))
a=time.localtime()
tanggal=""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
def convertTuple(tup):
    return ''.join([str(x) for x in tup])
def roles_required(role):
    def decorator(view_func):
        def wrapper(*args, **kwargs):
            if 'loggedin' in session:
            # User is loggedin show them the home page
                print(session['time'])
                if session['time'] != ""+str(time.gmtime().tm_year)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)+"":
                    print('session expired')
                    session.pop('loggedin', None)
                    session.pop('id', None)
                    session.pop('role', None)
                    session.pop('username', None)
                    session.pop('time', None)
                    return redirect(url_for('index'))
                if not session['role'] in role:
                    print('The user does not have this role.')
                    return render_template('403.html')
                else:
                    print(session['time'])
                    print(""+str(time.localtime().tm_year)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)+"")
                    print('The user is in this role.')
                    return view_func(*args, **kwargs)
            else:
                return redirect(url_for('index'))
 
        return wrapper
    return decorator
#Konfigurasi Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'databasegaya'
#Intialize MySQL
mysql = MySQL(app)

#SOURCE CODE CHATBOT
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot/model.h5')
import json
import random
intents = json.loads(open('chatbot/data.json').read())
words = pickle.load(open('chatbot/texts.pkl','rb'))
classes = pickle.load(open('chatbot/labels.pkl','rb'))

#FUNGSI LOGIN
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aksilogin", methods=["POST"])
def aksilogin():
    username = request.form["username"]
    password = request.form["password"]
    cur =  mysql.connection.cursor()
    cur.execute("Select id_login,no_induk, nama,kelas, level, password from login where nama = %s ",(username,)) 
    user = cur.fetchone()
    if user is not None and len(user) > 0:        
        session['loggedin']=True
        session['id'] = user[0]
        session['role'] = user[4]
        session['kelas'] = user[3]
        session['no_induk'] = user[1]
        session['username'] = user[2]
        session['time']= tanggal
        if password == user[5]:
            session['level'] = user[4]
            if user[4] == 'admin':
                return redirect(url_for('tampiladmin'))
            elif user[4] == "siswa":
                return redirect(url_for('viewsiswa'))
        else:
            flash("Gagal, username dan password tidak cocok")
            return redirect(url_for('login'))
    elif user == None:
        flash("Gagal, user tidak ditemukan")
        return redirect(url_for('login'))
    else:
        flash("Gagal, user tidak ditemukan")
        return redirect(url_for('login'))

@app.route("/login")
def login():
    return render_template("login1.html")
@app.route("/siswa")
@roles_required('siswa')
def viewsiswa():
    return render_template("siswa/view_siswa.html")
#@app.route("/admin/view_pernyataan")
#def insertPernyataan():
#   return render_template("admin/view_detail_hasil.html")   
#@app.route("/admin/home")
#def home():
 #   cur =  mysql.connection.cursor()
  #  cur.execute("Select * from login") 
   # home = cur.fetchall()    
    #print(home)
    #return render_template("admin/home.html", home=home) 
#CRUD ADMIN VIEW
@app.route("/admin/tampiladmin")
def tampiladmin():
    cur =  mysql.connection.cursor()
    cur.execute("Select * from login") 
    data = cur.fetchall()    
    print(data)
    return render_template("admin/tampil_admin.html", data=data) 
#CRUD ADMIN TAMBAH
@app.route("/admin/tambah", methods=['GET','POST'])
def tambahadmin(): 
    if request.method=='POST':
        no_induk= request.form['no_induk']
        nama = request.form['nama']
        kelas = request.form['kelas']
        password = request.form['password']
        level = request.form['level']
        cur =  mysql.connection.cursor()
        cur.execute("INSERT INTO login(no_induk,nama,kelas,password,level) values(%s,%s,%s,%s,%s) ",(no_induk,nama,kelas,password,level)) 
        mysql.connection.commit() 
        return redirect(url_for('tampiladmin')) 
    else:
        return render_template('admin/v_tambah_admin.html')     
#CRUD ADMIN HAPUS
@app.route("/admin/hapus/<id>")
def deleteadmin(id): 
    cur =  mysql.connection.cursor()
    cur.execute("delete from login where id_login= %s",(id,)) 
    mysql.connection.commit() 
    return redirect(url_for('tampiladmin'))
#CRUD ADMIN EDIT
@app.route("/admin/editadmin/<id_admin>", methods=['GET','POST'])
def editadmin(id_admin):
    cur= mysql.connection.cursor()
    if request.method=='POST':
        nama      = request.form['nama']
        kelas      = request.form['kelas']
        password  = request.form['password']
        level     = request.form['level']
        print(id_admin)
        cur.execute(' UPDATE login SET nama =%s,kelas =%s, password =%s, level=%s WHERE no_induk=%s',(nama,kelas,password,level,id_admin))
        mysql.connection.commit()
        # cur.close()
        return redirect(url_for('tampiladmin'))
    else:
        # cur = mysql.connection.cursor()
        cur.execute('SELECT id_login,no_induk,nama,kelas,password,level FROM login WHERE no_induk=%s ', (id_admin, ))
        editadmin=cur.fetchone()
        print(editadmin)
        return render_template("admin/v_editadmin.html", editadmin=editadmin)

# BAGIAN TAMPIL GAYA BELAJAR
@app.route("/admin/tampil_gb" , methods=['GET'])
def tampilgb():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jenis_gayabelajar")
    gayabelajar = cur.fetchall()
    cur.close()
    return render_template("admin/view_gayabelajar.html", gayabelajar=gayabelajar) 
#BAGIAN EDIT GAYA BELJAR
@app.route("/admin/editgayabelajar/<id_gayabelajar>", methods=['GET','POST'])
def editgayabelajar(id_gayabelajar):
    cur = mysql.connection.cursor()
    if request.method=='POST':
        saran = request.form['saran_belajar']
        sql = "UPDATE jenis_gayabelajar SET saran_belajar=%s WHERE id_gayabelajar=%s"
        val = (saran, id_gayabelajar )
        cur.execute(sql, val)
        mysql.connection.commit() 
        return redirect(url_for('tampilgb'))
    else:
        cur.execute("SELECT * FROM jenis_gayabelajar WHERE id_gayabelajar=%s", (id_gayabelajar))
        editgayabelajar = cur.fetchall()
        return render_template('admin/v_editgb.html',editgayabelajar=editgayabelajar)

#BAGIAN TAMPIL PERTANYAAN
@app.route("/admin/tampil_pertanyaan")
def tampil_pertanyaan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pertanyaan")
    pertanyaan  = cur.fetchall()
    cur.close()
    return render_template("admin/view_pertanyaan.html", pertanyaan=pertanyaan)    

#BAGIAN EDIT PERTANYAAN 
@app.route("/admin/editpertanyaan/<id_pertanyaan>", methods=['GET','POST'])
def editpertanyaan(id_pertanyaan):
    cur = mysql.connection.cursor()
    if request.method=='POST':
        kode_pertanyaan = request.form['kode_pertanyaan']
        print(kode_pertanyaan)
        pertanyaan = request.form['pertanyaan']
        print(pertanyaan)
        sql = "UPDATE pertanyaan SET kode_pertanyaan=%s, pertanyaan.pertanyaan=%s WHERE id_pertanyaan=%s"
        val = (kode_pertanyaan, pertanyaan,id_pertanyaan, )
        cur.execute(sql, val)
        mysql.connection.commit() 
        return redirect(url_for('tampil_pertanyaan'))
    else:
        cur.execute("SELECT * FROM pertanyaan WHERE id_pertanyaan=%s", (id_pertanyaan))
        editpertanyaan = cur.fetchall()
        return render_template('admin/v_editpertanyaan.html',editpertanyaan=editpertanyaan)
    
#LOGOUT
@app.route("/logout")
def logout():
    session['loggedin']=False
    session['id'] = ""
    session['role'] =""
    session['kelas'] = ""
    session['no_induk'] = ""
    session['username'] = ""
    session['time'] = ""
    session['level'] = ""
    return redirect(url_for("index"))

@app.route("/siswa/pertanyaan")
def pertanyaan():
    return render_template('siswa/view_siswa.html')
@app.route("/siswa/pertanyaan/insertHasil")
def pertanyaan_inserthasil():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pertanyaan")
    siswapertanyaan  = cur.fetchall()
    cur.close()
    return render_template("siswa/Ujian_Online.html", siswapertanyaan=siswapertanyaan)
#PREDIKSI
#manual
@app.route("/siswa/predict", methods=['POST'])
def predict():
    json =[]
    for i in range(1,21):
        jawaban = request.form['jawaban['+str(i)+']']
        json.append(int(jawaban))
    print(json)
    # A1 = request.form.get('A1')
    # A2 = request.form.get('A2')
    # A3 = request.form.get('A3')
    # A4 = request.form.get('A4')
    # A5 = request.form.get('A5')
    # A6 = request.form.get('A6')
    # A7 = request.form.get('A7')
    # A8 = request.form.get('A8')
    # A9 = request.form.get('A9')
    # A10 = request.form.get('A10')
    # A11 = request.form.get('A11')
    # A12 = request.form.get('A12')
    # A13 = request.form.get('A13')
    # A14 = request.form.get('A14')
    # A15 = request.form.get('A15')
    # A16 = request.form.get('A16')
    # A17 = request.form.get('A17')
    # A18 = request.form.get('A18')
    # A19 = request.form.get('A19')
    # A20 = request.form.get('A20')
    # #test_data= request.form [""]
    
    # print(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20)
    dataset = pd.read_excel("model/Acoba.xlsx")
    x = dataset.iloc[:,[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]].values
    y = dataset.iloc[:, -1].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y, random_state=1)
    classifier = GaussianNB()
    classifier.fit(x_train, y_train)
    test_data = json #jawaban hasil input
    test_data = np.array(test_data)
    test_data = test_data.reshape(1,-1)#
    print(test_data)
    file = open("model/model_baru.pkl","rb")
    trained_model = joblib.load(file)
    prediction = trained_model.predict(test_data)
    cur = mysql.connection.cursor()
    sql = "INSERT INTO hasil(Nama, no_induk,kelas, Tanggal_tes, Gaya_Belajar,status) VALUES(%s,%s,%s, %s,%s,%s)"
    val = (session['username'], session['no_induk'], session['kelas'],tanggal, prediction[0],'manual')
    cur.execute(sql, val)
    mysql.connection.commit()

    
    sql = "SELECT * from hasil"
    cur.execute(sql)
    jml_data = cur.fetchall()
    for i in range(1,20):
        print(i)
        sqll = "INSERT INTO detail_hasil(id_hasil,id_pertanyaan,nilai,status) VALUES(%s,%s,%s,%s)"
        id_hasil = i+len(jml_data)+1
        print(id_hasil)
        print(test_data[0][i])
        vall = (int(id_hasil),i,test_data[0][i],'manual')
        cur.execute(sqll, vall)
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT jenis_gayabelajar.gaya_belajar, jenis_gayabelajar.saran_belajar FROM  jenis_gayabelajar where id_gayabelajar = %s",(prediction[0],))
        a = cur.fetchone()
        data = (session['username'], a[0], a[1],tanggal)
        kembali = "/siswa"
        return render_template ('siswa/prediksi.html', data = data,kembali=kembali)
@app.route('/admin/prediksi/<id>')
def prediksiindex(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT hasil.Nama, jenis_gayabelajar.gaya_belajar, jenis_gayabelajar.saran_belajar, hasil.Tanggal_tes FROM hasil inner join jenis_gayabelajar on jenis_gayabelajar.id_gayabelajar = hasil.Gaya_belajar where hasil.id_hasil = %s",(id,))
    data = cur.fetchone()
    kembali = "/admin/tampiladmin"
    return render_template('siswa/prediksi.html',data=data,kembali=kembali)
@app.route('/admin/upload_file')
def uploadindex():
    cur =  mysql.connection.cursor()
    cur.execute("Select * from hasil") 
    data = cur.fetchall()   
    cur.execute("Select * from detail_hasil") 
    datadetail = cur.fetchall()   
    cur.execute("Select id_gayabelajar, gaya_belajar from jenis_gayabelajar") 
    gayabelajar = cur.fetchall()    
    print("coba")
    print(gayabelajar)
    return render_template('admin/uploadindex.html',data=data,datadetail=datadetail,gayabelajar=gayabelajar)

@app.route('/admin/hapusDataset/<id>')
def deletedataset(id):
    cur =  mysql.connection.cursor()
    cur.execute("update hasil set status='delete' where id_hasil= %s",(id,)) 
    cur.execute("update detail_hasil set status='delete' where id_hasil= %s",(id,)) 
    mysql.connection.commit() 
    return redirect(url_for('uploadindex'))
@app.route('/admin/predict', methods=["POST"])
def uploadfile():
    if 'upload' not in request.files:
        return jsonify({"msg":"tidak ada form upload"})
    file = request.files['upload']
    if file.filename == '':
        return jsonify({"msg":"tidak ada file excell yang dipilih"})
    if file and allowed_file(file.filename):
        df_siswa = pd.read_excel(file)
    #OTOMATIS EXCEL
        dataset = pd.read_excel("model/Acoba.xlsx")
        x = dataset.iloc[:,[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]].values
        y = dataset.iloc[:, -1].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y, random_state=1)
        classifier = GaussianNB()
        classifier.fit(x_train, y_train)
        file = open("model/model_baru.pkl","rb")
        trained_model = joblib.load(file)
        df_siswa_pred=df_siswa.iloc[:,3:23]
        print(df_siswa_pred.head())
        y_siswa_pred = trained_model.predict(df_siswa_pred)
        df_y_siswa_pred = pd.DataFrame(y_siswa_pred)
        df_y_siswa_pred=df_y_siswa_pred.rename(columns={0:'hasil Klasifikasi'})
        
        df_siswa_pred = pd.merge(df_siswa,df_y_siswa_pred,left_index=True, right_index=True)
        np_siswa_pred = df_siswa_pred.to_numpy()
        print(np_siswa_pred)
        print(y_siswa_pred[0])
        cur = mysql.connection.cursor()
        
        sql = "SELECT * from hasil"
        cur.execute(sql)
        jml_data = cur.fetchall()
        for i in range(len(np_siswa_pred)):
            sql = "INSERT INTO hasil(Nama, no_induk,kelas, Tanggal_tes, Gaya_Belajar,status ) VALUES(%s,%s,%s, %s,%s,%s)"
            print(np_siswa_pred[i][0])
            print(np_siswa_pred[i][1])
            print(np_siswa_pred[i][2])
            val = (np_siswa_pred[i][0], int(np_siswa_pred[i][1]),np_siswa_pred[i][2], tanggal, np_siswa_pred[i][-1],'aktif' )
            cur.execute(sql, val)
            mysql.connection.commit()
            
            for j in range(3,23):
                sqll = "INSERT INTO detail_hasil(id_hasil,id_pertanyaan,nilai,status) VALUES(%s,%s,%s,%s)"
                id_hasil = i+len(jml_data)+1
                vall = (int(id_hasil),j-2,np_siswa_pred[i][j],'aktif')
                cur.execute(sqll, vall)
                mysql.connection.commit()

        return redirect(url_for('uploadindex'))
        
    else:
        return jsonify({"msg":"format file harus xlsx "})

#BAGIAN HISTORI
@app.route("/admin/hasiltes/<id>")
def hasil(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_hasil,Nama, Tanggal_tes, Gaya_belajar FROM hasil where hasil.no_induk= %s ", (id,))
    data = cur.fetchall()
    print("jln")
    print(data)
    return render_template("admin/view_detail_hasil.html", data=data)
@app.route("/admin/rekap")
def rekap():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Count(*) from hasil where Gaya_Belajar = 0")
    audio = cur.fetchone()
    cur.execute("SELECT Count(*) from hasil where Gaya_Belajar = 1")
    kinestetik = cur.fetchone()
    cur.execute("SELECT Count(*) from hasil where Gaya_Belajar = 2")
    membacadanmenulis = cur.fetchone()
    cur.execute("SELECT Count(*) from hasil where Gaya_Belajar = 3")
    visual = cur.fetchone()
    value = [int(convertTuple(visual)),int(convertTuple(audio)),int(convertTuple(membacadanmenulis)),int(convertTuple(kinestetik))]
    return render_template('admin/rekap.html',value=value)
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

#@app.route("/rekap")
#def rekap():
 #   return render_template('admin/rekap.html')





