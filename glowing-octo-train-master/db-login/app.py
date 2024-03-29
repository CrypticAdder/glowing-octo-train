"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, session, url_for, redirect, escape, render_template, request,abort
import pymysql, hashlib, datetime

from hashlib import md5
app=Flask(__name__)

app.secret_key="daniel deng is bad"
def display_all_records(role="admin",Id=0):
	global data
	connection=create_connection()
	try:
		with connection.cursor() as cursor:
			#pull records and display using a left join
			#select_sql = "SELECT * from users"
			#if role not "admin"
			select_sql= "SELECT users.ID AS ID, users.Email AS Email, users.FirstName AS FirstName, users.FamilyName AS FamilyName FROM users"
			if int(Id)>0:
				print(select_sql)
				print (Id)
				select_sql = select_sql+" Where users.ID="+Id
				val=(int(Id))
				print(select_sql)
				cursor.execute(select_sql)
				data = cursor.fetchone()
				print(data)
			cursor.execute(select_sql)
			data = cursor.fetchall()
			data=list(data)
	finally:
		connection.close()



class ServerError(Exception):pass


def create_connection():
	return pymysql.connect(host='localhost',
							 user='root',
							 password='13COM',
							 db='workshopdb1',
							 charset='utf8mb4'
							 ,cursorclass=pymysql.cursors.DictCursor)


class ServerError(Exception):
   """Base class for other exceptions"""
   pass
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
	print(session.get('logged_in',"Not_Logged In"))
	if  session.get('logged_in'):
		print(session.get("username", "None Found"))
		username_session=escape(session['username']).capitalize()
		return render_template("index.html", session_user_name=username_session)
	username_session=''
	return render_template("index.html")
#	connection=create_connection()
#	try:
#		with connection.cursor() as cursor:
#			sql = "SELECT * from users"
#			cursor.execute(sql)
#			data = cursor.fetchall()
#			data=list(data)
#	finally:
#			connection.close()
	return render_template("Index.html", results=data)

@app.route('/workshops')
def workshop():
	if  session.get('logged_in'):
		username_session=escape(session['username']).capitalize()
		connection=create_connection()
		print('I Run1')
		try:
			with connection.cursor() as cursor:
				print('I Run2')
				select_sql ="SELECT * FROM workshop w"
				print('I Run2.5')
				cursor.execute(select_sql)
				print('I Run3')
				data=cursor.fetchall()
				data=list(data)
				print('I Run4')
		finally:
			print('I Run5')
			connection.close()
			return render_template('workshop.html', results=data, session_user_name=username_session)
	username_session=''
	return render_template('index.html')

#login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#	connection=create_connection()
#	if  session.get('logged_in'):
#		display_all_records()
#		username_session=escape(session['username']).capitalize()
#		return redirect(url_for("index", results=data,session_user_name=username_session))
#	error = None
#	try:
#		with connection.cursor() as cursor:
#			if request.method == 'POST':
#				username_form  = request.form['username']
#				select_sql = "SELECT COUNT(1) FROM users WHERE UserName = %s"
#				val =(username_form)
#				cursor.execute(select_sql,val)
#				#data = cursor.fetchall()

#			if not list(cursor.fetchone())[0]:
#				raise ServerError('Invalid username')

#			password_form  = request.form['password']
#			select_sql = "SELECT Password from users WHERE UserName = %s"
#			val=(username_form)
#			cursor.execute(select_sql,val)
#			data = list(cursor.fetchall())
#			#print (data)
#			for row in data:
#				print(md5(password_form.encode()).hexdigest())
#				if md5(password_form.encode()).hexdigest()==row['Password']:
#					session['username'] = request.form['username']
#					print

#					session['logged_in'] = True
#					return redirect(url_for('home'))

#			raise ServerError('Invalid password')
#	except ServerError as e:
#		error = str(e)
#		session['logged_in']=False
		
#	return render_template('login.html', error=error)
# update from form

@app.route('/add_user', methods=['POST','GET'])
def new_user():
	connection=create_connection()
	if request.method == 'POST':
		form_values = request.form 
		username = form_values.get("username")
		first_name = form_values.get("firstname")
		family_name = form_values.get("familyname")
		email = form_values.get("email")
		password = form_values.get("password")
		password = hashlib.md5(password.encode()).hexdigest()
		dob=form_values.get('dob')
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO `users` (FirstName,FamilyName,Email,Username,Password) VALUES (%s,%s,%s,%s,%s)"
				val=(first_name,family_name,email,username,password)
				cursor.execute(sql,(val))
				print('working')
				#save values in dbase
			connection.commit()
			cursor.close()
			with connection.cursor() as cursor:
				#pull records and display
				sql = "SELECT * from users"
				cursor.execute(sql)
				data = cursor.fetchall()
				data=list(data)
		finally:
			connection.close()
		return redirect(url_for('users'))
	return render_template("add_user.html")

