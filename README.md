# A simple, ready-to-go *Telegram* bot in Python.

![](logo.svg)

The bot learns from messages of users it chats with and replies to them.

 The messages it sends are generated through functions that use *Markov chains*, old messages the bot has received (they can be either completely random or context-related) or a composition of messages that are linked in a semi-random manner from one or more files.

The functions are completely customizable with little impact on the rest of the code.

This bot requires to be in a directory with a text file named **MAINTEXTFILE** and one named **SECONDARYTEXTFILE**, otherwise it will create such files.

If you don't need a secondary text file, you can remove the functions *getphrase5()* and *getphrase6()*. 

The secondary text file is accessed exclusively in read mode and therefore will remain empty until you manually fill it with arbitrary text. The latter will be combined with the text file containing all past messages. 
