# coding=utf-8
class HtmlDownload(object):
	"""docstring for HtmlDownload"""

	def html_download(city, keyWords, pages):
    # root URL
	    paras = {
	        'jl': city,
	        'kw': keyWords,
	        'pages': pages,
	        'isadv': 0
	    }
	    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?" + urlencode(paras)
	    response = requests.get(url)
	    if response.status_code == 200:
	        return response.text
	    else:
	        return None