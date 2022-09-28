# ----------------1.先提取一列实体名保存,放到data\lookup下 pip install pandas
# import numpy as np
import pandas as pd

data = pd.read_csv('newmovie_v3.csv')

data['title'].to_csv('newmovie_v4.csv',header=0,index=0)
# 然后直接改后缀

# 另外两个文件也一样，我是直接命令行里运行的就没整个记录下来


# ----------------2.jieba生成权重，词性 pip install jieba   X 
# 不晓得咋整的，直接依葫芦画瓢，直接在后加
data = pd.read_csv('person.csv')
tmp = data['name']+' 15 nr'
tmp.to_csv('person_v3.csv',index=0,header=0)

