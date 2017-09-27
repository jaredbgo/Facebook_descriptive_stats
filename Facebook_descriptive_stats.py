import requests_oauthlib
import webbrowser
import json
import pickle
import pprint
import requests
import unittest
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas
from pandas import Series, DataFrame
reload(sys)
sys.setdefaultencoding('utf-8')

#Post dictionary that gets data for indivual posts
class Post():
    def __init__(self, post_dict={}):
        if 'message' in post_dict:
            self.message = post_dict['message'] #extracts the message of each post
        else:
            self.message = ""
        self.user = post_dict["from"]["name"] #who posted it?
        self.timeposted = post_dict["created_time"].split("T")[1][0:8] #when was it created?
        if "comments" in post_dict:
            self.commentcount = len(post_dict["comments"]["data"])
            commentlist = []
            for each in post_dict["comments"]["data"]:
                commentlist.append(each["message"])
            self.commentlist = commentlist
        else:
            self.commentcount = 0
            self.commentlist = []
        
        if "likes" in post_dict:
            self.likecount = len(post_dict["likes"]["data"])
        else:
            self.likecount = 0
        if "shares" in post_dict:
            self.sharecount = int(post_dict["shares"]["count"])
        else:
            self.sharecount = 0
        self.organicreach = post_dict["insights"]["data"][8]["values"][0]["value"]
        self.organicimpressions = post_dict["insights"]["data"][9]["values"][0]["value"]
        if post_dict["insights"]["data"][20]["values"][0]["value"] == 0:
            self.isvideo = False
        else:
            self.isvideo = True
        self.engagementscore = self.likecount + self.commentcount + self.sharecount
        if "#" in self.message:
            hashtag_count = 0
            for char in self.message:
                if char == "#":
                    hashtag_count += 1
            self.hashtag_count = hashtag_count
        else:
            self.hashtag_count = 0
        #        self.userclicks = post_dict["insights"]["data"][-15]["values"][0]["value"]
        if "link clicks" in post_dict["insights"]["data"][47]["values"][0]["value"].keys():
            self.userclicks = post_dict["insights"]["data"][47]["values"][0]["value"]["link clicks"]
        else:
            self.userclicks = 0
        self.reachfromlike = post_dict["insights"]["data"][14]["values"][0]["value"]
        self.paidreach = post_dict["insights"]["data"][6]["values"][0]["value"]
        self.totalreach = post_dict["insights"]["data"][4]["values"][0]["value"]
        if post_dict["insights"]["data"][62]["values"][0]["value"] == 0:
            self.targeted = False
        else:
            self.targeted = True










#***** ACCESSING DATA *****

access_token = "EAACEdEose0cBACeX3QDzEmZAHhSTCBAOM9ZBJrMAQk8fdmZBSA9UTQYwOOdZBTa5FaRBgMbIb2xjwllrbMEc7Hc6ZCHA32QtO9FJTbpPzpZCdr0852H1mRIts7z7JTtorNukmXxNKffvjjJoPI1DkOmGyCqpIcCLz6uMotgHjgLsWtq6SXRPr0CBgbjevw8IUZD"

facebook_user_ID = 617205031730242


FB_url = "https://graph.facebook.com/v2.3/{}/posts".format(facebook_user_ID)


url_params = {}
url_params["access_token"] = access_token
url_params["fields"] = "message,created_time,from,comments{like_count,from,message,created_time}, likes, shares, insights" # Parameter key-value so you can get post message, comments, likes, etc. as described in assignment instructions.
url_params["limit"] = 100


#
raw_FB_data = requests.get(FB_url, url_params)

json_FB_data = json.loads(raw_FB_data.text)

pprint.pprint(json_FB_data)
fobj = open("facebookdata.txt", "w")
pickle.dump(json_FB_data, fobj)
fobj.close()
fobj1 = open("facebookdata.txt", 'r') #retrieving saved data from the disk
json_FB_data = pickle.load(fobj1)
fobj1.close()

#print json_FB_data
FB_json_list = json_FB_data["data"]
facebook_instance_list = [] #this is creating a list of post instances
for each in FB_json_list: #turning each dictionary into a post instance
    facebook_instance_list.append(Post(each)) # creating list of instances
