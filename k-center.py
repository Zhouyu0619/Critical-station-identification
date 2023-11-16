from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import pandas as pd
import random

#读取相似性矩阵
similarity = pd.read_excel('similarity_matrix.xlsx')
similarity.drop('Unnamed: 0',axis = 1,inplace = True)
similarity = np.array(similarity)
def distance(x, y):
    # 定义欧式距离的计算
    return 1-similarity[x][y]
def k_center(num_center):
    """
    选定好距离公式开始进行训练
    """
    indexs = [i for i in range(30)]
    data = [i for i in range(30)]
    random.shuffle(indexs)  # 随机选择质心
    centroids = indexs[:num_center]# 初始中心点
    # 确定种类编号
    levels = list(range(num_center))
    sample_target = []
    if_stop = False
    while(not if_stop):
        if_stop = True
        classify_points = [[centroid] for centroid in centroids]
        sample_target = []
        # 遍历数据
        for sample in data:
            # 计算距离，由距离该数据最近的核心，确定该点所属类别
            distances = [distance(sample, centroid) for centroid in centroids]
            cur_level = np.argmin(distances)
            sample_target.append(cur_level)
            # 统计，方便迭代完成后重新计算中间点
            if sample not in classify_points[cur_level]:
                classify_points[cur_level].append(sample)
        # 重新划分质心
        for i in range(num_center):  # 几类中分别寻找一个最优点
            distances = [distance(point_1, centroids[i]) for point_1 in classify_points[i]]
            now_distances = sum(distances)   # 首先计算出现在中心点和其他所有点的距离总和
            for point in classify_points[i]:
                distances = [distance(point_2, point) for point_2 in classify_points[i]]
                new_distance = sum(distances)
                # 计算出该聚簇中各个点与其他所有点的总和，若是有小于当前中心点的距离总和的，中心点去掉
                if new_distance < now_distances:
                    now_distances = new_distance
                    centroids[i] = point    # 换成该点
                    if_stop = False
    #计算轮廓系数
    sc = []
    for x1 in classify_points:
        for x2 in x1:
            a1 = 0    #组内
            a2 = []
            for x11 in x1:
                a1 += distance(x1[0],x11)
            if a1!= 0:
                a1 = a1/(len(x1)-1)
            #组外
            for x21 in classify_points:
                a2_temp = 0
                if x21 != x1:
                    for x22 in x21:
                        a2_temp += distance(x1[0],x22)
                    a2.append(a2_temp/len(x21))
            sc.append((min(a2)-a1)/max(min(a2),a1))
    min_distence=0
    for n in range(num_center):  # 几类中分别寻找一个最优点
        distances = [distance(point_1, centroids[n]) for point_1 in classify_points[n]]
        min_distence += sum(distances)
    return classify_points,min_distence,sum(sc)/30,centroids