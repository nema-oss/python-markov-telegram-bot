import logging
from random import randint
import requests
import re
from time import sleep
from io import open
from array import array
import markovify
from telegram import __version__ as TG_VER

MAINTEXTFILE = "scibile.txt"#name of the main text file
SECONDARYTEXTFILE = "mazza.txt" #name of the secondary text file; code will never fill this file, you have to do it manually
TOKEN = ''

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def meme(frase):
    res="0"
    if frase.endswith("cia"): 
        res="ciai la faccia da pirla"
    elif frase.endswith("sei") or frase.endswith("6"):
        res="6 scemo"
    elif frase.endswith("ma"):
        res="ma tu sorella"
    elif frase.endswith("mo"):
        res = "mortacci tua"
    return res


def getphrase1(frase):
	

	with open(MAINTEXTFILE) as f:
		text = f.read()

	text_model = markovify.NewlineText(text)
	s = text_model.make_sentence()
	while s == "null":
		s=text_model.make_sentence(tries=100)
	return s

def getphrase2():
	f = open(MAINTEXTFILE, "r")
	lines=f.readlines()
	hi =randint(0, len(lines)-1)
	f.close()
	return (lines[hi])

def getphrase3(frase):
	with open(MAINTEXTFILE) as f:
		text = f.read()

	text_model = markovify.Text(text)
	s = text_model.make_sentence()
	while s == "null":
		s=text_model.make_sentence(tries=100)
	return s
	
def getphrase4(mess):
	datamess = mess.split()
	j=len(datamess)
	index = randint(0, j-1)
	parola = datamess[index]
	f = open(MAINTEXTFILE, "r")
	lines=f.readlines()
	for x in range (0, 100):
		hi =randint(0, len(lines)-1)
		if parola in lines[hi]:
			break
	f.close()
	return (lines[hi])

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
	


async def resp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    op=randint(1, 8)	
    
    if update.message.text:	
        frase=update.message.text	
        if "fantuzzo" in frase or "Fantuzzo" in frase:
            op=1
        f = open(MAINTEXTFILE, "a")
        f.write("\r")
        f.write(frase)
        f.close()
        if op == 1:
            sleep(1.5)
								
            gf=randint(1, 6)
            is_meme = meme(frase)
            if is_meme!="0":
                r = is_meme
            elif gf==1:
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
            if r!="null" and r!="None":
                #await update.message.reply_text(r)
                await context.bot.send_message(update.effective_chat.id, r)
            op=randint(1, 8)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resp))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()