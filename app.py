#coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from xmlrpclib import ServerProxy
import os.path
import urllib
from json import JSONEncoder,loads,dumps
import datetime
import time
import re
from info_search import getUrlDict,asynchronous,asynchronous_page,multi_thread_page,multi_page,thread_page,threading_page,news_threading_page,threading_all_page,word_match,multiproc
import sugesstion
#import photos
#from hint_top import hint_top
#import hint_top_search
import relate_search
from tornado.options import define, options
#import recommend
#from record import onServerStartCreateLogTable,onQueryRecordLog
#from apscheduler.schedulers.blocking import BlockingScheduler
#import cgi
import ConfigParser


define("port", default=10116, type=int, help="runs on port")

cf=ConfigParser.ConfigParser()

cf.read("config.cfg")
local_ip=cf.get("local","ip")
local_port=cf.getint("local","port")
remote_ip=cf.get("remote","ip")
remote_port=cf.getint("remote","port")


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_name")
    def check_user(self):
        #return
        if not self.current_user:
            self.redirect("/login")
            return

def qitaQueryForLog(word,search_dict):
    suggestion_map = {}
    suggestion_map = sugesstion.start(word)# 联想词
    return (dumps(suggestion_map, ensure_ascii=False))

# 请求URL 路径为 　domain:port／的事件响应
class IndexHandler(BaseHandler):
    def get(self):
        #self.check_user()
        self.render('index.html')

class SuggestionHandler(BaseHandler):
    def get(self):
        return
        #self.check_user()
        word = self.get_argument('term', default='')
        print word
        print "after word"
        datas = {}
        if word == "":
            return
        else:
            print "word is not empty"
            datas = sugesstion2.start(word)
        result = []
        for key, value in datas.items():
            result.append(key + "--" + value)
        self.write(JSONEncoder().encode(result))

class SuggestionHandler2(BaseHandler):
    def get(self):
        datas = {}
        try:
            fobj = open('testsuggest2.txt', 'r')
        except IOError as err:
            print('file open error: {0}'.format(err))
        else:
            for eachLine in fobj:
                newkey = eachLine.split('|')[0]
                newvalue = eachLine.split('|')[1]
                datas[newkey] = "%s" %newvalue

            fobj.close()
        result = []
        for key, value in datas.items():
            print key + "--" + value
            result.append(key + "--" + value)
        self.write(JSONEncoder().encode(result))

class ResultItemModule(tornado.web.UIModule):
    def render(self, resultItem):
        return self.render_string(
            "modules/resultItem.html",
            resultItem=resultItem
        )

class NewsItemModule(tornado.web.UIModule):
    def render(self, resultItem):
        return self.render_string(
            "modules/newsItem.html",
            data=resultItem
        )

class HeaderItemModule(tornado.web.UIModule):
    def render(self, id):
        return self.render_string(
            "modules/headerItem.html",
            id=id
        )

'''
# 请求URL 路径为 　domain:port／query　的事件响应
class QueryHandler(BaseHandler):
    def get(self):
        #self.check_user()
        # 获取URL参数
        query = self.get_argument('q',default='')
        filte = self.get_argument('filte',default='false')
        pn = int(self.get_argument('pn',default='1'))
        url_type = self.get_argument('url_type', default='')

        search_dict={
            'baidu':self.get_argument('baidu',default='false'),
            's360':self.get_argument('s360',default='false'),
            'sogou':self.get_argument('sogou',default='false'),
            'china_so':self.get_argument('china_so',default='false'),
            'bing':self.get_argument('bing',default='false'),
            'shen_ma':self.get_argument('shen_ma',default='false'),
        }

        # 获取对应搜索引擎的推荐词
        recoDict = hint_top(query,search_dict)
        recoDataList = []
        showRecPic = 0
        #print "recoDict.values():------",len(recoDict.values())
        if recoDict['status'] == 1 and len(recoDict)>1:
            for value in recoDict.values():
                if value !=1 and len(value)>0:
                    recoDataList = value
                    showRecPic = 1

        # 获取所有搜索引擎第pn页的搜索结果
        datalist = threading_page(query, pn, search_dict)
        # 获取相关搜索数据
        suggestions = sugesstion.start(query)

        one_search_data = []
        if datalist :
            one_search_data = datalist[0]  # 一个search取一个data即可
            self.render(
                "query.html",
                searchResult=one_search_data,
                search_dict=search_dict,
                suggestions=suggestions,
                pn=pn,
                showRec=showRecPic,
                recoDataList=recoDataList,
                url_type=url_type,
                searchword=query)
        else :
            self.write("此引擎返回数据为空！")
'''
# 请求URL 路径为 　domain:port／queryAll　的事件响应
class AllQueryHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def remoteServer(self,remote_ip,content_type,query_init,suggestion_map,relate_search_map,hint_top_map):
        #s = ServerProxy("http://111.202.25.65:8080")
        s=ServerProxy("http://%s:%d"%(remote_ip,remote_port))
        s.onQueryRecordLog(remote_ip,str(content_type),query_init,suggestion_map,relate_search_map,hint_top_map)
        print "respones"

    def get(self):
        #self.check_user()
        # 获取URL参数
        query_init = self.get_argument('q',default='')
        query = self.get_argument('q',default='')
        query = urllib.quote(query.encode('utf-8'))
        filte = self.get_argument('filte',default='false')
        pn = int(self.get_argument('pn',default='1'))
        content_type = self.get_argument('content_type', default='2')

        search_dict={
            'huajiao':self.get_argument('huajiao',default='false'),
            'douyu': self.get_argument('douyu', default='false'),
            'meipai': self.get_argument('meipai', default='false'),
            'zhanqi': self.get_argument('zhanqi', default='false'),
            'bili': self.get_argument('bili', default='false'),
            'huya': self.get_argument('huya', default='false'),
            'yy': self.get_argument('yy', default='false'),

        }

        search_String = ""
        search_other_String = ""
        for key in search_dict:
            if search_dict[key] == 'true':
                search_String = search_String+"&"+key+"=true"
            else:
                search_other_String = search_other_String+"&"+key+"=true"

        self.set_cookie("search_String", search_String)
        self.set_cookie("search_other_String", search_other_String)


        url_dict = getUrlDict(query,pn,content_type,search_dict)
        if url_dict is None:
            url_dict = {}
        suggestion_map = qitaQueryForLog(query_init,search_dict)
	# 动作写入日志
        # 模板引擎动态生成网页

       # self.remoteServer(self.request.remote_ip,str(content_type),query_init,suggestion_map,relate_search_map,hint_top_map)
        self.render(
            "all-query.html",
            search_dict=search_dict,
            searchword=query,
            pn=pn,
            url_dict=url_dict,
            content_type=content_type)

