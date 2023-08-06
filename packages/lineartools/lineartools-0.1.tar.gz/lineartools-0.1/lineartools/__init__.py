import sys

self_names = []
















































tezhengzhitezhengxiangliang = '''
import numpy as np
a = input().split(" ")
if len(a) != 25:
    print("输入有错!")
else:
    try:
        a = [int(i) for i in a]
        a = [a[i:i + 5] for i in range(0, len(a), 5)]
    except:
        print("输入有错!")
    eig_vals, eig_vectors = np.linalg.eig(a)
    print(eig_vals, '\\n', eig_vectors)
'''



shouruzhichujuzhen = '''
import numpy as np
s1 = input()
s2 = input()
n = []
num = [float(n) for n in s1.split()]
for i in range(0, len(num), 31):
    x = num[i:i+31]
    n.append(x)
n = np.matrix(n)
nn = np.corrcoef(n)
print(nn)
'''



pisajiage = '''
import numpy as np
from sklearn.linear_model import LinearRegression
a = input()
b = input()
c = input()
X1 = list(map(int, a.split(' ')))
y1 = list(map(float, b.split(' ')))
n = int(c)
X = np.mat(X1).reshape(5, 1)
y = np.mat(y1).reshape(5, 1)
model = LinearRegression()
model.fit(X, y)
print("Predict 12 inch cost:$%.2f" % model.predict([[n]]), end="")
'''



fenleipanbie = '''
from numpy import *
import numpy as np
import math
x1 = array([float(i) for i in input().split(',')])
y1 = array([float(i) for i in input().split(',')])
w1 = mat(vstack((x1,y1)))
x2 = array([float(i) for i in input().split(',')])
y2 = array([float(i) for i in input().split(',')])
w2 = mat(vstack((x2, y2)))
mean1 = np.mean(w1, 1)
mean2 = np.mean(w2, 1)
dimens1, nums1 = w1.shape[:2]
samples_mean1 = w1 - mean1
s_in1 = 0
for i in range(nums1):
    x = samples_mean1[:, i]
    s_in1 += dot(x, x.T)
dimens2, nums2 = w2.shape[:2]
samples_mean2 = w2 - mean2
s_in2 = 0
for i in range(nums2):
    x = samples_mean2[:, i]
    s_in2 += dot(x, x.T)
s = s_in1 + s_in2
s_t = s.I
w = dot(s_t, mean1 - mean2)
w_new = w.T
m1_new = dot(w_new,mean1)
m2_new = dot(w_new,mean2)
pw1 = 0.6
pw2 = 0.4
w0 = m1_new*pw1+m2_new*pw2
0.23,1.52,0.65,0.77,1.05,1.19,0.29,0.25,0.66,0.56,0.90,0.13,-0.54,0.94,-0.21,0.05,-0.08,0.73,0.33,1.06,-0.02,0.11,0.
2.34,2.19,1.67,1.63,1.78,2.01,2.06,2.12,2.47,1.51,1.96,1.83,1.87,2.29,1.77,2.39,1.56,1.93,2.20,2.45,1.75,1.69,2.48,1
1.40,1.23,2.08,1.16,1.37,1.18,1.76,1.97,2.41,2.58,2.84,1.95,1.25,1.28,1.26,2.01,2.18,1.79,1.33,1.15,1.70,1.59,2.93,1
1.02,0.96,0.91,1.49,0.82,0.93,1.14,1.06,0.81,1.28,1.46,1.43,0.71,1.29,1.37,0.93,1.22,1.18,0.87,0.55,0.51,0.99,0.91,0
1,1.5
x = mat(array([float(i) for i in input().split(',')]).reshape(2,1))
y_i = w_new * x[:,0]
if y_i > w0:
    print('该点属于第一类')
else:
    print('该点属于第二类')
'''



kjuleizhongxin = '''
import numpy as np
from sklearn.cluster import KMeans
a = input()
b = input()
c = input()
t1 = np.array([float(i) for i in a.split(' ')])
t2, t3 = np.array([int(i) for i in b.split(' ')])
t4 = int(c)
n = np.array(t1).reshape(t2, t3)
kmeans = KMeans(n_clusters=t4)
kmeans.fit(n)
m = kmeans.labels_[0]
print("A公司所在类的中心为:{:.2f},{:.2f}。".format(kmeans.cluster_centers_[m, 0], kmeans.cluster_centers_[m,
1]))
'''