paidlist = []
unpaidlist = []

for each in facebook_instance_list:
    if each.paidreach == 0:
        unpaidlist.append(each)
    else:
        paidlist.append(each)

unpaiddict = {"message": [each.message for each in unpaidlist], "time":[each.timeposted for each in unpaidlist], "reach":[each.organicreach for each in unpaidlist],"engagement":[each.engagementscore for each in unpaidlist], "clicks":[each.userclicks for each in unpaidlist], "type": [each.isvideo for each in unpaidlist]}
paiddict = {"message": [each.message for each in paidlist], "time":[each.timeposted for each in paidlist], "reach":[each.organicreach for each in paidlist],"engagement":[each.engagementscore for each in paidlist], "clicks":[each.userclicks for each in paidlist], "type": [each.isvideo for each in paidlist]}
paidframe = DataFrame(paiddict)
unpaidframe = DataFrame(unpaiddict)

print "overall descriptives -- paid"
print paidframe.describe()
print "overall descriptives -- unpaid"
print unpaidframe.describe()

print "Photos vs videos"
print "Paid posts with videos"
print paidframe[paidframe.type == True].describe()
print "Paid posts without videos"
print paidframe[paidframe.type == False].describe()
print "Unpaid posts w vids"
print unpaidframe[unpaidframe.type == True].describe()
print "Unpaid posts without vids"
print unpaidframe[unpaidframe.type == False].describe()


print "Timing analysis"


paidlunch = []
paidnighttime = []
unpaidlunch = []
unpaidnighttime = []
for each in paidlist:
    if int(each.timeposted[0:2]) >= 10 and int(each.timeposted[0:2]) < 12:
        paidlunch.append([each.organicreach, each.engagementscore, each.userclicks, each.timeposted])
    elif int(each.timeposted[0:2]) >= 18 and int(each.timeposted[0:2]) < 21:
        paidnighttime.append([each.organicreach, each.engagementscore, each.userclicks, each.timeposted])
paidlunchdict = {"reach":[each[0] for each in paidlunch], "engagement": [each[1] for each in paidlunch], "clicks": [each[2] for each in paidlunch], "time": [each[3] for each in paidlunch]}
paidnightdict = {"reach":[each[0] for each in paidnighttime], "engagement": [each[1] for each in paidnighttime], "clicks": [each[2] for each in paidnighttime], "time": [each[3] for each in paidnighttime]}
paidlunchframe = DataFrame(paidlunchdict)
paidnightframe = DataFrame(paidnightdict)
for each in unpaidlist:
    if int(each.timeposted[0:2]) >= 10 and int(each.timeposted[0:2]) < 12:
        unpaidlunch.append([each.organicreach, each.engagementscore, each.userclicks, each.timeposted])
    elif int(each.timeposted[0:2]) >= 18 and int(each.timeposted[0:2]) < 21:
        unpaidnighttime.append([each.organicreach, each.engagementscore, each.userclicks, each.timeposted])
unpaidlunchdict = {"reach":[each[0] for each in unpaidlunch], "engagement": [each[1] for each in unpaidlunch], "clicks": [each[2] for each in unpaidlunch], "time": [each[3] for each in unpaidlunch]}
unpaidnightdict = {"reach":[each[0] for each in unpaidnighttime], "engagement": [each[1] for each in unpaidnighttime], "clicks": [each[2] for each in unpaidnighttime], "time": [each[3] for each in unpaidnighttime]}
unpaidlunchframe = DataFrame(unpaidlunchdict)
unpaidnightframe = DataFrame(unpaidnightdict)
print "paid around lunch"
print paidlunchframe.describe()
print "paid night time"
print paidnightframe.describe()
print "unpaid around lunch"
print unpaidlunchframe.describe()
print "unpaid night time"
print unpaidnightframe.describe()

#question marks
def question(astring):
    if "?" in astring:
        return True
    else:
        return False
def notaquestion(astring):
    if "?" in astring:
        return False
    else:
        return True