class HeaderQueryHandler(BaseHandler):
    def get(self):
        #self.check_user()
        # 获取URL参数
        query = self.get_argument('q',default='')
        filte = self.get_argument('filte',default='false')
        pn = int(self.get_argument('pn',default='1'))
        content_type = int(self.get_argument('content_type', default='2'))
        # 模板引擎动态生成网页
        self.render("header.html",
                    searchword=query,
                    pn=pn,
                    content_type=content_type)


# 请求URL 路径为 　domain:port／queryQita　的事件响应
class QitaQueryHandler(BaseHandler):
    def get(self):
        #self.check_user()
        word = self.get_argument('q',default='')
        #qita类型 1代表联想次 2代表相关搜索 3代表为您推荐
        q_type = self.get_argument('q_type', default='1')
        is_ajax = self.get_argument('is_ajax', default="false")
        print word
        if word == "":
            return
        data_map = {}
        if q_type == '1':
            data_map = sugesstion.start(word)# 联想词
        if is_ajax == "true":
            self.write(dumps(data_map))
        else:
            self.render(
                "qitaQuery.html",
                data_map=data_map,
                searchword=word)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie("user_name")=="ming"):
            self.clear_cookie("user_name")
            fslog=open("login_logs","a")
            cur_time = str(time.strftime('%Y-%m-%d %X',time.localtime()))
            fslog.write( cur_time+" "+self.request.remote_ip+" logout"+"\n")
            fslog.close()
           # self.render("index.html")
        #else:
        self.render("login.html")
    def post(self):
        try:
            user_name=self.get_argument("username")
            password=self.get_argument("password")
            
        except:
            self.render("login.html")
            return 
        #send to DB ,return true or flase
        if user_name =="ming" and password=="127":
            # rights_list=[1,2,3]
             #self.set_secure_cookie("rights_list",rights_list)
             self.set_secure_cookie("user_name",user_name,expires_days=None);
             fslog=open("login_logs","a")
             cur_time = str(time.strftime('%Y-%m-%d %X',time.localtime()))
             fslog.write( cur_time+" "+self.request.remote_ip+" login\n")
             fslog.close()
             #self.render("index.html")
             self.redirect("/")
        else:
             self.render("login.html")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
    'cookie_secret' : 'S6Bp2cVjSAGFXDZqyOh+hfn/fpBnaEzFh22IVmCsVJQ='
    }
    app = tornado.web.Application(
        # handler url正则匹配响应事件
        handlers=[(r"/login", LoginHandler),
                  (r"/", IndexHandler),
                  (r"/queryAll", AllQueryHandler),
                  (r"/queryHeader", HeaderQueryHandler),
                  (r"/queryQita", QitaQueryHandler),
                  (r"/suggest",SuggestionHandler),
                  (r"/suggest2", SuggestionHandler2)],

        # 设置　templates　及　static 路径，可在html 中引用本地文件
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        ui_modules={"ResultItem": ResultItemModule,"HeaderItem": HeaderItemModule,"NewsItem": NewsItemModule},
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        #开启此项，修改代码后服务器自动重启
        debug=True,**settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    #tornado.ioloop.IOLoop.instance().start()
    #s = ServerProxy("http://10.159.81.64:8080")

    #s=ServerProxy("http://%s:%d"%(remote_ip,remote_port))
    #s.onServerStartCreateLogTable()

    tornado.ioloop.IOLoop.instance().start()

