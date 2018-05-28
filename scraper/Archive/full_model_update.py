from IPython import get_ipython
# imports
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import timeit  # for timing models
import json
import requests

from sklearn import model_selection
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit

# city abbreviation code
city = 'PH'
# limit on number of lines returned from sql queries (for debugging)
limit = 100
# today's date for output filenames
today = dt.date.today()

# where to save the xgb models - they get huge so keep them out of any git path
path = '/home/ivoytov/rentalnerd-models/'

# data columns used for the booster
factors = ['property_id', 'bedrooms', 'bathrooms', 'sqft','longitude', 'latitude','zipcode', 'elevation', 'garage'
                          ,'year_built', 'level','dist_to_park','dist_to_golf_course', 'has_pool'
                          ,'date_closed','multifamily', 'hoa_fees', 'lot']

# booster parameters
param = {'verbose': 1, 'max_depth':6, 'num_parallel_tree': 10000, 'eval_metric':'mae' }
num_round = 10
plst = param.items()

# slack webhook secret url
webhook_url = 'https://hooks.slack.com/services/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'

# disable warning on assignment without copy
pd.options.mode.chained_assignment = None  # default='warn'

get_ipython().magic(u'load_ext sql')


# %sql mysql://root@localhost/rental_nerd
get_ipython().magic(u'sql mysql://prod:nerd@52.2.153.189/rental_nerd')

def sanitize(data, zipcode_list = None):
    # filters out any non-sensical values or fat finger mistakes in MLS listings
    print("Entries before filter: ", len(data))
    data = data[  (data.sqft <= 10000) 
                & (data.price <= 400000) 
                & (data.bedrooms <= 6) 
                & (data.bathrooms <= 6) 
                & (data.sqft != 0) 
                & (data.home_type == 'sfh')]
    if(data.transaction_type.iloc[0] == 'sales'):
        data = data[ data.price > 50000 ]
    else:
        data = data [ data.price > 500 ]
    
    if(zipcode_list is not None):
        data = data[data.zipcode.isin(zipcode_list)]

    
    print("Entries after filter: ",len(data))
    
    # fills in some sensible defaults where data is missing
    data["near_golf_course"] = data["near_golf_course"].apply(lambda x: True if x == 1.0 else False)
    data["has_pool"] = data["has_pool"].apply(lambda x: True if x == 1.0 else False)
    data["garage"] = data["garage"].apply(lambda x: True if x == 1.0 else False)
    data["multifamily"] = data["home_type"].apply(lambda x: True if x == "mfh" else False)
    data['date_closed'] = data['date_closed'].apply(lambda x: (x - dt.date(2000, 1, 1)))
    data['date_closed'] = data['date_closed'].astype(int)
    
    return data

def query(transaction_type, transaction_status, city, zipcode, limit, start_date="2000-01-01 10:01:13", end_date=today):
    # convert array of zipcodes into sql string
    placeholders= ', '.join(zipcode)
    
    # sql query helper function
    query = get_ipython().magic(u'sql (    select      *      from      properties,     property_transaction_logs,     area_name_zipcodes     where      property_transaction_logs.created_at > :start_date and     property_transaction_logs.created_at < :end_date and     area_name_zipcodes.`area_name` LIKE :city and     area_name_zipcodes.`zipcode` = properties.`zipcode` and         properties.`id` = property_transaction_logs.`property_id` and     property_transaction_logs.`transaction_status` = :transaction_status and     property_transaction_logs.`transaction_type` = :transaction_type and     property_transaction_logs.`is_latest` = true     order by     property_transaction_logs.id desc     limit :limit)')

    return query.DataFrame().T.groupby(level=0).first().T

def output_model_metrics( x, ypred, y_known ):
    #Print model report:
    mae = metrics.mean_absolute_error(y_known, ypred)
    r2 = metrics.explained_variance_score(y_known, ypred)
  
    slack("Model Report: \n MAE Score (Train): %f \n R^2: %f" % (mae, r2))

