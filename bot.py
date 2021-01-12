# A simple Telegram bot that learns from messages of users it chats with and replies; the messages it sends are generated through functions that use Markov chains, old messages the bot has received (they can be either completely 
# random or context-related) or a composition of messages that are linked in a semi-random manner from one or more files.
# The functions are completely customizable with little impact on the main
# This bot requires to be in a folder with a text file named MAINTEXTFILE and one named SECONDARYTEXTFILE else it will create such files. If you don't need a secondary text file, you can remove the function getphrase5() and getphrase6()

BOTNAME = "name" #fill this with the name of the bot so that if someone mentions it will automatically reply
RATE = 4 # rate at which the bot replies: 1 reply every 1 / (RATE * receivedMessages)
MAINTEXTFILE = "main.txt"#name of the main text file
SECONDARYTEXTFILE = "secondary.txt" #name of the secondary text file
TOKEN = 'T0K3N' # pretty self explanatory but remember to put your token here

from telegram.ext import (MessageHandler, Filters, Updater, CommandHandler)
import requests
import re
from random import randint
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from io import open
from array import array
import markovify

# checks if the message ends with "cia", "6", "ma" or "mo" and returns an arbitrary string. You can either delete this and its call in resp or delete everything but res="0" 
def meme(frase):
	dim=len(frase)
	res="0"
	if (frase[dim-1]=='a' and frase [dim-2]=='i' and frase[dim-3]=='c'):
		res="ciai la faccia da pirla"
		return res
	elif(frase[dim-1]=='6'):
		res="6 scemo"
		return res
	elif(frase[dim-1]=='a' and frase[dim-2]=='m'):
		res="ma tu sorella"
		return res
	elif (frase[dim - 1] == 'o' and frase[dim - 2] == 'm'):
		res = "mortacci tua"
		return res
	return res

# returns a string generated through the markovify method NewlineText
def getphrase1(frase):

	with open(MAINTEXTFILE) as f:
		text = f.read()

	text_model = markovify.NewlineText(text)
	s = text_model.make_sentence()
	while s == "null":
		s=text_model.make_sentence(tries=100)
	return s

# returns a random string in MAINTEXTFILE
def getphrase2():
	f = open(MAINTEXTFILE, "r")
	lines=f.readlines()
	i=0
	for x in lines:
		i=i+1
	hi =randint(0, i-1)
	f.close()
	return (lines[hi])

# returns a string generated through the markovify method Text
def getphrase3(frase):

	with open(MAINTEXTFILE) as f:
		text = f.read()

	text_model = markovify.Text(text)
	s = text_model.make_sentence()
	while s == "null":
		s=text_model.make_sentence(tries=100)
	return s

# chooses a random word in the message and searches for that word in random messages in the text file until it finds a message containing that word; then returns that message as a string
def getphrase4(mess):
	datamess = mess.split()
	j=len(datamess)
	index = randint(0, j-1)
	parola = datamess[index]
	f = open(MAINTEXTFILE, "r")
	lines=f.readlines()
	i=0
	for x in lines:
		i=i+1
	for x in range (0, 100):
		hi =randint(0, i-1)
		if parola in lines[hi]:
			break
	f.close()
	return (lines[hi])

# returns a string generated through the markovify method combine which combines two messages; the latter are generated through the markovify method Text applied to each text file
def getphrase5():
	with open(MAINTEXTFILE) as f:
		texta = f.read()
	with open(SECONDARYTEXTFILE) as g:
		textb=g.read()

	modela = markovify.Text(texta)
	modelb = markovify.Text(textb)
	model_combo = markovify.combine([ modela, modelb ], [ 1, 1.5 ])
	s = model_combo.make_sentence()
	
	return s

# same as getphrase5() but the NewlineText method is applied instead
def getphrase6():
	with open(MAINTEXTFILE) as f:
		texta = f.read()
	with open(SECONDARYTEXTFILE) as g:
		textb=g.read()

	modela = markovify.NewlineText(texta)
	modelb = markovify.NewlineText(textb)
	model_combo = markovify.combine([ modela, modelb ], [ 1, 1.5 ])
	s = model_combo.make_sentence()
	
	return s

def resp(bot, g):
	global update_id
	op=randint(1, RATE) 
		
	frase=""
	for update in bot.get_updates(offset=update_id, timeout=5):
		update_id = update.update_id + 1

		if update.message:  # your bot can receive updates without messages
				# Reply to the message
			
			
			frase = update.message.text
			if frase is not None:
				if BOTNAME in frase.lower(): 
					op=1
				print(update.message.from_user.username)
			f = open(MAINTEXTFILE, "a")
			
			if frase:

				f.write("\r")
				f.write(frase)

				f.close()
				
			if frase and f!=0 and g>=5: # g is the number of messages the bot will wait before it can reply
				stat=meme(frase)
				if stat!="0":
					update.message.reply_text(stat)
			if op == 1 and frase and g!=0: # choosing whether to reply or not. "1" is an arbitrary value, however it needs to be <= than RATE
				sleep(1.5)
								
				gf=randint(1, 6) # choosing which function to call to generate a reply
				if gf==1:
					r=getphrase1(frase)
				elif gf==2:
					r=getphrase2()
				elif gf==3:
					r=getphrase3(frase)
				elif gf==4:
					r=getphrase4(update.message.text)
				elif gf==5:
					r=getphrase5()
				else:
					r=getphrase6()				
				if r!="null":
					update.message.reply_text(r)
			op=randint(1, 4)


def main():
	global update_id
	# Telegram Bot Authorization Token
	bot = telegram.Bot(TOKEN)

	# get the first pending update_id, this is so we can skip over it in case
	# we get an "Unauthorized" exception.
	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	i=0
	while True:
		try:

			resp(bot, i)
			i=i+1
		except NetworkError:
			sleep(1)
		except Unauthorized:
			#The user has removed or blocked the bot.
			update_id += 1

if __name__ == '__main__':
    main()
