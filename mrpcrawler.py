from lxml import html
import requests
from multiprocessing.dummy import Pool as ThreadPool
from pk import * 
final_dict={}
error_urls=[]
def get_max_price(item):
	flipkart_xpaths=["//a[@class='pricing fk-display-block tpadding5 lpadding10 rpadding10']//text()","//div[@class='pricing line']//span//text()"]
	snapdeal_xpaths=["//span[@id='original-price-id']/text()"]
	id=item.keys()[0]
	url=item[id]
	prices=[]
	max_price=-1
	try:
		if 'flipkart' in url:
			page=requests.get(url)
		        tree=html.fromstring(page.text)
			flipkart_price=[]
			for x_path in flipkart_xpaths:
				all_fk_prices=tree.xpath(x_path)
				if all_fk_prices:
					for unr_price in all_fk_prices:
						if 'Rs' in unr_price and 'EMI' not in unr_price:
							flipkart_price.append(int(unr_price.replace('Rs. ','').replace(',','')))
					break
			if flipkart_price:
				max_price=max(flipkart_price)			
		
		if 'snapdeal' in url:
			page=requests.get(url)
		        tree=html.fromstring(page.text)
			snapdeal_price=[]
			for x_path in snapdeal_xpaths:
				all_sd_prices=tree.xpath(x_path)
				if all_sd_prices:
					for unr_price in all_sd_prices:
						snapdeal_price.append(int(unr_price))
					break
			if snapdeal_price:
				max_price=max(snapdeal_price)
				
			
	except Exception,e :
		if 'snapdeal' in url or 'flipkart' in url:
			error_urls.append({id:url})
		print str(e),id,url
	
	print max_price
	
	if id in final_dict:
		final_dict[id].append(max_price)
	else:
		final_dict[id]=[max_price]
	
		


all_items=[{'_id':'1','url':'http://www.snapdeal.com/product/huawei-ascend-y600-android-phone/1350772303'},{'_id':'1','url':'https://paytm.com/shop/p/micromax-canvas-a1-android-one-black-MOBMICROMAX-CANICE-39090A92349C2'}]
pool = ThreadPool(6) 
#all_items=final()
results = pool.map(get_max_price,all_items)
pool.close() 
pool.join() 

print "crawling finished"
if error_urls:
	print error_urls
	map(get_max_price,error_urls)

print final_dict

error_lists=[]
success_lists=[]

for item in final_dict:
	mrps=final_dict[item]
	if max(mrps)==-1:
		error_lists.append(item)
	else:
		success_lists.append([item,max(mrps)])



error_lists.extend(not_exist)

import json
with open('success_file.json','w') as writefile:
	json.dump(success_lists,writefile)


with open('error_file.json','w') as writefile2:
	json.dump(error_lists,writefile2)








