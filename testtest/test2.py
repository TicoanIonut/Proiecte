import requests
import pandas as pd
response = requests.get("http://api.open-notify.org/astros.json")
print(response.status_code)
print(response.json())
res = pd.DataFrame(response.json()["people"])
print(res.head())
print(res)

