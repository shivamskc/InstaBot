import requests
from pprint import pprint
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# importing libraries for colored output
from termcolor import colored


print (colored('*******************Hey! Welcome to InstaBot!*******************************','blue'))
print ('\n')

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()

#response = requests.get('https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN').json()
print(response)
APP_ACCESS_TOKEN=response['access_token']

# BASE_URL for getting self_info of instagram
BASE_URL='https://api.instagram.com/v1/'


# Function for extracting info


#   checking if user exits or not and printing its info
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

#owner_info()

# Extracting Owners Recent Posts
def owner_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:

       #pprint(r)
        url= r['data'][1]['images']['standard_resolution']['url']
        name=r['data'][1]['id']+'.jpg'
        urllib.urlretrieve(url,name)
        print("Great...Your Image has been downloaded")
    else:
        print("STATUS CODE RECIEVED OTHER THAN 200 Again...!!! ")


#owner_post()


def get_user_id(uname):
    r=requests.get("%susers/search?q=%s&access_token=%s" %(BASE_URL,uname,APP_ACCESS_TOKEN)).json()
    pprint (r)
    return r['data'][0]['id']




def user_info(uname):
    # Getting the user info
    user_id=get_user_id(uname)
    r = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()

    # checking meta code
    if r['meta']['code'] == 200:
        # pprint(r)

        print(colored("USERNAME IS: %s" % r['data']['username']), 'green')
        print(colored("My No.of Followers are : %s" % r['data']['counts']['followed_by']), 'green')
    else:
        print("STATUS CODE RECIEVED OTHER THAN 200...!!! ")




def user_post(username):
    user_id=get_user_id(username)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:
        # pprint(r)
        url = r['data'][1]['images']['standard_resolution']['url']
        name = r['data'][1]['id'] + '.jpg'
        urllib.urlretrieve(url, name)
        urllib.urlretrieve(url, name)
        print("Great...Your Image has been downloaded")


def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
       return r['data'][1]['id']



def like_post(uname):
    media_id=get_media_id(uname)
    payload={"access_token": APP_ACCESS_TOKEN}
    url=(BASE_URL + 'media/%s/likes')%(media_id)
    r=requests.post(url,payload).json()
    if r['meta']['code'] == 200:
        print("Like Successful")
    else:
        print("Like Unsuccessful")



def comment_post(uname):
    media_id=get_media_id(uname)
    comment=raw_input("What's your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text":comment}
    url = BASE_URL + 'media/%s/comments' % (media_id)
    r = requests.post(url, payload).json()
    if r['meta']['code'] == 200:
        print("Comment Successful")
    else:
        print("Comment Unsuccessful")


def del_comment(uname):
    media_id=get_media_id(uname)
    r=requests.get("%smedia/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            for i in range(0,len(r['data'])):
                cmnt_id=r['data'][i]['id']
                cmnt_text=r['data'][i]['text']
                blob = TextBlob(cmnt_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (cmnt_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, cmnt_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!'
                    else:
                        print 'Could not delete the comment'


        else:
            print"Sorry...NO Comments Found"
    else:
        print"OOPS...Error Occured"



def start_bot():
    show_menu=True
    while show_menu:
        query=input("What do you want to do ?\n 1. Get Owner Info. \n 2. Get Owner post. \n 3. Get User Info. \n 4. Get User Post. \n 5. Like A Post. \n 6. Comment On a Post. \n 7. Delete Negetive Comment. \n 0. EXIT ")
        if query==1:
            owner_info()
        elif query==2:
            owner_post()
        elif query==3:
            username=raw_input("Please enter the username of that user: ")
            user_info(username)
        elif query==4:
            username = raw_input("Please enter the username of that user: ")
            user_post(username)
        elif query==5:
            username = raw_input("Please enter the username of that user: ")
            like_post(username)
        elif query==6:
            username = raw_input("Please enter the username of that user: ")
            comment_post(username)
        elif query==7:
            username = raw_input("Please enter the username of that user: ")
            del_comment(username)

        elif query==0:
            show_menu=False
        else:
            print("INVALID INPUT")


start_bot()




print colored("==================================================================",'yellow')
print colored("                                 InstaBot             ",'red')
print colored("                         Developed by Shivam Chaurasia  ",'red')
print colored("====================================================================",'yellow')
print ""