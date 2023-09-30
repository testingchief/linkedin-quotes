import requests
import logging
from html2image import Html2Image
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw, ImageOps
from pilmoji import Pilmoji
import os
import sys

# enable logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger("linkedin-quotes")

# get user input
embed_code = sys.argv[1]
if len(sys.argv) > 2:
    template_color = sys.argv[2]
else:
    template_color = ''

# set directory paths and file names
project_path = os.path.normpath('')
images_path = os.path.join(project_path, 'images')
data_path = os.path.join(project_path, 'data')
templates_path = os.path.join(project_path, 'templates')
post_file = os.path.join(data_path, 'post.html')
img_template = os.path.join(templates_path, 'template' + template_color + '.png')
img_user_icon = os.path.join(templates_path, 'img_user.jpeg')
img_linkedin_logo = os.path.join(templates_path, 'linkedin_logo.png')
img_quote = os.path.join(templates_path, 'quote.png')
img_mask = os.path.join(templates_path, 'mask.png')
img_name = 'post.png'
img_file = os.path.join(images_path, img_name)
log.info('Image file name set as %s', img_name)

# read user input
post_src = 'https://www.linkedin.com/embed/feed/update/' + embed_code
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
log.info('Image URL: %s', user_img_url)
with open(img_user_icon, 'wb') as f:
    f.write(requests.get(user_img_url, timeout=5).content)
log.info('User image retrieved')

# create image and add content
# input_color = 'white'
# img = Image.new(mode="RGBA", size=(post_height, post_height), color=input_color)
img = Image.open(img_template)

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

# reusable method to get wrapped text with line break
def get_wrapped_text_nlfix(text: str, font: ImageFont.ImageFont, line_length: int): 
    return "\n".join([get_wrapped_text(line, font, line_length) for line in text.splitlines()])

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
content_length = len(content)
content_size = 1500
log.info('Content fetched')
# log.info(content)
log.info('Content length: %s', content_length)

if len(content) <= 100:
    font_size = 90
elif len(content) > 100 and len(content) <200:
    font_size = 60
elif len(content) >= 200 and len(content) <500:
    font_size = 35
elif len(content) >= 500 and len(content) <1000:
    font_size = 25
elif len(content) <1500:
    font_size = 15
else:
    content = content[:content_size] + ' ...'
    font_size = 15


font_ttf3 = os.path.join(data_path, 'Gontserrat-Light.ttf')
content_font = ImageFont.truetype(font_ttf3, font_size)
content_font_color = "black"
content_x = 200
content_y = 350

with Pilmoji(img) as pilmoji:
    pilmoji.text((200, 350), get_wrapped_text_nlfix(content.strip(), content_font, 900), (0,0,0), content_font)


# add testingchief
brand_text = '@testingchief'
font_ttf4 = os.path.join(data_path, 'Roboto-Light.ttf')
brand_font = ImageFont.truetype(font_ttf4, 15)
brand_font_color = "grey"
brand_x = 965
brand_y = 1130
draw_image.text((brand_x, brand_y), brand_text, font=brand_font, fill=brand_font_color)

# add created by
creator_text = 'Created with linkedin-quotes'
brand_x = 920
brand_y = 1110
draw_image.text((brand_x, brand_y), get_wrapped_text_nlfix(creator_text.strip(), brand_font, 200), font=brand_font, fill=brand_font_color)


# add likes & time?
# TODO

img.save(img_file)
# img.show()