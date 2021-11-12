from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/interview_schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    names = db.Column(db.String(100))
    Start_time = db.Column(db.Time)
    End_time = db.Column(db.Time)
    def __init__(self, names, Start_time, End_time):
 
        self.names = names
        self.Start_time = Start_time
        self.End_time = End_time
 
    def __rep__(self):
        return '<Event %r>' % self.id
 

@app.route('/',methods=['GET'])
def index():
    return render_template('imp.html')
@app.route('/create',methods=['POST','GET'])
def create():
    if request.method == 'POST':
 
        name = request.form['emails']
        start = request.form['st']
        end = request.form['en']
 
 
        my_data = Data(name, start, end)
        db.session.add(my_data)
        db.session.commit()
        flash("Interview Schedule Added Successfully")
        
    return render_template('create.html')

@app.route('/view',methods=['GET','POST'])
def view():
    if request.method == 'GET': 
        return render_template('view.html',employees = Data.query.all())

@app.route('/edit',methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        #my_data = Data.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        name = request.form['email']
        start = request.form['stt']
        end = request.form['ent']
        my_data = Data(name, start, end)
        db.session.add(my_data)
        db.session.commit()
        #db.session.commit()
        flash("Interview Schedule Updated Successfully")
 
        return redirect(url_for('view'))
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Interview Schedule Deleted Successfully")
 
    return redirect(url_for('view'))

if __name__=="__main__":
    app.run(debug=True,port=8000)