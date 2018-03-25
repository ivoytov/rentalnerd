#!/usr/bin/python
import MySQLdb
import sys
import pandas as pd
import datetime as dt
import math
import xgboost as xgb
import numpy as np
import csv

model_path = '/home/ilya/rentalnerd-models/'
factors_path = 'factors.csv'

today = (dt.date.today() - dt.date(2000, 1, 1)).days

def sanitize(data):

    data.fillna(value=0, inplace=True)

    data.drop(['bookmarked', 'created_at', 'id', 
                      'notes', 'source', 'updated_at', 'home_type', 'sfh', 'description', 
                    'event_name', 'neighborhood'], axis=1, inplace=True)
    
    # fills in some sensible defaults where data is missing
    data["near_golf_course"] = data["near_golf_course"].apply(lambda x: True if x == 1.0 else False)
    data["has_pool"] = data["has_pool"].apply(lambda x: True if x == 1.0 else False)
    data["garage"] = data["garage"].apply(lambda x: True if x == 1.0 else False)
    data["adult"] = data["adult"].apply(lambda x: True if x == 1.0 else False)
    data["construction"] = data["construction"].apply(lambda x: True if x == 1.0 else False)
    data["townhouse"] = data["townhouse"].apply(lambda x: True if x == 1.0 else False)
    data["mobile"] = data["mobile"].apply(lambda x: True if x == 1.0 else False)
    
    data["fixer"] = data["fixer"].apply(lambda x: True if x == 1.0 else False)
    data["foreclosure"] = data["foreclosure"].apply(lambda x: True if x == 1.0 else False)

    data["school_district_id"] = data["school_district_id"].astype(str)
    data['year_built'] = data['year_built'].apply(lambda x: 1980 if math.isnan(x) else x)

    data['date_listed'] = 6233 #today
    data['days_on_market'] = today - data.date_listed
    data['days_on_market_accu'] = 0
    data['fsbo'] = 0
    data['is_latest'] = 1

    data['lot'] = data['lot'].apply(lambda x: int(0 if x is None else x))
    data['hoa_fees'] = data['hoa_fees'].apply(lambda x: int(0 if x is None else x))
    data['rooms'] = data['rooms'].apply(lambda x: int(0 if x is None else x))
    data['saves'] = data['saves'].apply(lambda x: int(0 if x is None else x))
    data['stories'] = data['stories'].apply(lambda x: int(0 if x is None else x))
    data['days_on_market_accu'] = data['days_on_market_accu'].apply(lambda x: int(0 if x is None else x))

    data['school_district_id_100.0'] = 0
    data['school_district_id_11.0'] = 0
    data['school_district_id_124.0'] = 0
    data['school_district_id_145.0'] = 0
    data['school_district_id_162.0'] = 0
    data['school_district_id_168.0'] = 0
    data['school_district_id_172.0'] = 0
    data['school_district_id_187.0'] = 0
    data['school_district_id_19.0'] = 0
    data['school_district_id_190.0'] = 0
    data['school_district_id_222.0'] = 0
    data['school_district_id_224.0'] = 0
    data['school_district_id_28.0'] = 0
    data['school_district_id_35.0'] = 0
    data['school_district_id_37.0'] = 0
    data['school_district_id_40.0'] = 0
    data['school_district_id_43.0'] = 0
    data['school_district_id_47.0'] = 0
    data['school_district_id_48.0'] = 0
    data['school_district_id_5.0'] = 0
    data['school_district_id_57.0'] = 0
    data['school_district_id_60.0'] = 0
    data['school_district_id_67.0'] = 0
    data['school_district_id_68.0'] = 0
    data['school_district_id_75.0'] = 0
    data['school_district_id_87.0'] = 0
    data['school_district_id_90.0'] = 0
    data['school_district_id_93.0'] = 0
    data['school_district_id_96.0'] = 0
    data['school_district_id_0.0'] = 0

    data['zipcode_85003'] = 0
    data['zipcode_85004'] = 0
    data['zipcode_85006'] = 0
    data['zipcode_85007'] = 0
    data['zipcode_85008'] = 0
    data['zipcode_85009'] = 0
    data['zipcode_85012'] = 0
    data['zipcode_85013'] = 0
    data['zipcode_85014'] = 0
    data['zipcode_85015'] = 0
    data['zipcode_85016'] = 0
    data['zipcode_85017'] = 0
    data['zipcode_85018'] = 0
    data['zipcode_85019'] = 0
    data['zipcode_85020'] = 0
    data['zipcode_85021'] = 0
    data['zipcode_85022'] = 0
    data['zipcode_85023'] = 0
    data['zipcode_85024'] = 0
    data['zipcode_85027'] = 0
    data['zipcode_85028'] = 0
    data['zipcode_85029'] = 0
    data['zipcode_85031'] = 0
    data['zipcode_85032'] = 0
    data['zipcode_85033'] = 0
    data['zipcode_85034'] = 0
    data['zipcode_85035'] = 0
    data['zipcode_85037'] = 0
    data['zipcode_85042'] = 0
    data['zipcode_85043'] = 0
    data['zipcode_85044'] = 0
    data['zipcode_85050'] = 0
    data['zipcode_85051'] = 0
    data['zipcode_85053'] = 0
    data['zipcode_85085'] = 0
    data['zipcode_85087'] = 0
    data['zipcode_85138'] = 0
    data['zipcode_85139'] = 0
    data['zipcode_85201'] = 0
    data['zipcode_85202'] = 0
    data['zipcode_85203'] = 0
    data['zipcode_85205'] = 0
    data['zipcode_85206'] = 0
    data['zipcode_85207'] = 0
    data['zipcode_85209'] = 0
    data['zipcode_85210'] = 0
    data['zipcode_85212'] = 0
    data['zipcode_85215'] = 0
    data['zipcode_85224'] = 0
    data['zipcode_85225'] = 0
    data['zipcode_85226'] = 0
    data['zipcode_85249'] = 0
    data['zipcode_85250'] = 0
    data['zipcode_85251'] = 0
    data['zipcode_85253'] = 0
    data['zipcode_85254'] = 0
    data['zipcode_85255'] = 0
    data['zipcode_85257'] = 0
    data['zipcode_85258'] = 0
    data['zipcode_85259'] = 0
    data['zipcode_85260'] = 0
    data['zipcode_85283'] = 0
    data['zipcode_85284'] = 0
    data['zipcode_85286'] = 0
    data['zipcode_85301'] = 0
    data['zipcode_85302'] = 0
    data['zipcode_85303'] = 0
    data['zipcode_85304'] = 0
    data['zipcode_85305'] = 0
    data['zipcode_85306'] = 0
    data['zipcode_85307'] = 0
    data['zipcode_85308'] = 0
    data['zipcode_85310'] = 0
    data['zipcode_85345'] = 0
    data['zipcode_85351'] = 0
    data['zipcode_85353'] = 0
    data['zipcode_85373'] = 0
    data['zipcode_85381'] = 0
    data['zipcode_85382'] = 0
    data['zipcode_85383'] = 0
    data['zipcode_85396'] = 0
    data['zipcode_85936'] = 0

    # set the zipcode and school district variables
    t = 'zipcode_' + data['zipcode'].iloc[0]
    data[t] = 1
    u = 'school_district_id_' + data.school_district_id.iloc[0] + '.0'
    data[u] = 1
    data['city_code_PH'] = 1

    return data

