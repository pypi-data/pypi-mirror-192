import feedparser
import pytz
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from lingua_franca.time import now_local
from ovos_ocp_rss_plugin import OCPRSSFeedExtractor
from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from pytz import timezone
from urllib.request import urlopen


class OCPNewsExtractor(OCPStreamExtractor):
    NPR_URL = "https://www.npr.org/rss/podcast.php"
    TSF_URL = "https://www.tsf.pt/stream"
    GPB_URL = "http://feeds.feedburner.com/gpbnews"
    GR1_URL = "https://www.raiplaysound.it"
    FT_URL = "https://www.ft.com"
    ABC_URL = "https://www.abc.net.au/news"

    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("news", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["news"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               any([uri.startswith(url) for url in [
                   self.TSF_URL, self.GPB_URL, self.NPR_URL,
                   self.GR1_URL, self.FT_URL, self.ABC_URL
               ]])

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("news//"):
            uri = uri[6:]
        if uri.startswith(self.NPR_URL):
            return self.npr()
        elif uri.startswith(self.TSF_URL):
            return self.tsf()
        elif uri.startswith(self.GPB_URL):
            return self.gpb()
        elif uri.startswith(self.GR1_URL):
            return self.gr1()
        elif uri.startswith(self.FT_URL):
            return self.ft()
        elif uri.startswith(self.ABC_URL):
            return self.abc()

    @classmethod
    def tsf(cls):
        """Custom inews fetcher for TSF news."""
        uri = None
        i = 0
        status = 404
        date = now_local(timezone('Portugal'))
        feed = (f'{cls.TSF_URL}/audio/{date.year}/{date.month:02d}/'
                'noticias/{day:02d}/not{hour:02d}.mp3')
        while status != 200 and i < 6:
            uri = feed.format(hour=date.hour, year=date.year,
                              month=date.month, day=date.day)
            status = requests.get(uri).status_code
            date -= timedelta(hours=1)
            i += 1
        if status != 200:
            return None
        return {"uri": uri,
                "title": "TSF Radio Noticias",
                "author": "TSF"}

    @classmethod
    def gpb(cls):
        """Custom news fetcher for GPB news."""
        feed = f'{cls.GPB_URL}/GeorgiaRSS?format=xml'
        data = feedparser.parse(feed)
        next_link = None
        for entry in data['entries']:
            # Find the first mp3 link with "GPB {time} Headlines" in title
            if 'GPB' in entry['title'] and ('Headlines' in entry['title']):
                next_link = entry['links'][0]['href']
                break
        html = requests.get(next_link)
        # Find the first mp3 link
        # Note that the latest mp3 may not be news,
        # but could be an interview, etc.
        mp3_find = re.search(r'href="(?P<mp3>.+\.mp3)"'.encode(), html.content)
        if mp3_find is None:
            return None
        uri = mp3_find.group('mp3').decode('utf-8')
        return {"uri": uri, "title": "GPB News", "author": "GPB"}

    @classmethod
    def npr(cls):
        url = f"{cls.NPR_URL}?id=500005"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "NPR News", "author": "NPR"}

    @classmethod
    def gr1(cls):
        json_path = f"{cls.GR1_URL}/programmi/gr1.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        resp = requests.get(json_path, headers=headers).json()
        path = resp['block']['cards'][0]['path_id']
        grjson_path = f"{cls.GR1_URL}{path}"
        resp = requests.get(grjson_path, headers=headers).json()
        uri = resp['downloadable_audio']['url']
        return {"uri": uri, "title": "Radio Giornale 1", "author": "Rai GR1"}

    @classmethod
    def ft(cls):
        page = urlopen(f"{cls.FT_URL}/newsbriefing")
        # Use bs4 to parse website and get mp3 link
        soup = BeautifulSoup(page, features='html.parser')
        result = soup.find('time')
        target_div = result.parent.find_next('div')
        target_url = 'http://www.ft.com' + target_div.a['href']
        mp3_page = urlopen(target_url)
        mp3_soup = BeautifulSoup(mp3_page, features='html.parser')
        uri = mp3_soup.find('source')['src']
        return {"uri": uri, "title": "FT news briefing", "author": "Financial Times"}

    @classmethod
    def abc(cls):
        """Custom news fetcher for ABC News Australia briefing"""
        # Format template with (hour, day, month)
        url_temp = ('https://abcmedia.akamaized.net/news/audio/news-briefings/'
                    'top-stories/{}{}/NAUs_{}00flash_{}{}_nola.mp3')
        now = pytz.utc.localize(datetime.utcnow())
        syd_tz = pytz.timezone('Australia/Sydney')
        syd_dt = now.astimezone(syd_tz)
        hour = syd_dt.strftime('%H')
        day = syd_dt.strftime('%d')
        month = syd_dt.strftime('%m')
        year = syd_dt.strftime('%Y')
        url = url_temp.format(year, month, hour, day, month)

        # If this hours news is unavailable try the hour before
        response = requests.get(url)
        if response.status_code != 200:
            hour = str(int(hour) - 1)
            url = url_temp.format(year, month, hour, day, month)

        return {"uri": url,
                "title": "ABC News Australia",
                "author": "Australian Broadcasting Corporation"}


if __name__ == "__main__":
    # dedicated parsers
    "http://www.rtp.pt//play/itunes/5442"
    print(OCPRSSFeedExtractor.get_rss_first_stream("rss//https://www.rtp.pt/rdpafrica/rss"))
    exit()
    print(OCPNewsExtractor.npr())
    print(OCPNewsExtractor.tsf())
    print(OCPNewsExtractor.gr1())
    print(OCPNewsExtractor.gpb())
    print(OCPNewsExtractor.ft())
    print(OCPNewsExtractor.abc())
    # RSS
    print(OCPRSSFeedExtractor.get_rss_first_stream("rss//https://www.cbc.ca/podcasting/includes/hourlynews.xml"))
    print(OCPRSSFeedExtractor.get_rss_first_stream("rss//https://podcasts.files.bbci.co.uk/p02nq0gn.rss"))
    print(OCPRSSFeedExtractor.get_rss_first_stream("rss//https://www.pbs.org/newshour/feeds/rss/podcasts/show"))
