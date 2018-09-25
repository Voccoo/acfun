# -*- coding: utf-8 -*-
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Line
from pyecharts import Geo
import urllib.request
import urllib.parse
import json
import pymysql


# 获取指定区间内男女比例
def create_gender_round():
    sql = "select gender,count(*) from user_info group by gender "
    datas = get_all_data(sql)
    info_name = ['隐藏', '男性', '女性', 'Acer']
    man = 0
    women = 0
    Xman = 0
    acer = 0
    for i in datas:
        if i[0] == -1:
            Xman = i[1]
        elif i[0] == 1:
            man = i[1]
        elif i[0] == 0:
            women = i[1]
        elif i[0] == 2:
            acer = i[1]
    pie = Pie('男女用户比例')
    pie.add('性别比例图', info_name, [Xman, man, women, acer], radius=None, center=None, rosetype='')
    # rosetype 是否展示成南丁格尔图，通过半径区分数据大小，有
    # 'radius'和'area'两种模式。默认为
    # 'radius'
    # radius：扇区圆心角展现数据的百分比，半径展现数据的大小
    # area：所有扇区圆心角相同，仅通过半径展现数据大小
    # pie.render('detail\性别比例图.html')
    pie.render('detail\比例图.png')


# 每年注册人数
def create_bar_year():
    sql = "select regtime from user_info order by regtime"
    data = get_all_data(sql)
    yera = {}
    for i in data:
        y = i[0][0:4]
        if y in yera:
            count = yera.get(y)
            count += 1
            yera[y] = count
        else:
            yera[y] = 0

    bar = Bar("每年注册人数", "按年划分")
    bar.add("", list(yera.keys()), list(yera.values()))
    # 生成折线图
    create_lin('每年注册人数', list(yera.keys()), list(yera.values()), '每年注册人数')
    bar.render(path='detail\注册人数划分_年.html')


# 每个月注册人数
def create_bar_month():
    sql = "select regtime from user_info order by regtime"
    data = get_all_data(sql)
    months = {'01': 0,
              '02': 0,
              '03': 0,
              '04': 0,
              '05': 0,
              '06': 0,
              '07': 0,
              '08': 0,
              '09': 0,
              '10': 0,
              '11': 0,
              '12': 0,
              }
    for i in data:
        regTime = i[0][5:7]
        count = months.get(regTime)
        count += 1
        months[regTime] = count
    create_lin('每个月注册人数', list(months.keys()), list(months.values()), '')
    bar = Bar("每个月注册人数", "按月划分")
    bar.add("", list(months.keys()), list(months.values()))
    #生成折线图
    create_lin('注册人数划分_月',list(months.keys()),list(months.values()),'注册人数划分_月')
    bar.render(path='detail\注册人数划分_月.html')  # 生成本地 HTML 文件


