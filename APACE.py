
# coding: utf-8

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
from selenium import webdriver
from pandas import ExcelWriter
from time import sleep
import logging
now=datetime.date.today()


# In[2]:


logging.basicConfig(filename='apace_report.log', level=logging.DEBUG)


# In[3]:


logging.warning('is when this event was logged.'+datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p'))


# In[4]:


path = r'chromeextension'
count = 0


# In[5]:


xetra_url = 'http://www.xetra.com/xetra-en/instruments/shares/new-issues'
db_url = 'http://www.deutsche-boerse-cash-market.com/dbcm-en/instruments-statistics/statistics/primary-market-statistics/1558792!search'


# In[6]:


euronext_url='https://www.euronext.com/en/welcome?quicktabs_25=1#quicktabs-25'
firstnorth_url = "http://www.nasdaqomxnordic.com/news/listings/firstnorth/2018"
omxnordic_url = "http://www.nasdaqomxnordic.com/news/listings/main-market/2018"
moscow_url = 'http://www.moex.com/en/news/?ncat=208'
bse_url = 'http://www.bseindia.com/markets/PublicIssues/IPOIssues_new.aspx?id=1&Type=p'
krx_url = 'http://global.krx.co.kr/contents/GLB/03/0306/0306010000/GLB0306010000.jsp'
tse_url = "http://www.jpx.co.jp/english/listing/stocks/new/index.html"
szse_url = 'http://www.szse.cn/main/en/AboutSZSE/SZSENews/NewListings/'
sehk_url = "http://www.hkexnews.hk/reports/newlisting/new_listing_announcements.htm"
klse_url = "http://www.bursamalaysia.com/market/listed-companies/initial-public-offerings/ipo-summary/"
sgx_url = 'http://www.sgx.com/wps/portal/sgxweb/home/company_disclosure/ipos/ipo_prospectus/!ut/p/c5/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gjR0cTDwNnA0sDC3cLA0_XsDBfFzcPQ4tgc6B8JJK8f6ihuYFnqFOgiVNYqKG3owkB3X4e-bmp-gW5EeUAmormkw!!/dl3/d3/L2dBISEvZ0FBIS9nQSEh/'
lse_url = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/new-and-recent-issues/new-issues.html"
thailand_first_url = 'https://www.set.or.th/set/ipo.do?language=en&country=US'
thailand_second_set_url = 'https://www.set.or.th/en/company/ipo/upcoming_ipo_set.html'
thailand_second_mai_url = 'https://www.set.or.th/en/company/ipo/upcoming_ipo_mai.html'


# In[7]:


# # requirements
# 1. We need Selenium in the system.
# 2. We need python installed in the system
# 3. Chrome Driver
# 4. Change the path of the Driver
# 5. Change the path of the excel file


# In[8]:


def thailand_first(url):
    thailand_first = requests.get(url)
    thailand_first_soup = BeautifulSoup(thailand_first.content)
    thailand_first_table = thailand_first_soup.find_all('table', attrs={'class':'table table-profile table-hover table-set-border-yellow'})
    
    #making it constant since the headers have rowspan in them, doesn't make sense
    headers=['Symbol','Industry Group','','IPO','','','First Trading','']
    second_header = ['','','Issued Size(M/Bhat)', 'Mkt. Cap','Price','Close Price','%Change','Date']
    thailand_first_dataframe = pd.DataFrame(columns=headers)
    
    thailand_first_dataframe.loc[0] = second_header
    
    pos=1
    for tr in thailand_first_table[1].find_all('tr'):
        temp_list= []
        td = tr.find_all('td')
        for j in range(len(td)):
            temp_list.append(td[j].string)
        if len(temp_list) != 0:
            thailand_first_dataframe.loc[pos] = temp_list
            pos+=1 

   
    return thailand_first_dataframe


# In[9]:


def thailand_second_set(url):
    thailand_set = requests.get(url)
    thailand_soup = BeautifulSoup(thailand_set.content)
    
    thailand_table = thailand_soup.find_all('table', attrs={'cellspacing':'0'})
    
    thailand_second_dataframe = pd.DataFrame(columns=['1','2'])
    pos = 0
    tables = thailand_table[0].find_all('table')
    for i in range(2,len(tables)):
        tbody = tables[i].find_all('tbody')
        tr = tbody[0].find_all('tr')

        data = tr[0].find_all('td', attrs={'class': 'line-yellow-underline'})
        data =str(data[0].text)
        data = data.split(':')
        thailand_second_dataframe.loc[pos] = data
        pos+=1
    
    
        for j in range(1, len(tr)):
            temp_list = []
            td = tr[j].find_all('td')
            for data in td:
                try:
                    if len(data.string) != 1:
                        temp_list.append(data.string)  
                except:
                    pass
         
            try:          
                thailand_second_dataframe.loc[pos] = temp_list
                pos+= 1    
            except:
                pass
        
        thailand_second_dataframe.loc[pos] = [' ',' ']
        pos+=1
        
    return thailand_second_dataframe
    


# In[10]:


def thailand_second_mai(url):
    
    thailand_set = requests.get(url)
    thailand_soup = BeautifulSoup(thailand_set.content)
    thailand_table = thailand_soup.find_all('table', attrs={'cellspacing':'0'})
    
    thailand_second_dataframe = pd.DataFrame(columns=['1','2'])
    pos = 0
    #tables = thailand_table[0].find_all('table')
    for i in range(1,len(thailand_table)):
        tbody = thailand_table[i].find_all('tbody')
        tr = tbody[0].find_all('tr')

        data = tr[0].find_all('td', attrs={'class': 'line-yellow-underline'})
        data =str(data[0].text)
        data = data.split(':')
        thailand_second_dataframe.loc[pos] = data
        pos+=1
    
    
        for j in range(1, len(tr)):
            temp_list = []
            td = tr[j].find_all('td')
            for data in td:
                try:
                    if len(data.string) != 1:
                        temp_list.append(data.string)  
                except:
                    pass
         
            try:          
                thailand_second_dataframe.loc[pos] = temp_list
                pos+= 1    
            except:
                pass
        
        thailand_second_dataframe.loc[pos] = [' ',' ']
        pos+=1
        
    return thailand_second_dataframe

thailand_first(thailand_first_url)
thailand_second_set(thailand_second_set_url)
thailand_second_mai(thailand_sec_mai_url)
i=0
while (i<=len(thailand_first_df)):
    try:
        if thailand_first_df.iloc[0,1]==0:
            i+=1
            print('i am in if condition')
        else:
            print('i am in else condition')
            i+=1

# In[11]:


thailand_first_df = thailand_first(thailand_first_url)
thailand_second_set_df = thailand_second_set(thailand_second_set_url)
thailand_second_mai_df = thailand_second_mai(thailand_second_mai_url)


# In[12]:


def six_swiss_ipo():
    six_swiss_data = requests.get('http://www.six-swiss-exchange.com/issuers/equities/ipo/2018/overview_en.html')
    swiss_soup = BeautifulSoup(six_swiss_data.content)
    
    if swiss_soup.title.string == 'Error':
        six_swiss_data = requests.get('http://www.six-swiss-exchange.com/issuers/equities/ipo/2017/upcoming_en.html')
        swiss_soup = BeautifulSoup(six_swiss_data.content)
    
    swiss_table = swiss_soup.find_all('table', attrs={'class':'table-grid'})
    
    swiss_tr = swiss_table[0].find_all('tr')

    headers_list = []
    td = swiss_tr[1].find_all('td')
    for data in td:
        if data.string is None:
            headers_list.append('Listing Agent')
        else:
            headers_list.append(data.string)

    swiss_dataframe = pd.DataFrame(columns=headers_list)
    pos = 0
    for i in range(2,len(swiss_tr)):
        temp_list = []
        for td in swiss_tr[i].find_all('td'):
            temp_list.append(td.text)
        
        swiss_dataframe.loc[pos] = temp_list
        pos+=1
    
    return swiss_dataframe
#     print(headers_list)
#     for i in range(2, len(swiss_tr)):
#         temp_list = []
#         td = swiss_tr[i].find_all('td')
#         for data in td:
#             temp_list.append(data.string)
            
#         swiss_dataframe.loc[pos] = temp_list
#         pos+=1
    
     
    


# In[13]:


swiss = six_swiss_ipo()


# In[14]:


def bse_crawler(url):
    bse_page = urlopen(url)
    bse_soup = BeautifulSoup(bse_page)
        
    
    bse_data = bse_soup.find_all('table', class_='tablesorter')
    
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]

    tbody = bse_data[0].find_all('tbody')

    for rows in tbody[0].find_all('tr'):
        cells = rows.find_all('td')
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=True))
        C.append(cells[2].find(text=True))
        D.append(cells[3].find(text=True))
        E.append(cells[4].find(text=True))
        F.append(cells[5].find(text=True))
        G.append(cells[6].find(text=True))
    
    bse_data=pd.DataFrame()
    bse_data['Security']=A
    bse_data['Start Date']=B
    bse_data['End Date']=C
    bse_data['Offer Price']=D
    bse_data['Face Value']=E
    bse_data['Type of Issues']=F
    bse_data['Issue Status'] = G
    
    return bse_data
    
    
    


