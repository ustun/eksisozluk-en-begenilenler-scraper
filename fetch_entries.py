import requests
import json
from pyquery import PyQuery as pq

def fetch_raw_entries(begenilen_url):
    d = pq(requests.get(begenilen_url).text)
    entries = []
    for entry_dom in d.find('ol.topic-list li'):
        try:
            entry = {"href": "https://eksisozluk.com" + entry_dom.find('a').attrib['href'],
                     "konu": entry_dom.find('a').find('span').text,
                     "author": entry_dom.find('a').find('div').text}
            entries.append(entry)
        except Exception as exc:
            print exc

    return entries

def extract_entry_from_url(entry_url):
    try:
        return pq(requests.get(entry_url).text).find('div.content').html()
    except:
        # sometimes fails due to ads, retry
        return pq(requests.get(entry_url).text).find('div.content').html()

def enhance_raw_entries(raw_entries):
    for entry in raw_entries:
        entry['detail'] = extract_entry_from_url(entry['href'])
    return raw_entries



DUNUN_EN_BEGENILENLERI = "https://eksisozluk.com/istatistik/dunun-en-begenilen-entryleri"
HAFTANIN_EN_BEGENILENLERI = "https://eksisozluk.com/istatistik/gecen-haftanin-en-begenilen-entryleri"


if __name__ == '__main__':
    import os
    try:
        os.makedirs("data")
    except:
        pass # already exists

    open("data/dun.json", "w").write(json.dumps(fetch_raw_entries(DUNUN_EN_BEGENILENLERI)))
    open("data/hafta.json", "w").write(json.dumps(fetch_raw_entries(HAFTANIN_EN_BEGENILENLERI)))

    open("data/dun_enhanced.json", "w").write(json.dumps(enhance_raw_entries(fetch_raw_entries(DUNUN_EN_BEGENILENLERI))))
    open("data/hafta_enhanced.json", "w").write(json.dumps(enhance_raw_entries(fetch_raw_entries(HAFTANIN_EN_BEGENILENLERI))))
