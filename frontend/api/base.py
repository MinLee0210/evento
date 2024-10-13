import requests

def get_quote(url:str):
    try: 
        if not url: 
            raise ValueError("URL is missing")
        quote_res = requests.get(url)
        # Check for successful response
        if quote_res.status_code == 200:  # 201 Created
            print("GET created successfully!")
            return quote_res.json()
        else:
            print(f"Error creating GET: {quote_res.status_code}")
            raise requests.HTTPError(f"Error {quote_res.status_code}: {quote_res.text}")
    except Exception as e: 
        raise requests.HTTPError(e)