# In[15]:


bse_ipo = bse_crawler(bse_url)


# In[16]:


def budapest_ipo(url):
    budapest_data = requests.get(url)
    budapest_soup = BeautifulSoup(budapest_data.content)
    
    #so find method gives the exact match whereas find_all is giving us all the matches in the form of an array
    budapest_div = budapest_soup.find('div', class_="article-body")
    budapest_ipo_table = budapest_div.find('table')
    budapest_ipo_table = budapest_ipo_table.find('tbody')
    
    flag = 0
    pos = 0
    for tr in budapest_ipo_table.find_all('tr'):
        temp_list = []
    
        if flag == 0:
            for td in tr.find_all('td'):
                temp_string = td.find_all('p')
                temp_list.append(temp_string[0].string)
            budapest_dataframe = pd.DataFrame(columns=temp_list)   
            flag = 1
        else:
            for td in tr.find_all('td'):
                temp_string = td.find_all('p')
                temp_list.append(temp_string[0].string)
            budapest_dataframe.loc[pos] = temp_list
            pos += 1
    
    return budapest_dataframe


# In[17]:


budapest_ipo = budapest_ipo("https://www.bse.hu/Issuers/Recent-Listings")


# In[18]:


def deutsche_ipo(url):
    db_page = requests.get(url)
    
    db_soup = BeautifulSoup(db_page.content)
    
    xetra_ol = db_soup.find_all('ol', class_="list")
    
    xetra_dataframe = pd.DataFrame(columns=['Date of Issue', 'Name of the Issue', 'ISIN'])

    pos = 0
    for li in xetra_ol[0].find_all('li'):
        temp_list = []
        date = ''
        date = li.find_all('span')
        date = (date[0].string).split(' ')
        date_int = int(date[2])
        if date_int == (datetime.datetime.now()).year:
            link = li.find_all('a', href=True)
            temp_list.append(((li.find_all('span'))[0]).string)
            temp_list.append(((li.find_all('a'))[0]).string)
        
            temp_url = 'http://www.xetra.com' + link[0]['href']
            temp_page = requests.get(temp_url)
            temp_soup = BeautifulSoup(temp_page.content)
            dl = temp_soup.find_all('dl', class_="list-tradable-details")
            dt = dl[0].find_all('dt')
            dd = dl[0].find_all('dd')
            row = 0
            for data in dt:
                if data.string == 'ISIN:':
                    break
                row += 1   
            if row < len(dt):
                temp_list.append(dd[row].string)
        
            xetra_dataframe.loc[pos] = temp_list
            pos += 1
        
        
    return xetra_dataframe
    
    


