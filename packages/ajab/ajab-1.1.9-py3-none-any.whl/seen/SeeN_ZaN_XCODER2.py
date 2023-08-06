from datetime import datetime
from time import sleep
import rainbowtext, pyfiglet
from re import findall
from pyrubi import *


auth = ["camcjnmqzualrliinjvlivifguwmvkpx","jfozpdtdslwpnkjfalrowxlfpyjeyoiw","nqfxrlifumcyuxaomcefppqenxmdlyha","ewnxlwzdpnqnpzftfdykwnprnatfdrrz","fxneiswtuhggndyndywabntvswkpncls","eawuyhlhqratnpqogoeozdzdlwbdgxqd"]

post_link = ["https://rubika.ir/upload_film_27/ECJDDEHFGBCEFFA","https://rubika.ir/upload_film_27/EDDEGGIGFCCGFFA"]

time_sleep = 0.5


class color:
	red = '\033[91m'
	green = '\033[92m'
	blue = '\033[94m'
	yellow = '\033[93m'
	magenta = '\033[95m'
	cyan = '\033[96m'
	white = '\033[97m'
	bold = '\033[1m'
	underline = '\033[4m'
	black='\033[30m'

text = '       X CODER'
txt = rainbowtext.text(pyfiglet.figlet_format(text))
print(txt)
print(f"\n {color.blue}      [+] - O W N E R  ID : @X_CODER\n       [+] - Channell ID   : @X_CODER_2721\n")
print(f"{color.yellow}______________________________________________________\n")

su , dum , td_link , List_Gap , td_acc = 0 , 0 , [] , [] , []

while True:
	try:
		xco_get = Bot(auth[0])
		for Linkdooni_Guid in xco_get.search_chats('لینکدونی'):
			try:
				last_id = xco_get.get_chat_info(Linkdooni_Guid['object_guid'])['chat']['last_message_id']
				for Channel_Message in xco_get.get_chat_messages(Linkdooni_Guid['object_guid'],last_id):
					for Group_Link in findall(r"rubika.ir/joing/\w{32}", Channel_Message['text']):
						List_Gap.append(Group_Link)
			except:continue
	except:print('eror get link')
	print(f'Found Link : {len(List_Gap)}\n')

	try:
		for links in List_Gap:
			try:
				sleep(time_sleep)
				td_acc.append('.')
				if len(td_acc) > len(auth):
					td_acc.clear()
				xco = Bot(auth[len(td_acc) - 1])
				time = datetime.now().strftime("%H:%M:%S")
				join_gap = xco.join_group(links)
				gap_guid = join_gap['group']['group_guid']
				gap_name = join_gap['group']['group_title']
				gap_member = join_gap['group']['count_members']
				gap_access = join_gap['chat_update']['chat']['access']
				List_Gap.remove(links)
				if 'SendMessages' in gap_access:
					td_link.append('.')
					if len(td_link) > len(post_link):
						td_link.clear()
					post = post_link[len(td_link) - 1]
					try:
						psg = xco.get_link_info(post)
						x = psg["object_guid"]
						c = psg["message_id"]
					except:print('Post Not Found'),exit()
					for_bn = xco.forward_message(x,[c],gap_guid)
					if for_bn['status'] == 'OK':
						su += 1
						xco.leave_group(gap_guid)
						seen = for_bn['message_updates'][0]['message']['count_seen']
						print(f"""{color.red}  X CODER {color.white}| {color.blue}BoT {color.red}> > > {color.green}SenDeD TO GaP

{color.magenta} [ {color.blue}NAME GaP{color.magenta}   ]   {color.red}: {color.magenta}[x{color.cyan}{gap_name}{color.magenta}x]
{color.magenta} [ {color.blue}TIME FOR{color.magenta}   ]   {color.red}: {color.magenta}[{color.cyan}{time}{color.magenta}]
{color.magenta} [ {color.blue}SEEN BNR{color.magenta}   ]  {color.red} : {color.magenta}[{color.cyan}{seen}{color.magenta}]
{color.magenta} [ {color.blue}NUMBER FOR{color.magenta} ]  {color.red} : {color.magenta}[{color.cyan}{su}{color.magenta}]
{color.magenta} [ {color.blue}MEMBER GaP{color.magenta} ]  {color.red} : {color.magenta}[{color.cyan}{gap_member}{color.magenta}]
{color.magenta} [ {color.blue}LINK GaP{color.magenta}   ]   {color.red}:
{color.magenta}[{color.cyan}{links}{color.magenta}]

{color.yellow}______________________________________________________
""")
					else:
						xco.leave_group(gap_guid)
						print('Your ACC Rep For')
						exit()
				else:
					dum +=1
					xco.leave_group(gap_guid)
					print(f"""{color.red}  X CODER {color.white}| {color.blue}BoT {color.red}> > > {color.red}DonT SeND GaP LoCKED !!

{color.magenta}[ {color.blue}NAME GaP LOCK{color.magenta} ] {color.red}: {color.magenta}[x{color.cyan}{gap_name}{color.magenta}x]
{color.magenta}[ {color.blue}NUMBER LOCK{color.magenta}   ] {color.red}: {color.magenta}[  {color.cyan}{dum}{color.magenta}  ]

{color.yellow}______________________________________________________
""")
			except:continue
	except:pass