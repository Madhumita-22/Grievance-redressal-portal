from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from flask_googlemaps import Map


engine = create_engine('postgresql://postgres:kgisl@localhost/solidwastemanagement')
app = Flask(__name__)

GoogleMaps(app, key="my-key")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kgisl@localhost/solidwastemanagement'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



@app.route("/user_login")
def userlogin():
	return render_template("user_login.html")
	

@app.route("/registerform")
def registerform():
	return render_template("user_signup.html")

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/registration")
def registration():
	return render_template("reg_success.html")
	
@app.route("/admin_registerform")
def admin_registerform():
	return render_template("admin_signup.html") 

@app.route("/authority_signup")
def authority_signup():
	return render_template("authority_signup.html")

@app.route("/authority_login")
def authority_login():
	return render_template("authority_login.html")


@app.route("/adminlogin")
def login1():
	return render_template("admin_login.html")

@app.route("/input")
def user_text():
	return render_template("user_text.html")

@app.route("/reply")
def reply():
	return render_template("reply.html")


@app.route("/area_check")
def authnotification():
	return render_template("area_check.html")

	
@app.route("/dashboard")
def dashboard():
	return render_template('user_check.html')

@app.route("/add_officer")
def addingofficer():
	return render_template("add_officer.html")	
	
@app.route("/enquiry")
def enquiry():
	return render_template("enquiry.html")

@app.route("/incharge")
def incharge():
	return render_template("incharge.html")	

@app.route("/notification")
def notification():
		return render_template('notification.html', Enquiry=Enquiry.query.all())

@app.route("/officerdetail")
def officerdetail():
	return render_template("officer_detail.html")	


@app.route("/usermsg")
def usermsg():
	return render_template("user_dashboard.html")	

@app.route("/auth_notification")
def auth_notification():
	return render_template("auth_notification.html")	
	
	
	
@app.route('/map', methods=["GET"])
def my_map():
    mymap = Map(

                identifier="view-side",

                varname="mymap",

                style="height:720px;width:1100px;margin:0;", # hardcoded!

                lat=37.4419, # hardcoded!

                lng=-122.1419, # hardcoded!

                zoom=15,

                markers=[(37.4419, -122.1419)] # hardcoded!

            )

    return render_template('map.html', mymap=mymap)
""" *****************************************DATA RETRIEVAL******************************** """   
@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		user=request.form['Area']
		return redirect(url_for('success',name=user))
	else:
		user=request.form['Area']
		return redirect(url_for('success',name=user))
		
@app.route('/drag/<name>')
def success(name):
	return render_template('officer_detail.html',add_officer=add_officer.query.filter_by(Area='%s'%name))


@app.route('/area',methods=['POST','GET'])
def area():
	if request.method=='POST':
		user=request.form['area']
		return redirect(url_for('success1',name=user))
	else:
		user=request.form['area']
		return redirect(url_for('success1',name=user))
		
@app.route('/dragarea/<name>')
def success1(name):
	return render_template('auth_notification.html',Enquiry=Enquiry.query.filter_by(Area='%s'%name))

@app.route('/usercheck',methods=['POST','GET'])
def usercheck():
	if request.method=='POST':
		user=request.form['Username']
		return redirect(url_for('success2',name=user))
	else:
		user=request.form['Username']
		return redirect(url_for('success2',name=user))
		
@app.route('/draguser/<name>')
def success2(name):
	return render_template('user_dashboard.html',reply=reply.query.filter_by(User_Name='%s'%name))


""" *********************************LOGIN VALIDATION***********************************************"""
@app.route('/login_check',methods= ["GET", "POST"])
def login_check():
	POST_USERNAME=str(request.form['Username'])
	POST_PASSWORD=str(request.form['Password'])
	Username = request.form['Username']
	#session['username']=username
	
	Session = sessionmaker(bind = engine)
	s = Session()
	query = s.query(user_register).filter(user_register.Username.in_([POST_USERNAME]),user_register.Password.in_([POST_PASSWORD]))
	result=query.first()
	
	if result:
		session['loggin_in'] = True 
		#return redirect(url_for('input'))
		return render_template("user_text.html")
	else:
		flash('wrong password')
		#return redirect(url_for('login'))
		return render_template('user_login.html')
		
		
@app.route('/admin_login_check',methods= ["GET", "POST"])
def admin_login_check():
	POST_USERNAME=str(request.form['Username'])
	POST_PASSWORD=str(request.form['Password'])
	Username = request.form['Username']
	#session['username']=username
	
	Session = sessionmaker(bind = engine)
	s = Session()
	query = s.query(admin_register).filter(admin_register.Username.in_([POST_USERNAME]),admin_register.Password.in_([POST_PASSWORD]))
	result=query.first()
	
	if result:
		session['loggin_in'] = True 
		#return redirect(url_for('input'))
		return render_template("add_officer.html")
	else:
		flash('wrong password')
		#return redirect(url_for('login'))
		return render_template('admin_login.html')

