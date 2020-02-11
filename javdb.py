import re
from lxml import etree
import json
from ADC_function import *


# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)
def getTitle(a):
    try:
        html = etree.fromstring(a, etree.HTMLParser())
        result = str(html.xpath('/html/body/section/div/h2/strong/text()')).strip(" ['']")
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', '').replace(' : ', ''))
    except:
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', ''))


def getActor(a):  # //*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = html.xpath('//strong[contains(text(),"演員")]/../following-sibling::span/text()')
    result2 = html.xpath('//strong[contains(text(),"演員")]/../following-sibling::span/a/text()')
    return result1 + result2


def getActorPhoto(actor):  # //*[@id="star_qdt"]/li/a/img
    d = {}
    for i in actor:
        if ',' not in i or ')' in i:
            p = {i: ''}
            d.update(p)
    return d


def getStudio(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"片商")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"片商")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getRuntime(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"時長")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"時長")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').rstrip('mi')


def getLabel(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"系列")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"系列")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getNum(a):
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath('//strong[contains(text(),"番號")]/../following-sibling::span/text()')).strip(" ['']").replace('_', '-')
    result2 = str(html.xpath('//strong[contains(text(),"番號")]/../following-sibling::span/a/text()')).strip(" ['']").replace('_', '-')
    return str(result2 + result1).strip('+')


def getYear(getRelease):
    try:
        result = str(re.search('\d{4}', getRelease).group())
        return result
    except:
        return getRelease


def getRelease(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"時間")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"時間")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+')


def getTag(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"类别")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"类别")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace(",\\xa0", "").replace("'", "").replace(' ', '').replace(',,',
                                                                                                             '').lstrip(
        ',')


def getCover_small(a, count):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result = html.xpath("//div[@class='item-image fix-scale-cover']/img/@src")[count]
    if not 'https' in result:
        result = 'https:' + result
    return result


def getCover(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath("//div[@class='column column-video-cover']/a/img/@src")).strip(" ['']")
    return result


def getDirector(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"導演")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"導演")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getOutline(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//*[@id="introduction"]/dd/p[1]/text()')).strip(" ['']")
    return result


def main(number):
    try:
        a = get_html('https://javdb.com/search?q=' + number + '&f=all').replace(u'\xa0', u' ')
        html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        counts = len(html.xpath(
            '//div[@id=\'videos\']/div[@class=\'grid columns\']/div[@class=\'grid-item column\']'))
        if counts == 0:
            dic = {
                'title': '',
                'actor': '',
                'website': '',
            }
            js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
            return js
        count = 1
        number_get = ''
        movie_found = 0
        for count in range(1, counts + 1):  # 遍历搜索结果，找到需要的番号
            number_get = html.xpath(
                '//div[@id=\'videos\']/div[@class=\'grid columns\']/div[@class=\'grid-item column\'][' + str(
                    count) + ']/a[@class=\'box\']/div[@class=\'uid\']/text()')[0]
            number_get = number_get.replace('_', '-')
            if number_get == number.upper() or number_get == number.lower():
                movie_found = 1
                break
        result1 = html.xpath('//*[@id="videos"]/div/div/a/@href')[count - 1]
        b = get_html('https://javdb.com' + result1).replace(u'\xa0', u' ')
        actor = getActor(b)
        if len(actor) == 0 and 'FC2-' in number_get:
            actor.append('FC2-NoActor')
        if movie_found == 1:
            dic = {
                'actor': str(actor).strip(" [',']").replace('\'', ''),
                'title': getTitle(b).replace("\\n", '').replace('_', '-').replace(number_get, '').strip().replace(' ', '-').replace('--', '-'),
                'studio': getStudio(b),
                'outline': getOutline(b).replace('\n', ''),
                'runtime': getRuntime(b),
                'director': getDirector(b),
                'release': getRelease(b),
                'number': number_get,
                'cover': getCover(b),
                'cover_small': getCover_small(a, count - 1),
                'imagecut': 3,
                'tag': getTag(b),
                'label': getLabel(b),
                'year': getYear(getRelease(b)),  # str(re.search('\d{4}',getRelease(a)).group()),
                'actor_photo': getActorPhoto(actor),
                'website': 'https://javdb.com' + result1,
                'source': 'javdb.py',
            }
        else:  # 未找到番号
            dic = {
                'title': '',
                'actor': str(actor).strip(" [',']").replace('\'', ''),
                'website': '',
            }
    except:
        if a == 'ProxyError':
            dic = {
                'title': '',
                'actor': '',
                'website': 'timeout',
            }
        else:
            dic = {
                'title': '',
                'actor': '',
                'website': '',
            }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


# print(main('ADZ-081'))
# input("[+][+]Press enter key exit, you can check the error messge before you exit.\n[+][+]按回车键结束，你可以在结束之前查看和错误信息。")
# print(main('abs-141'))
# print(main('040409-562'))
# print(main('n1403'))
