import email, smtplib, time, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tweepy'))
import tweepy
import util

class Email:
    def __init__(self, ui):
        self.ui = ui
        self.email = ui.config('email', 'address')
        self.fromaddr = ui.config('email', 'from')
        self.host = ui.config('email', 'host')

    def notify(self, updates):
        data = '\n'.join(('%s (%s)' % (label, url))
                         for (sid, label, url) in updates)
        data = (data + '\n').encode('utf-8')
        self._sendmail([self.email], 'Web updates', data)

    def _sendmail(self, tos, title, data):
        msg = email.MIMEMultipart.MIMEMultipart()
        msg['From'] = self.fromaddr
        for to in tos:
            msg['To'] = to
        msg['Date'] = email.Utils.formatdate(localtime=True)
        msg['Subject'] = title
        msg.attach(email.MIMEText.MIMEText(data))

        self.ui.info('Sending notification... ')
        server = smtplib.SMTP(self.host)
        server.sendmail(self.fromaddr, tos, msg.as_string())
        server.close()
        self.ui.info('done\n')

class Twitter:
    def __init__(self, ui):
        self.ui = ui
        self.consumerkey = ui.config('twitter', 'consumerkey')
        self.consumersecret = ui.config('twitter', 'consumersecret')
        self.accesstoken = ui.config('twitter', 'accesstoken')
        self.accesssecret = ui.config('twitter', 'accesssecret')

    def notify(self, updates):
        self.ui.info('Tweeting... ')
        auth = tweepy.OAuthHandler(self.consumerkey, self.consumersecret)
        auth.set_access_token(self.accesstoken, self.accesssecret)
        api = tweepy.API(auth)
        for i, (sid, label, url) in enumerate(reversed(updates)):
            if i != 0:
                time.sleep(1.0)
            status = '%s %s' % (label, url)
            status = status.encode('utf-8')
            api.update_status(status=status)
        self.ui.info('done\n')