@app.route('/authority_login_check',methods= ["GET", "POST"])
def authority_login_check():
	POST_USERNAME=str(request.form['Username'])
	POST_PASSWORD=str(request.form['Password'])
	Username = request.form['Username']
	#session['username']=username
	
	Session = sessionmaker(bind = engine)
	s = Session()
	query = s.query(authority_register).filter(authority_register.Username.in_([POST_USERNAME]),authority_register.Password.in_([POST_PASSWORD]))
	result=query.first()
	
	if result:
		session['loggin_in'] = True 
		#return redirect(url_for('input'))
		return render_template("area_check.html")
	else:
		flash('wrong password')
		#return redirect(url_for('login'))
		return render_template('authority_login.html')
		

"""***********************************************DATA BASE **********************************************"""
class user_register(db.Model):
	First_Name=db.Column(db.String)
	Last_Name=db.Column(db.String)
	Address=db.Column(db.String)
	City=db.Column(db.String)
	State=db.Column(db.String)
	Zip=db.Column(db.Integer)
	Phone_Number=db.Column(db.Integer)
	Email_Address=db.Column(db.String)
	Username=db.Column('username',db.String,primary_key=True)
	Password=db.Column(db.String)
	
	def __init__(self,First_Name,Last_Name,Address,City,State,Zip,Phone_Number,Email_Address,Username,Password):
		self.First_Name=First_Name
		self.Last_Name=Last_Name
		self.Address=Address
		self.City=City
		self.State=State
		self.Zip=Zip
		self.Phone_Number=Phone_Number
		self.Email_Address=Email_Address
		self.Username=Username
		self.Password=Password
		
		
	@app.route("/user_register_db",methods=["GET","POST"])
	def user_register_db():
		if request.method == 'POST':
			if not request.form['First_Name'] or not request.form['Last_Name'] or not request.form['Address'] or not request.form['City'] or not request.form['State']or not request.form['Zip']or not request.form['Phone_Number']or not request.form['Email_Address']or not request.form['Username']or not request.form['Password']:
				flash("Error")
			else:
				user=user_register(request.form['First_Name'],request.form['Last_Name'],request.form['Address'],request.form['City'],request.form['State'],request.form['Zip'],request.form['Phone_Number'],request.form['Email_Address'],request.form['Username'],request.form['Password'])
				db.session.add(user)
				db.session.commit()
			#return redirect(url_for('login'))
		return render_template("reg_success.html")
		
		
		
class authority_register(db.Model):
	First_Name=db.Column(db.String)
	Last_Name=db.Column(db.String)
	Address=db.Column(db.String)
	City=db.Column(db.String)
	State=db.Column(db.String)
	Zip=db.Column(db.Integer)
	Phone_Number=db.Column(db.Integer)
	Email_Address=db.Column(db.String)
	Username=db.Column('username',db.String,primary_key=True)
	Password=db.Column(db.String)
	
	def __init__(self,First_Name,Last_Name,Address,City,State,Zip,Phone_Number,Email_Address,Username,Password):
		self.First_Name=First_Name
		self.Last_Name=Last_Name
		self.Address=Address
		self.City=City
		self.State=State
		self.Zip=Zip
		self.Phone_Number=Phone_Number
		self.Email_Address=Email_Address
		self.Username=Username
		self.Password=Password
		
		
	@app.route("/authority_register_db",methods=["GET","POST"])
	def authority_register_db():
		if request.method == 'POST':
			if not request.form['First_Name'] or not request.form['Last_Name'] or not request.form['Address'] or not request.form['City'] or not request.form['State']or not request.form['Zip']or not request.form['Phone_Number']or not request.form['Email_Address']or not request.form['Username']or not request.form['Password']:
				flash("Error")
			else:
				authority=authority_register(request.form['First_Name'],request.form['Last_Name'],request.form['Address'],request.form['City'],request.form['State'],request.form['Zip'],request.form['Phone_Number'],request.form['Email_Address'],request.form['Username'],request.form['Password'])
				db.session.add(authority)
				db.session.commit()
			#return redirect(url_for('login'))
		return render_template("reg_success.html")

		
