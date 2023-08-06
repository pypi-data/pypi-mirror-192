import requests
import json
import pandas as pd
import datetime as dt

class nasdaq_grabber:
  def __init__(self):
      self.headers = {
        "authority": "api.nasdaq.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "origin": "https://www.nasdaq.com",
        "referer": "https://www.nasdaq.com/",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

  def nasdaq_stocks(self, limit):
    url = "https://api.nasdaq.com/api/screener/stocks"

    querystring = {"tableonly":"true","limit":str(limit),"offset":"0"}

    response = requests.request("GET", url, headers=self.headers, params=querystring)
    json_r = json.loads(response.text)

    return(pd.json_normalize(json_r['data']['table']['rows']))

  def nasdaq_data(self, ticker, type_key):
    types = { 1: 'targetprice',
             2: 'peg-ratio',
             3: 'estimate-momentum',
             4: 'earnings-forecast',
             5: 'earnings-surprise',
             6: 'eps'}

    url = f"https://api.nasdaq.com/api/analyst/{ticker}/{types[type_key]}"

    response = requests.request("GET", url, headers=self.headers)
    json_r = json.loads(response.text)

    return(pd.json_normalize(json_r['data']))

  def nasdaq_financals(self, ticker, frequency):
    # frequency 1 for annual and 2 for semi annual #
    url = f"https://api.nasdaq.com/api/company/{ticker}/financials"
    querystring = {"frequency":str(frequency)}

    response = requests.request("GET", url,  headers=self.headers, params=querystring)
    json_r = json.loads(response.text)

    return(pd.json_normalize(json_r['data']))

  def nasdaq_historical_price(self, ticker, from_date, to_date):
    url = f"https://api.nasdaq.com/api/quote/{ticker}/historical"
    date_format = "%Y-%m-%d"
    a = dt.datetime.strptime(from_date, date_format)
    b = dt.datetime.strptime(to_date, date_format)
    delta = b - a
    
    querystring = {"assetclass":"stocks","fromdate":str(from_date),"limit":str(delta.days),"todate":str(to_date)}

    response = requests.request("GET", url, headers=self.headers, params=querystring)
    json_r = json.loads(response.text)
    df = pd.json_normalize(json_r['data']['tradesTable']['rows'])
    df['volume'] = pd.to_numeric(df['volume'].str.replace(',',''))

    for c in ['close','open','high','low']:
      df[c] = pd.to_numeric(df[c].str[1:].replace(',',''))

    return(df)