# In[19]:


db_response = False
while not db_response:
    if count < 3:
        try:         
            db = deutsche_ipo(db_url)
            db_response = True
            count = 0
        except:
            count+=1
            print('DB is not responding !!!')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+db_url+ ' is not responding')
        count = 0
        break


# In[20]:


def xetra_ipo(url):
    #fetch the ool class list  search-results 
    xetra_page = requests.get(url)
    xetra_soup = BeautifulSoup(xetra_page.content)
    xetra_ol = xetra_soup.find_all('ol', class_="list")
    
    xetra_dataframe = pd.DataFrame(columns=['Date of Issue', 'Name of the Issue', 'ISIN'])

    pos = 0
    for li in xetra_ol[0].find_all('li'):
        temp_list = []
        date = ''
        date = li.find_all('span')
        date = (date[0].string).split(' ')
        date_int = int(date[2])
        if date_int == (datetime.datetime.now()).year:
            link = li.find_all('a', href=True)
            temp_list.append(((li.find_all('span'))[0]).string)
            temp_list.append(((li.find_all('a'))[0]).string)
            
            temp_url = 'http://www.xetra.com' + link[0]['href']
            temp_page = requests.get(temp_url)
            temp_soup = BeautifulSoup(temp_page.content)
            dl = temp_soup.find_all('dl', class_="list-tradable-details")
            dt = dl[0].find_all('dt')
            dd = dl[0].find_all('dd')
            row = 0
            for data in dt:
                if data.string == 'ISIN:':
                    break
                row += 1   
            if row < len(dt):
                temp_list.append(dd[row].string)
        
            xetra_dataframe.loc[pos] = temp_list
            pos += 1
        
    return xetra_dataframe 
    


# In[21]:


response = False
while not response:
    if count < 3:
        try:         
            xetr = xetra_ipo(xetra_url)
            response = True
            count = 0
        except:
            count+=1
            print('Xetra is not responding !!!')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+xetra_url+' is not responding')
        count = 0
        break


# In[22]:


def euro_next(url):
    r=requests.get(url)
    c=r.content
    Euronext_soup=BeautifulSoup(c,'html.parser')
    Euronext_s1=Euronext_soup.find_all("div",{"id":"quicktabs_tabpage_25_1"})
    Euronext_s2=Euronext_s1[0].find_all("thead")
    Euronext_s3=Euronext_s2[0].find_all("th")
    now=datetime.date.today()
    Euronext_temp_list=[]
    for i in range(len(Euronext_s3)):
        Euronext_temp_str=str(Euronext_s3[i].text)
        Euronext_temp_list.append(Euronext_temp_str.strip())
    Euronext_df1=pd.DataFrame(columns=Euronext_temp_list)
    Euronext_df1['Ticker']=''
    Euronext_df1['Subsector'] = ''
    Euronext_df1['Issue Type'] = ''
    Euronext_s4=Euronext_s1[0].find_all("tbody")
    Euronext_s5=Euronext_s4[0].find_all("tr")
    Euronext_s6=Euronext_s5[0].find_all("td")
    Euronext_pos=0
    for Euronext_b in range(len(Euronext_s5)):
        Euronext_final=[]
        for Euronext_a in Euronext_s5[Euronext_b].find_all("span",{"class":"date-display-single"}):
            Euronext_final.append(Euronext_a.text)
        for Euronext_a in Euronext_s5[Euronext_b].find_all("a"):
            Euronext_final.append(Euronext_a.text)
        for Euronext_a in Euronext_s5[Euronext_b].find_all("td",{"class":"views-field views-field-field-iponi-isin-code-value"}):
            Euronext_final.append(Euronext_a.text)
        for Euronext_a in Euronext_s5[Euronext_b].find_all("td",{"class":"views-field views-field-tid"}):
            Euronext_final.append(Euronext_a.text)
        for Euronext_a in Euronext_s5[Euronext_b].find_all("td",{"class":"views-field views-field-tid-1"}):
            Euronext_final.append(Euronext_a.text)
        for Euronext_a in Euronext_s5[Euronext_b].find_all("a"):
            Euronext_l1=Euronext_a.get('href')
            Euronext_l2="https://www.euronext.com"+Euronext_l1
            Euronext_r1=requests.get(Euronext_l2)
            Euronext_soup1=BeautifulSoup(Euronext_r1.content)
            Euronext_s10=Euronext_soup1.find_all("div",{"class":"if-block"})
            Euronext_s11=Euronext_s10[0].find_all("div")
            l=len(Euronext_s11)
            Euronext_final.append((Euronext_s11[l-1].find_all('strong'))[0].string)
            Euronext_final.append((Euronext_s11[l-3].find_all('strong'))[0].string)
            #Now going for Issue type
            euro_issue = Euronext_soup1.find_all("div",{"class":"column right"})
            inside_euro_issue = euro_issue[0].find_all("div",{"class":"if-block"})
            divs_inside = inside_euro_issue[0].find_all("div")
            l = len(divs_inside)
            
            Euronext_final.append((divs_inside[1].find_all('strong'))[0].string)#If there is a error on this line check the site
        Euronext_df1.loc[Euronext_pos]=Euronext_final
        Euronext_pos+=1
    
    return Euronext_df1


