# coding:utf-8
import requests
from urllib import urlencode
from bs4 import BeautifulSoup
import re
import xlwt
import csv
import sys
import urllib2
from tqdm import tqdm

reload(sys)
sys.setdefaultencoding('utf-8')

def html_download(city, keyWords, page):
    # root URL
	    paras = {
	        'jl': city,
	        'kw': keyWords,
	        'p': page,
	        'isadv': 0
	    }
	    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?" + urlencode(paras)
	    response = requests.get(url)
	    if response.status_code == 200:
	        return response.text
	    else:
	        return None

def html_parser(html_cont):
    position = ""
    soup = BeautifulSoup(html_cont, 'html.parser')
    tables = soup.find_all('table', class_="newlist")    
    """
    # 职位名称正则表达式解析
	<a href="http://jobs.zhaopin.com/352508827250282.htm" 
	par="ssidkey=y&amp;ss=201&amp;ff=03&amp;sg=d48919d31bca47678fdbeaa6c72e0d32&amp;so=60" 
	style="font-weight: bold" 
	target="_blank">
	<b>Java</b>开发实习生
	</a>
	<td class="zwmc" style="width: 250px;">
    <input data-monitor="CC120002369J90310854000|60" name="vacancyid" onclick="zlapply.uncheckAll('allvacancyid')" type="checkbox" value="CC120002369J90310854000_854_1_03_201__1_"/>
    <div style="width: 224px;*width: 218px; _width:200px; float: left">
    <a href="http://jobs.zhaopin.com/120002369310854.htm" par="ssidkey=y&amp;ss=201&amp;ff=03&amp;sg=cc4eb87dc13e4bae83bc8cf41efa42be&amp;so=60" style="font-weight: bold" target="_blank"><b>JAVA</b>开发工程师</a>
    </div>
    </td>
    # 公司名称正则表达式解析
    <td class="gsmc"><a href="http://special.zhaopin.com/jn/2011/plrj05168891/" target="_blank">普联软件股份有限公司</a>
    #地点
    <li class="newlist_deatil_two"><span>地点：西安</span>
    <span>公司性质：股份制企业</span>
    <span>公司规模：1000-9999人</span>
    <span>经验：3-5年</span>
    <span>学历：本科</span>
    <span>职位月薪：6000-10000元/月</span>
    #职位描述
    <li class="newlist_deatil_last"> 一、工作职责  .掌握公司平台架构下的软件开发规范  .
    根据系统需求，完成系统的开发工作（包括设计、编码与测试）  .配合系统实施及支持人员编写用户手册  .解答系统实施及支持人员提出的问题  
    二、岗位要求  1.<b>Java</b>要求  .熟悉J2EE架构，了解MVC模式；  .具有良好的&lt;...</li>	
    #代码实现
    location_pattern = re.compile(
        '<td class="gsmc"><a href=.*? target="_blank">(.*?)</a>', re.S)
    locations = re.findall(location_pattern,html_cont)
    for location in locations:
    	print location
    """
    count = 0
    jobs_list = []
    for table in tables:
    	data = {}
        #print "*" * 50
        #print table
        #position = re.findall(position_pattern,table)
        '''
        第一种：
        根据bs的select选择器获取网页元素,返回list对象，其中每个元素为tag对象
        元素调用函数getText() 返回元素的文字内容  position_select[0].getText()
        attrs返回元素属性 position_select[0].attrs
        str() 返回字符串，字符串包含标签符  str(position_select[0]
        '''
        position_select = table.select('td[class="zwmc"] a')
        company_select = table.select('td[class="gsmc"] a')
        salary_select = table.select('td[class="zwyx"]')
        location_select = table.select('td[class="gzdd"]')
        detail_select = table.select('li[class="newlist_deatil_two"] span')
        description_select = table.select('li[class="newlist_deatil_last"]')
        publish_time_select = table.select('td[class="gxsj"] span')
        if count == 0:
        	pass
        else:
        	data['position'] = position_select[0].getText()
        	data['company'] = company_select[0].getText()
        	data['url'] = (company_select[0].attrs).get('href')
        	data['location'] = location_select[0].getText()
        	data['salary'] = salary_select[0].getText()
        	data['description'] = description_select[0].getText()
        	data['publish'] = publish_time_select[0].getText()
        	jobs_list.append(data)
        count += 1
        '''
        第二种：
        标记名获取法，直接用soup对象加标记名，返回tag对象.这种方式，选取唯一标签的时候比较有用。
        或者根据树的结构去选取，一层层的选择
        元素调用函数getText() 返回元素的文字内容
        '''
        '''
        position_tag = table.a
        if position_tag != None:
        	position = position_tag.getText()
        	print position
        else:
        	print table 
        print "*" * 50
    	'''
    return jobs_list

def retrive_value(data,header_en):
	data_list = []
	for item in header_en:
		data_list.append(data.get(item))
	return data_list
	
def excel_output(jobs_list):
    # 创建工作薄
    file = xlwt.Workbook(encoding="utf-8")
    sheet = file.add_sheet("Jobs")
    header = [u'网址', u'职位', u'公司名称', u'薪资', u'工作地点', u'发布时间', u'岗位描述']
    header_en = [u'url',u'position',u'company',u'salary',u'location',u'publish',u'description']
    # 写表头
    for i in range(0,len(header)):
    	sheet.write(0,i,header[i])
    # 写表内容
    row = 1
    for data in jobs_list:
    	for item in data.keys():
    		sheet.write(row,header_en.index(item),data.get(item))
    	row += 1

    file.save('result/jobs.xlsx')

    # 写入csv
    with open('result/jobs.csv','w') as csvfile:
    	writer = csv.writer(csvfile)
    	writer.writerow(header)
    	for data in jobs_list:
    		# 自定义方法根据表头获取值
    		row_list = retrive_value(data,header_en)
    		writer.writerow(row_list)
    		# 使用lambda表达式获取值
    		#writer.writerow(map(lambda x:data.get(x), header_en ))

def main(city, keyWords):
	#获取总页数
    root_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=西安&kw=java&p=1&isadv=0"
    response = urllib2.urlopen(root_url)
    if response.getcode() != 200:
    	return None
    else:
    	first_content = response.read()
    	soup = BeautifulSoup(first_content, 'html.parser')
    	#pages_pattern = re.compile('<span class="search_yx_tj">共<em>(.*?)</em>个职位满足条件</span>'
        #, re.S)
        #pages = re.findall(pages_pattern,first_content)
    	count = soup.find('span',class_="search_yx_tj").find("em").getText()
    	pages = int(count)/60
    if pages<float(count)/60:
    	pages = pages+1
    jobs = []
    for page in tqdm(range(pages)):
    	html_cont = html_download(city, keyWords, 1)
        jobs_list = html_parser(html_cont)
        for job in jobs_list:
        	jobs.append(job)
    excel_output(jobs)


if __name__ == '__main__':
    main('西安', 'java')
