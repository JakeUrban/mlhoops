# mlhoops
Machine learning application of NCAA basketball game predictions 

# Dependencies
- python3
- pip3
- mysql

# Install
Install the environment:
- virtual environment
    - `$ make venv`

Initialize the database:
- Create a local mysql database `<db_name>` (mlhoops is suggested)
- Activate the virtual environment, then:
    - `$ export SQLALCHEMY_DATABASE_URI='mysql+pymysql://<your_user>@localhost/<db_name>'`
    - `$ python3 mlhoops/mlhoops/db/init_db.py`
