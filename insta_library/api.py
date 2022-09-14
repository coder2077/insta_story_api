import os
import time

from uuid import uuid4
from api.db import r

from instagrapi import Client
from instagrapi import exceptions

from .challenge import challenge_code_handler



class InstagramAPI():
	""" Helper for API """

	def __init__(self) -> None:
		self.client = Client()
		self.client.challenge_code_handler = challenge_code_handler


	def login(self, username: str, password: str, verification_code: str = ''):
		try:
			data = self.client.login(username=username, password=password, verification_code=verification_code)
			if data == True:
				json_response = {
					'error': False, 
					'message': 'Logged in successfully', 
					'response': self.client.get_settings(), 
				}
				return json_response
			else:
				json_response = {
					'error': True, 
					'message': 'Login failed', 
					'response': self.client.get_settings(), 
				}
				return json_response

		except exceptions.TwoFactorRequired:
			two_factor_info = self.client.last_json['two_factor_info']
			if two_factor_info['sms_two_factor_on'] == True:
				r.set(username, two_factor_info['two_factor_identifier'])
				json_response = {
					'error': True, 
					'message': '2 FA sms code sent your phone number, please pass it to /pass_sms_code endpoint', 
					'response': self.client.last_json
				}
				return json_response

			json_response = {
				'error': True, 
				'response': self.client.last_json
			}
			return json_response

		except Exception as e:
			json_response = {
				'error': True, 
				'response': e, 
			}
			return json_response


	def login_by_sessionid(self, sessionid: str):
		try:
			data = self.client.login_by_sessionid(sessionid=sessionid)
			if data == True:
				json_response = {
					'error': False, 
					'response': 'Logged in successfully', 
				}
				return json_response
			else:
				json_response = {
					'error': True, 
					'response': 'Login failed, please try with /login endpoint', 
				}
				return json_response

		except Exception as e:
			print(e)
			json_response = {
				'error': True, 
				'response': 'Login failed, please try with /login endpoint', 
			}
			return json_response


	def pass_sms_code(self, username: str, sms_code: str):
		two_factor_id = r.get(username).decode()
		data = {
			"verification_code": sms_code,
			"phone_id": self.client.phone_id,
			"two_factor_identifier": two_factor_id,
			"username": username,
			"trust_this_device": "0",
			"guid": self.client.uuid,
			"device_id": self.client.android_device_id,
			"waterfall_id": str(uuid4()),
			"verification_method": "1"
		}

		logged = self.client.private_request("accounts/two_factor_login/", data, login=True)
		self.client.authorization_data = self.client.parse_authorization(
			self.client.last_response.headers.get('ig-set-authorization')
		)

		self.client.dump_settings('lol.json')
		if logged:
			self.last_login = time.time()
			json_response = {
				'error': False, 
				'response': 'Logged in successfully', 
			}
			return json_response

		return False


	def set_proxy(self, dsn: str):
		try:
			data = self.client.set_proxy(dsn=dsn)
			json_response = {
				'error': False, 
				'response': data
			}
			return json_response
		except Exception as e:
			json_response = {
				'error': True, 
				'response': e
			}
			return json_response


	def get_sessionid(self):
		json_response = {
			'error': False, 
			'response': {'sessionid': self.client.sessionid}
		}
		return json_response


	def upload_photo_story(self, file_name, link_class):
		try:
			data =  self.client.photo_upload_to_story(file_name, links=[link_class])
			json_response = {
				'error': False, 
				'message': 'Uploaded successfully',  
				'response': data
			}
		except Exception as e:
			json_response = {
				'error': True, 
				'response': e
			}
		try:
			os.remove(file_name)
		except:
			pass

		return json_response


	def upload_video_story(self, file_name, link_class):
		try:
			data =  self.client.video_upload_to_story(file_name, links=[link_class])
			json_response = {
				'error': False, 
				'message': 'Uploaded successfully',  
				'response': data
			}
		except Exception as e:
			json_response = {
				'error': True, 
				'response': e
			}
		try:
			os.remove(file_name)
		except:
			pass

		return json_response

