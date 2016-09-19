#coding:utf-8

import requests
import sys
import re
import threading
import json

reload(sys)
sys.setdefaultencoding("utf8")

def huYaSuggest(word,dalay=False):
    global mutex
    url="http://www.huya.com/member/index.php?m=Search&do=getSearchContent&uid=0&app=11&v=1&typ=-6&callback=jQuery11110194651358750203_1473146796960&q="+word
    try:
        response=requests.get(url,timeout=2)
    except:
        print "get suggestion from huYa failed"
        return
    result=response.text
    result=result.replace('\\"','"')
    pattern=r'\[(.*?)\]'
    matchObj=re.findall(pattern,result,re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        for key in matchObj:
            ks=key.split(',')
            for item in ks:
                its=item.split(":")
                try:
                    its=its[1]
                    k=eval('u'+its[0:-1])
                    if(datas.has_key(k)):
                        if datas[k].find("huYa")==-1:
                            datas[k] = datas[k]+";huYa"
                    else:
                        datas[k] = "huYa"
                except:
                    pass
        mutex.release()

def meiPaiSuggest(word,dalay=False):
    global mutex
    url="https://www.meipai.com/search/word_assoc?q="+word
    try:
        response=requests.get(url,timeout=2)
    except:
        print "get suggestionfrom meiPai faild"
        return
    result=response.text
    pattern=r'\[(.*?)\]'
    result=result.strip('\n')
    matchObj=result[1:-1]#re.findall(pattern,result,re.M)
    if(len(matchObj)>0):
        mutex.acquire()
        keys=matchObj.split(',')
        for key in keys:
            try:
                key=eval("u"+key)
                if(datas.has_key(key)):
                    if datas[key].find("meiPai")==-1:
                        datas[key] = datas[key]+";meiPai"
                else:
                    datas[key] = "meiPai"
            except:
                pass
        mutex.release()
def yySuggest(word,dalay=False):
    global mutex
    url="http://www.yy.com/search/search.json?q="+word+".&t=-3&n=1"#&s=10"
    try:
        response=requests.get(url,timeout=2)
    except:
        print "get suggestion from YY failed"
        return
    result=response.text
    pattern=r'\"key\":(.*?)[,}]'
    matchObj=re.findall(pattern,result,re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        for key in matchObj:
            key=key[1:-1]
            if(datas.has_key(key)):
                if datas[key].find("YY")==-1:
                    datas[key] = datas[key]+";YY"
            else:
                datas[key] = "YY"
        mutex.release()

def huaJiaoSuggest(word,delay=False):
    global mutex
    url = "http://sug.huajiao.com/?_callback=jQuery110209953296366906192_1473129636790&fmt=jsonp&q="+word
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from huaJiao failed"
        return

    result = response.text
    pattern = r'\{\"nickname\":(.*?)\}'
    matchObj = re.findall(pattern, result, re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        for key in matchObj:
            key=eval("u"+key)
            if(datas.has_key(key)):
                datas[key] = datas[key]+";huaJiao"
            else:
                datas[key] = "huaJiao"
        mutex.release()

def start(word):
    global datas,mutex
    mutex = threading.Lock()
    threads=[]
    datas={}
    threads.append(threading.Thread(target=huaJiaoSuggest,args=(word,False)))
    threads.append(threading.Thread(target=yySuggest,args=(word,False)))
    threads.append(threading.Thread(target=huYaSuggest,args=(word,False)))
    threads.append(threading.Thread(target=meiPaiSuggest,args=(word,False)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()



    if "" in datas.keys():
        datas.pop("",None)

   # for key in datas.keys():
   #     print "["+key+"]-----"+datas[key]

   # datas = json.dumps(datas,encoding='UTF-8',ensure_ascii=False)
   # print datas
    return datas

if __name__ == "__main__":
    word = "1"

    search_dict={
        'baidu':'false',
        's360':'true',
        'sogou':'false',
        'china_so':'false',
        'bing':'true',
        'shen_ma':'false',
    }
    start(word)
