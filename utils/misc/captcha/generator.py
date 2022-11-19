import os
from pathlib import Path
import random
from captcha.image import ImageCaptcha



class CaptchaPhoto:
	def __init__(self):
		self.key = None
		self.path = None

		self.image = ImageCaptcha(width=280, height=90)
		self.symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


	def generate_captcha(self):
		random.shuffle(self.symbols)
		captcha_key = ''.join(self.symbols)[:6]
		cur_dir = Path(__file__).parent
		img_path = f'{cur_dir}\img\{captcha_key}.jpg'

		self.image.generate(captcha_key)
		self.image.write(captcha_key, img_path)

		self.key = captcha_key
		self.path = img_path