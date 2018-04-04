import time
import datetime
import os
import json
import string
import http.client

oauth_token = 'EAACEdEose0cBAIsVikedIpP6sGrWebK6vUgyUKG3oujLXRRZB8YPji5LXRq1tJqXHp8rz9keLhGXGqhJyB2fysCecEod2khE3fA8wZBtVow30rNvY2NYfanjxZAYaJkKRm6wZC3IBV8W0hV3phGapv8JGWSNnyX3yhZAt0k717WGhSLnZAHR7pZA3HkLSSp3ZABOdziOiOr5kwZDZD'
stolen_body = '__user=XXXXXXXXXX&__a=1&__dyn=aKhoFeyfyGmaomgDxyIGzG85oWq2WiWF298yeqrWpEqBxCbzES2N6xCaxu13CxKqEaUgDyUJi28rxuF8WVpFXDm4XzErDWxaFQ3uaVVojxCVEiHWCDxi5-uifz8lUlwkEG9ADBxi48hzEKbwBxq69LZ1aiJ129x-F8lF4yplzElCUmyE9Vt4gmx2ii49umqubAxxy8Cu4rGU&__af=iw&__req=z&__be=-1&__pc=PHASED%3ADEFAULT&__rev=2865362&fb_dtsg=AQEfYaOm45f0%3AAQEE5o0V81fL&ttstamp=26581691028997791095253102485865816969531114886564910276&ft[top_level_post_id]=10211989110467959&ft[tl_objid]=10211989110467959&ft[throwback_story_fbid]=10211989110467959&ft[fbfeed_location]=10&ft[thid]=XXXXXXXXXX%3A306061129499414%3A2%3A0%3A1491029999%3A7571120560628648925'
stolen_cookie = 'datr=7FqaWP59uYPDPmN9YwKTCvqc; sb=FZ6aWEuOnQJTxSVLd0MZ3Aus; pl=n; lu=gA-Od09ePUIxv_QyoTcL867Q; c_user=XXXXXXXXXX; xs=39%3AKHV9EhP-hE2sgg%3A2%3A1486528022%3A14122; fr=0A7muzCXYx671fEWk.AWUaPm9levAB09Fer3lK4uHmSjE.BYmlrs.2H.Fi3.0.0.BYuATz.AWUBYRF8; csm=2; p=-2; presence=EDvF3EtimeF1488456061EuserFA2XXXXXXXXXXA2EstateFDutF1488456061277CEchFDp_5fXXXXXXXXXXF7CC; act=123467812361%2F9'
post_visibility = '286958161406148'

interval = 60000
start_date = datetime.datetime(1998, 1, 1, 0, 0, 0)
start_datetime = int(time.mktime(start_date.timetuple()))
end_date = datetime.datetime(2017, 12, 31, 23, 59, 59)
end_datetime = int(time.mktime(end_date.timetuple()))

for cursor in range(start_datetime, end_datetime, interval):
    graph_connection = http.client.HTTPSConnection("graph.facebook.com")
    graph_connection.request("GET", '/me/posts?access_oauthtoken=' + oauthtoken + '&since=' + str(cursor) + '&until=' + str(cursor + interval))
    graph_response = graph_connection.getresponse()
    print("Getting post ids")
    if graph_response.status == 200:
        print("Succeeded, status: " + str(graph_response.status))
    else:
        print("Failed to get post ids, status " + str(graph_response.status) + ", reason: " + str(graph_response.read()))
    
    d = json.load(graph_response)

    for dd in d['data']:
        post_id = dd['id'].split('_')[1]
        body = stolen_body
        header = {
                "Cookie": stolen_cookie,
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
                }
        privacy_connection = http.client.HTTPSConnection("www.facebook.com")
        privacy_connection.request("POST", "/privacy/selector/update/?privacy_fbid=" + post_id +
                "&post_param=" + post_visibility +
                "&event_expansion_type=0&render_location=1&is_saved_on_select=true&should_return_tooltip=true&prefix_tooltip_with_app_privacy=false&replace_on_select=false&ent_id=" + post_id + 
                "&tag_expansion_button=friends_of_tagged", body, header)
        privacy_response = privacy_connection.getresponse()
        print("Setting visibility " + post_visibility + " to post " + post_id) 
        if privacy_response.status == 200:
            print("Succeeded, status: " + str(privacy_response.status))
        else: 
            print("Failed, status: " + str(privacy_response.status) + ", reason: " + str(privacy_response.read()))
