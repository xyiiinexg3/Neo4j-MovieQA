import numpy as np
import pandas as pd

#读取数据，将空值形式的缺失值转换为可识别的类型
# data = pd.read_csv('movie.csv',encoding='GBK')
data = pd.read_csv('movie.csv')

#用NaN代替空值

# data = data.replace('',np.NaN)

# print(data.columns)
#['id','label','a','b','c','d']
#将每列的缺失值个数统计出来

# null_all = data.isnull().sum()
#isnull函数检查数据是否有缺失返回布尔值，元素为空或者NaN返回Ture，否则就是False

#data.isnull().any()判断哪些列包含缺失值，该列存在缺失值则返回True，反之False

#data.isnull().sum()返回每列缺失值的数量

#用一个字符串代替缺失值，
fill_data = data.fillna('missing')
fill_data.to_csv('newmovie.csv')