class admin_register(db.Model):
	First_Name=db.Column(db.String)
	Last_Name=db.Column(db.String)
	Address=db.Column(db.String)
	City=db.Column(db.String)
	State=db.Column(db.String)
	Zip=db.Column(db.Integer)
	Phone_Number=db.Column(db.Integer)
	Email_Address=db.Column(db.String)
	Username=db.Column('username',db.String,primary_key=True)
	Password=db.Column(db.String)
	
	def __init__(self,First_Name,Last_Name,Address,City,State,Zip,Phone_Number,Email_Address,Username,Password):
		self.First_Name=First_Name
		self.Last_Name=Last_Name
		self.Address=Address
		self.City=City
		self.State=State
		self.Zip=Zip
		self.Phone_Number=Phone_Number
		self.Email_Address=Email_Address
		self.Username=Username
		self.Password=Password
		
		
	@app.route("/admin_register_db",methods=["GET","POST"])
	def admin_register_db():
		if request.method == 'POST':
			if not request.form['First_Name'] or not request.form['Last_Name'] or not request.form['Address'] or not request.form['City'] or not request.form['State']or not request.form['Zip']or not request.form['Phone_Number']or not request.form['Email_Address']or not request.form['Username']or not request.form['Password']:
				flash("Error")
			else:
				admin=admin_register(request.form['First_Name'],request.form['Last_Name'],request.form['Address'],request.form['City'],request.form['State'],request.form['Zip'],request.form['Phone_Number'],request.form['Email_Address'],request.form['Username'],request.form['Password'])
				db.session.add(admin)
				db.session.commit()
			#return redirect(url_for('login'))
		return render_template("reg_success.html")

	

class add_officer(db.Model):
	Name=db.Column(db.String)
	Designation=db.Column(db.String)
	Office_address=db.Column(db.String)
	City=db.Column(db.String)
	Area=db.Column(db.String)
	Mail_id=db.Column('Mail_id',db.String,primary_key=True)
	
	def __init__(self,Name,Designation,Office_address,City,Area,Mail_id):
		self.Name=Name
		self.Designation=Designation
		self.Office_address=Office_address
		self.City=City
		self.Area=Area
		self.Mail_id=Mail_id
	
@app.route("/add_officer_db",methods=["GET","POST"])
def add_officer_db():
	if request.method == 'POST':
		if not request.form['Name'] or not request.form['Designation'] or not request.form['Office_address'] or not request.form['City'] or not request.form['Area'] or not request.form['Mail_id']:
			flash("error")
		else:
			officer=add_officer(request.form['Name'],request.form['Designation'],request.form['Office_address'],request.form['City'],request.form['Area'],request.form['Mail_id'])
			db.session.add(officer)
			db.session.commit()
			#return redirect(url_for('add_officer_db'))
		return render_template("add_officer.html")
		
class Enquiry(db.Model):
	Name=db.Column(db.String)
	User_Name=db.Column('User_Name',db.String,primary_key=True)
	Mail_id=db.Column(db.String)
	Area=db.Column(db.String)
	Subject=db.Column(db.String)
	Query=db.Column(db.String)
	
	def __init__(self,Name,User_Name,Mail_id,Area,Subject,Query,Status):
		self.Name=Name
		self.User_Name=User_Name
		self.Mail_id=Mail_id
		self.Area=Area
		self.Subject=Subject
		self.Query=Query
		
		
		
@app.route("/Enquiry_db",methods=["GET","POST"])
def Enquiry_db():
	if request.method == 'POST':
		if not request.form['Name'] or not request.form['Name'] or not request.form['Mail_id'] or not request.form['Area'] or not request.form['Subject'] or not request.form['Query']:
			flash("error")
		else:
			msg=Enquiry(request.form['Name'], request.form['User_Name'], request.form['Mail_id'], request.form['Area'], request.form['Subject'], request.form['Query'])
			db.session.add(msg)
			db.session.commit()
			#return redirect(url_for('Enquiry_db'))
		return render_template("enquiry.html")


class reply(db.Model):
	User_Name=db.Column('User_Name',db.String,primary_key=True)
	Area=db.Column(db.String)
	Subject=db.Column(db.String)
	Query=db.Column(db.String)

	def __init__(self,User_Name,Area,Subject,Query):
		self.User_Name=User_Name
		self.Area=Area
		self.Subject=Subject
		self.Query=Query
		
@app.route("/reply_db",methods=["GET","POST"])
def reply_db():
	if request.method == 'POST':
		if not request.form['User_Name'] or not request.form['Area'] or not request.form['Subject'] or not request.form['Query']:
			flash("error")
		else:
			replymsg=reply(request.form['User_Name'], request.form['Area'], request.form['Subject'], request.form['Query'])
			db.session.add(replymsg)
			db.session.commit()
			#return redirect(url_for('Enquiry_db'))
		return render_template("reply.html")



if __name__ == '__main__':
	db.create_all()
	app.run(debug=True, use_reloader=True)