def top_zipcodes(n = 100):
    # query the top 100 zipcodes in the database (roughly equal to all zipcodes >10k properties)
    query = get_ipython().magic(u'sql (    SELECT zipcode, COUNT(id)     FROM properties     GROUP BY zipcode     ORDER BY 2 DESC     limit :n)')

    zipcode_filter = query.DataFrame()
    print("Top zipcode by count is",zipcode_filter.iloc[0,0],"with",zipcode_filter.iloc[0,1],"properties")
    print("100th zipcode by count is",zipcode_filter.iloc[99,0],"with",zipcode_filter.iloc[99,1],"properties")
    return zipcode_filter.zipcode.values


def slack(text):
    print("Slacking: " + text)
    response = requests.post(webhook_url, data=json.dumps(text), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))


# get list of top zipcodes to only run the model on them
zipcode_list = top_zipcodes(100)

sales_train = query('sales', 'closed', city, zipcode_list, limit)
sales_train = sanitize(sales_train, zipcode_list)

# train model based on historical sales information
start_time = timeit.default_timer()

dtrain = xgb.DMatrix(sales_train[factors].values, label=sales_train.price, feature_names=factors)
bst = xgb.train( plst, dtrain, num_round )

elapsed = timeit.default_timer() - start_time
print("Time to train model: ", elapsed)

# predict the training set using the model - note this is in sample testing
ypred = bst.predict(dtrain)
output_model_metrics( dtrain, ypred, sales_train.price )


for_sale = query('sales', 'open', city, zipcode_list, limit)
# use today's date for 'close date' since the transaction is still open i.e. home is currently listed for sale
for_sale.date_closed = today

# need this to clean data but also to adjust the "date closed" to be # of secs from 1/1/2000 (the format the model uses)
for_sale = sanitize(for_sale, zipcode_list)

target = xgb.DMatrix( for_sale[factors].values, feature_names=factors)

ypred = bst.predict(target)

values = np.column_stack((for_sale.property_id.values
                         ,for_sale.address.values
                         ,ypred
                         ,for_sale.price.values
                         ,ypred-for_sale.price))
output = pd.DataFrame(values[:,1:],index=values[:,0],columns=['address','ypred','list','gain-loss'])
output = output.sort_values(by='gain-loss',ascending=False)
output.head(20)

rent_train = query(transaction_type='rental',transaction_status='closed', city=city,zipcode=zipcode_list, limit=limit)
rent_train = sanitize(rent_train, zipcode_list)

# train rental model
start_time = timeit.default_timer() # start timer
dtrain = xgb.DMatrix(rent_train[factors].values, label=rent_train.price, feature_names=factors)
rent_bst = xgb.train( plst, dtrain, num_round )

elapsed = timeit.default_timer() - start_time # end timer
print("Time to train model: ", elapsed)

# predict the training set using the model - note this is in sample testing
ypred = rent_bst.predict(dtrain)
output_model_metrics( dtrain, ypred, rent_train.price )

# predict rent prices for home that are listed for sale
ypred = rent_bst.predict(target)
ypred = pd.Series(ypred,index=output.index)
ypred.name = "rent"

# calculate estimated cap rate
cr = ypred * 12 / output.list
cr.name = "cap rate"

# combine rent predictions to homes listed for sale
best_of = pd.concat([output,ypred, cr],axis=1)
best_of = best_of[ (best_of['gain-loss'] < 50000) & ((best_of['gain-loss'] / best_of.list).abs() < 0.5) ]
best_of.head(30)

# save target list
best_of.to_csv(city+'_target_list.csv')

xgb.plot_importance(bst)
xgb.plot_importance(rent_bst)

# save model
bst.save_model(path + 'TEST_' + city.lower() + '_sales_' + today.strftime('%Y%m%d') + '.model')

# save rental model
rent_bst.save_model(path + 'TEST_' + city.lower() + '_rent_' + today.strftime('%Y%m%d') + '.model')


