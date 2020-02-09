from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
import os 
import subprocess
import smtplib
import getpass
import sys


home = os.getenv('HOME')
pymail_cache = home + '/.cache/pymail/tmp'
if not os.path.isdir(pymail_cache): os.makedirs(pymail_cache)



mail_scratch = pymail_cache + '/.s'+ str(random.randint(1,10000000000))
mail_to_send =  pymail_cache + '/.m' + str(random.randint(1,10000000000))
cmd1 = 'cat > ' +  mail_scratch
cmd2  = 'echo \'<p>\' > '  + mail_to_send
cmd3 = 'sed "s,$,<br>,g" ' +  mail_scratch  + ' >> ' + mail_to_send

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

mail = MIMEMultipart()

mail["From"] = str(input('From: '))

try:
    server.login(mail['From'], getpass.getpass('Type your password: '))
except smtplib.SMTPAuthenticationError as err:
    print(err)
    print('In order to run pymail you must allow less secure apps on your gmail account ')
    print('got to:  https://myaccount.google.com/lesssecureapps')
    sys.exit()


mail["To"] = str(input('To: '))
mail['Subject'] = str(input('Subject: '))




try:
    subprocess.run(cmd1, shell=True)
except KeyboardInterrupt as err:
    del(err)
  
subprocess.run(cmd2, shell=True)
subprocess.run(cmd3, shell=True)


with open(mail_to_send, 'r') as f:
    lines = f.readlines()
    f.close()
print()

remove_trash = 'rm -rf ' + pymail_cache
subprocess.run(remove_trash, shell=True)

msg = ''

for line in lines:
    msg += line.rstrip()


mail.attach(MIMEText(str(msg), 'html'))



server.sendmail(mail['From'], mail['To'], mail.as_string())