# In[23]:


response = False
while not response:
    if count < 3:
        try:         
            euro_next = euro_next(euronext_url)
            response = True
            count = 0
        except:
            count+=1
            print('EuroNext is not Responding !!!'+' Trying Again')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+euronext_url+' is not responding')
        count = 0
        break


# In[24]:


def firstnorth_ipo(url):
    firstnorth_r=requests.get("http://www.nasdaqomxnordic.com/news/listings/firstnorth/2018")
    firstnorth_soup=BeautifulSoup(firstnorth_r.content)
    firstnorth_s2=firstnorth_soup.find_all("div",{"class":"row"})
    firstnorth_s3=firstnorth_s2[0].find_all("div",{"class":"componentContent ui-corner-bottom"})
    
    all_ps = firstnorth_s3[1].find_all('p')
    
    first_north_df = pd.DataFrame(columns=['Company','Country','ISIN','Ticker','Date'])
    pos = 0
    for i in range(len(all_ps)-1):
        temp_list = []
        country_date = all_ps[i].find_all('b')
        country_date = country_date[0].string
        country_date = country_date.split(',')
        
        links = all_ps[i].find_all('a')
        links = links[0].get('href')
        
        going_inside_link = requests.get(links)
        link_soup = BeautifulSoup(going_inside_link.content)
        getting_header = link_soup.find_all('header', attrs={'class': 'navigationTitleHeader'})
        getting_header = getting_header[0].find_all('h1')
        getting_header = getting_header[0].string
        getting_header = getting_header.split(',')
        
        temp_list.append(getting_header[1])
        temp_list.append(country_date[0])
        temp_list.append(getting_header[2])
        temp_list.append(getting_header[0])
        temp_list.append(country_date[1])
        first_north_df.loc[pos] = temp_list
        pos+=1
    
    return first_north_df


# In[25]:


response = False
while not response:
    if count < 3:
        try:         
            firstnorth = firstnorth_ipo(firstnorth_url)
            response = True
            count = 0
        except:
            count+=1
            print('FirstNorth is not Responding !!!'+' Trying Again')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+firstnorth_url+' is not responding')
        count = 0
        break


# In[26]:


def omx_nordic_ipo(url):
    omx_r=requests.get("http://www.nasdaqomxnordic.com/news/listings/main-market/2018")
    omx_soup=BeautifulSoup(omx_r.content)
    omx_s2=omx_soup.find_all("div",{"class":"row"})
    omx_s3=omx_s2[0].find_all("div",{"class":"componentContent ui-corner-bottom"})
    omx_s4=omx_s3[0].find_all("p")
    
    omx_df = pd.DataFrame(columns=['Company', 'Country', 'ISIN', 'Ticker', 'Date'])
    pos = 0
    for i in range(len(omx_s4)):
        temp_list = []
        country_date = omx_s4[i].find_all('b')
        country_date = country_date[0].string
        country_date = country_date.split(',')
        
        links = omx_s4[i].find_all('a')
        links = links[0].get('href')
        going_inside_links = requests.get(links)
        link_soup = BeautifulSoup(going_inside_links.content)
        
        getting_header = link_soup.find_all('header', attrs={'class': 'navigationTitleHeader'})
        getting_header = getting_header[0].find_all('h1')
        getting_header = getting_header[0].string
        getting_header = getting_header.split(',')
        
        temp_list.append(getting_header[1])
        temp_list.append(country_date[0])
        temp_list.append(getting_header[2])
        temp_list.append(getting_header[0])
        temp_list.append(country_date[1])
        
        omx_df.loc[pos] = temp_list
        pos+=1
     
    return omx_df


# In[27]:


response = False
while not response:
    if count < 3:
        try:         
            omx_nordic = omx_nordic_ipo(omxnordic_url)
            response = True
            count = 0
        except:
            count+=1
            print('FirstNorth Main Market is not Responding !!!'+' Trying Again')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+omxnordic_url+' is not responding')
        count = 0
        break


# In[28]:


def klse_ipo(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    klse_data=soup.find_all("div",{"class":"bm_tabs_content"})
    klse_s2=klse_data[0].find_all("tr",{"class":"bm_col_hdr"})
    table_list=[]
    for th in klse_s2[0].find_all("th"):
        table_list.append(th.string)
    klse_s3=klse_data[0].find_all("tbody")
    klse_s4=klse_s3[0].find_all("tr")
    klse_s5=klse_s3[0].find_all("td")
    templist=[]
    klse_df=pd.DataFrame(columns=templist)
    klse_df['company']=''
    klse_df['Opening']=''
    klse_df['Closing']=''
    klse_df['ISSUE PRICE']=''
    klse_df['Public Issue']=''
    klse_df['Offer For Sale']=''
    klse_df['Private Placement']=''
    klse_df['AC NO']=''
    klse_df['Market']=''
    klse_df['DATE OF LISTING']=''
    klse_pos=0

    for j in range(len(klse_s4)):
        data_test=[]
        for i in klse_s4[j].find_all("td"):
            data_test.append(i.string)
        klse_df.loc[klse_pos]=data_test
        klse_pos+=1
    
    return klse_df


# In[29]:


response = False
while not response:
    if count < 3:
        try:         
            klse = klse_ipo(klse_url)
            response = True
            count = 0
        except:
            count+=1
            print('KLSE is not Responding !!!'+' Trying Again')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+klse_url+' is not responding')
        count = 0
        break


