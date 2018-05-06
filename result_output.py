#coding="utf-8"
import xlwt
import csv

class ResultOutput(object):
	"""docstring for ResultOutput"""
	def __init__(self, arg):
		super(ResultOutput, self).__init__()
		self.arg = arg
		
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