import requests
import logging
from html2image import Html2Image
from bs4 import BeautifulSoup as bs
import os
import sys

# enable logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# set directory paths and file names
project_path = os.path.normpath('')
images_path = os.path.join(project_path, 'images')
data_path = os.path.join(project_path, 'data')
post_file = os.path.join(data_path, 'post.html')
img_template = os.path.join(project_path, 'template', 'template.png')
# screenshot = os.path.join(images_path, 'screenshot.png')

# get user input
# embed_code = sys.argv[1]
embed_code = '<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7107451783974645760" height="905" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>'
soup = bs(embed_code, 'html.parser')
iFrame = soup.find(title='Embedded post')
post_src = iFrame['src']
post_height = int(iFrame['height'])-250
post_width = int(iFrame['width'])

# get post content and write to HTML
response = requests.get(post_src, allow_redirects=True )
open(post_file, 'wb').write(response.content)

# convert HTML to Image
hti = Html2Image()
hti.size = (post_width, post_height)
hti.screenshot(html_file=post_file, save_as='screenshot.png')