import telebot
from telebot import types
import os
import matplotlib.pyplot as plt
from PIL import  Image
import numpy as np
import io
import json
import requests
import random

my_chat_id = 521838846
bot = telebot.TeleBot('1041646233:AAHffk2S581omIFIZW1H7K0YUVFA2EzJ43E')
@bot.message_handler(commands=["start"])
def welcome(message):
	text = "Send me your photo ;)"
	bot.send_message(message.chat.id,text)


def predict_result(image_arr):
	data = json.dumps({"signature_name": "serving_default", "instances": image_arr.tolist()})
	headers = {"content-type": "application/json"}
	json_response = requests.post('http://localhost:8501/v1/models/1113_model:predict', data=data, headers=headers)
	prediction = json.loads(json_response.text)['predictions']
	class_pred = np.where(prediction[0] == np.amax(prediction[0]))[0][0]
	print(prediction)
	return class_pred

def save_image(image,folder_path):
	name=random.randint(0,99999999999)

	image.save(f"{folder_path+str(name)}+.jpg", "JPEG", quality=85)

@bot.message_handler(content_types=['photo'])
def photo(message):

	fileID = message.photo[-1].file_id

	file_info = bot.get_file(fileID)

	downloaded_file = bot.download_file(file_info.file_path)

	image= Image.open(io.BytesIO(downloaded_file))
	image_arr = np.asarray(image.resize((224, 224)))
	image_std = (image_arr.reshape(1,224,224,3))/np.std(image_arr)
	predict  = predict_result(image_std)


	if predict == 1 :
		bot.send_message(message.chat.id, "IN MASK")
		bot.send_message(message.chat.id, "😷")

		save_image(image,'/home/vladislav/PycharmProjects/tftest/Images/saved_from_telegram/1/')

	elif predict == 0 :
		bot.send_message(message.chat.id, "WITHOUT MASK😀")

		save_image(image, '/home/vladislav/PycharmProjects/tftest/Images/saved_from_telegram/0/')
	elif predict == 2 :
		#bot.send_message(message.chat.id, "Please, send another photo.")

		bot.send_message(message.chat.id, "Please, send me another photo. "
										  "May be, i can't see your face clearly on it.")


		save_image(image, '/home/vladislav/PycharmProjects/tftest/Images/saved_from_telegram/2/')
	else :
		'''bot.send_message(message.chat.id, "I think, you have forgotten to put on your mask, "
										  "though not with huge confidence. ")'''
		bot.send_message(message.chat.id, "WITHOUT MASK😀")

		save_image(image, '/home/vladislav/PycharmProjects/tftest/Images/saved_from_telegram/3/')

bot.polling()