kafeidoujulei = '''
import numpy as np
from sklearn.cluster import AgglomerativeClustering
temp = np.array([float(i) for i in input().split(' ')])
n_samplesj, n_features = np.array([int(i) for i in input().split(' ')])
X =np.array(temp).reshape(n_samplesj, n_features)
n_clusters = int(input())
hc=AgglomerativeClustering(n_clusters = n_clusters, affinity = 'correlation', linkage = 'complete')
hc.fit(X.T)
hcl=hc.labels_
if hcl[0]==hcl[2]:
    print("香气和酸质属于一类。")
else:
    print("香气和酸质不属于一类。")
'''

gongxianlvzuida = '''
import numpy as np
a=input()
b=input()
b1=np.array([int (i) for i in b.split(',')])
num=np.array([float(i) for i in a.split(',')]).reshape(b1[0],b1[1])
# 均值标准化
x=(num-np.mean(num))/np.std(num)
x1=np.cov(x.T)
# 特征值、特征向量
u,v=np.linalg.eig(x1)
# 比较特征值,得出最大的特征值
if u[0]>u[1]:
    index=0
else:
    index=1
print(' 第 1 主成分 ={:.5f}*(x1-{:.2f}){:+.5f}*(x2-{:.2f})'.format(v[0][index], np.mean(num, axis=0)[0], v[1][index], np.mean(num, axis=0)[1]))
'''


