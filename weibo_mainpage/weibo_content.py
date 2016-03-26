#usr/bin/env Python27
# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888'
}
headers = {
    'Accept-Encoding': 'gzip,deflate',
    'X-Log-Uid': '5846206381',
    'User-Agent': 'TianTian_4.3_weibo_6.3.0_android',
    'Host': 'api.weibo.cn',
    'Connection': 'Keep-Alive',
}

url_model = """http://api.weibo.cn/2/cardlist?fid=230283%(weibo_id)s_-_INFO&uid=5846206381&lfid=230283%(weibo_id)s&count=20&aid=01AjFe6l5UwowPQ9_QUMbdQVozNKmM-llyAE2S29sY0lRKVIw.&from=1063095010&networktype=wifi&lang=zh_CN&lcardid=more_web&skin=default&sflag=1&gsid=_2A257467vDeRxGeNG71QT8CjPwz2IHXVWuKUnrDV6PUJbrdANLVLukWpLHet5hWfyoF3b-gdt298P7JJWDc4mVQ..&page=1&need_head_cards=1&containerid=230283%(weibo_id)s_-_INFO&oldwm=4209_8001&v_p=27&v_f=2&c=android&wm=4209_8001&luicode=10000198&i=b1727db&s=1ff725e3&ua=TiantianVM-TianTian__weibo__6.3.0__android__android4.3&uicode=10000011&imsi=310260209279797"""
import requests
from rabbit.rabbit import CsvManager
import json
import time
import glob
weibo_id_list = json.load(open('weibo-id.json'))


def weibo_content(weibo_id_list):
    pass_id = open('success.log').read()
    error_log = open('error.log', 'ab')
    success_log = open('success.log', 'ab')
    for weibo_id in weibo_id_list:
        weibo_id = str(weibo_id)
        if weibo_id in pass_id:
            continue
        print weibo_id,
        url = url_model % {'weibo_id': weibo_id}
        resp = requests.get(url,
                            headers=headers,
                            verify=False)
                            #proxies=proxies)
        if resp.status_code == 200:
            json.dump(resp.json(), open('./output/%s.json' % weibo_id, 'wb'))
            print 'ok'
            success_log.write(weibo_id)
            success_log.write('\n')
        else:
            print 'error'
            error_log.write(weibo_id)
            error_log.write('\n')
        time.sleep(2)

if __name__ == '__main__':
    weibo_content(weibo_id_list)
