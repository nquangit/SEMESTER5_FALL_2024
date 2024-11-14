# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = "http://py4e-data.dr-chuck.net/comments_2091006.html"
url = input("Enter - ")
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

nums = []

# Retrieve all of the span tags
tags = soup('span')
for tag in tags:
    content = tag.contents[0]
    try:
        number = int(content)
    except:
        continue

    nums.append(number)

print(f"Count: {len(nums)}")
print(f"Sum: {sum(nums)}")
