from flask import Flask,render_template,request
import requests 
import os
from datetime import datetime

app=Flask(__name__)


#the api key (get yours at fastapi.com)
API_KEY=os.environ.get('API_KEY')

url='https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total'

req_headers={
	'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': API_KEY
}


previous_data=[]

# @app.route('/')
# def index():
# 	data=previous_data

# 	return render_template('index.html',data=data)




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

		last_checked=str(data['lastChecked']).replace('T',' at ')

		last_reported=str(data['lastReported']).replace('T',' at ')

		print(data)

		

		context={
		'data':data,
		'last_checked':last_checked,
		'last_reported':last_reported
		}

	return render_template('index.html',**context)




if __name__ == '__main__':
	app.run(debug=True)


