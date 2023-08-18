from requests import get, post, put, delete
portolio_id = -1
def print_response(response):
	print(response)
	if response.text:
		print(response.json())
	if response.status_code == 201:
		print(f"Asset created at {response.headers['Location']}")
		
res = get(f"http://localhost:5000/")
print_response(res)
res = post("http://localhost:5000/", json={"asset_type": 'Bond' , "asset_ticker": "NULL",
                                           "asset_name": '5-year Treasury Bond', "amount_holding": 1,
                                            "buy_datetime": '2023-08-17 12:46:00',
                                           "mature_datetime": '2028-08-17 12:46:00', "currency": 'USD'})
print_response(res)

if res.status_code == 201 and "Location" in res.headers:
    URI = res.headers["Location"]
    portolio_id = int(URI.split('/')[-1])
else:
        exit()

res = get(f"http://localhost:5000/{portolio_id}")
print_response(res)

res = put(f"http://localhost:5000/{portolio_id}", json={"asset_type": 'Bond' , "asset_ticker": "NULL",
                                           "asset_name": '5-year Treasury Bond', "amount_holding": 1,
                                            "buy_datetime": '2023-08-18 12:46:00',
                                           "mature_datetime": '2028-08-18 12:46:00', "currency": 'USD'})
print_response(res)

res = get(f"http://localhost:5000/{1}")
print_response(res)

res = delete(f"http://localhost:5000/{portolio_id}")
print_response(res)

res = get(f"http://localhost:5000/{portolio_id}")
print_response(res)

