# rentalnerd

## Pre-requisities
- sqlite3
- Python 2.7
- pip

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

## Setting up

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

Installing virtual environment
  ```
  pip install virtualenv 

  # Run to make sure its been installed
  which virtualenv
  ```

Setting up virtual environment
  ```
  mkdir venv
  virtualenv venv
  ```

Activating into virtual environment
  ```
  source venv/bin/activate
  ```

Installing MySQL database client binaries - 5.6
  ```
  brew install mysql@5.6
  ```

Setting MySQL binaries (Ubuntu)
  ```
  sudo apt-get install python-mysqldb
  sudo apt-get install libmysqlclient-dev
  ```

Installing MySql dependency
  ```
  # requires MySQL 5.6 client binaries installed
  easy_install MySQL-python
  ```

Installing XGBoost pre-requisites
  - http://xgboost.readthedocs.io/en/latest/build.html#building-on-osx
  

Install requirements
  ```
  pip install  --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org  -r requirements.txt --upgrade
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