# rentalnerd

## Pre-requisities
- sqlite3
- Python 2.7
- pip


### MacOS X
Installing dependent image libraries
```
# Install libpng directly -- http://mac-dev-env.patrickbougie.com/libpng/
brew reinstall libpng 

brew reinstall freetype
```

Installing Python 2.7
```
brew install python
```

Install PIP
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

Installing virtual environment
```
pip install virtualenv 

# Run to make sure its been installed
which virtualenv
```

Setting locale
  ```
  # Add the following two lines in ~/.bash
  export LC_ALL=en_US.UTF-8
  export LANG=en_US.UTF-8
  ```

Setting MySql path
  ```
  export PATH=$PATH:/usr/local/mysql/bin
  ```


Installing MySQL database client binaries - 5.6
  ```
  brew install mysql@5.6
  ```

Installing MySql dependency
  ```
  # requires MySQL 5.6 client binaries installed
  easy_install MySQL-python
  ```

### Ubuntu
Installing pre-requisities (Ubuntu)
```
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install libssl-dev

sudo apt-get install python-pip python-dev build-essential 
```

Install PIP
```
sudo pip install --upgrade pip 
```

Install Virtual Environment
```
sudo pip install --upgrade virtualenv 
```

Setting MySQL binaries (Ubuntu)
```
sudo apt-get install python-mysqldb
sudo apt-get install libmysqlclient-dev
```

## Setting up

Setting up virtual environment
  ```
  mkdir venv
  virtualenv venv
  ```

Activating into virtual environment
  ```
  source venv/bin/activate
  ```

Installing XGBoost pre-requisites
  - http://xgboost.readthedocs.io/en/latest/build.html#building-on-osx
  

Install requirements
  ```
  # pip install  --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org  -r requirements.txt --upgrade
  pip install -r requirements.txt --upgrade
  ```

Setting up Matlab backend for python
  ```
  touch ~/.matplotlib/matplotlibrc

  # Add the following line to the newly created file
  backend: TkAgg
  ```

## Running NoteBook
  When we want to train new prediction models

  ```
  # Python 2.7
  ipython notebook scraper/PHX\ Model.ipynb 
  ```

## Running webserver
  We expose our trained model as a webservice to be called externally
  ```
  # Running the webservice at port 10003
  python service/web_server.py 10003

  # using make file
  make web
  ```