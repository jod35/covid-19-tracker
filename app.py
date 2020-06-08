from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import requests 
import os
from datetime import datetime

app=Flask(__name__)

DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/COVID'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)

#the api key (get yours at fastapi.com) mine is an environment variable
API_KEY=os.environ.get('API_KEY')

url='https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total'

req_headers={
	'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': API_KEY
}


previous_data=[]



class Record(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	deaths=db.Column(db.Integer,nullable=False)
	confirmed=db.Column(db.Integer,nullable=False)
	recovered=db.Column(db.Integer,nullable=False)
	location=db.Column(db.String(35),nullable=False)
	last_checked=db.Column(db.Text)

	def __repr__(self):
		return f'{self.id} record' 

@app.route('/search',methods=['GET','POST'])

def search_cases_by_country():
	data=""

	if request.method =='POST':

		country=request.form['country']

		#search cases by country
		queryString={'country':country}

		response=requests.get(url,headers=req_headers,params=queryString)

		
		resp_data=response.json()

		data=resp_data['data']
		print(data)


		new_record=Record(
			confirmed=data['confirmed'],
			deaths=data['deaths'],
			recovered=data['recovered'],
			location=data['location'],
			last_checked=data['lastChecked']

			)

		db.session.add(new_record)
		db.session.commit()


		

	context={
	'data':data,
	}

	return render_template('index.html',**context)


#display previous searches

@app.route('/records')
def return_records():
	records=Record.query.order_by(Record.id.desc()).all()
	context={
	'records':records
	}
	return render_template('records.html',**context)



if __name__ == '__main__':
	app.run(debug=True)


