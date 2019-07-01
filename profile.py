# access_token Facebook library 
# author: nguyentri729
import requests
import hashlib 
import urllib
class Profile:
	def __init__(self, user = '', pwd = ''):
	 	self.user = user
	 	self.pwd = pwd
	def sign_creator(self):
		global data
		data = {
			"api_key" : "3e7c78e35a76a9299309885393b02d97",
			"email" : self.user,
			"format" : "JSON",
			"generate_machine_id" : "1",
			"generate_session_cookies" : '1',
			"locale" : "vi_vn",
			"method" : "auth.login",
			"password" : self.pwd,
			"return_ssl_resources" : "0",
			"v": "1.0"
		}
		sig = ''
		for c in data:
			sig += c + '=' + data[c]

		sig = sig + 'c1e620fa708a1d5696fb991c1bde5662'
		data['sig'] =  hashlib.md5(sig.encode()).hexdigest()
	
		return data

	def get_access_token(self):
		data = self.sign_creator()
		#rest_api = 'https://api.facebook.com/restserver.php?'+'&'.join(["{}={}".format(k, v) for k, v in data.items()])
		resp = requests.get('https://api.facebook.com/restserver.php', params = data)
		if resp.status_code == 200:

			responsive = resp.json()
			cookie = ''
			for x in responsive['session_cookies']:
				 cookie += x['name'] + '=' + x['value'] + '; '
			access_token_resp = responsive['access_token'] 	
			global info
			info = {
				'access_token' : access_token_resp,
				'cookie'	: cookie,
				'uid'		: responsive['uid']
			}
		else:
			return false
	def get_info(self, access_token):
		resp = requests.get('https://graph.facebook.com/me?access_token='+access_token+'')
		if resp.status_code == 200:
			responsive = resp.json()
			global info
			info = {
				'access_token' : access_token,
				'cookie'	: '',
				'uid'		: responsive['id']
			}
			return info
		else:
			return false
	
	def profile_shielded(self, access_token='', status = 'true'):
		if access_token == '':
			self.get_access_token()
		else:
			self.get_info(access_token)	
			
		token = info['access_token']	
		uid  = info['uid']	
		headers = {
			'Authorization' : 'OAuth ' + token
		}
		data = 'variables={"0":{"is_shielded":'+status+',"session_id":"9b78191c-84fd-4ab6-b0aa-19b39f04a6bc","actor_id":"'+uid+'","client_mutation_id":"b0316dd6-3fd6-4beb-aed4-bb29c5dc64b0"}}&method=post&doc_id=1477043292367183&query_name=IsShieldedSetMutation&strip_defaults=true&strip_nulls=true&locale=en_US&client_country_code=US&fb_api_req_friendly_name=IsShieldedSetMutation&fb_api_caller_class=IsShieldedSetMutation'
		resp = requests.post('https://graph.facebook.com/graphql', data=data, headers=headers)
		return('Profile Picture Guard : ON') if status == 'true' else 'Profile Picture Guard : OFF'

# token = Profile()
# print(token.profile_shielded(status = 'false'))
import socket  
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)   
choice = ''
print('''
						PROFILE MANAGER  
						 ('''+IPAddr+''') 
					    

1: Get access_token   						3: Get cookie
2: Profile Picture Guard 					4: Rip access

						5: Exit

		'''.center(25))
while choice != '5':

	choice = input('*** Select choice (1-5): ')
	if choice == '1':
		u = input('>>> username: ')
		p = input('>>> password: ')
		print('loading...please wait...')
		try:
			token = Profile(u, p)
			result = token.get_access_token()
			print('\n')
			print(info['access_token'])
			
			print('\a')
			print('\n')
		except:
		  print("Can't get access_token, an exception occurred ! User pwd wrong ! ") 
	if choice == '3':
		u = input('>>> username: ')
		p = input('>>> password: ')
		print('please wait...Logining')
		try:
			token = Profile(u, p)
			result = token.get_access_token()
			print('\n')
			print(info['cookie'])
			
			print('\a')
			print('\n')
		except:
		  print("Can't get cookie, an exception occurred ! User pwd wrong ! ") 
	if choice == '2':
		#u = input('>>> username (optional): ')
		#p = input('>>> password (optional): ')
		t = input('>>> access_token : ')
		p = input('>>> status (true, false): ')
		print('please wait...')
		try:
			token = Profile()
			
			guard = token.profile_shielded(t, p)

			print('\n')

			print(guard)

			print('\a')
			print('\n')
		except:
		  print("Access token wrong ! ") 
	if choice == '4':
		

		t = input('>>> access_token : ')
		
		print('please wait...')
		try:
			resp = requests.get('https://api.facebook.com/restserver.php?method=auth.expireSession&access_token='+t+'')

			print('\n')

			print('Deleted :)) ')

			print('\a')
			print('\n')
		except:
		 	print("Access token wrong ! ") 
