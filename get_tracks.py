#! /usr/bin/python3.7

from pyppeteer.launcher import launch
import asyncio
import time
import re
import http.cookiejar
import os
import requests


js1 = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''

js3 = '''() => {
        window.navigator.chrome = {
    runtime: {},
    // etc.
  };
    }'''

js4 = '''() =>{
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
        }'''

js5 = '''() =>{
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
        }'''

async def main():
    browser = await launch(args=['--disable-infobars'], headless=False)
    page = await browser.newPage()

    await page.setViewport(viewport={'width': 1280, 'height': 800})
    await page.setJavaScriptEnabled(enabled=True)
    await page.evaluate(js1)
    await page.evaluate(js3)

    headers = {'Host': 'equibase.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9',}

#            'Host': 'www.equibase.com',
#'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#'Accept-Language': 'en-US,en;q=0.5',
#'Accept-Encoding': 'gzip, deflate',
##'Referer': 'http://www.equibase.com/static/chart/pdf/index.html?SAP=SM',
#'Connection': 'keep-alive',
##'Cookie': 'D_IID=B1EFC939-DCAC-39F8-B694-96318AC5045B; D_UID=3720F6BF-D739-31BC-BBCD-40114AE621AA; D_ZID=F69C43B4-3142-3D85-B8BD-F0AE7912CF76; D_ZUID=1F0E121D-3DD3-3416-AC1D-77D21D94DACC; D_HID=73B45F46-D5F8-37B1-8E7E-C6BC4D270897; D_SID=99.71.98.233:fHcl6rUbxiMGBCe5SMbOoEiHGXTvDfLajJKXGI2Bkao; EQBHOME=2; _ga=GA1.2.20890486.1565828540; __qca=P0-2068533508-1565828542062; __gads=ID=87641d67609be65e:T=1565828542:S=ALNI_MaQi9eBmv1XLOXSRUK4JAjmlMZn1g; _awl=2.1567281324.0.4-865bdc9c-dce912550d6e122beb1a4c200d3e9285-6763652d75732d63656e7472616c31-5d6ad0ac-1; clickandchat.com=284-1565986014853; _gid=GA1.2.1057046415.1567193841; SAP=3008191752TN; COOKIE_TEST=TEST',
#'Upgrade-Insecure-Requests': '1',
#'Cache-Control': 'max-age=0'}
#
    await page.setExtraHTTPHeaders(headers)
    await page.setCacheEnabled(False)
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.39 Safari/537.36')
    resp = None
#    while resp and resp.status == 404:
    r = requests.get('http://www.equibase.com/premium/eqpVchartBuy.cfm?mo=9&da=5&yr=2019&trackco=ALL;ALL&cl=Y', headers=headers)

    print(r)
#    
#    all_tracks = re.findall(r'<option value="(.*?)" autocomplete="off">', content)
#    for track in all_tracks:
#        if track == 'ALL;ALL':
#            continue
#        track = track.replace('&amp;', '&')
#        print(track)
#        abv, country, track = track.split(';')
#        print(abv)
#
#
    await page.waitForNavigation(waitUntil='load')
    title = await page.title()

    if title == 'Equibase | Horse Racing':
        cookies = await page.cookies()
        print(cookies)

#    urls = re.findall(r'<a href="(eqbPDFChartPlusIndex.cfm?tid=(.*?)&dt=(.*?)&ctry=(.*?))" title=".*?" class="dkbluesm">\d+</A>', content)

#    print(urls)


    await asyncio.sleep(3)
    await browser.close()

asyncio.run(main())

