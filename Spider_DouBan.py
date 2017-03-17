# -*- coding:utf8 -*-
"""
简单的实现爬取豆瓣网中排名前200个电影名称以及评分
"""
import urllib2
import re

class SpiderDouBan(object):
    """
    属性介绍：
    page：当前正在抓取的页面
    cur_url：当前页面的url
    results：存储抓取结果
    ratingResult:评分
    top_num：记录top号
    """
    def __init__(self):
        self.page=1
        self.cur_url="http://movie.douban.com/top250?start={page}&filter=&type="
        self.results=[]
        self.ratingResult=[]
        self.top_num=1
        print "准备就绪、可以开始抓取了:"
    def get_page(self,cur_page):
        """
           根据当前页码爬取网页HTML
           Args:
           cur_page: 表示当前所抓取的网站页码
           Returns:
           返回抓取到整个页面的HTML(unicode编码)
           Raises:
           URLError:url引发的异常
        """
        url=self.cur_url
        try:
            my_page=urllib2.urlopen(url.format(page=(cur_page-1)*25)).read().decode("utf8")
        except urllib2.URLError,e:
            if hasattr(e,"code"):
                print "请求失败！"
                print "错误代码：%s" % e.code
            elif hasattr(e,"reason"):
                print "查看原因、核对url"
                print "出错原因：%s" % e.reason
        return my_page
    def get_title(self,my_page):
        """
            通过返回的整个网页HTML, 正则匹配前200的电影名称
            Args:
            my_page: 传入页面的HTML文本用于正则匹配
        """
        temp_data=[]
        rating_data=[]
        movie_items=re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        rating_num=re.findall(r'<span.*?property="v:average">(.*?)</span>', my_page, re.S)
        for i,temp in enumerate(rating_num):
            if temp.find("&nbsp")==-1:
                rating_data.append(temp)
        self.ratingResult.extend(rating_data)
        for index,item in enumerate(movie_items):
            if item.find("&nbsp")==-1:
                temp_data.append("Top_"+str(self.top_num)+":"+item)
                self.top_num+=1
        self.results.extend(temp_data)
    def start_spider(self):
        """
        爬虫入口, 并控制爬虫抓取页面的范围
        """
        while self.page<=8:
            my_page=self.get_page(self.page)
            self.get_title(my_page)
            self.page+=1
def main():
    print """
         爬取豆瓣网中排行前200的电影名称、以及对应评分
          """
    my_spider=SpiderDouBan()
    my_spider.start_spider()
    for index,item in enumerate(my_spider.results):

       print item+"##"+my_spider.ratingResult.__getitem__(index)
    print "抓取结束"
if __name__ =='__main__':
    main()


