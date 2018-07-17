# MLHoops
Data collection and analysis application for NCAA basketball game predictions. MLHoops consists of a web scraping system, object relational mapping layer, and a collection of models built in a variety of languages and libraries. The web scraping system has collected information on every player, team, and game for every NCAA season since 1993.


# Install
Installing according to these instructions will set up the development environment needed to use this package. It will NOT install a copy of the dataset I have collected by using this package.

Dependencies:
- python3
- pip3
- mysql

Install the environment:
- virtual environment
    - `$ make venv`

Initialize the database:
- Create a local mysql database `<db_name>` (mlhoops is suggested)
- Activate the virtual environment, then:
    - `$ export SQLALCHEMY_DATABASE_URI='mysql+pymysql://<your_user>@localhost/<db_name>'`
    - `$ python3 mlhoops/mlhoops/db/init_db.py`
        - This will create the database schema and add sample rows to each table for inital testing.
