from currency_converter  import CurrencyConverter
c = CurrencyConverter()

def xe(amount:float,input_currency:str,output_currency:str):
    converted_amount=round(c.convert(float(amount), input_currency.upper(),output_currency.upper()),2)
    return('Currently '+str(amount)+' '+input_currency.upper()+' is equivalent to '+str(converted_amount)+' '+output_currency.upper())