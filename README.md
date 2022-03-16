# Python CRUD Based Flask Application
Fullstack python based web application built using:
- Flask
- NHSUK front-end library
- SQLAlchemy
- Heroku
- Github

## Run web application locally using virtualenv
1. In the root directory of python_app, run the following commands to start the application:

**Ensure you have pythonversion 3 installed on your machine**

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
2. Create a .env file in the root directory and copy and paste the following variables:
```
FLASK_APP=./web_application/run.py
FLASK_ENV=development
SECRET_KEY=my_secrets
DATABASE_URI= (Connection to your postgresDb. E.g: postgresql://mayankuser:mayankpassword@localhost/mayankdb)
```
3. Start the application by running: `flask run`

4. Visit `http://127.0.0.1:5000/` to view running application

## Alternative option
You deployed version of the application at https://python-app-mayank.herokuapp.com

Admin login details:
- Email: mayank.patel@admin.com
- Password: admin

Standard login details:
- Email: mayank.patel@standard.com
- Password: standard

## Application Tests
To run application tests, ensure python package `nose2` is installed (automatically installed through `requirement.txt` file)

Run tests using command below in your terminal:
`cd web_application && nose2`

## Application Monitoring
This application also has activity monitoring dashboard to view all activities such as amount of visits to specific page, API hits, any errors logs or compare report between two days or months.

Visit: https://python-app-mayank.herokuapp.com/dashboard to view the dashboard.

Default login details:
- Login: admin
- Password: admin

![alt text](Img/Monitoring-Dashboard.png)

