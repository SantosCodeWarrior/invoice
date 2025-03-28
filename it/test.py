import requests

api_url="http://0.0.0.0:8004/hb/get_chm_data/"
api_method="GET"
parameters={'key'	: 	"938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
response = requests.get(api_url, params=parameters)
print(response.content)