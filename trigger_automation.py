import urllib.request

# Make a request to the website
url = 'https://automation.rubick.org/'
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)

# Read the response content
content = response.read()
print(content)