tiankong = '''
Numpy中创建全为0的矩阵使用 zeros
pandas中， read_csv 用来读取csv文件
多元分析研究的是 多指标问题的统计总体。
协方差和相关系数仅仅是变量间 离散程度 的一种度量，并不能刻画变量间可能存在的 关联程度关系
设随机向量X=(x1，x2, x3, x4)'的相关阵R为 则x1和x3的相关系数为 -0.5
设a=(2,-4,1)'，b=(4,1,-4)'，则a和b的夹角为 90
若A为4阶非退化矩阵，若2为矩阵A的一个特征值，对应的特征向量为（1，0，3，4），则A逆矩阵的一个特征值为 0.5
对 应特征向)量为（ 1，0，3，4)
设矩阵A的秩为2，则λ= 1
设X=(X_1,X_2,…,X_p)'有为p个分量，μ为X的均值向量，则μ是 p
几何平面上的点p=(x1,x2)到原点O=(0,0)的欧氏距离是 (x1^2+x2^2)^(1⁄2)
设X、Y从均值向量为μ，协方差阵为∑的总体G中抽取的两个样品，定义X、Y两点之间的马氏距离为 (X-Y)’Σ^(-1) (X-Y)
如果正态随机向量X的协方差阵∑是对角阵，则X的各分量是 相互独立
在实际问题中,通常可以假定被研究的对象是 多元正态分布
数理统计中常用的抽样分布卡方分布，在多元统计中,与之对应的分布为 Wishart分布
多元统计研究的是多指标问题,为了了解总体的特征,通过对总体抽样得到代表总体的样本但因为信息是分散在每个样本上的,就需要对样本进行加工,把样本的信息浓缩到不包含未知量的样本函数中,这个函数称为 统计量
S^2是样本方差
x上面一个横线是 样本均值 的计算公式。
Cov是 总体协方差 的计算公式
多元数据的协方差阵检验中，需分析当前的波动幅度与过去的波动情形有无显著差异，此时要检验的假设H0为 Σ=Σ_0
多元数据协方差阵检验中，需要了解这多个总体之间的波动幅度有无明显的差异，此时要检验的假设的备择假设H1为 Σ_i不全相等
多总体的均值向量检验中，假设r个总体的方差相等，要检验的假设H0是μ_1=μ_2=⋯=μ_r,备择假设H1是至少存在两个均值不等
散点图矩阵是借助两变量散点图的作图方法，它可以看作是一个大的图形方阵，其每一个非主对角元素的位置上是对应行的变量与对应列的变量的散点图。
进行单指标检验时，假设H0: H0:μ=μ_0,H1: μ≠μ_0,计算得到统计量的数值为1.833，临界值t为0.45，此时应 拒绝
针对连续变量的统计推断方法中，最常用的有T检验和 方差分析
当q=1时，它表示 曼哈顿距离
当q=2时，它表示 欧式距离
当q趋于正无穷时，它表示 切比雪夫距离
如果X和Y在统计上独立，则相关系数等于 0
相关系数r的取值范围是 -1≤r≤1
判别分析是判别样品 所属类型 的一种统计方法，常用的判别方法有 距离判别 Fisher判别Bayes判别逐步判别法。
聚类分析就是分析如何对样品(或变量)进行量化分类的问题。通常聚类分析分为 Q型 聚类和 R型
当q=2时，它表示 欧氏距离
学习回归分析的目的是对实际问题进行 预测  和控制。
判别分析适用于被解释变量是 非度量 变量的情形。
与其他多元线性统计模型类似，判别分析的假设之一是每一个判别变量（解释变量）不能是其他判别变量的 线性
组合，假设 之二是各组变量的 协方差矩阵 相等，假设之三是各判别变量遵从 多元正态
贝叶斯统计的思想是：假定对研究对象已有一定的认识，常用 先验概率 分布来描述这种认识，然后我们取得一个样本，用样本来 修正已有的认识，得到 后验概率 分布，各种统计推断就都可以通过这个分布来进行。
按经典假设，线性回归模型中的解释变量应是非随机变量，且与随机误差项 不相关
回归分析中定义的解释变量和被解释变量都是 随机
聚类和分类的区别是， 分类 分析是一种有监督学习方法，而 聚类 分析是一种无监督学习方法。
聚类分析是将分类对象分成若干类，相似的归为同一类，不相似的归为不同的类。
进行系统聚类分析时，计算初始6个样本（X1…X6）的距离矩阵为： 若类之间连接应用最大距离方法，最先聚类的是 X5，X6
进行系统聚类分析时，计算初始6个样本（X1…X6）的距离矩阵为：若类之间连接应用最小距离方法，假设将X5和X6聚为一类定义为X7，则X7与X1的距离d(7,1)= 6
Q型聚类法是按样品进行聚类，R型聚类法是按变量进行聚类,9. Q型聚类相似度统计量是 距离而R型聚类统计量通常采用
相似系数
回归分析中从研究对象上可分为一元和 多元
聚类分析中， 模糊聚类方法的基本思想是通过优化目标函数得到每个样本点对所有类中心的隶属度，从而对样本进行自动分类
回归分析中，被预测或被解释的变量称为 因变量
因子分析中，将每个原始变量分解为两个部分，一个部分由所有变量共同具有的少数几个 公共因子 组成的，另一个部分是每个变 量独自具有的因素，即 特殊因子
x_1的共同度 = 0.872 ，x_1的剩余方差 = 0.128 ，公因子F_1与x_1的协方差= 0.934
对多元数据X（x1,x2,x3,x4,x5）进行了主成分分析, 样本的特征值λ_1=2.857，λ_2=0.809，λ_3=0.609，λ_4=0.521，λ_5=0.203对应特征向量p1= (0.464,0.457,0.470,0.421,0.421), p1= (0.240,0.509,0.260,-0.526,-0.582),则第一主成分Y1的计算公式是
Y1=0.464x1+0.457x2+0.470x3+0.421x4+0.421x5
进行K-均值聚类时，碎石图如图所示，则最优的分类数为 3
主成分分析 是利用降维的思想，在损失很少信息的前提下把多个指标转化为几个综合指标的多元统计
主成分分析通常把转化生成的综合指标称之为主成分，其中每个主成分都是原始变量的 线性组合 ，且各个主成分之间互不相关， 这就使得主成分比原始变量具有某些更优越的性能
主成分分析中我们所说的保留原始变量尽可能多的信息，也就是指的生成的较少的综合变量的方差和尽可能接近于原始变量 方差 的总和。
主成分分析中可以利用 协方差矩阵)求解主成分。
对多元数据X（x1,x2,x3,x4）进行了主成分分析, 样本的特征值λ_1=2.857，λ_2=0.809，λ_3=0.702，λ_4=0.025，则第一主成分的方差贡献率是 65 %。
在进行主成分分析得出协方差阵或是相关阵发现最小特征根接近于零时，意味着中心化以后的原始变量之间存在 多重共线性
即原始变量存在着不可忽视的重叠信息。
主成分的协方差矩阵为 对角矩阵
因子分析中因子载荷系数aij的统计意义是第i个变量与第j个公因子的 相关系数
多元分析中常用的统计量有 样本 均值向量 样本协差阵  样本离差阵 样本相关系数矩阵 每题可以有多个空。 答案一|答案二|答案三 题目创建后不可修改填空数量
主成分分析是利用 降维 的思想，在损失很少的信息前提下，把多个指标转化为几个综合指标的多元统计方法
'''


for i in dir(sys.modules[__name__]):
    if '__' in i or i in ['getAll', 'sys', 'self_names']:
        continue
    self_names.append(i)

def getAll():
    for i in self_names:
        try:
            x = open(i + '.py', 'w', encoding='UTF8')
            x.write(globals()[i])
            x.close()
        except:
            pass

