import json
import requests
import bs4
import threading

try:
	from keys import *
except:
	API_KEY = raw_input("API_KEY: ")

headers = {
'authorization': "Bearer {}".format(API_KEY),
'cache-control': "no-cache",
}

def log(string):
	print(string)

def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

def get_mobile_site(url):
	log("Getting URL: {}".format(url))
	# Gets the mobile site
	headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except Exception as exp:
			log("Network Call Failed #{} | URL: {} | Exception: {}".format(i, url, exp))
	log("Final Network Call Failed: {}".format(url))

def get_desktop_site(url):
	# Gets the desktop site
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except Exception as exp:
			log("Network Call Failed #{} | URL: {} | Exception: {}".format(i, url, exp))
	log("Final Network Call Failed: {}".format(url))
 
#need the following parameters (type dict) to perform business search. 
#params = {'name':'walmart supercenter', 'address1':'406 S Walton Blvd', 'city':'bentonville', 'state':'ar', 'country':'US'}


def search(term, location, saveAs="file.csv"):
	params = {'term':term, 'location':location}
	log("Searching: {} in {}".format(term, location))
	#param_string = urllib.parse.urlencode(params)
	#conn = http.client.HTTPSConnection("api.yelp.com")
	#res = requests.get("https://api.yelp.com/v3/businesses/matches/best?", headers=headers, params=params)
	res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)

	#res = conn.getresponse()
	#data = res.read()
	#data = json.loads(data.decode("utf-8"))
	data = res.json()
	log(json.dumps(data, indent=4))
	#input("CONTINUE")
	a = []
	# Iterate over all of the results for this search

	results = data["businesses"]
	#print(len(results))

	return results

def main(key, verbose):
	threads = input("Number of threads [Default 20]: ")
	if len(threads) == 0:
		threads = 20
	search_term = input("Search Term: ")
	location = input("City: ")
	state = input("State: ")
	saveAs = input("CSV Filename [leave blank for stdout only]: ")
	print("\n\n")
	if len(saveAs) == 0:
		search(search_term, int(threads), location + " " + state)
	else:
		search(search_term, int(threads), location + " " + state, saveAs)


if __name__ == '__main__':
	print("""
** SMALL BUSINESS FINDER 2.0 **
\nThis script uses the Yelp fusion API to find
nearby small businesses with no online presence\n\n
	""")
	search_term = raw_input("Search Term: ")
	location = raw_input("City: ")
	state = raw_input("State: ")
	print("\n\n")
	print json.dumps(search(search_term, location + " " + state), indent=4)
	