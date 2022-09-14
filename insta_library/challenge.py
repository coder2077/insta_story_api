import time

from instagrapi.mixins.challenge import ChallengeChoice
from api.db import r


def challenge_code_handler(username, choice):
	if choice == ChallengeChoice.SMS:
		l_time = 0
		while True:
			print('Waiting for sms_code from redis ...\n')
			l_time += 2
			time.sleep(2)
			if r.get(username + '_challenge_code') != None:
				c_code = r.get(username + '_challenge_code').decode()
				if c_code.isdigit():
					print(f'Redis challenge sms_code received : {c_code}')
					r.delete(username + '_challenge_code')
					return c_code
			if l_time >= 150.0:
				break
		print('didnt received sms_code from redis . closed')
		return '123456'


	elif choice == ChallengeChoice.EMAIL:
		l_time = 0
		while True :  
			print('Waiting for email_code from redis ...\n')
			l_time += 2
			time.sleep(2)
			if r.get(username + '_challenge_code') != None:
				c_code = r.get(username + '_challenge_code').decode()
				if c_code.isdigit():
					print(f'Redis challenge email_code received : {c_code}')
					r.delete(username + '_challenge_code')
					return c_code
			if l_time >= 150.0 :
				break
		print('didnt received email_code from redis . closed')
		return '123456'
