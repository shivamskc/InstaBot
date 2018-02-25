import requests
from pprint import pprint

# importing libraries for colored output
from termcolor import colored

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()

#response = requests.get('https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN').json()

APP_ACCESS_TOKEN=response['access_token']

# BASE_URL for getting self_info of instagram
BASE_URL='https://api.instagram.com/v1/'


# Function for extracting info

def owner_info():
    #Getting the user info
    r=requests.get('%susers/self/?access_token=%s' %(BASE_URL,APP_ACCESS_TOKEN)).json()

    #checking meta code
    if r['meta']['code']==200:
       # pprint(r)

        print(colored ("USERNAME IS: %s" %r['data']['username']), 'green')
        print(colored ("My No.of Followers are : %s" %r['data']['counts']['followed_by']), 'green')
    else:
        print("STATUS CODE RECIEVED OTHER THAN 200...!!! ")

owner_info()

# Extracting Owners Recent Posts
def owner_recent_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:

        pprint(r)
        print("User Recent Posts are : %s " %r['data'][0]['link'])
    else:
        print("STATUS CODE RECIEVED OTHER THAN 200 Again...!!! ")


owner_recent_post()







print colored("==================================================================",'yellow')
print colored("                                 InstaBot             ",'red')
print colored("                         Developed by Shivam Chaurasia  ",'red')
print colored("====================================================================",'yellow')
print ""
print (colored('*******************Hey! Welcome to InstaBot!*******************************','blue'))
print ('\n')