import pymysql.cursors
import urllib.request
import json
import xlsxwriter
import datetime
def get_com_to_mysql(appname,startDate):

	
	days = 1
	# input(appname)
	
	# Connect to the database
	connection = pymysql.connect(host='115.159.202.238',
	                             user='revuser',
	                             port=3306,
	                             password='revuser121',
	                             db='rev',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	
	tablename = appname + '_comment'
	
	
	
	#Time 

	# gameId : 
	
	gameids = {
	    'wechat' : '109',
	    'faceu' : '7571',
	    'ins' :'1762',
	    'meiyan' : '4098'
	}     
	appid = gameids[appname]
	# print(appid)
	
	
	# categoryId : { 9 : 'App Store',
	#                8 : '豌豆荚',
	#                17: 'oppo应用商店'
	#                18: 'vivo应用商店'}
	catename = 'appstore'
	categoryids = {
	    'appstore' : '9',
	    'oppo' : '17',
	    'wdj' :'8',
	    'vivo' : '18',
        'baidu':'10',
        '360':'12',
        'meizu':'19'
	} 
	categoryId = categoryids[catename]
	
	
	page = 0
	
	comCount = 0
	maxPage = 100
	
	# print("开始抓取APP:"+appname+"的从"+startDate + "到"+endDate +"的数据 *** 数据表:" + tablename)
	while page < maxPage:
	    myurl = "http://wetest.qq.com/bee/DataSearchAjax?startDate="+str(startDate)+"+00%3A00%3A00&endDate="+str(startDate)+"+23%3A29%3A00&keywords=&entityId=0&gameId="+str(appid)+"&&nextPage="+str(page)+"&rank=0&isTitle=1&orderBy=2&cateType=2&cateType=2&filterRubbish=1&or_and=and"  
	    response = urllib.request.urlopen(myurl)
	    myjson = json.loads(response.read().decode())
	    maxPage = myjson['ret']['pages']
	    totalcomment = myjson['ret']['total']
	    for aCom in myjson["ret"]["searchDatas"]:
	        with connection.cursor() as cursor:
	            sql = "INSERT INTO " + tablename + " (`name`,`content`,`score`, `date`,`platform`) VALUES (%s,%s,%s,%s,%s)"
	            cursor.execute(sql, (aCom["author"] , aCom["content"] , aCom["rank"] , aCom["createtime"] ,aCom["categoryComment"]))
	            connection.commit()
	    # print("Current Page : " + str(page))
	    # print("Max     Page : " + str(maxPage))
	    page = page + 1
	    pass
	# print("本次获取评论总数:"+str(totalcomment))
	pass


today = datetime.datetime.today() #今天
endDate  = today.strftime('%Y-%m-%d')
beforeDay = today - datetime.timedelta(days = 1)
startDate = beforeDay.strftime('%Y-%m-%d') #昨天

#更新昨天一天的数据
get_com_to_mysql('meiyan',startDate)
get_com_to_mysql('faceu',startDate)