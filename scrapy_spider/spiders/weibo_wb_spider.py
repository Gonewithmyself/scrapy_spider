#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : huangtao
# * Create time   : 2018/4/17 下午1:22
# * Last modified : 2018/4/17 下午1:22
# * Filename      : weibo_wb_spider.py
# * Description   : 微博某人发布的微博信息
# **********************************************************

import datetime
import scrapy
from scrapy.http import Request
from scrapy_spider.items import WeiboWBItem
from scrapy_spider.spiders.util import *
import json


class WeiBoWBSpider(scrapy.Spider):
    name = 'weibo_wb_spider'
    allowed_domains = ['weibo.com']
    url_head = 'https://m.weibo.cn/api/container/getIndex?containerid='

    def __init__(self, *args, **kwargs):
        super(WeiBoWBSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://m.weibo.cn/u/1855152373']

    # 把网页URL转化为接口URL
    def start_requests(self):
        for start_url in self.start_urls:
            if 'https://m.weibo.cn/p/' in start_url:
                containerid = '107603' + start_url.replace('https://m.weibo.cn/p/', '')[6:]
            elif 'https://m.weibo.cn/u/' in start_url:
                containerid = '107603' + start_url.replace('https://m.weibo.cn/u/', '')
            if containerid:
                origin_url = '%s%s' % (self.url_head, containerid)

            yield Request(origin_url, callback=self.parse)

    def parse(self, response):
        content = json.loads(response.body)
        weibo_info = content.get('cards', []) or content.get('data').get('cards')
        weibo_wb_item = WeiboWBItem()
        tsksParser = innerHtml()
        print(len(weibo_info))
        for info in weibo_info:
            if info.get('card_type') != 9:
                continue
            mlog = info.get('mblog')
            
            # ignore zhiding msg
            if mlog is None or mlog.get('title') is not None:
                continue
            txt = mlog.get('text')
            weibo_wb_item['content'] =  tsksParser.extract_info(txt)
            yield  weibo_wb_item

def _extract_info(src, pstr):
    patt = re.compile(pstr)
    # space = re.compile(r'<br />')
    m = re.sub(patt, '', src)
    return m

def on_match_at(txt):
    return txt

def on_match_sharp(txt):
    # print("ddddddddddddddddddd")
    # print ("match #...", txt)
    m = re.search(r'(>[\s\S]*?<)', txt).group(1)
    m = m.lstrip(">").rstrip('<')
    return m

def on_match_url(txt):
    return re.search(r'"([\s\S]*?)"', txt).group(1)

CH = r'\s\S'
class innerHtml(object):
    handlers = {
        'do @':[r'(@[\s\S]*?</a>)', on_match_at],    
        'do #':[r'(<span class="surl-text">[\s\S]*?</span>)', on_match_sharp],
        'do url':[r'(data-url="[\s\S]+?")', on_match_url],
    }
    trns = {
        ' &amp; ':'&',
        '</a>':'',
        '<br />':'\n',
    }   
    pstr = r'(<a[\s\S]*?>[\s\S]+?</a>)|(<br />)'
    patt = re.compile(pstr)

    def __init__(self):
        map(self._compile, self.handlers.keys())
    
    def _compile(self, key):
        pstr = self.handlers[key][0]
        self.handlers[key][0] = re.compile(pstr)
    
    def extract_inner_html(self, mobj):
        txt = mobj.group(0)
        ret = ''
        for v in self.handlers.values():
            m = re.search(v[0], txt)
            if m and m.group(1):
                ret = v[1](m.group(1))
        return ret

 
    def extract_info(self, text):
        m = re.sub(self.patt, self.extract_inner_html, text)
        for key, tn in self.trns.items():
            m = m.replace(key, tn)
        
        m = m.replace("&amp;", "&")
        m.strip(" ")
        return m 
        

# def handle_inner_html(html):
#     pstr = r'(<a[\s\S]*?>[\s\S]+?</a>)|(<br />)'
#     patt = re.compile(pstr)
#     # space = re.compile(r'<br />')
#     m = re.sub(patt, '', html)

    

#     for v in handlers.values:

#     # print ("ex ... ", m)
#     return m


        #     weibo_wb_item['title'] = clearHtml(txt)
        #     print(txt, weibo_wb_item['title'])
        # # for info in weibo_info:
        #     if info.get('card_type') == 9:
        #         #=======发布时间
        #         now = datetime.datetime.now()
        #         if '刚刚' in info.get('mblog').get('created_at'):
        #             info_time = now
        #         elif '分钟' in info.get('mblog').get('created_at'):
        #             time_str = -int(info.get('mblog').get('created_at').replace("分钟前", ''))
        #             info_time = now + datetime.timedelta(minutes=time_str)
        #         elif '小时' in info.get('mblog').get('created_at'):
        #             time_str = -int(info.get('mblog').get('created_at').replace("小时前", ''))
        #             info_time = now + datetime.timedelta(hours=time_str)
        #         elif '昨天' in info.get('mblog').get('created_at'):
        #             time_str = info.get('mblog').get('created_at').split(' ')[1]
        #             date_str = "%s" % ((now + datetime.timedelta(-1)).date())
        #             time_str = "%s %s:00" % (date_str, time_str)
        #             info_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        #         elif '前天' in info.get('mblog').get('created_at'):
        #             time_str = info.get('mblog').get('created_at').split(' ')[1]
        #             date_str = "%s" % ((now + datetime.timedelta(-2)).date())
        #             time_str = "%s %s:00" % (date_str, time_str)
        #             info_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        #         else:
        #             time_str = info.get('mblog').get('created_at')
        #             if len(time_str.split('-')) == 2:
        #                 year = now.year
        #                 info_time = "%s-%s 00:00:00" % (year, time_str)
        #                 info_time = datetime.datetime.strptime(info_time, "%Y-%m-%d %H:%M:%S")
        #             else:
        #                 info_time = "%s 00:00:00" % (time_str)
        #                 info_time = datetime.datetime.strptime(info_time, "%Y-%m-%d %H:%M:%S")

        #         # =======如果是转发别人的微博
        #         pics = ''
        #         if info.get('mblog').get('retweeted_status'):
        #             is_original = 0
        #             title_1 = info.get('mblog').get('raw_text')
        #             title_2 = clearHtml(info.get('mblog').get('retweeted_status').get('text'))
        #             title = title_1 + '<WRAP>' + title_2
        #             is_have_video = 1 if info.get('mblog').get('retweeted_status').get('page_info') and info.get(
        #                 'mblog').get('retweeted_status').get('page_info').get('type') == 'video' else 0
        #             if is_have_video:
        #                 pics = info.get('mblog').get('retweeted_status').get('page_info').get('page_pic').get('url', '')
        #             else:
        #                 if info.get('mblog').get('retweeted_status').get('pics'):
        #                     pics = ','.join(
        #                         map(lambda x: x.get('url'), info.get('mblog').get('retweeted_status').get('pics')))
        #                 elif info.get('mblog').get('retweeted_status').get('page_info') and info.get('mblog').get(
        #                         'retweeted_status').get('page_info').get('type') == 'article':
        #                     pics = info.get('mblog').get('retweeted_status').get('page_info').get('page_pic').get(
        #                         'url') if info.get('mblog').get('retweeted_status').get('page_info').get(
        #                         'page_pic') else ''
        #         else:
        #             title = clearHtml(info.get('mblog').get('text'))
        #             is_original = 1
        #             if info.get('mblog').get('page_info') and info.get('mblog').get('page_info').get('type') == 'video':
        #                 is_have_video = 1
        #                 pics = info.get('mblog').get('page_info').get('page_pic').get('url', '')
        #             else:
        #                 is_have_video = 0
        #                 if info.get('mblog').get('pics'):
        #                     pics = ','.join(map(lambda x: x.get('url'), info.get('mblog').get('pics')))
        #                 elif info.get('mblog').get('page_info') and info.get('mblog').get('page_info').get(
        #                         'type') == 'article':
        #                     pics = info.get('mblog').get('page_info').get('page_pic').get('url') if info.get(
        #                         'mblog').get('page_info').get('page_pic') else ''
        #                 else:
        #                     pics = ''

        #         weibo_wb_item['isOriginal'] = is_original
        #         weibo_wb_item['isHaveVideo'] = is_have_video
        #         weibo_wb_item['isHavePicture'] = 1 if pics else 0
        #         weibo_wb_item['pictureUrls'] = pics
        #         weibo_wb_item['title'] = clearHtml(title)
        #         weibo_wb_item['url'] = "https://m.weibo.cn/status/%s" % info["mblog"]["mid"]
        #         weibo_wb_item['publishTime'] = info_time

        #         print ('======微博内容======')
        #         print (weibo_wb_item['isOriginal'])
        #         print (weibo_wb_item['isHaveVideo'])
        #         print (weibo_wb_item['isHavePicture'])
        #         print (weibo_wb_item['pictureUrls'])
        #         print (weibo_wb_item['title'])
        #         print (weibo_wb_item['url'])
        #         print (weibo_wb_item['publishTime'])
        #         yield weibo_wb_item

