from flask import Flask,render_template,redirect, url_for, request,session
import pymysql
from collections import Counter
import json
import wordcloud as wc
from wordcloud import  ImageColorGenerator
from PIL import Image
import numpy as np


app = Flask(__name__)

conn = pymysql.connect(host="localhost", user="root", password="zch001004", db="lindashixi", charset="utf8")
cur = conn.cursor()
bidsubnums={}

@app.route("/")
def index():
    words=worddb()
    return render_template("/index.html",listwords=words)


# 提取t_avdata表数据
def worddb():
    arraywords=[]
    strwords=""
    sql = "select typeId,keywords from t_avdata1"
    cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        arraywords.append({"tid":item[0],"keywords":item[1]})
        strwords+=item[1]+" "
    conn.commit()

    # 生成词云图
    mask = np.array(Image.open("c.png"))
    graph = np.array(mask)
    # 设置背景形状图片
    # mask = np.array(Image.open("fivestar.png"))

    # 画图
    word_cloud = wc.WordCloud(font_path="/System/Library/Fonts/STHeiti Light.ttc", mask=graph, background_color='white')  # 字体、背景形状
    word_cloud.generate(strwords)
    image_color = ImageColorGenerator(graph)  # 生成词云的颜色
    word_cloud.to_file("./static/a2.png")  # 绘制到一个图片里

    return arraywords

@app.route("/search",methods=['GET','POST'])
def backlogin():
    arraybid=[]
    bidsub = []
    if(request.method=="GET"):
        gword=request.args.get("gword")
        print("gword:",gword)
        # sql="select t_bid.id,t_bid.bkid,t_bid.classtype,t_avdata.keywords from t_bid  right join t_avdata on t_bid.classtype=t_avdata.type WHERE t_avdata.keywords='%s'"%(gword)
        sql = "select * from t_avdata1 where keywords='%s'"%(gword)
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            bidsub.append(item[2])
            arraybid.append({"userid": item[0], "keywords": item[1], "type": item[2]})
            conn.commit()
        print(item)
        # cur.close()
        # conn.close()
    #     统计数组成员重复个数
    global bidsubnums
    bidsubnums = dict(Counter(bidsub))
    return render_template("/index.html",arraybid=arraybid)








# 搜索图表
@app.route("/ajaxdata",methods=['GET','POST'])
def ajaxdata():
    temparray=[]
    for k, v in bidsubnums.items():
        temparray.append({"value":v,"name":k})
    return json.dumps(temparray)



if __name__ == '__main__':
   app.run(debug = True)


