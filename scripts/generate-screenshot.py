import requests
import logging
from html2image import Html2Image
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import shutil
import os
import sys

# enable logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger("linkedin-pikaso")

# set directory paths and file names
project_path = os.path.normpath('')
images_path = os.path.join(project_path, 'images')
data_path = os.path.join(project_path, 'data')
post_file = os.path.join(data_path, 'post.html')
img_template = os.path.join(project_path, 'template', 'template.png')
img_user_icon = os.path.join(project_path, 'template', 'img_user.jpeg')
img_linkedin_logo = os.path.join(project_path, 'template', 'linkedin_logo.png')
img_quote = os.path.join(project_path, 'template', 'quote.png')
img_mask = os.path.join(project_path, 'template', 'mask.png')
img_file = os.path.join(project_path, 'images', 'post.png')

# get user input
# embed_code = sys.argv[1]
embed_code = '<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7107451783974645760" height="905" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>'
# embed_code = '<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7108659246350639104" height="531" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>'
soup = bs(embed_code, 'html.parser')
iFrame = soup.find(title='Embedded post')
post_src = iFrame['src']
# post_height = int(iFrame['height'])
# post_width = int(iFrame['width'])
post_height = 1200
post_width = 1200

# get post content and write to HTML
response = requests.get(post_src, allow_redirects=True )
open(post_file, 'wb').write(response.content)
log.info('Response retrived from LinkedIn.')

# get required content from HTML
# get user image
html_soup = bs(response.content, 'html.parser')
user_img_html = html_soup.find("img", class_='inline-block')
user_img_url = user_img_html['data-delayed-url']
log.info(user_img_url)
with open(img_user_icon, 'wb') as f:
    f.write(requests.get(user_img_url, timeout=5).content)

# create image and add content
input_color = 'white'
img = Image.new(mode="RGBA", size=(post_height, post_height), color=input_color)

# add user image
mask = Image.open(img_mask).convert('L')
user_pict = Image.open(img_user_icon).resize((200,200))
user_pict_x = 100
user_pict_y = 900
img_file_output = ImageOps.fit(user_pict, mask.size, centering=(0.5,0.5))
img_file_output.putalpha(mask)
img.paste(img_file_output, (user_pict_x, user_pict_y),img_file_output )

# draw text
draw_image = ImageDraw.Draw(img)


# reusable method to get wrapped text
def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)


# add user name
user_name_html = html_soup.find("a", class_='text-sm')
user_name_text = user_name_html.text
font_ttf = os.path.join(data_path, 'BebasNeue-Regular.ttf')
user_name_font = ImageFont.truetype(font_ttf, 70)
user_name_font_color = "black"
user_name_x = 225
user_name_y = 900
draw_image.text((user_name_x, user_name_y), user_name_text, font=user_name_font, fill=user_name_font_color)

# add user role
user_role_html = html_soup.find("p", class_='!text-xs')
user_role_text = user_role_html.text

if len(user_role_text) > 72:
    user_role_text = user_role_text[:72] + '...'

font_ttf2 = os.path.join(data_path, 'Roboto-Light.ttf')
user_role_font = ImageFont.truetype(font_ttf2, 30)
user_role_font_color = "grey"
user_role_x = 380
user_role_y = 1040
draw_image.text((user_role_x, user_role_y), get_wrapped_text(user_role_text, user_role_font, 500), font=user_role_font, fill=user_role_font_color)

# add content
content_html = html_soup.find("p", class_='attributed-text-segment-list__content')
content = content_html.text

if len(content) > 150:
    font_size = 30
elif len(content) > 100:
    font_size = 50
else:
    font_size = 70

font_ttf3 = os.path.join(data_path, 'AltoneTrial-Regular.ttf')
content_font = ImageFont.truetype(font_ttf3, font_size)
content_font_color = "black"
content_x = 200
content_y = 350
draw_image.text((content_x, content_y), get_wrapped_text(content,content_font,800), font=content_font, fill=content_font_color)

# add logo
logo = Image.open(img_linkedin_logo).resize((150,150))
logo_x = 960
logo_y = 960
img.paste(logo, (logo_x, logo_y), logo)

# add quote
quote = Image.open(img_quote).resize((250,250))
quote_x = 100
quote_y = 100
img.paste(quote, (quote_x, quote_y), quote)

# add testingchief




# add likes?

img.show()
img.save(img_file)