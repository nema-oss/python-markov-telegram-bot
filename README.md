A simple, ready-to-go Telegram bot written in basic python3.
The bot learns from messages of users it chats with and replies to them; the messages it sends are generated through functions that use Markov chains, old messages the bot has received (they can be either completely random or context-related) or a composition of messages that are linked in a semi-random manner from one or more files.
The functions are completely customizable with little impact on the rest of the code.
This bot requires to be in a folder with a text file named MAINTEXTFILE and one named SECONDARYTEXTFILE otherwise it will create such files. If you don't need a secondary text file, you can remove the function getphrase5() and getphrase6()