#users
@app.route('/users')
def users():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		username_session=escape(session['username']).capitalize()
		display_all_records("admin")
		print(data)
	return render_template("users.html",results = data, session_user_name=username_session)


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
	connection=create_connection()
	if  session.get('logged_in'):
		display_all_records()
		username_session=escape(session['username']).capitalize()
		return redirect(url_for("index", results=data,session_user_name=username_session))
	error = None
	try:
		with connection.cursor() as cursor:
			if request.method == 'POST':
				username_form  = request.form['username']
				select_sql = "SELECT COUNT(1) FROM users WHERE UserName = %s"
				val =(username_form)
				cursor.execute(select_sql,val)
				#data = cursor.fetchall()

				if not list(cursor.fetchone())[0]:
					raise ServerError('Invalid username')

				password_form  = request.form['password']
				select_sql = "SELECT Password from users WHERE UserName = %s"
				val=(username_form)
				cursor.execute(select_sql,val)
				data = list(cursor.fetchall())
				#print (data)
				for row in data:
					#print(md5(password_form.encode()).hexdigest())
					if md5(password_form.encode()).hexdigest()==row['Password']:
						session['username'] = request.form['username']
						session['logged_in'] = True
					return redirect(url_for('home'))

			raise ServerError('Invalid password')
	except ServerError as e:
		error = str(e)
		session['logged_in']=False

	return render_template('login.html', error=error)

@app.route('/edit_user', methods=['POST','GET'])
def update_user():
	user_id = request.args.get('id')
	print(f'user id is{user_id}')
	connection=create_connection()
	if request.method == 'POST':
			form_values = request.form 
			first_name = form_values.get("firstname")
			family_name = form_values.get("familyname")
			email = form_values.get("email")
			print(f'email is {email}')
			password = form_values.get("password")
			password = hashlib.md5(password.encode()).hexdigest()
			user_id = request.args.get('id')
			print(f'id is {user_id}')
			try:
				with connection.cursor() as cursor:
					# Create a new record
					sql = "UPDATE `users` SET FirstName=%s,FamilyName=%s,Email=%s,Password=%s WHERE ID=%s"
					print('1')
					val=(first_name,family_name,email,password,user_id)
					print('2')
					cursor.execute(sql,(val))
					print('3')
					data = cursor.fetchall()
					print('4')
					data=list(data)
					#save values in dbase
				connection.commit()
				cursor.close()
			finally:
				connection.close()
			return redirect(url_for('users'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_id)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("Edit_record.html",data=data)

@app.route('/delete_user', methods =["GET","POST"])
def delete_record():
	user_ID = request.args.get("id")
	print(f'deleting {user_ID}')
	connection=create_connection()
	if request.method == "POST":
		form = request.form
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "DELETE FROM  `users` WHERE Id = %s "
				print(user_ID)
				val=(user_ID)
				cursor.execute(sql,(val))
				data = cursor.fetchall()
				data=list(data)
			#save values in dbase
			connection.commit()
			cursor.close()
		finally:
			connection.close()
			return redirect(url_for('users'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_ID)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("delete_record.html",data=data)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session['logged_in']=False
	return redirect(url_for("home"))




@app.route('/issue', methods = ['GET', "POST"])
def issue():
	connection=create_connection()
	print('Hello 1')
	if request.method == "POST":
		#get data from form
		print('Hello 2')
		form = request.form
		student = form['users']
		workshop=form['workshop']
		date = datetime.datetime.now()
		print('Hello 2.3')
		try:
			print('Hello 2.6')
			with connection.cursor() as cursor:
				print('Hello 3')
				sql = "INSERT INTO tblworkshop (WorkshopID, UserID) VALUES (%s,%s,%s);"
				vals=(laptop,student,date)
				print('Hello 4')
				print(vals)
				cursor.execute(sql,vals)
				print('Hello 5')
				connection.commit()
				print("executed")

		finally:
			connection.close()
			print('Hello 9')
			return redirect(url_for('workshops'))
	try:
		print('Hello 5.5')
		with connection.cursor() as cursor:
			sql = "SELECT * FROM users;"
			cursor.execute(sql)
			users = cursor.fetchall()
			users = list(users)
			print('Hello 6')
			sql = "SELECT * FROM tblworkshop;"
			cursor.execute(sql)
			workshop = cursor.fetchall()
			workshop = list(workshop)
	finally:
		connection.close
		print('Hello 7')
	print('Hello 8')
	return render_template('issue.html',users=users, workshop=workshop)


if __name__ == '__main__':
	import os
	HOST = os.environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(os.environ.get('SERVER_PORT', '5555'))
	except ValueError:
		PORT = 5555
	app.run(HOST, PORT, debug=True)
