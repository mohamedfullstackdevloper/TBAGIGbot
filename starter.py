import Login
import Grabber
import Story_id
import telebot
token = "6238963317:AAGWpqOkXHj_b1f9Qjm2tDdPPy3qntv7KzY"
bot = telebot.TeleBot(token)
loggin = Login
grabber = Grabber
stories = Story_id
inputs = False
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,'سجل دخول بحسابك الشخصي اولا\nارسل اليوزر الخاص بحساب الانستا')
@bot.message_handler(commands=['restart'])
def restart(message):
    ask(message)
@bot.message_handler(content_types=['text'])
def user_handler(message):
    global username 
    username = message.text
    bot.reply_to(message,'هسه باسورد')
    bot.register_next_step_handler(message , user_handler2)
def user_handler2(message):
    global password #'zxdzxd123':'zxdh.p1'
    password = message.text
    bot.reply_to(message,str(username) + ' : '+ str(password)+' جاري تسجيل الدخول')
    dict = loggin.Login_starter(password=password,username=username,bot=bot,message=message) # equal  {'logged':'True','cookies':v['cook'],'requests_session':r,'head':v['head']}
    if dict['logged']=='True':
        global cookies_dict
        global requ
        global head
        cookies_dict = dict['cookies']
        requ = dict['requests_session']
        head = dict['head']
        ask(message)
    else:
        exit()
def ask(message):
    bot.send_message(message.chat.id,'ارسل يوزر الصفحة لجلب متابعينها')
    bot.register_next_step_handler(message , page_handler)
def page_handler(message):
    global page
    page = message.text
    bot.send_message(message.chat.id,'ارسل عدد المتابعين لجلبهم')
    bot.register_next_step_handler(message , count_handler)
def count_handler(message):
    global limit
    limit = int(message.text)
    grab = grabber.Grabber_starter(cook=cookies_dict,req=requ,bot=bot,message=message,page=page,limit=limit) # equal {'grabbed':'True','ids':self.ides_list,'users':self.user_username,'requests_session':self.req,'cookies':self.cook}
    if grab['grabbed'] == 'True':
        global idss,users,req2,cook2
        idss= grab ['ids']
        users=grab['users']
        req2=grab['requests_session']
        cook2=grab['cookies']
        bot.send_message(message.chat.id,('تم الجلب'))
        bot.send_message(message.chat.id,('ارسل ثواني السليب بين حساب وحساب'))
        bot.register_next_step_handler(message , story_sleep1)
    else:
        bot.send_message(message.chat.id,('restart the bot'))
def story_sleep1(message):
        global sleep1
        sleep1 = int(message.text)
        bot.send_message(message.chat.id,('ارسل ثواني السليب بين ستوري وستوري'))
        bot.register_next_step_handler(message , story_sleep2)
def story_sleep2(message):
        global sleep2
        sleep2 = int(message.text)
        story_watcher(message)
def story_watcher(message):
        tray = stories.starter(cook=cook2,req=req2,head=head,users=users,ids=idss,sleep1=sleep1,sleep2=sleep2,bot=bot,message=message)
bot.infinity_polling()
