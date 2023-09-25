from flask import *
from scripts.loan import MainPage, RegistrationForm
from scripts.tic_tac_toe import TicTacToe
from scripts.convertor import Currency_Convertor
from decouple import config

app = Flask(__name__)
app_key = config('APP_SECRET_KEY')
app.secret_key = app_key
tictactoe = TicTacToe()
convertor = Currency_Convertor()


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/about-me")
def about_me():
	return render_template("about.html")



@app.route("/loan-app", methods=["GET", "POST"])
def loan():
    message = ''
    if request.method == 'POST':
        id = request.form['id']
        # this class checking if there a certain name in database and returns data
        find_data = MainPage()
        try:
            row = find_data.search(id)
            return render_template('loan/show_loans.html', data=row)
        except find_data.Error as e:
            message = e
    return render_template("loan/loan.html", message = message)
  
    
@app.route("/loan-app/registration", methods=["GET", "POST"])
def loan_registration():
    message = ''
    if request.method == 'POST':
        #this class checks if the entered data correct, if a borrower is blacklisted or there was loan request in 24 hours 
        registration_form = RegistrationForm()
        try:
            register_data = registration_form.submit_registration(request.form)
            #prepare data for showing
            print(register_data)
            rewrite_data = MainPage()
            data = rewrite_data.rewrite(register_data)
            return render_template('loan/show_loans.html', data=data)
        except registration_form.Error as e:
            message = e
            
        
    return render_template('loan/register.html', message = message)



@app.route("/currency-exchanger", methods=["GET", "POST"])
def exchanger():
    message = ''
    if request.method == 'POST':
        try:
            data = convertor.convert_currency(request.form)
            return render_template("exchanger/result.html", data = data)
        except convertor.Error as e:
            message = e
    return render_template("exchanger/exchanger.html", message = message)



@app.route("/games/tic-tac-toe", methods=["GET", "POST"])
def tic_tac_toe():
    board = tictactoe.get_board()
    message = ''
    if request.method == "GET":
        board = tictactoe.reset()
    if request.method == 'POST':
        if request.form.get("RESET"):
            board = tictactoe.reset()
        else:
            board, message = tictactoe.game(request.form)
    return render_template("games/tic_tac_toe.html", board=board, message=message)

    

# execute command with debug function
if __name__ == '__main__':
	app.run(debug=True)
