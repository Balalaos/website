import requests
import json
import math, os
from decouple import config
from include_files.convertor.currencies_data import rates_dict

# This class:
# downloading rates
# caching them
# converting currencies from one to another
# searching best ones for costumer and server
# showing them on the screen
class Currency_Convertor():
    def __init__(self):
        pass
    
    class Error(Exception):
        def __init__(self, message):
            super().__init__(message)
        
    # This function is downloading rates and cahcing them.
    # TODO: optimize API request - Previously currency rates should be loaded with app start, now they are loaded with user request
    def get_currency_rates(self):
        currencies = ["USD", "EUR", "GBP", "NZD", "CAD", "AUD", "CHF", "NOK", "SEK", "CNH"]
        # Link for API
        url = config('CONVERTOR_URL')
        # All needed headers
        headers = {
            "X-Request-ID": config('CONVERTOR_REQUEST_ID')
        }
        app_id = config('CONVERTOR_APP_ID')
        
        # In the used API currencies rates are presented in only one way. For example there is EURUSD rate, but there is not USDEUR rate.   
        # To find opposite rate 1 is divided by provided by API rate.
        # For example: API send data for EUR -> USD exchange - 1.04, in this case USD -> EUR exchange rate = 1/1.04
       
        # Because of that there is need to check if currency is available in API and in what format. For that function checks all available 
        # formats in the json file. 
        json_file_path = os.path.dirname(os.path.realpath(__file__)) 
        json_file_path = json_file_path.replace("scripts", "include_files\\convertor\\all_currencies.json")

        # Open the JSON file for reading
        with open(json_file_path, "r") as json_file:
            # Parse the JSON data from the file
            all_currencies = json.load(json_file)
        
        data = {'USD': {}, 'EUR': {}, 'GBP': {}, 'NZD': {}, 'CAD': {}, 'AUD': {}, 'CHF': {}, 'NOK': {}, 'SEK': {}, 'CNH': {}}
        for currency in currencies:
            # Check all available currencies and add the to the API request
            intermediaries = [currency + c for c in currencies if c not in [currency] and currency + c in all_currencies]
            intermediaries = ','.join(intermediaries)
            querystring = {"currencyPairs":intermediaries,"app-id":app_id}
            # Get all rates for current currency
            if intermediaries:
                response = requests.request("GET", url, headers=headers, params=querystring)
                response = response.json()
            for pos in response:
                # Find exchange rate from first currency to second
                money = (pos["askRate"]+pos["bidRate"])/2
                data[pos["currencyPair"][:3]].update({pos["currencyPair"][3:]:round(money,7)})
                # Find exchange rate from second currency to first
                data[pos["currencyPair"][3:]].update({pos["currencyPair"][:3]:round((1/money),7)})
        # Save data in cache
        return data
        
       
    # This function get rates of 2 named by user currencies from cache 
    def get_rates_for_currency(self, From_currency, To_currency, currency_rates):
        # Coppies rates from first currency to intermidiary currency
        to_intermediaries_rates = {}
        to_intermediaries_rates.update(currency_rates[From_currency])
        # Deleting the second currency from dictonary
        del to_intermediaries_rates[To_currency]
        
        # Coppies rates from intermidiary currency to second currency
        # As money should be converted to second currency from intermidiary, this loop searching all rates from intermidiary 
        # currency to second currency
        from_intermediaries_rates = {}
        for currency in currency_rates:
            for item in currency_rates[currency]:
                if item == To_currency and currency != From_currency:
                    from_intermediaries_rates[currency] = currency_rates[currency][item]
        return to_intermediaries_rates, from_intermediaries_rates



    # This function convert entered by user amount from one currency to another
    def convert_currency(self, data):
        message = ''
        # This function takes API provided rates
        try:
            currency_rates = self.get_currency_rates()  
        # If API is not available, saved rates data is used. USer will get message about that
        except:
            currency_rates = rates_dict
            message = 'The saved currencies rates data was used'
            
        # Checks if entered number is float
        try:
            amount = float(data["amount"])
        except:
            raise self.Error("Please use numbers for amount")
        From_currency = data["from_currency"]
        To_currency = data["to_currency"]
        
        # Checks if currencies is different
        if From_currency == To_currency:
            raise self.Error("Please use different currencies")
        
        # Getting rates for converting from first currency to intermidiary currency and from intermidiary currency to final one
        to_intermediaries, from_intermediaries = self.get_rates_for_currency(From_currency, To_currency, currency_rates)
        to_intermediaries = dict(sorted(to_intermediaries.items()))
        from_intermediaries = dict(sorted(from_intermediaries.items()))
        
        profit = {}
        max_money = 0
        max_money_key = []
        max_profit = 0
        max_profit_key = []
        # This loop is making converting to intermidiary currency and the final one and finding the best options for user and service
        for currency in to_intermediaries:
            # Converting to intermidiary currency 
            to_intermediaries[currency] = amount * to_intermediaries[currency]
            # Converting to the final currency
            num = from_intermediaries[currency] * to_intermediaries[currency]
            
            # Searching the best options for user
            if num > max_money:
                max_money = num
                max_money_key = []
                max_money_key.append(currency)
            elif num == max_money:
                max_money_key.append(currency)
            max_money = round(max_money, 4)
            # Round numbers
            num = round(num, 4)
            from_intermediaries[currency] = num
            to_intermediaries[currency] = round(to_intermediaries[currency], 4)

            # Counting fractions of cents
            rounded_num = math.floor(num * 100)/100.0
            decimal_num =  round(num - rounded_num, 4)
            profit[currency] = decimal_num
            
            # Searching the best options for service
            if decimal_num > max_profit:
                max_profit = decimal_num
                max_profit_key = []
                max_profit_key.append(currency)
            elif decimal_num == max_profit:
                max_profit_key.append(currency)
        
        max_money_key = ', '.join(max_money_key)
        max_profit_key = ', '.join(max_profit_key)
        # Creating directory with all best options for user and service
        maximus = {"max_money": max_money, "max_money_key":max_money_key, "max_profit":max_profit, "max_profit_key":max_profit_key}
        # Returning all converted money to intermediaries currencies, to the final currency, also returning
        # best options and profit for intermediaries currencies 
        result = {}
        result["from_intermediaries_rates"] = from_intermediaries
        result["to_intermediaries_rates"] = to_intermediaries
        result["maximus"] = maximus
        result["profit"] = profit
        result["From_currency"] = From_currency
        result["To_currency"] = To_currency
        result["amount"] = amount
        return result, message

