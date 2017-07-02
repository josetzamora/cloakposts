import time
import datetime
import os
import json
import string
import http.client

oauthtoken = 'EAACEdEose0cBAIsVikedIpP6sGrWebK6vUgyUKG3oujLXRRZB8YPji5LXRq1tJqXHp8rz9keLhGXGqhJyB2fysCecEod2khE3fA8wZBtVow30rNvY2NYfanjxZAYaJkKRm6wZC3IBV8W0hV3phGapv8JGWSNnyX3yhZAt0k717WGhSLnZAHR7pZA3HkLSSp3ZABOdziOiOr5kwZDZD'
stolenbody = '__user=XXXXXXXXXX&__a=1&__dyn=aKhoFeyfyGmaomgDxyIGzG85oWq2WiWF298yeqrWpEqBxCbzES2N6xCaxu13CxKqEaUgDyUJi28rxuF8WVpFXDm4XzErDWxaFQ3uaVVojxCVEiHWCDxi5-uifz8lUlwkEG9ADBxi48hzEKbwBxq69LZ1aiJ129x-F8lF4yplzElCUmyE9Vt4gmx2ii49umqubAxxy8Cu4rGU&__af=iw&__req=z&__be=-1&__pc=PHASED%3ADEFAULT&__rev=2865362&fb_dtsg=AQEfYaOm45f0%3AAQEE5o0V81fL&ttstamp=26581691028997791095253102485865816969531114886564910276&ft[top_level_post_id]=10211989110467959&ft[tl_objid]=10211989110467959&ft[throwback_story_fbid]=10211989110467959&ft[fbfeed_location]=10&ft[thid]=XXXXXXXXXX%3A306061129499414%3A2%3A0%3A1491029999%3A7571120560628648925'
stolencookie = 'datr=7FqaWP59uYPDPmN9YwKTCvqc; sb=FZ6aWEuOnQJTxSVLd0MZ3Aus; pl=n; lu=gA-Od09ePUIxv_QyoTcL867Q; c_user=XXXXXXXXXX; xs=39%3AKHV9EhP-hE2sgg%3A2%3A1486528022%3A14122; fr=0A7muzCXYx671fEWk.AWUaPm9levAB09Fer3lK4uHmSjE.BYmlrs.2H.Fi3.0.0.BYuATz.AWUBYRF8; csm=2; p=-2; presence=EDvF3EtimeF1488456061EuserFA2XXXXXXXXXXA2EstateFDutF1488456061277CEchFDp_5fXXXXXXXXXXF7CC; act=123467812361%2F9'
postvisibility = '286958161406148'

interval = 60000
startdate = datetime.datetime(1998, 1, 1, 0, 0, 0)
startdatetime = int(time.mktime(startdate.timetuple()))
enddate = datetime.datetime(2017, 12, 31, 23, 59, 59)
enddatetime = int(time.mktime(enddate.timetuple()))

for cursor in range(startdatetime, enddatetime, interval):
    graphconnection = http.client.HTTPSConnection("graph.facebook.com")
    graphconnection.request("GET", '/me/posts?access_oauthtoken=' + oauthtoken + '&since=' + str(cursor) + '&until=' + str(cursor + interval))
    graphresponse = graphconnection.getresponse()
    print("Getting post ids")
    if graphresponse.status == 200:
        print("Succeeded, status: " + str(graphresponse.status))
    else:
        print("Failed to get post ids, status " + str(graphresponse.status) + ", reason: " + str(graphresponse.read()))
    
    d = json.load(graphresponse)

    for dd in d['data']:
        postid = dd['id'].split('_')[1]
        body = stolenbody
        header = {
                "Cookie": stolencookie,
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
                }
        privacyconnection = http.client.HTTPSConnection("www.facebook.com")
        privacyconnection.request("POST", "/privacy/selector/update/?privacy_fbid=" + postid +
                "&post_param=" + postvisibility +
                "&event_expansion_type=0&render_location=1&is_saved_on_select=true&should_return_tooltip=true&prefix_tooltip_with_app_privacy=false&replace_on_select=false&ent_id=" + postid + 
                "&tag_expansion_button=friends_of_tagged", body, header)
        privacyresponse = privacyconnection.getresponse()
        print("Setting visibility " + postvisibility + " to post " + postid) 
        if privacyresponse.status == 200:
            print("Succeeded, status: " + str(privacyresponse.status))
        else: 
            print("Failed, status: " + str(privacyresponse.status) + ", reason: " + str(privacyresponse.read()))