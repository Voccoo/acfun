import numpy as np
import pandas as pd
import jieba
import wordcloud
from scipy.misc import imread
import matplotlib.pyplot as plt
from pylab import mpl
import seaborn as sns
from PIL import Image
import pymysql

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus']


def txt_cut(novel, stop_list):
    return [w for w in jieba.cut(novel) if w not in stop_list and len(w) > 1]


def Statistics(txtcut,save_path):
    # Series是指pandas的一维，获取txtcut中按照降序排列后0~20的数据
    word_count = pd.Series(txtcut).value_counts().sort_values(ascending=False)[0:20]
    # print(word_count)
    # 是以这种形式展现的数据，

    # 创建一个图形是咧 大小是15*8（长*宽）单位是英寸
    plt.figure(figsize=(15, 8))
    x = word_count.index.tolist()  # 获取的是index列，转换成list
    y = word_count.values.tolist()  # 获取的是values列，转换成list
    # barplot是作图方法，传入xy值，palette="BuPu_r" 设置的是柱状图的颜色样式
    # BuPu_r 从左到右，颜色由深到浅，BuPu与之相反
    sns.barplot(x, y, palette="BuPu_r")
    plt.title('词频Top20')  # 标题
    plt.ylabel('count')  # Y轴标题
    # 如果不加这局，那么出现的就是个四方的框，这个是用来溢出轴脊柱的，加上bottom=tur，意思就是连下方的轴脊柱也溢出
    sns.despine(bottom=True)
    # 图片保存
    plt.savefig(save_path, dpi=400)
    plt.show()


def cloud(result, img_path, cloud_path, cloud_name):
    result = " ".join(result)  # 必须给个符号分隔开分词结果,否则不能绘制词云
    # 1、初始化自定义背景图片
    image = Image.open(img_path)
    graph = np.array(image)

    # 2、产生词云图
    # 有自定义背景图：生成词云图由自定义背景图像素大小决定
    wc = wordcloud.WordCloud(font_path=r"I:\word-ttf\XingKai.ttf",  # 字体地址
                             background_color='white',  # 背景色
                             max_font_size=100,  # 显示字体最大值
                             max_words=100,  # 最大词数
                             mask=graph)  # 导入的图片
    wc.generate(result)

    # 3、绘制文字的颜色以背景图颜色为参考
    image_color = wordcloud.ImageColorGenerator(graph)  # 从背景图片生成颜色值
    wc.recolor(color_func=image_color)
    wc.to_file(cloud_path)  # 按照背景图大小保存绘制好的词云图，比下面程序显示更清晰

    # 4、显示图片
    plt.title(cloud_name)  # 指定所绘图名称
    plt.imshow(wc)  # 以图片的形式显示词云
    plt.axis("off")  # 关闭图像坐标系
    plt.show()

#链接数据库，获取存入的数据
def open_db():
    conn = pymysql.connect(host="localhost", user="root", passwd="Cs123456.", db="acfun", charset="utf8")
    cursor = conn.cursor()
    sql = "select * from user_info where 1=1 and tan !='这个人很懒，什么都没有写...' and tan !='' and tan !='才、才不是懒得写签名呢！只是在思考'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

#对数据处理，获取想要的数据，我这里的list[3]就是查询出的数据获取的
def data_process(data):
    comment_ob = ''
    if data is not None:
        for list in data:
            comment_ob += list[6] + ','
        return comment_ob


def stop_list(stop_path):
    stopwords_path = stop_path
    stop_list = []
    stop_list1 = open(stopwords_path, encoding="utf-8").readlines()
    for line in stop_list1:
        stop_list.append(line.strip('\n').strip())
    return stop_list


if __name__ == '__main__':
    #停词地址
    stop_path = 'I:/鬼吹灯小说分析/stop_word2.txt'
    stop_list = stop_list(stop_path)
    #词云背景图地址
    img_path = "I:/Acfun/ac_bg3.jpg"
    #词云图保存地址
    cloud_path = 'C:/Users/Administrator/Desktop/ac3.jpg'
    #柱状图保存地址
    stat_path = 'C:/Users/Administrator/Desktop/dzd6_stat.jpg'
    #词云名称
    cloud_name = 'A站用户常用个签频词'
    data = open_db()
    ob = data_process(data)
    jb_comment = txt_cut(ob, stop_list)
    #Statistics(jb_comment,stat_path)
    cloud(jb_comment, img_path, cloud_path, cloud_name)