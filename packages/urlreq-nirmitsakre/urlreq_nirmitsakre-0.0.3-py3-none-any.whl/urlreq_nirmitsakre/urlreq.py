import urllib.request

def urldatareq(url):
	response = urllib.request.urlopen(url)
	return response.read()
