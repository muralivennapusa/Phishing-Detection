import requests
from flask import Flask,render_template,request
app=Flask(__name__)

b="The mail you receive contains safe url.\nThe email is Legimate"#flag 0
c="This Email may be phishing due to fake url"#flag 1
d="The protocol is not safe but the email is probably legitimate"#flag 2
e="the format of the url is wrong"#flag 3

s1=""

def extract_url1(url):
    s1=url[0:5]
    a=0
    for i in range(0,len(url)):
        if url[i]=='@':
            break
        a+=1
    a+=1
    s1=url[a:]
    s1=s1[:s1.find('/')]
    s1=s1[:s1.index('.')]
    print("The format of given url is wrong\n")
    return s1


def output(flag):
    if flag==0:
        return "The mail you receive contains safe url.\nThe email is Legimate"
    elif flag==1:
        return "This Email may be phishing due to fake url"
    elif flag==2:
        return "The protocol is not safe but the email is probably legitimate"
    else:
        return "the format of the url is wrong"

def extract_url3(url):
    print("The protocol of given url "+url+" is "+url[0:4]+"\n")
    print("The actual safe protocol is https\n")
    flag=2
    return 0


def extract_url2(url):
    s1=url[4:]
    s1=s1[:s1.index('.')]
    return s1


def extract_url4(url):
    s=url[8:]
    if s[3]=='.':
        s=extract_url2(s)
        return s
    elif s[0]!='w':
        if '.' in s:
            s=s[:s.index('.')]
            return s


def unshorten_url(url):
    try:
        response = requests.head("https://"+url, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException:
        return None


def check_domain(domain,flag):
    trueDomains = ['facebook', "messenger", "instagram", "google", "microsoft", "netflix", "paypal", "steampowered",
                   "twitter", "tiktok", "playstation", "twitch", "pinterest", "linkedin", "snapchat", "quora", "ebay",
                   "spotify", "proton", "reddit", "adobe", "badoo", "deviantart", "supercell", "ajio", "garena", "jio",
                   "pubg", "telegram", "youtube", "airtel", "rockstargames", "live", "olacabs", "origin", "amazon",
                   "mozilla", "amazon", "dropbox", "yahoo", "wordpress", "yandex", "vk", "stackoverflow", "mediafire",
                   "xbox", "gitlab", "github", "apple", "icloud", "myspace", "vimeo", "coinmarketcap", "verizon",
                   "roblox", "discord", "ubereats", "zomato", "whatsapp", "hotstar", "paytm", "mobikwik", "phonepe",
                   "teachable", "flipkart", "tracxn", "aminoapps", "bitcoin","ccn","t","youtube","sanji","zoro",
                   "baidu","wikipedia","instagram","facebook","similarweb","tiktok","live","openai" ,"linkedin",
                   "prime","docomo","dzen","naver","samsung","turbopages","mail","microsoftonline","weather",
                   "pininterest","qq","zoom","quora","duckduckgo","aajtak","globo","ebay","msn","bing",
                   "instructure","walmart","zillow","etsy","indeed","accuweather","aol","imdb","craigslist","t-mobile",
                   "canva","realtor","wellsfargo","lowes","ticketmaster","fedex","tumbir","homedepot","biospot","patreon",
                   "rbi","radiogarden","justwatch","buzzfeed","photopea","forvo","futureme","fotoforensics","ligthningmaps",
                   "pointerpointer","nullschools","naturalreaders","all8","futuretimeline","archive","redmi"]
    if flag == 1:
        for i in trueDomains:
            if domain == i:
                flag=0
                return flag
    return flag

def verify(url):
    domain=""
    flag=1

    if '@' in url:
        domain = extract_url1(url)
        flag=check_domain(domain,flag)
    elif url[0:3]=='www':
        domain = extract_url2(url)
        flag=check_domain(domain,flag)
    elif url[0:5] == 'http:':
        flag = extract_url3(url)
    elif url[0:5]=='https':
        domain = extract_url4(url)
        flag=check_domain(domain,flag)
    else:
        do=unshorten_url(url)
        if do[:5]=="https":
            domain=extract_url4(do)
            flag=check_domain(domain,flag)
        elif do[:5]=="http:":
            domain=extract_url3(do)
            flag=check_domain(domain,flag)
        else:
            print("failed")

    s1=output(flag)
    return s1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_input():
    url = request.form['user_input']
    s1=verify(url)
    return render_template('pass.html',Result=s1)


if __name__=="__main__":
    app.run(debug=True)