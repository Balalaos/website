from flask import *
from scripts.loan import MainPage, RegistrationForm
from scripts.tic_tac_toe import TicTacToe
from scripts.convertor import Currency_Convertor
from decouple import config



#defining app and classes
app = Flask(__name__)
try:
    app_key = config('APP_SECRET_KEY')
except:
    app_key = "asdfosdfawefkkoffgia42"
app.secret_key = app_key
tictactoe = TicTacToe()
convertor = Currency_Convertor()



# Main page of the website where user can choose what page to visit
@app.route("/")
def home():
	return render_template("main_pages/home.html")


# Page telling about the developer
@app.route("/about-me")
def about_me():
	return render_template("main_pages/about.html")



## Loan app where user can borrow money or find an information about the existing loans
# Main page of the app where user can find information about the loans using ID number
@app.route("/loan-app", methods=["GET", "POST"])
def loan():
    message = ''
    if request.method == 'POST':
        find_data = MainPage()
        try:
            # This function search id through the database and shows information on another page
            user_data = find_data.search(request.form['id'])
            return render_template('projects/loan/show_loans.html', data=user_data)
        # In the case of error or if there is not such ID app shows message about that
        except find_data.Error as e:
            message = e
    return render_template("projects/loan/loan.html", message = message)
  
   
# This is loan registration page, where user can borrow a new loan by entering his data and the desired amount of money
@app.route("/loan-app/registration", methods=["GET", "POST"])
def loan_registration():
    message = ''
    if request.method == 'POST':
        registration_form = RegistrationForm()
        try:
            # This function checks if the entered data correct, if a borrower is blacklisted or there was loan request in 24 hours 
            # After it saves borrower data to database and returns it for the showing
            register_data = registration_form.submit_registration(request.form)
            #prepare data for showing
            rewrite_data = MainPage()
            user_data = rewrite_data.rewrite(register_data)
            return render_template('projects/loan/show_loans.html', data=user_data)
        # In the case of error app shows message about that
        except registration_form.Error as e:
            message = e
    return render_template('projects/loan/register.html', message = message)



# This is an application for converting money from one currency to another through intermediary currency
@app.route("/currency-exchanger", methods=["GET", "POST"])
def exchanger():
    message = ''
    if request.method == 'POST':
        try:
            # This function takes curency rates using API and finds the best option for costumer and company
            # It returns all exchange data and error message if there is problem with connection to API
            data, message = convertor.convert_currency(request.form)
            return render_template("projects/exchanger/result.html", data = data, message=message)
        except convertor.Error as e:
            message = e
    return render_template("projects/exchanger/exchanger.html", message = message)



# This is general TIC TAC TOE game. It can be played with another person
# TODO: playing against computer
@app.route("/games/tic-tac-toe", methods=["GET", "POST"])
def tic_tac_toe():
    board = tictactoe.get_board()
    message = ''
    # reset field when page is downloaded
    if request.method == "GET":
        board = tictactoe.reset()
    if request.method == 'POST':
        # reset field when RESET button is pressed
        if request.form.get("RESET"):
            board = tictactoe.reset()
        else:
            # This function takes entered field and checks if there winner or not
            board, message = tictactoe.game(request.form)
    return render_template("games/tic_tac_toe.html", board=board, message=message)

    

if __name__ == '__main__':
	app.run(debug=True)
