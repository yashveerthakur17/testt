"""
PYMYSQL NO LONGER WORKS WITH PANDAS 2.x SO HAD TO SHIFT TO MORE MAIN STREAM SQLALCHEMY
WAS PREVIOUSLY TRYING TO USE A CURSOR TO BYPASS THIS ISSUE BUT DIDNT WORK...

import os
import sys
import pandas as pd
from dotenv import load_dotenv
import pymysql
from src.mlproject.logger import logging
from src.mlproject.exceptions import CustomException

# Load environment variables from the .env file
load_dotenv()

# Retrieve the credentials from environment variables
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
db = os.getenv("DB")

def read_sql_data():
    logging.info('Reading SQL database started')
    try:
        # Establish the MySQL connection using pymysql
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info('MySQL connection successful')

        # Execute the SQL query using a cursor and fetch all results
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students.student')
            result = cursor.fetchall()  # Fetch all rows

            # Convert the fetched data into a pandas DataFrame
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            print(df.head())  # Display the first few rows for verification

        return df  # Return the DataFrame

    except Exception as e:
        logging.error(f"Error reading SQL data: {e}")
        # Raise a custom exception to handle errors properly
        raise CustomException(e, sys)

    finally:
        # Ensure the MySQL connection is closed
        if connection:
            connection.close()
            logging.info('MySQL connection closed')"""




import os
import sys
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sqlalchemy import create_engine
from src.mlproject.logger import logging
from src.mlproject.exceptions import CustomException
import pickle
from sklearn.model_selection import GridSearchCV, train_test_split
import numpy as np

# Load the environment variables from .env
load_dotenv()

# Retrieve the MySQL credentials from the environment variables
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
db = os.getenv("DB")
port = os.getenv("PORT", "3306")  # Default to 3306 if PORT is not provided

# Create the SQLAlchemy engine using the loaded credentials
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')

def read_sql_data():
    logging.info('Reading SQL database started')
    try:
        # Use pandas with the SQLAlchemy engine to execute the query
        df = pd.read_sql_query('SELECT * FROM college.students', engine)
        logging.info('MySQL connection successful')
        print(df.head())  # Display the first few rows

        return df  # Return the DataFrame

    except Exception as e:
        logging.error(f"Error reading SQL data: {e}")
        raise CustomException(e, sys)

    #getting pickle file from obj and its path
def save_object(file_path,obj):
    try:
        dir_path= os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(X_train, X_test, y_train, y_test):
    try:

        report={}

        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs=GridSearchCV(model, param_grid=para,cv=2)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            report[list(models.keys())[i]]=train_score


    except Exception as e:
        raise CustomException(e, sys)



    except Exception as e:
        raise CustomException
