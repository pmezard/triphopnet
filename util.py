import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'BeautifulSoup-3.2.0'))
import urllib, urllib2, re, datetime, time, ConfigParser
import BeautifulSoup

class MissingConfigError(Exception):
    pass

class Ui:
    def __init__(self, debug=False):
        self.debugflag = debug

    def readconfig(self, path):
        cfg = ConfigParser.RawConfigParser()
        cfg.read([path])
        self.cfg = cfg

    def config(self, section, name, default=None, required=True):
        try:
            return self.cfg.get(section, name)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            if required:
                raise MissingConfigError('%s.%s' % (section, name))
            return default

    def info(self, s):
        sys.stdout.write(s)

    def debug(self, s):
        if self.debugflag:
            self.info(s)

    def error(self, s):
        sys.stderr.write(s)

class AbstractApi(object):
    def __init__(self, ui, name):
        self.ui = ui
        self.name = name

    def getupdates(self):
        raise NotImplementedError

class BaseApi(AbstractApi):
    def __init__(self, ui, name, delay):
        super(BaseApi, self).__init__(ui, name)
        self.lastrequest = 0
        self.delay = float(delay)

    def _request(self, url, data=None, headers=None):
        self.ui.info('fetching %s\n' % url)
        now = time.time()
        if now < (self.lastrequest + self.delay):
            delay = self.lastrequest + self.delay - now
            self.ui.debug('sleeping: %s\n' % delay)
            time.sleep(delay)
        headers = headers or {}
        headers['User-Agent'] = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0.1) '
                                 'Gecko/20100101 Firefox/5.0.1')
        if data:
            headers['Content-Type'] = 'application/x-www-form-urlencoded';
        rq = urllib2.Request(url, data=data, headers=headers)
        rsp = urllib2.urlopen(rq)
        s =  rsp.read()
        self.lastrequest = time.time()
        return s

    def _parseupdates(self, html):
        raise NotImplementedError

    def _getupdates(self, url, html=None):
        if html is None:
            html = self._request(url)
        return self._parseupdates(html)

def readseen(path):
    seen = set()
    if os.path.isfile(path):
        for line in file(path):
            seen.add(line.strip())
    return seen

def addseen(path, sids):
    fp = file(path, 'ab')
    for sid in sorted(sids):
        fp.write('%s\n' % sid.strip())
    fp.close()
