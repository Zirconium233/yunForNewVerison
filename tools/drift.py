import json
import math
import random
import os
def change_pace(path, target_speed:float):
    print("当前处理：" + path)
    print("目标配速：" + str(target_speed))
    tasklist_ = dict()
    with open(file=path, mode="r+", encoding="utf-8") as f:
        data = f.read()
        tasklist_ = json.loads(data)
    tasklist = tasklist_['data']
    print("当前配速：" + str(tasklist['recodePace']))
    factor = target_speed / tasklist['recodePace']
    print("时间放缩因子：" + str(factor))
    if factor > 1:
        print("已经超越目标时间，停止放缩。")
        return
    tasklist['recodePace'] = round(target_speed, 2)
    tasklist['duration'] = int(factor * tasklist['duration']) # 放缩时间
    tasklist['recodeCadence'] = int(tasklist['recodeCadence'] / factor) # 增大步频
    pointList = tasklist['pointsList']
    for point in pointList:
        point['speed'] = round(factor * point['speed'], 2)
        point['runTime'] = str(int(float(point['runTime']) * factor))
        point['runStep'] = str(int(float(point['runStep']) / factor))
    print(f"完成，耗时变为：{tasklist['duration']}秒, 步频变成{tasklist['recodeCadence']}每分钟")
    with open(file=path, mode="w+", encoding="utf-8") as f:
        data = json.dumps(tasklist_)
        print(f"write to {path}. ")
        f.write(data)
#代码来源：./PaceChanger.py

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
    print("此脚本用于对已有的tasklist进行少量偏移、步频配速重新随机、并写回到原json中")
    pos_choice = input("你需要修改哪一个校区tasklist？(1.翡翠湖 2.屯溪路 3.其他)")

    path = "./tasks_fch" if pos_choice == "1" else "./tasks_txl" if pos_choice == "2" else "./tasks_else"
    chi = input("Input Change jsonfile id: ")

    FilePath = os.path.join(path, "tasklist_" + chi + ".json")
    drift = random.uniform(-0.000000001, 0.000000001)
    lonData, latData = LoadJson(FilePath)

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

    with open(FilePath, 'r+', encoding='utf-8') as f:
        jsondata = json.load(f)
        for i in range(min(len(ChangedData), len(jsondata['data']['pointsList']))):
            jsondata['data']['pointsList'][i]['point'] = ChangedData[i]
        jsondata['data']['recordMileage'] = Distance
        # 重置文件指针并写回修改后的 JSON 数据
        f.seek(0)
        json.dump(jsondata, f, indent=4, ensure_ascii=False)
        f.truncate()  
    change_pace(FilePath, round(random.uniform(4.5, 5.5), 2)) #使用已有的pace_changer.py对刚刚生成的新json步频进行放缩

    print('End of Program')
