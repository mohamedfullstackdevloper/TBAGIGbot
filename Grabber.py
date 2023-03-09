class DGrabber:
    #self.bot.send_message(self.msg.chat.id,'')
    def __init__(self,cook,req,bot,message,page,limit):
        self.msg = message
        self.bot = bot
        self.req = req
        self.cook = cook
        self.page = page
        self.limit = limit
        global idurl
        global ides_list
        idurl = f"https://www.instagram.com/{self.page}/?__a=1&__d=dis" #get all info about the page
        ides_list = []
        self.user_username = []
    def grab(self):
        users_count = 12
        end_curso = []
        csrftoken = self.cook['csrftoken']
        sessionid = self.cook['sessionid']
        rur = self.cook['rur']
        ds_user_id = self.cook['ds_user_id']
        try:
            try:
                uid = self.req.get(idurl)
                if uid.json()["graphql"]["user"]['is_private'] == True:
                    self.bot.send_message(self.msg.chat.id,('this account is private \n restart the bot...'))
                    return {'grabbed':'False'}
                id = uid.json()["graphql"]["user"]["id"]#get page id
            except:
                self.bot.send_message(self.msg.chat.id,('page Username is error'))
                return {'grabbed':'False'}
            #getting first end_cursor
            end_ucrsor_url = f'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={id}&first=12&after='
            end_ucrsor_data = {'query_id':'17851374694183129', 'id':str(id), 'first':'12', 'after':''}
            end_curso_headers = {
            "accept": "'text/html,application/xhtml+xml,application/xml;q=0.9','image/avif,image/webp','image/apng','*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'",
            "accept-encoding": "'gzip', 'deflate', 'br'",
            "accept-language": "'en-GB','en-US;q=0.9','en;q=0.8','ar;q=0.7'",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }
            end_ucrsor_get = self.req.get(end_ucrsor_url,headers=end_curso_headers,data=end_ucrsor_data)
            try:
                first_end_cursor = end_ucrsor_get.json()["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                end_curso.append(first_end_cursor)
            except:
                self.bot.send_message(self.msg.chat.id,('Error getting more than 12 Followers `ECU`'))
                return {'grabbed':'False'}
            if self.limit < users_count:
                self.bot.send_message(self.msg.chat.id,('too little count'))
                return {'grabbed':'False'}
            while self.limit > users_count:
                followers_url = f'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={id}&first=12&after={str(end_curso[0])}'
                followers_data = {'query_id':'17851374694183129' , 'id':str(id) , 'first':str(users_count) , 'after':str(end_curso[0])}
                followers_headers = {
                'referer': f'https://www.instagram.com/{self.page}/followers/',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'viewport-width': '464',
                'x-asbd-id': '198387',
                'Cookie':f'csrftoken={csrftoken}; rur={rur}; ds_user_id={ds_user_id}; sessionid={sessionid} ',
                'x-csrftoken': csrftoken,
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR3U9SgkUz2nZg_Jx4m0AQA2dLs7aqjooR_FknrkUz-uknd6',
                'x-requested-with': 'XMLHttpRequest'
                }
                users_count+=12
                friendships = self.req.get(followers_url,headers=followers_headers,data=followers_data,allow_redirects=True)
                friendships_json = friendships.json()
                try:
                    next_end_cursor = friendships_json["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                    end_curso.clear()
                    end_curso.append(next_end_cursor)
                    all_users_info = friendships_json["data"]["user"]["edge_followed_by"]["edges"]
                    for user in all_users_info:
                        user_id = user['node']['id']
                        user_username = user['node']['username']
                        ides_list.append(user_id)
                        self.user_username.append(user_username)
                        self.bot.send_message(self.msg.chat.id,(str(user_username) + ' ; ' +str(user_id)))
                except:
                    self.bot.send_message(self.msg.chat.id,('Error getting more than 12 Followers `EXC`'))
                    return {'grabbed':'False'}
            return {'grabbed':'True'}
        except:
            self.bot.send_message(self.msg.chat.id,('Account Blocked'))
            return {'grabbed':'False'}
    def end(self):
        if self.grab()['grabbed'] == 'True':
            return {'grabbed':'True','ids':ides_list,'users':self.user_username,'requests_session':self.req,'cookies':self.cook}
        else:
            return {'grabbed':'False'}
def Grabber_starter(cook,req,bot,message,page,limit):
    bot.send_message(message.chat.id,('جاري الجلب'))
    x = DGrabber(cook=cook,req=req,bot=bot,message=message,page=page,limit=limit).end()
    if x['grabbed'] == 'True':
        return x
    else:
        return {'grabbed':'False'}