from requests import get, post, put, delete
portfolio_id = -1
def print_response(response):
	print(response)
	if response.text:
		print(response.json())
	if response.status_code == 201:
		print(f"Asset created at {response.headers['Location']}")
		
res = get(f"http://localhost:5000/")
print_response(res)

# Create(i.e.) Buy new asset
res = post("http://localhost:5000/", json={"asset_type": 'stock' , "asset_ticker": "APPL",
                                           "asset_name": 'Apple Inc.', "amount_holding": 10,
                                            "buy_datetime": '2023-08-17 12:46:00',
                                           "mature_datetime": '2028-08-17 12:46:00', "currency": 'USD'})
print_response(res)

if res.status_code == 201 and "Location" in res.headers:
    URI = res.headers["Location"]
    portfolio_id = int(URI.split('/')[-1])
else:
        exit()

portfolio_id = 5
res = get(f"http://localhost:5000/{portfolio_id}")
print_response(res)

# Buy action
res = put(f"http://localhost:5000/{portfolio_id}", json={"transaction_type":"BUY",
                                                         "transaction_amount":"10",
                                                         "transaction_price":"140",
                                                         "transaction_datetime":'2023-08-17 12:46:00'})
print_response(res)

# Sell action
res = put(f"http://localhost:5000/{portfolio_id}", json={"transaction_type":"SELL",
                                                         "transaction_amount":"50",
                                                         "transaction_price":"143",
                                                         "transaction_datetime":'2023-08-17 12:48:00'})
print_response(res)

# get information about certain asset
res = get(f"http://localhost:5000/{portfolio_id}")
print_response(res)


