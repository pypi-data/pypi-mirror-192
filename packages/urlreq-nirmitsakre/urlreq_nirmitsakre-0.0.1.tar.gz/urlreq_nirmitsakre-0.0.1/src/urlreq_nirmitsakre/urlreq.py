import urllib.request

def urldatareq(url):
	response = urllib.request.urlopen(url)
	return data = response.read()
