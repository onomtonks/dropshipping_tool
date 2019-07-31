from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.proxy import Proxy, ProxyType

import smtplib
import openpyxl
elink=[]
elink2=[]
PROXY='104.236.248.219:3128'
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu') 
driver=webdriver.Chrome( options=chrome_options,executable_path =r'file location' )
bsObj=""
'opening excel file'
workbook=openpyxl.load_workbook(r'excel file location') 
sheet=workbook.get_sheet_by_name('Sheet1')
def email(subject,elink,url):
	server=smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('email',"password")
	body="ebaylink:"+""+ str(elink)+""+'sourcelink:'+""+str(url)
	msg=f"Subject:{subject}\n\n{body}"
	server.sendmail(
		'email from',
		"email to",
		msg)
def browse(url):
	driver.get(elink2[x])
	html=driver.page_source
	soup=BeautifulSoup(html,"html.parser")
	return soup
for v in range(sheet.max_row-1):
	t=v+2
	x='c'+str(t)
	y='d'+str(t)
	'getting prices from ebay'
	elink.append(sheet[x].value)
	elink2.append(sheet[y].value)
for x in range(v):
	driver.get(elink[x])
	#bsObj = BeautifulSoup(html)
	html=driver.page_source
	soup=BeautifulSoup(html,"html.parser")
	try:
		e_price=soup.find("span",{"class":"notranslate"}).text
		ep=float(e_price[4:])
	except:
		print(' not found')


	url=elink2[x]
	
	if url.startswith('none'):
		print('none')
	elif url.startswith("https://www.amazon.com"):
		soup=browse(url)
		try:

			price=soup.find("span",{"class":"a-size-large a-color-price olpOfferPrice a-text-bold"}).string
			up=price.strip()
			uc=float(up[1:])
		except:
			try:	
				price=soup.find("span",{"class":"a-size-medium a-color-price priceBlockBuyingPriceString"}).string
	
				up=price.strip()
				uc=float(up[1:])
			except:
				try:
					price=soup.find("span",{"class":"a-color-price"}).string	
					up=price.strip() 
					uc=float(up[1:])
				except:
					print(""+"not found")
					uc=ep

	elif url.startswith('https://www.homedepot.com/'):
		driver.get(url)
		html=driver.page_source
		soup=BeautifulSoup(html,"html.parser")
		price=soup.find("span",{"class":"price__dollars"}).text.strip()+'.'+soup.find("span",{"class":"price__cents"}).string.strip()
		up=price.strip()
		uc=float(up)		
	elif url.startswith('https://www.lowes.com/'):
		driver.get(url)
		html=driver.page_source
		soup=BeautifulSoup(html,"html.parser")
		price=soup.find("span",{"class":"primary-font jumbo strong art-pd-price"}).text
		up=price
		print('lowes'+str(up))
		uc=float(up[1:])
	elif url.startswith('https://www.abebooks.com'):
		driver.get(url)
		html=driver.page_source 
		soup=BeautifulSoup(html,"html.parser")
		try:
			price=soup.find("div",{"class":"srp-item-price"}).text
			up=price.strip()
			uc=float(up[4:])
		except:
			print('error in abebooks')
	'email sending part'
	
	if uc<ep*0.75:
		subject="your price is too high"
		email(subject,elink,url)
		print('true')
	elif uc>ep:
		subject="you are going in loss"
		email(subject,elink,url)					
	elif uc>ep*0.86:
		subject="your price is too low"
		email(subject,elink,url)
		