# In[30]:


def krx_main(for_attr, browser):
    
    browser.find_element_by_id(for_attr).click()
    div = browser.find_element_by_xpath('//div[@class="design-center"]')
    div.find_element_by_class_name('btn-board').click()
    
    sleep(3) #page load
    krx_soup = BeautifulSoup(browser.page_source)
        
    krx_table = krx_soup.find_all('table', attrs={'class': 'CI-GRID-BODY-TABLE'})

    krx_head = krx_table[0].find_all('thead')
    krx_tr = krx_head[0].find_all('tr')
    
    header_list = []
    for th in krx_tr[0].find_all('th'):
        header_list.append(th.string)
    krx_dataframe = pd.DataFrame(columns=header_list)   
    
    
    krx_tbody = krx_table[0].find_all('tbody')
    krx_tr = krx_tbody[0].find_all('tr')
    
    if len(krx_tr) > 1:
        
        for i in range(len(krx_tr)):
            temp_list = []
            for td in krx_tr[i].find_all('td'):
                temp_list.append(td.string)
            krx_dataframe.loc[i] = temp_list
    else:
        return 0
        
    return krx_dataframe    


# In[31]:


#krx Special Case

headless = webdriver.ChromeOptions()
headless.add_argument('--headless')
headless.add_argument('--disable-gpu')
headless_browser = webdriver.Chrome(path, options=headless) #path to the driver