def my_range(start, end, step):
	while start <= end:
	    yield start
	    start += step

# function for the web service
def good_sell_service(property_id):
	with open(factors_path,'r') as f:
		reader = csv.reader(f)
		read_factors = list(reader)[0]

	db = MySQLdb.connect(host="52.2.153.189",  # your host 
		                 user="prod",       # username
		                 passwd="nerd",     # password
		                 db="rental_nerd")   # name of the database
	 
	# Create a Cursor object to execute queries.
	cur = db.cursor()
	 
	# Select data from table using SQL query.
	cur.execute("SELECT  \
		*, \
		properties.id as 'property_id', \
		property_school_districts.school_district_id \
		FROM  \
		properties \
		LEFT JOIN \
		property_school_districts ON property_school_districts.property_id = properties.id \
		WHERE \
		properties.id = %s", [property_id])
	 
	# print the columns
	field_names = [i[0] for i in cur.description]
	#print(str(field_names))
	# print the row
	for row in cur.fetchall() :
		print(row[1])

	df = pd.DataFrame.from_records([row], columns=field_names)
	df = df.loc[:,~df.columns.duplicated()]
	df.set_index('property_id',inplace=True)
	df.index.name = 'property_id'
	df = sanitize(df)


	ind2remove = ['Unnamed: 0', 'id', 'address', 'area_name', 'listed_diff_id', 'lookup_address',
		          'origin_url', 'neighborhood', 'zipcode', 'luxurious', 'transaction_status', 'transaction_type',
		          'images','zestimate_sale','zestimate_rent', 'price', 'date_closed', 'price_closed', 'date_transacted_latest', 'school_district_id_145.0', 'school_district_id_224',
		          'school_district_id', 'broker_phone','broker_name','broker_license', 'broker_company', 'recrawled_at', 
		          'city_code']

	factors = np.setdiff1d(df.columns, ind2remove).tolist()

	bst = xgb.Booster()
	bst.load_model(model_path + 'good_sell_20180325.model')

	#print(factors)
	#print(df[factors].values)
	output = ""
	for x in my_range(100000, 500000, 50000):
		df['price_listed'] = x

		target = xgb.DMatrix( df[read_factors], feature_names=read_factors)
		ypred = bst.predict(target, ntree_limit=int(bst.attributes()['best_iteration']))

		output = output + ("Predicted good sell at price $%i: %f\n" % (df.price_listed.iloc[0], ypred))

	df.to_csv("service_df.csv")	


	return(output)


if __name__ == '__main__':
    # Running as a script
	if len(sys.argv) != 2:
		print("wrong number of arguments")
		quit()
	else:
		property_id = sys.argv[1]
		print("processing property_id %s" % property_id)
		print(good_sell_service(property_id))

	

