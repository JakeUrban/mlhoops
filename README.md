# mlhoops
Data collection and analysis application for NCAA basketball game predictions. Mlhoops is primarily a web scraping system currently, and has been used to collect data from each player, team, and game for all seasons since 1993. This package will ultimately be a showcase for my skills in data science and engineering.


# Install
Installing according to these instructions will set up the development environment needed to use this package. It will NOT install a copy of the dataset I have collected by using this package.


Install the environment:
- virtual environment
    - `$ make venv`

# Dependencies
- python3
- pip3
- mysql

Initialize the database:
- Create a local mysql database `<db_name>` (mlhoops is suggested)
- Activate the virtual environment, then:
    - `$ export SQLALCHEMY_DATABASE_URI='mysql+pymysql://<your_user>@localhost/<db_name>'`
    - `$ python3 mlhoops/mlhoops/db/init_db.py`