paidquestionseries = paidframe.message.apply(question)
paidnoquestion = paidframe.message.apply(notaquestion)
print "Paid posts with questions"
print paidframe.ix[paidquestionseries].describe()
print "Paid posts without questions"
print paidframe.ix[paidnoquestion].describe()
unpaidquestionseries = unpaidframe.message.apply(question)
unpaidnoquestion = unpaidframe.message.apply(notaquestion)
print "Unpaid posts with questions"
print unpaidframe.ix[unpaidquestionseries].describe()
print "unpaid posts without questions"
print unpaidframe.ix[unpaidnoquestion].describe()

#length

len1 = []
len2 = []
len3 = []
len4 = []
len5 = []
for each in paidlist:
    if len(each.message.split()) <= 20:
        len1.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <=40:
        len2.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <= 60:
        len3.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <= 80:
        len4.append([each.organicreach, each.engagementscore, each.userclicks])
    else:
        len5.append([each.organicreach, each.engagementscore, each.userclicks])
len_dict = {}
len_dict["0-20"] = len1 #0-20
len_dict["20-40"] = len2 #20-40
len_dict["40-60"] = len3
len_dict["60-80"] = len4
len_dict["80+"] = len5 #over 80

lengthsample = [len(len1), len(len2), len(len3), len(len4), len(len5)]
print "sample for paid"
print lengthsample


#length vs organic reach
len_reach = {}
for each in len_dict.keys():
    list = []
    for post in len_dict[each]:
        list.append(post[0])
    len_reach[each] = np.average(list)
len_reach_items = sorted(len_reach.items(), key = lambda x: int(x[0][0]))
xbar = []
ybar = []
for each in len_reach_items:
    xbar.append(each[0])
    ybar.append(each[1])

plt.bar(np.arange(len(xbar)), ybar, align = "center", width = .3, color = "r")
plt.xticks(np.arange(len(xbar)), xbar)
#plt.bar(range(len(len_reach)), len_reach.values(), align='center', width = .3,color = "r")
#plt.xticks(range(len(len_reach)), len_reach.keys())
plt.ylabel("Average Organic Reach (Unique Users)")
plt.xlabel("Length of Post (Words)")
plt.title("Average Organic Reach for Posts of Different Lengths")

plt.show()

labels = ["", "0-20", "20-40", "40-60", "60-80", "80+"]

len1reach = [each[0] for each in len1]
len2reach = [each[0] for each in len2]
len3reach = [each[0] for each in len3]
len4reach = [each[0] for each in len4]
len5reach = [each[0] for each in len5]




plt.boxplot([len1reach, len2reach, len3reach, len4reach, len5reach])
plt.ylabel("Organic Reach (Unique Users)")
plt.xlabel("Length of Post (Words)")
plt.xticks(np.arange(len(labels)), labels)
plt.title("Organic Reach for Posts of Different Lengths")
plt.show()


#length vs engagement

len_engagement = {}
for each in len_dict.keys():
    list = []
    for post in len_dict[each]:
        list.append(post[1])
    len_engagement[each] = np.average(list)

len_engagement_items = sorted(len_engagement.items(), key = lambda x: int(x[0][0]))
xbar = []
ybar = []
for each in len_engagement_items:
    xbar.append(each[0])
    ybar.append(each[1])

plt.bar(np.arange(len(xbar)), ybar, align = "center", width = .3, color = "r")
plt.xticks(np.arange(len(xbar)), xbar)

#plt.bar(range(len(len_engagement)), len_engagement.values(), align='center', width = .3,color = "r")
#plt.xticks(range(len(len_engagement)), len_engagement.keys())
plt.ylabel("Average # of Post Likes, Comments, and Shares")
plt.xlabel("Length of Post (Words)")
plt.title("Average User Engagement for Posts of Different Lengths")

plt.show()



len1eng = [each[1] for each in len1]
len2eng = [each[1] for each in len2]
len3eng = [each[1] for each in len3]
len4eng = [each[1] for each in len4]
len5eng = [each[1] for each in len5]




plt.boxplot([len1eng, len2eng, len3eng, len4eng, len5eng])
plt.ylabel("# of Post Likes, Comments, and Shares")
plt.xlabel("Length of Post (Words)")
plt.xticks(np.arange(len(labels)), labels)
plt.title("User Engagement for Posts of Different Lengths")
plt.show()

"***Length Data for Paid based on this many posts (ordered by length): {}, and total {}".format(lengthsample, np.sum(lengthsample))
print "len reach data is"
print len_reach
print "len engagement data is"
print len_engagement

