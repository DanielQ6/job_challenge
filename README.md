
# Software needed

* Visual Studio Code
* MSSQL Server
* Power BI Desktop

# Steps to make this project work

## 1- MS SQL Server

New database and tables were created by using the code from ddl.sql file

## 2- Visual Studio Code:

Create new folder called: API_FLASK_SQLSERVER

Open the terminal and run the following code to create a new environment: virtualenv -p python env

Activate the environment by executing: .\env\Scripts\activate

Install Flask, which will be used to create the restAPI:
pip install flask

Inside main folder (API_FLASK_SQLSERVER), create another folder called: static
This is the place where csv will be stored when getting them through the web-server

Create a new folder called: src
Inside that folder, create a new file called: app.py
Write the restAPI code here (code can be found in the file called: restapi_code.txt)
Inside src folder, create another one called: templates, and add the file called: index.html
This HTML file has the source code of the website that user can use to transfer csv data into MSSQL Server tables

Now, if website is used, data will be taken from the csv files and transferred into MS SQL Server tables created beforehand

To access website, execute code and enter the IP+route in a new browser window, e.g.: http://127.0.0.1:5000/add_file
"add_file" is the route

## 3- MS SQL Server (again)

Created tables for challenge 2 (visuals for requirement 1 and 2) using the code from the following files:
challenge_2_requirement_1.sql and challenge_2_requirement_2.sql

## 4- Power BI Desktop

Visual for both requirements were created in 1 single tab
Data was pulled from tables created in SQL Server (step #3)
"Import" was used as the connection method to cached the data in the file itself, therefore it could be opened by anyone who has PBI Desktop installed without worrying about DB credentials
