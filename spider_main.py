#coding="utf-8"
import html
class JobsSpiderMain(object):
	"""docstring for JobsSpoderMain"""
	def __init__(self, arg):
		super(JobsSpoderMain, self).__init__()
		self.arg = arg
		self.downloader = html_download.HtmlDownload()
		self.parser = html_parser.HtmlParser()