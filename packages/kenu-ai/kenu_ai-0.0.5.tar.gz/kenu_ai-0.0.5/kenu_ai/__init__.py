from googletrans import Translator
import requests

def chat(value):
	translator = Translator()
	t = translator.translate(value, dest="en")
	response = requests.get("http://api.brainshop.ai/get?bid=153868&key=rcKonOgrUFmn5usX&uid=1&msg=" + t.text)
	veri = response.text.split(':"')[-1].split('"}')[0]
	translated = translator.translate(veri, dest="tr")
	return translated.text

