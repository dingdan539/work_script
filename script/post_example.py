import urllib
import urllib2


def getresponse(post_parm):
    test_data_urlencode = urllib.urlencode(post_param)
    requrl="http://oms.yihaodian.com.cn/api/notification/event/"
    req = urllib2.Request(url=requrl,data=test_data_urlencode,headers={"Authorization": "Basic ZXZlbnRfcG9zdDpkaW5nZ28="})
    return urllib2.urlopen(req).read()
post_param={"level_id":500,"source_id":12,"ip":"10.4.1.1","title":"RROR LOG","message":"you are a boy 11111111111","type_id":7}
appjson=getresponse(post_param)
print appjson