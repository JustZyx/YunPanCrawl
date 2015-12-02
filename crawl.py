#coding:utf-8
import requests
import json
import logging
# logging.info()
# logging.warning()
# logging.error()

def get_page(url):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'BAIDUID=077C3BF0EFEDD5A18FFB4CD2B1629F30:FG=1; BIDUPSID=077C3BF0EFEDD5A18FFB4CD2B1629F30; PSTM=1448335682; PANWEB=1; Hm_lvt_a3139a1feb7fec092cafd367407ee051=1448348249,1448358047; BDUSS=9nYTVpLWRvdmdzNW1PbHotcnlqcUNwY0tMVUxobmpaSHU3eVFZZDR3R0otbjFXQVFBQUFBJCQAAAAAAAAAAAEAAACCEEMzuvrL-crK1q4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIltVlaJbVZWLW; bdshare_firstime=1448505600823; Hm_lvt_773fea2ac036979ebb5fcc768d8beb67=1448349344,1448504731,1448610324,1448778276; Hm_lvt_adf736c22cd6bcc36a1d27e5af30949e=1448349344,1448504731,1448610324,1448778276; Hm_lvt_1d15eaebea50a900b7ddf4fa8d05c8a0=1448775564,1448778182,1448778369,1448877813; Hm_lvt_f5f83a6d8b15775a02760dc5f490bc47=1448775564,1448778182,1448778369,1448877813; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1438_18155_12824_17971_17000_17072_15278_11779_18016_10633; PANPSC=11973760722451719680%3AmTP0WM%2Fa3KxzFjuFTmEy0bHQG6qeixv0HlHmLmMG4yNwKQucHOr0TvXV3pnfkFSxMMKOMtLkW72H5d5WUzKdJPtiKu6MCKJHsg0gWUDJHkjXG9GmBZpeFc0jB6D5VoTsv2Arrvb%2BpkRqk%2B%2BTPuaY%2B73NUJmmAWZJC6RVR%2FKVa4UeUeYuYwbjI3ApC5wc6vRO9dXemd%2BQVLHw99dx76zmRJBLNayaNvQBTT2A%2BQxzQmp9tn9thbnTphh5muSlKgbe',
    'Host':'yun.baidu.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
}
    req = requests.get(url, headers=headers)
    html = req.text.strip()
    if html == "":
        logging.error('无输出')
    else:
        return html

def get_resource(uk):
    url = 'http://yun.baidu.com/pcloud/feed/getsharelist?category=0&auth_type=1&request_location=share_home&start=0&limit=60&query_uk='+uk+'&channel=chunlei&clienttype=0&web=1&bdstoken=fdfeb052c2788652319a33fd95cc10af'
    response_dict = json.loads(get_page(url))
    if response_dict['errno'] == 0:
        resource_list = response_dict['records']
        if len(resource_list) != 0: #如果该用户有分享资源
            resource_dict = {}
            for resource in resource_list:
                if(resource['feed_type'] == "share"):
                    resource_dict[resource['title']] = 'http://yun.baidu.com/share/link?uk='+str(resource['uk'])+'&shareid='+str(resource['shareid'])
                elif(resource['feed_type'] == 'album'):
                    resource_dict[resource['title']] = 'http://yun.baidu.com/pcloud/album/info?uk='+str(resource['uk'])+'&album_id='+str(resource['album_id'])
                else:
                    pass
            return resource_dict
        else:
            return {}
    else:
        logging.error('请求错误')
        print uk
    return {}

def follow(uk):
    url='http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk='+str(uk)+'&limit=24&start=0&bdstoken=fdfeb052c2788652319a33fd95cc10af&channel=chunlei&clienttype=0&web=1'
    follow_list = json.loads(get_page(url))['follow_list']
    if len(follow_list) != 0:
        follow_uk_list = []
        for follow in follow_list:
            follow_uk_list.append(follow['follow_uk'])
        return follow_uk_list
    else:
        return []

def fans(uk):
    url = 'http://yun.baidu.com/pcloud/friend/getfanslist?query_uk='+str(uk)+'&limit=24&start=0&bdstoken=fdfeb052c2788652319a33fd95cc10af&channel=chunlei&clienttype=0&web=1'
    html_dict = json.loads(get_page(url))
    fan_list = []
    fan_list = html_dict["fans_list"]
    # print fan_list
    if len(fan_list) != 0:
        fans_uk_list = []
        for fan in fan_list:
            fans_uk_list.append(fan['fans_uk'])
        return fans_uk_list
    else:
        return []

def eleminate(uk):
    fans_uk_list = fans(uk)
    follow_uk_list = follow(uk)
    set_uk = set(fans_uk_list)
    for follow_uk in follow_uk_list:
        set_uk.add(follow_uk)
    eleminate_list = []
    for uk in set_uk:
        eleminate_list.append(uk)
    return eleminate_list

def printResult(uk):
    uks = eleminate(uk);
    for uk in uks:
        uk = str(uk)
        resources_dict = get_resource(uk)
        if len(resources_dict) != 0:
            for d,x in resources_dict.items():
                print d, ':'+x
        else:
            # print "该用户暂未分享"
            logging.error('资源列表为空')
    for uk in uks:
        printResult(uk)

if __name__ == '__main__':
    # url = 'http://yun.baidu.com/pcloud/feed/getdynamiclist?auth_type=1&filter_types=11000&query_uk=272092316&category=0&limit=50&start=0&bdstoken=f009ae8b79e66ad60ef0860ac925ddc9&channel=chunlei&clienttype=0&web=1'
    # html = get_page(url)
    uk = '272092316' #开始个人uk
    # resources = get_resource(uk)
    # for k,v in resources.items():
    #     print k, ':'+v
    printResult(uk)
    # s = eleminate(uk)
    # for i in s:
    #     print i
    # follow(uk)
    # print get_resource(uk)