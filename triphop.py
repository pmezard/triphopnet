import sys, os, re
sys.path.append(os.path.join(os.path.dirname(__file__), 'BeautifulSoup-3.2.0'))
import BeautifulSoup
import util

class TripHopNet(util.BaseApi):
    def __init__(self, ui, delay=10):
        super(TripHopNet, self).__init__(ui, 'trip-hop.net', delay)

    def _parseupdates(self, html):
        releases = []
        doc = BeautifulSoup.BeautifulSoup(html, convertEntities=True)
        reviews = doc.findAll('div', {'class': 'chronique_home'})
        for e in reviews:
            headers = e.find('h4').findAll('a')
            group = headers[0].text
            album = headers[1].text
            url = headers[1]['href'].encode('utf-8')
            # http://www.trip-hop.net/album-2487-submotion-orchestra-finest
            # -hour-exceptional-records.html
            sid = url.rsplit('/', 1)[-1].lower().replace('\n', ' ')
            if sid.endswith('.html'):
                sid = sid[:-5]
            sid = '%s:%s' % (self.name, sid)
            label = '%s - %s' % (group, album)
            releases.append((sid, label, url))
        return releases

    def getupdates(self, html=None):
        return self._getupdates('http://www.trip-hop.net/derniersajouts-0.html',
                html)
