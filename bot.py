import telebot
import redis
r = redis.Redis('localhost')
from tempmail import TempMail
token = '232204590:AAHnmzmxw51R_Rz6uSA2EbXHr2rsqjzo2wY'
bot = telebot.TeleBot(token)
user = bot.get_me().username
@bot.message_handler(commands=['start'])
def start(m):
  # start text
  text = 'Hi.\nWelcome to {}.\nCommands: \n/newmail: For making a new Email.\n/mails: For reading new emails.creator:@sina08753'.format(user)
  bot.send_message(m.chat.id, text)
@bot.message_handler(commands=['newmail'])
def newmail(m):
        #initialize Temp-Male and making a new Email.
        tm = TempMail()
        email = tm.get_email_address()
        r.set('email:{}:mail'.format(str(m.from_user.id)), email)
        bot.send_message(m.chat.id, 'Your new Email: '+email)
@bot.message_handler(commands=['mails'])
def mails(m):
    try :
        #initialize Temp-Mail and read recieved Mails.
        mail = r.get('email:{}:mail'.format(str(m.from_user.id)))
        if not mail:
                bot.send_message(m.from_user.id, 'Make an email first.\nUse /newmail')
                return
        parts = mail.split('@')
        tm = TempMail(login=parts[0], domain='@'+parts[1])
        mails = tm.get_mailbox()
        if not mails :
                bot.send_message(m.from_user.id, 'There is no email...')
        else:
            if 'error' in mails :
                bot.send_message(m.from_user.id, 'There is no email...')
            else:
                print mails
                for i in mails:
                        bot.send_message(m.from_user.id, 'Mail from: '+i['mail_from']+'\n\nSubject: '+i['mail_subject']+'\n\nText: ' +i['mail_text'])
    except:
        bot.send_message(m.from_user.id, 'There is no email...')

bot.polling()
