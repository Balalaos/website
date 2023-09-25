# WEBSITE
This is a set of various programs I created combined on one website. Currently the loan and exchange apps and tic tac toe game are ready. Battleship is under development now.

## Instalation
This is Python Flask app. It does not required specific libraries, but app uses some general pip libraries, such as flask, sqlite3 etc. Before running the app APP_SECRET_KEY should be added in .env file (app will work without that, but in this case it will use secret key mentioned in the main code). For using the app run app.py file and go to http://127.0.0.1:5000 page in your web browser. You will get to the main page where you can navigate to another web pages with projects.

## Projects
On every webpage with project or game there is short description about every project. There is writtten some usage instructions.

### Loan app
This is a loan app, where user can make a new loan or find the information about the existed loan.

### Exchanger app
This is an application for converting money from one currency to another. The transfer takes place through intermediary currency.
To obtain data on current exchange rates, the API from SWEDBANK is used. For using SWEDBANK API you need create an .env file and add your SWEDBANK API url, request ID and cliend ID there (use CONVERTOR_URL, CONVERTOR_REQUEST_ID, CONVERTOR_APP_ID respectively). If you do not enter this tokens app will use saved currencies rates data.


### Tic Tac Toe
This is the basic Tic Tac Toe game, which you can play with you friend. Playing agianst computer is under development.