#UNPAID

len1 = []
len2 = []
len3 = []
len4 = []
len5 = []
for each in unpaidlist:
    if len(each.message.split()) <= 20:
        len1.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <=40:
        len2.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <= 60:
        len3.append([each.organicreach, each.engagementscore, each.userclicks])
    elif len(each.message.split()) <= 80:
        len4.append([each.organicreach, each.engagementscore, each.userclicks])
    else:
        len5.append([each.organicreach, each.engagementscore, each.userclicks])
len_dict = {}
len_dict["0-20"] = len1 #0-20
len_dict["20-40"] = len2 #20-40
len_dict["40-60"] = len3
len_dict["60-80"] = len4
len_dict["80+"] = len5 #over 80

lengthsample = [len(len1), len(len2), len(len3), len(len4), len(len5)]
print "sample for unpaid"
print lengthsample


#length vs organic reach
len_reach = {}
for each in len_dict.keys():
    list = []
    for post in len_dict[each]:
        list.append(post[0])
    len_reach[each] = np.average(list)
len_reach_items = sorted(len_reach.items(), key = lambda x: int(x[0][0]))
xbar = []
ybar = []
for each in len_reach_items:
    xbar.append(each[0])
    ybar.append(each[1])

plt.bar(np.arange(len(xbar)), ybar, align = "center", width = .3, color = "r")
plt.xticks(np.arange(len(xbar)), xbar)
#plt.bar(range(len(len_reach)), len_reach.values(), align='center', width = .3,color = "r")
#plt.xticks(range(len(len_reach)), len_reach.keys())
plt.ylabel("Average Organic Reach (Unique Users)")
plt.xlabel("Length of Post (Words)")
plt.title("Average Organic Reach for Posts of Different Lengths")

plt.show()

labels = ["", "0-20", "20-40", "40-60", "60-80", "80+"]

len1reach = [each[0] for each in len1]
len2reach = [each[0] for each in len2]
len3reach = [each[0] for each in len3]
len4reach = [each[0] for each in len4]
len5reach = [each[0] for each in len5]




plt.boxplot([len1reach, len2reach, len3reach, len4reach, len5reach])
plt.ylabel("Organic Reach (Unique Users)")
plt.xlabel("Length of Post (Words)")
plt.xticks(np.arange(len(labels)), labels)
plt.title("Organic Reach for Posts of Different Lengths")
plt.show()


#length vs engagement

len_engagement = {}
for each in len_dict.keys():
    list = []
    for post in len_dict[each]:
        list.append(post[1])
    len_engagement[each] = np.average(list)

len_engagement_items = sorted(len_engagement.items(), key = lambda x: int(x[0][0]))
xbar = []
ybar = []
for each in len_engagement_items:
    xbar.append(each[0])
    ybar.append(each[1])

plt.bar(np.arange(len(xbar)), ybar, align = "center", width = .3, color = "r")
plt.xticks(np.arange(len(xbar)), xbar)

#plt.bar(range(len(len_engagement)), len_engagement.values(), align='center', width = .3,color = "r")
#plt.xticks(range(len(len_engagement)), len_engagement.keys())
plt.ylabel("Average # of Post Likes, Comments, and Shares")
plt.xlabel("Length of Post (Words)")
plt.title("Average User Engagement for Posts of Different Lengths")

plt.show()



len1eng = [each[1] for each in len1]
len2eng = [each[1] for each in len2]
len3eng = [each[1] for each in len3]
len4eng = [each[1] for each in len4]
len5eng = [each[1] for each in len5]




plt.boxplot([len1eng, len2eng, len3eng, len4eng, len5eng])
plt.ylabel("# of Post Likes, Comments, and Shares")
plt.xlabel("Length of Post (Words)")
plt.xticks(np.arange(len(labels)), labels)
plt.title("User Engagement for Posts of Different Lengths")
plt.show()

"***Length Data for Unpaid based on this many posts (ordered by length): {}, and total {}".format(lengthsample, np.sum(lengthsample))
print "len reach data is"
print len_reach
print "len engagement data is"
print len_engagement
for each in facebook_instance_list:
    print each.targeted


