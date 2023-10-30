
#----------------------MODULES SECTION-------------------------------------
from flask import Flask, request, render_template, redirect, url_for #module for restAPI
import os
import numpy as np
from os.path import join, dirname, realpath
import pandas as pd #module to parse csv data into pandas dataframe
import pyodbc #module for connecting to MSSQL Server
from werkzeug.utils import secure_filename #module
#------------------------------------------------------------------------

app = Flask(__name__) #instanciate "app" with Flask object

#folder where csv files will be stored
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

#funtion to verify if file has ".csv" extension
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#function to upload file retrieved from web-server to folder
#@app.route('/', methods=['GET', 'POST'])
@app.route('/add_file', methods=['GET','POST']) #define route and method, POST = send data to server for storing it, e.g. when uploading a file like in this case
def upload_file():

    if request.method == 'POST':
        file = request.files['file'] #retrieve csv file from web-server

        if file and allowed_file(file.filename): #if = True when: an actual file is selected in web app and it is a .csv
            filename = secure_filename(file.filename) #remove special characters, in case file name comes with "/"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) #define path inweb-server where file should be stored
            file.save(file_path) #save file into chosen locatin
            parse_csv(file_path, filename) #call function to parse csv data into dataframe for further processing

        return redirect(url_for('upload_file')) #redirect website to route used by upload_file function
    
    return render_template('index.html') #load HTML website from index.html file

#function to parse csv data into pandas dataframe and do further processing
def parse_csv(file_path, filename):

    valid_filenames = ['hired_employees', 'departments', 'jobs'] #list of "valid" file names (without .csv extension)
    new_filename = os.path.splitext(filename)[0] #remove extension from filename

    #list of required columns per file
    hired_employees_headers = ['id', 'name', 'datetime', 'department_id', 'job_id']
    departments_headers = ['id', 'department']
    jobs_headers = ['id', 'job']
    
    #define col_headers according to file that is currently being processed
    if new_filename == valid_filenames[0]:
        col_headers = hired_employees_headers
    elif new_filename == valid_filenames[1]:
        col_headers = departments_headers
    elif new_filename == valid_filenames[2]:
        col_headers = jobs_headers
    else:
        return 'No valid file selected'
    
    #read csv with pandas and store it in a dataframe, file is delimited by comma, hence the [sep=','] parameter
    data_df = pd.read_csv(file_path, names=col_headers, header=None, sep=',')
    #data_df.fillna(0, inplace = True) #replace blanks with nulls

    #connection to MSSQL Server
    try:
        conn = pyodbc.connect(driver='{SQL Server}', server='localhost\SQLEXPRESS', database='TEST_DB', trusted_connection='yes') #define DB connection
        cursor = conn.cursor() #object to execute SQL query
    except Exception as ex: #error handling when connection doesn't work
        return "DB connection error"

    #loop through data in pandas dataframe
    for i, row in data_df.iterrows():

        #HIRED EMPLOYEES SECTION
        if new_filename == valid_filenames[0]:

            #sql query string, positional arguments in ODBC are defined with the "?" symbol
            #added "IF NOT EXISTS..." statment for verifying whether or not a record to be inserted already exists in table
            sql_query = """IF NOT EXISTS (SELECT 1 FROM TEST_DB.dbo.HIRED_EMPLOYEES WHERE ID = ?)
                        BEGIN
                        INSERT TEST_DB.dbo.HIRED_EMPLOYEES (ID, NAME, DATETIME, DEPARTMENT_ID, JOB_ID) VALUES (?, ?, ?, ?, ?)
                        END;"""
            insert_into_values = (row['id'], row['id'], row['name'], row['datetime'], row['department_id'], row['job_id']) #values to be inserted
            
            #validation #1: check if values are null or NaN
            if (pd.isnull(insert_into_values[1]) or pd.isnull(insert_into_values[2]) or pd.isnull(insert_into_values[3]) or pd.isnull(insert_into_values[4]) or pd.isnull(insert_into_values[5])):
                if (pd.isna(insert_into_values[1]) or pd.isna(insert_into_values[2]) or pd.isna(insert_into_values[3]) or pd.isna(insert_into_values[4]) or pd.isna(insert_into_values[5])):
                    continue
            
            #validation #2: check if integer values have the correct data type
            if int(insert_into_values[1]) != insert_into_values[1] or int(insert_into_values[4]) != insert_into_values[4] or int(insert_into_values[5]) != insert_into_values[5]:
                continue

            cursor.execute(sql_query, insert_into_values) #execute sql query
            conn.commit() #confirm transaction
        
        #DEPARTMENTS SECTION
        elif new_filename == valid_filenames[1]:

            #sql query string, positional arguments in ODBC are defined with the "?" symbol
            #added "IF NOT EXISTS..." statment for verifying whether or not a record to be inserted already exists in table
            sql_query = """IF NOT EXISTS (SELECT 1 FROM TEST_DB.dbo.DEPARTMENTS WHERE ID = ?)
                        BEGIN
                        INSERT TEST_DB.dbo.DEPARTMENTS(ID, DEPARTMENT) VALUES (?, ?)
                        END;"""
            insert_into_values = (row['id'], row['id'], row['department']) #values to be inserted

            #validation #1: check if values are null or NaN
            if (pd.isnull(insert_into_values[1]) or pd.isnull(insert_into_values[2])):
                if (pd.isna(insert_into_values[1]) or pd.isna(insert_into_values[2])):
                    continue
            
            #validation #2: check if integer values have the correct data type
            if int(insert_into_values[1]) != insert_into_values[1]:
                continue

            cursor.execute(sql_query, insert_into_values) #execute sql query
            conn.commit() #confirm transaction
        
        #JOBS SECTION
        elif new_filename == valid_filenames[2]:

            #sql_query = "INSERT INTO TEST_DB.dbo.JOBS (ID, JOB) VALUES (?, ?)" #sql query string, positional arguments in ODBC="?"
            #added "IF NOT EXISTS..." statment for verifying whether or not a record to be inserted already exists in table
            sql_query = """IF NOT EXISTS (SELECT 1 FROM TEST_DB.dbo.JOBS WHERE ID = ?)
                        BEGIN
                        INSERT TEST_DB.dbo.JOBS(ID, JOB) VALUES (?, ?)
                        END;"""
            insert_into_values = (row['id'], row['id'], row['job']) #values to be inserted

            #validation #1: check if values are null or NaN
            if (pd.isnull(insert_into_values[1]) or pd.isnull(insert_into_values[2])):
                if (pd.isna(insert_into_values[1]) or pd.isna(insert_into_values[2])):
                    continue
            
            #validation #2: check if integer values have the correct data type
            if int(insert_into_values[1]) != insert_into_values[1]:
                continue

            cursor.execute(sql_query, insert_into_values) #execute sql query
            conn.commit() #confirm transaction
        
        else:
            print("No data to add")

#function to avoid "error 404" when web-server can't return anything to client request
def website_not_found(error):
    return "<h1>La pagina no existe</h1>", 404

#app runs if app.py is being executed from main snippet
if __name__ == '__main__':
    app.register_error_handler(404, website_not_found) #"Error 404" handler
    app.run(debug=True) #run app with debug mode activated