response = False
while not response:
    if count < 3:
        try:         
            headless_browser.get(krx_url)
            
            for_attr = headless_browser.find_element_by_xpath("//label[text()='KOSDAQ']").get_attribute("for")
            for_attr2 = headless_browser.find_element_by_xpath("//label[text()='KONEX']").get_attribute("for")

            krx_kasdaq = krx_main(for_attr, headless_browser)
            krx_konex = krx_main(for_attr2, headless_browser)
            
            response = True
            count = 0
        except:
            count+=1
            print('KRX is not Responding !!!'+' Trying Again')
    else:
        logging.warning(datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')+' '+krx_url+' is not responding')
        count = 0
        break


# In[32]:


def lse_ipo(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    lse_scrape=soup.find_all("div",{"class":"column1_nomenu"},{"class":"lineh1"})
    lse_scrape2=lse_scrape[0].find_all("th")
    table_list=[]
    for i in range(len(lse_scrape2)-1): 
        for th in lse_scrape2[i].find_all("p",{"class":"floatsx linenormal"}):
            table_list.append(th.string)
    lse = pd.DataFrame(columns=table_list)
    lse['amount raised']=''
    pos = 0
    s1=lse_scrape[0].find_all("tbody")
    s2=s1[0].find_all("tr")
    for a in range(len(s2)):
        temp_list = []
        for i in s2[a].find_all("td"):
            temp_list.append(i.string)
        lse.loc[pos] = temp_list
        pos += 1
    
    return lse
    


# In[33]:


lse = lse_ipo(lse_url)


# In[34]:


#  browser = webdriver.ChromeOptions()
# web_page = webdriver.Chrome(path, options=browser)#path to the driver 


# In[43]:


def nse_ipo(path):
    
    browser = webdriver.ChromeOptions()
    browser.add_argument('--headless')
    browser.add_argument('--disable-gpu')
                                                           
    web_page = webdriver.Chrome(path, options=browser)#path to the driver                                                           
    web_page.get('https://www.nseindia.com/products/content/equities/ipos/homepage_ipo.htm')
    sleep(5)
    source = web_page.page_source

    nse_soup = BeautifulSoup(source)
    
    nse_div = nse_soup.find_all('div', attrs={"class": "tabular-data-historic"})
    
    sleep(5)
    nse_tbody = nse_div[0].find_all('tbody')
    
    
    head = nse_tbody[0].find_all('tr', attrs={'class':'alt'})
    table_headers = []
    for data in head[0].find_all('td'):
        table_headers.append(data.string)
    
    table_headers.append('Symbol')
#     table_headers.append('Issue Type')
    
    nse_dataframe = pd.DataFrame(columns=table_headers)  
    tr = nse_tbody[0].find_all('tr')

    pos = 0
    for i in range(1, len(tr)):
        temp_list = []
        td = tr[i].find_all('td')
        
        for data in td:
            temp_list.append(data.string)
        
        link = td[0].find_all('a')
        if link:
            link = link[0].get('href')
            primt
            web_page.get('https://www.nseindia.com'+link)
            sleep(5)
            extra_data = web_page.page_source
            extra_soup = BeautifulSoup(extra_data)
        
            extra_div = extra_soup.find_all("div", attrs={"id":"ipo_mid"})
            extra_table = extra_div[0].find_all('table')
        
            extra_tbody = extra_table[0].find_all('tbody')
            extra_tr = extra_tbody[0].find_all('tr')
            temp_str = ''
            for j in range(1, len(extra_tr)):
                td = extra_tr[j].find_all('td')
                temp_str = td[0].string
                try:
                    temp_str = temp_str.replace(' ','')
                except:
                    pass
                if temp_str == 'Symbol':
                    temp_list.append(td[1].string)
                    break
                 
        #THis needs to be looked after                
        try:
            if len(temp_list) >= 1:
                nse_dataframe.loc[pos] = temp_list
                pos+= 1
        except:
            pass
    
    web_page.get('https://www.nseindia.com/products/content/equities/ipos/homepage_ipo.htm')
    sleep(5)
    source = web_page.page_source

    nse_soup = BeautifulSoup(source)
    
    red_herring = nse_soup.find_all('div', attrs={'id': 'rhpFinal'})
    red_herring_table = red_herring[0].find_all('tbody')
    
    table_headers = []
    red_herring_tr = red_herring_table[0].find_all('tr')
    pos = 0
    
    for td in red_herring_tr[0].find_all('td'):
        table_headers.append(td.string)
    
    nse_red_herring = pd.DataFrame(columns=table_headers)
    
    for k in range(1, len(red_herring_tr)):
        temp_list = []
        td = red_herring_tr[k].find_all('td')
        for data in td:
            temp_list.append(data.string)
        try:
            nse_red_herring.loc[pos] = temp_list
        except:
            pass
        pos+=1
    
    #The code for the sme starts here...both the active and forthcoming issues
    web_page.get('https://www.nseindia.com/emerge/live_market/content/live_watch/ipo/sme_ipo.htm')
    sleep(5)
    source = web_page.page_source
    sme_soup = BeautifulSoup(source)
    
    sme_div = sme_soup.find_all('div', attrs={'class' : 'tabular_data_live_analysis'})
    sleep(5)
    sme_table = sme_div[0].find_all('table')
    sme_tbody = sme_table[0].find_all('tbody')
    sme_tr = sme_tbody[0].find_all('tr')
    head = sme_tr[1]

    table_headers = []
    for data in head.find_all('th'):
        table_headers.append(data.string)

    sme_nse_dataframe = pd.DataFrame(columns=table_headers)

    pos = 0
    for i in range(2,len(sme_tr)):
        temp_list = []
        for td in sme_tr[i].find_all('td'):
            
            temp_list.append(td.string)

        try:
            sme_nse_dataframe.loc[pos] = temp_list
        except:
            pass
#             temp_list.append(None)
#             sme_nse_dataframe.loc[pos] = temp_list
        pos+=1

    sample = web_page.find_element_by_xpath('//*[@id="tab8"]')
    sample.click()
    sleep(5)  #for the site to come alive
    source = web_page.page_source
    sme_soup = BeautifulSoup(source)
    sme_table = sme_soup.find_all('table', attrs={'id':'dataTable'})
    sme_table_tr = sme_table[1].find_all('tr')
    
    header_list = []
    for data in sme_table_tr[1].find_all('th'):
        header_list.append(data.string)
    sme_dataframe_forthcoming = pd.DataFrame(columns=header_list)
    pos = 0
    for i in range(2, len(sme_table_tr)):
        temp_list = []
        for data in sme_table_tr[i].find_all('td'):
            temp_list.append(data.string)  
        try:
            if len(temp_list) > 1:
                sme_dataframe_forthcoming.loc[pos] = temp_list    
            pos+=1
        except:pass
    return (nse_dataframe, sme_nse_dataframe, nse_red_herring, sme_dataframe_forthcoming)


# In[44]:


nse_dataframe, sme_nse_dataframe, nse_red_herring, sme_dataframe_forthcoming = nse_ipo(path)

sme_nse_dataframe.drop('Sr No',1,inplace=True)
sme_dataframe_forthcoming.drop('Sr No',1,inplace=True)


# In[ ]:


def moscow_ipo(url):
    rts_r=requests.get(url)
    rts_c=rts_r.content
    rts_soup=BeautifulSoup(rts_c)
    rts_s1=rts_soup.find_all("div",{"class":"news-list__content"})
    rts_s5=rts_soup.find_all("div",{"class":"news-list__date"})
    rts_table_list=[]
    rts_df=pd.DataFrame(rts_table_list)
    rts_df['date']=''
    rts_df['comment']=''
    rts_df['URL']=''
    rts_pos=0
    for rts_i in range(len(rts_s1)):
        rts_temp_list=[]
        for rts_link in rts_s1[rts_i].find_all('a'):
            rts_l1=rts_link.get('href')
            rts_l2="http://www.moex.com"+rts_l1
            rts_temp_list.append(rts_s5[rts_i].string)
            rts_temp_list.append(rts_s1[rts_i].string)
            rts_temp_list.append(rts_l2)
            rts_df.loc[rts_i]= rts_temp_list   
      
    return rts_df


# In[ ]:


moscow_exchange = moscow_ipo(moscow_url)


# In[ ]:


def sehk_ipo(url):# test this
    r=requests.get("http://www.hkexnews.hk/reports/newlisting/new_listing_announcements.htm")
    soup=BeautifulSoup(r.content)
    s1=soup.find_all("table",{"class":"table_grey_border ms-rteTable-BlueTable_ENG"})
    s2 = s1[0].find_all('tbody')
    tr = s2[0].find_all('tr')
    header_list = []
    for td in tr[0].find_all('td'):
        header_list.append(td.string)
    header_list.append('Link1')
    header_list.append('Link2')
    temp_df = pd.DataFrame(columns=header_list)
    pos = 0
    # counter = 0
    for i in range(1,len(tr)):
        temp_list = []
        link_list = []
        for td in tr[i].find_all('td'):
    #         temp_list.append(td.string)
            temp_str = td.find('a')
            if temp_str != None:
                link_list.append('http://www.hkexnews.hk'+temp_str.get('href'))
            temp_list.append(td.string)  

        temp_list.extend(link_list)

        try:
            temp_df.loc[pos] = temp_list
        except:
            temp_list.append(None)
            temp_df.loc[pos] = temp_list

        pos+=1
    
    return temp_df


# In[ ]:


sehk = sehk_ipo(sehk_url)


# In[ ]:


sehk


# In[ ]:


def sgx_ipo(url, path):
    browser = webdriver.ChromeOptions()
    browser.add_argument('--headless')
    browser.add_argument('--disable-gpu')
    web_page = webdriver.Chrome(path, options=browser)
    web_page.get(url) 
    sleep(5)
    source = web_page.page_source
    soup=BeautifulSoup(source)
    s1=soup.find_all("div",{"class":"gridMainContainer"})
    sleep(3)
    s2=s1[0].find_all("thead")
    data_test=[]
    df=pd.DataFrame(columns=data_test)
    df['company']=''
    df['date']=''
    s3=s1[0].find_all("tbody")
    s4=s3[0].find_all("tr")
    pos=0
    for i in range(len(s4)):
        temp_list=[]
        s5=s4[i].find_all("td")
        temp_list.append(s5[0].string)
        temp_list.append(s5[1].string)
        df.loc[pos]=temp_list
        pos+=1
    
    return df


# In[ ]:


# PageIdDown2ns_Z7_2AA4H0C098FQE0I104R8P12AF0_
# PageIdDown3ns_Z7_2AA4H0C098FQE0I104R8P12AF0_


# In[ ]:


sgx = sgx_ipo(sgx_url,path)


# In[ ]:


def szse_ipo(url, path):#test this
    browser = webdriver.ChromeOptions()
    browser.add_argument('--headless')
    browser.add_argument('--disable-gpu')
                                                           
    web_page = webdriver.Chrome(path, options=browser)#path to the driver                                                           
    web_page.get(url)
    sleep(3)
    SZSE_source = web_page.page_source
    SZSE_soup=BeautifulSoup(SZSE_source)
    SZSE_s1=SZSE_soup.find_all("td",{"class":"cod"})
    SZSE_s2=SZSE_s1[0].find_all("tbody")
    SZSE_s3=SZSE_s2[0].find_all("tr")
    SZSE_df=pd.DataFrame(columns=["Company","Date of Listing","Ticker Code"])
    SZSE_pos=0
    for SZSE_i in range(len(SZSE_s3)):
        for SZSE_link in SZSE_s3[SZSE_i].find_all('a'):
                SZSE_temp_list=[]
                SZSE_l1=SZSE_link.get('href').lstrip("javascript:openArticle('")
                SZSE_l2=SZSE_l1.rstrip("');")
                SZSE_l3='http://www.szse.cn'+SZSE_l2
                SZSE_s5=SZSE_s3[SZSE_i].find_all("span")
                SZSE_s4=SZSE_s3[SZSE_i].find_all("a")
                SZSE_r1=requests.get(SZSE_l3)
                SZSE_c=SZSE_r1.content
                SZSE_soup1=BeautifulSoup(SZSE_c)
                SZSE_s11=SZSE_soup1.find_all("div",{"class":"news_zw"})
                SZSE_s12=SZSE_s11[0].find_all("span")
                SZSE_s7=SZSE_s12[0].text
                SZSE_temp_list.append(SZSE_s4[0].string.replace(' to List on SZSE',''))
                SZSE_temp_list.append(SZSE_s5[0].string)
                SZSE_temp_list.append(SZSE_s7)
                SZSE_df.loc[SZSE_pos]=SZSE_temp_list
                SZSE_pos+=1
     
    return SZSE_df


# In[ ]:


szse = szse_ipo(szse_url,path)


# In[ ]:


def tse_ipo(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    for sup in soup.find_all('sup'):
        sup.unwrap()
    s1=soup.find_all("div",{"class":"component-normal-table"})
    s2=s1[0].find_all("table",{"class":"fix-header"})
    s3=s2[0].find_all("tr")
    s4=s3[0].find_all("th")

    test_data=[]
    for i in range(len(s4)):
        test_data.append(s4[i].text)
    df1=pd.DataFrame(columns=test_data)
    s5=s2[0].find_all("tbody")
    s6=s5[0].find_all("tr")
    pos=0
    for tr in s5[0].find_all("tr"): 
        temp_list = []
        for td in tr.find_all("td"):
            temp_str=str(td.text)
            temp_list.append(temp_str.strip())  
        df1.loc[pos]=temp_list
        pos+=1
     
    return df1


# In[ ]:


tse = tse_ipo(tse_url)


# In[ ]:


def asx_ipo(url):
    asx_source=requests.get(url)
    asx_soup=BeautifulSoup(asx_source.content)
    asx_div=asx_soup.find_all("div",{"class":"ucf_col1"})
    asx_table=asx_div[0].find_all("table",{"class":"table-responsive"})
    asx_thead=asx_table[0].find_all("thead")
    table_list=[]
    for th in asx_thead[0].find_all("th"):
        table_list.append(th.string)
    asx_df = pd.DataFrame(columns=table_list)
    asx_tbody=asx_table[0].find_all("tbody")
    # path=r'\\II02FIL001.mhf.mhc\FT\2. Operations\MDCA - Securities Management\MDCA Securities Management Processes\6.MDCA-IPO Process'

    asx_pos = 0
    for i in asx_tbody[0].find_all("tr"):
        temp_list = []
        rows = i.find_all("td")
        for i in range(len(table_list)):
            temp_list.append(rows[i].find(text=True))

        asx_df.loc[asx_pos] = temp_list
        asx_pos += 1
    
    return asx_df


# In[ ]:


asx_df=asx_ipo('https://www.marketindex.com.au/')


# In[ ]:


bse_ipo['End Date'] = pd.to_datetime(bse_ipo['End Date'])
budapest_ipo['Listing date']=pd.to_datetime(budapest_ipo['Listing date'])
db['Date of Issue']=pd.to_datetime(db['Date of Issue'])
euro_next['Date']=pd.to_datetime(euro_next['Date'])
klse['DATE OF LISTING']=pd.to_datetime(klse['DATE OF LISTING'])
lse['Expected first day of trading:']=pd.to_datetime(lse['Expected first day of trading:'])
moscow_exchange['date']=pd.to_datetime(moscow_exchange['date'])
df1=szse['Date of Listing']
l = list(df1)
for i in range(len(l)):
    df1[i] = df1[i].lstrip('[')
    df1[i] = df1[i].rstrip(']')
szse['Date of Listing']=df1
szse['Date of Listing']=pd.to_datetime(szse['Date of Listing'])
tse['Date of Listing']=pd.to_datetime(tse['Date of Listing'])
xetr['Date of Issue']=pd.to_datetime(xetr['Date of Issue'])
krx_kasdaq['Initial listing date']=pd.to_datetime(krx_kasdaq['Initial listing date'])
nse_dataframe['Issue Start Date']=pd.to_datetime(nse_dataframe['Issue Start Date'])
sme_nse_dataframe['Start Date']=pd.to_datetime(sme_nse_dataframe['Start Date'])


# In[ ]:


writer=ExcelWriter(r'link')

thailand_first_df.to_excel(writer, 'Thailand First')
thailand_second_set_df.to_excel(writer, 'Thailand Second Set')
thailand_second_mai_df.to_excel(writer, 'Thailand Second Mai')

swiss.to_excel(writer, 'SIX_SWISS', index=False)
bse_ipo[bse_ipo['End Date']>=str(now)].to_excel(writer,'BSE',index=False)
budapest_ipo[budapest_ipo['Listing date']>=str(now)].to_excel(writer,'Budapest',index=False) #date logic added
db.to_excel(writer,'DB',index=False) #date logic removed
euro_next[euro_next['Date']>=str(now)].to_excel(writer,'EuroNext',index=False)
firstnorth.to_excel(writer,'FirstNorth',index=False)
klse[klse['DATE OF LISTING']>=str(now)].to_excel(writer,'KLSE',index=False)
lse[lse['Expected first day of trading:']>=str(now)].to_excel(writer,'LSE',index=False)
omx_nordic.to_excel(writer,'OMX',index=False)
moscow_exchange[moscow_exchange['date']>=str(now)].to_excel(writer,'RTS',index=False)
sehk.to_excel(writer,'SEHK',index=False)
sgx.to_excel(writer,'SGX',index=False)
szse[szse['Date of Listing']>=str(now)].to_excel(writer,'SZSE',index=False)
tse[tse['Date of Listing']>=str(now)].to_excel(writer,'TSE',index=False)
xetr.to_excel(writer,'Xetra',index=False) #date logic removed
asx_df.to_excel(writer,'ASX',index=False)
krx_kasdaq.to_excel(writer,'Kosdaq',index=False) #date logic removed
nse_dataframe[nse_dataframe['Issue Start Date']>=str(now)].to_excel(writer, 'NSE',index=False)
sme_nse_dataframe[sme_nse_dataframe['Start Date']>=str(now)].to_excel(writer, 'Emerging NSE IPO',index=False)
sme_dataframe_forthcoming.to_excel(writer, 'Emerging Forthcoming NSE IPO', index=False)
try:
    krx_konex.to_excel(writer,'Konex',index=False) #date logic removed
except:
    pass
writer.save()


# In[ ]:


# companies_list = []


# In[ ]:


# companies_list.extend(bse_ipo['Security'])
# companies_list.extend(budapest_ipo['Issuer name'])
# companies_list.extend(db['Name of the Issue'])
# companies_list.extend(euro_next['Company name'])
# companies_list.extend(firstnorth['company'])
# companies_list.extend(klse['company'])
# companies_list.extend(lse['Company Name:'])
# companies_list.extend(omx_nordic['company'])
# companies_list.extend(moscow_exchange['comment'])
# companies_list.extend(sehk['Stock Code'])
# companies_list.extend(sgx['company'])
# companies_list.extend(szse['Company'])
# companies_list.extend(tse['Issue Name*2'])
# companies_list.extend(xetr['Name of the Issue'])
# companies_list.extend(asx_df['Company'])
# companies_list.extend(krx_kasdaq['Name'])
# companies_list.extend(nse_dataframe['Company Name'])
# companies_list.extend(sme_nse_dataframe['Company Name'])


# In[ ]:


# companies_list_dataframe = pd.DataFrame(companies_list)


# In[ ]:


# company_writer = ExcelWriter(r'C:\Users\mendajawahar\Downloads\apace_company.xlsx')


# In[ ]:


# companies_list_dataframe.to_excel(company_writer, 'apace_excel', index=False)
# company_writer.save()


# In[46]:


sme_nse_dataframe

