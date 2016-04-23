# rentalnerd

## Pre-requisities
- sqlite3
- python 2.7
- pip

Installing dependent image libraries
```
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

Installing MySql dependency
  ```
  easy_install MySQL-python
  ```

Install requirements
  ```
  pip install -r requirements.txt --upgrade
  ```

Setting up Matlab backend for python
  ```
  touch ~/.matplotlib/matplotlibrc

  # Add the following line to the newly created file
  backend: TkAgg
  ```

## Running NoteBook
  ```
  ipython notebook scraper/PHX\ Model.ipynb 
  ```