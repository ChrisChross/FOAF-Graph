import numpy as np
from PIL import Image, ImageDraw
import requests
import os
import shutil


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
  x, y = im.size
  size = max(min_size, x, y)
  new_im = Image.new('RGB', (size, size), fill_color)
  new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
  return new_im


# Open the input image as numpy array, convert to RGB
def circle_image(image_link, node_format="circle", size=(250, 250)):
  url = image_link
  response = requests.get(url, stream=True)

  if not os.path.exists("images/"):
    os.makedirs("images/")
    if not os.path.exists("images/original/"):
      os.makedirs("images/original/")
    if not os.path.exists("images/cropped/"):
      os.makedirs("images/cropped/")

  img1 = image_link.rsplit("/", 1)[1]
  img2 = img1.rsplit("?", 1)[0]
  image_name = img2.rsplit(".", 1)[0]
  # display(image_name)
  # print(type(image_name))

  with open(f'images/original/{img2}', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
  del response

  img = Image.open(f"images/original/{img2}").convert("RGB")
  if node_format == "circle":
    img = make_square(img, fill_color=(255, 255, 255, 0))

  img.thumbnail(size, Image.ANTIALIAS)
  npImage = np.array(img)
  h, w = img.size

  # Create same size alpha layer with circle
  alpha = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(alpha)
  draw.pieslice([0, 0, h, w], 0, 360, fill=255)

  # Convert alpha Image to numpy array
  npAlpha = np.array(alpha)

  # Add alpha layer to RGB
  npImage = np.dstack((npImage, npAlpha))
  circle_image = Image.fromarray(npImage)
  Image.fromarray(npImage).save(f'images/cropped/circle_{image_name}.png')
  base_filename = f'./images/cropped/circle_{image_name}.png'
  #dir_name = os.getcwd()
  #full_file_path = os.path.join(dir_name, base_filename)
  return base_filename #full_file_path
