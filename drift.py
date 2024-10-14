import json
import math
import random
import os
import pace_changer

# 加载 JSON 文件并提取经纬度
def LoadJson(path):
    with open(path, 'r', encoding='utf-8') as file:
        json_str = file.read()
    
    data = json.loads(json_str)
    lonData = []
    latData = []

    # 遍历 pointsList 中的每一个点
    for point in data['data']['pointsList']:
        point_str = point['point']  
        lon, lat = map(float, point_str.split(','))  
        lonData.append(lon)
        latData.append(lat)
    
    return lonData, latData



# 计算两点之间的距离（使用 Haversine 公式）
def haversine_distance(lat1, lon1, lat2, lon2):
    EARTH_RADIUS = 6371000 #地球半径 用于计算两点间距离
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    Distance = EARTH_RADIUS * c
    return  Distance
#Chatgpt真好用啊#

if __name__ == '__main__':
    chi = input("Input Change jsonfile id: ")
    path = os.path.join(".", "tasks", "tasklist_" + chi + ".json")
    drift = random.uniform(-0.000000001, 0.000000001)
    lonData, latData = LoadJson(path)

    for index in range(len(lonData)):
        lonData[index] += drift
    for index in range(len(latData)):
        latData[index] += drift

#计算总距离
    Distance = 0.0
    for index in range(len(lonData) - 1):
        Distance += haversine_distance(latData[index], lonData[index], latData[index + 1], lonData[index + 1])
    Distance = round(Distance / 10) / 100
# 生成修改后的坐标列表
    ChangedData = [f"{lon},{lat}" for lon, lat in zip(lonData, latData)]

    with open(path, 'r+', encoding='utf-8') as f:
        jsondata = json.load(f)
        for i in range(min(len(ChangedData), len(jsondata['data']['pointsList']))):
            jsondata['data']['pointsList'][i]['point'] = ChangedData[i]
        jsondata['data']['recordMileage'] = Distance
        # 重置文件指针并写回修改后的 JSON 数据
        f.seek(0)
        json.dump(jsondata, f, indent=4, ensure_ascii=False)
        f.truncate()  
    pace_changer.change_pace(path, round(random.uniform(4.5, 5.5), 2)) #使用已有的pace_changer.py对刚刚生成的新json步频进行放缩

    print('End of Program')