# 根据sql获取指定区间内的数据
def get_all_data(sql):
    conn = pymysql.connect(host="localhost", user="root", passwd="Cs123456.", db="acfun", charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# 注册人数与当年活跃人数对比图
def year_2():
    sql = "select regtime,lastLoginTime from user_info order by regtime"
    data = get_all_data(sql)
    yera = {}
    for i in data:
        y = i[0][0:4]
        y2 = str(i[1])[0:4]
        if y in yera:
            count = yera.get(y)[0]
            count += 1
            yera[y][0] = count

            if y2 in yera:
                count_2 = yera.get(y2)[1]
                count_2 += 1
                yera[y2][1] = count_2

            else:
                yera[y2] = [0, 0]

        else:
            yera[y] = [0, 0]

    bar = Bar("年注册人数与每年最后一次上线人数", "按年划分")
    bar.add("", [k for k in sorted(yera.keys())], [yera[k][0] for k in sorted(yera.keys())])
    bar.add("", [k for k in sorted(yera.keys())], [yera[k][1] for k in sorted(yera.keys())])

    bar.render(path='detail\每年注册人数与每年最后一次上线人数.html')


# 折线图,若想显示两条或多条，自己处理下，就是多加个add的事情
def create_lin(h_name, k, val, line_name):
    line = Line(h_name)
    line.add(line_name, k, val, mark_point=["average"])
    line.render('detail\%s_折线图.html' % h_name)



def geo_formatter(params):
    return params.name + ' : ' + params.value[2]


# map图，指定区间内，全国省用户分布图
def Geo_create():
    sql = "select comeFrom,count(*) from user_info where 1=1 and comeFrom is not NULL and comeFrom !='未知' and comeFrom !='' and lastLoginTime >= '2018-01-01 00:00:00' group by comeFrom order by comeFrom"
    datas = get_all_data(sql)

    city = {}
    country = {}
    for data in datas:

        b = data[0].find(',')
        s = data[0].encode('utf-8').decode('utf-8').find('市')
        sheng = data[0].encode('utf-8').decode('utf-8').find('省')
        zzq = data[0].encode('utf-8').decode('utf-8').find('自治区')
        if b is not -1:
            res, count = get_city_name(data, b, city)
            # print('b',data[0], '---', res, '-----', count, '----', sheng)
            if res in city:
                count = city[res]
                count += data[1]
                # print(res, '---', count)
                city[res] = count
            else:
                city[res] = data[1]
        elif zzq is not -1:
            res, count = get_city_name(data, zzq, city)
            # print('zzq',data[0], '---', res, '-----', count, '----', sheng)
            if res in city:
                count = city[res]
                count += data[1]
                # print(res, '---', count)
                city[res] = count
            else:
                city[res] = data[1]
        elif sheng is not -1:
            res, count = get_city_name(data, sheng, city)
            # print('sheng',data[0], '---', res, '-----', count, '----', sheng)
            if res in city:
                count = city[res]
                count += data[1]
                # print(res, '---', count)
                city[res] = count
            else:
                city[res] = data[1]
        elif s is not -1:
            res, count = get_city_name(data, b, city)
            # print('s',data[0], '---', res, '-----', count, '----', sheng)
            if res in city:
                count = city[res]
                count += data[1]
                # print(res, '---', count)
                city[res] = count
            else:
                city[res] = data[1]
        else:
            # print(data[0],'------',data[1])
            if data[0] in country:
                count = country[data[0]]
                count += data[1]
            else:
                country[data[0]] = data[1]

    del city['海外']
    del country['AFRINIC']
    del country['APNIC']
    del country['RIPE']
    del country['IANA']
    del country['运营商级NAT']
    country['中国'] = 0
    for i in city:
        country['中国'] += city[i]
    f_country = {}
    for i in list(country.keys()):
        f_country[fanyi(i)] = country.pop(i)
    # print(city)
    print(f_country)
    create_geo('2018截止8月全国Acer省分布情况', '', city, 'detail/2018截止8月全国Acer省分布情况.html', 'china')
    # create_geo('2018截止8月全世界Acer省分布情况', '', f_country, 'detail/2018截止8月世界Acer省分布情况.html', 'world')


def fanyi(content):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=http://fanyi.youdao.com/'
    # 有道翻译查询入口
    data = {  # 表单数据
        'i': content,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
        'typoResult': 'false'
    }

    data = urllib.parse.urlencode(data).encode('utf-8')
    # 对POST数据进行编码

    response = urllib.request.urlopen(url, data)
    # 发出POST请求并获取HTTP响应

    html = response.read().decode('utf-8')
    # 获取网页内容，并进行解码解码

    target = json.loads(html)
    # json解析

    return target['translateResult'][0][0]['tgt']


def create_geo(pname, cname, data, path, map_type):
    # geo = Geo(pname, cname, title_color="#fff", title_pos="center", width=1200, height=600,
    #           background_color="#404a59", )
    # attr, value = geo.cast(data)
    # geo.add("", attr, value, type="heatmap", is_random=True, is_legend_show=False,
    #         maptype=map_type,
    #         tooltip_formatter=geo_formatter,  # 重点在这里，将函数直接传递为参数。
    #         effect_scale=5)
    #
    geo = Geo(
        pname,
        cname,
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color="#404a59",
    )
    attr, value = geo.cast(data)
    geo.add(
        "",
        attr,
        value,
        type="heatmap",
        maptype=map_type,
        is_visualmap=True,
        visual_range=[0, 300],
        visual_text_color="#fff",
    )

    geo.render(path=path)


def get_city_name(data, n_len, city_list):
    res = data[0][0:n_len]
    count = 0
    if res in city_list:
        count = city_list[res]
        count += data[1]
    else:
        count = data[1]

    return res, count


if __name__ == '__main__':
    #create_gender_round()
    #create_bar_month()
    #create_bar_year()
    #year_2()
    Geo_create()
