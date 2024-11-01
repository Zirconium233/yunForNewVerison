import json
import matplotlib.pyplot as plt

# 读取JSON
with open('tasklist_5.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取经纬度
points_list = data['data']['pointsList']
latitudes = []
longitudes = []

for point in points_list:
    longitude, latitude = map(float, point['point'].split(','))
    latitudes.append(latitude)
    longitudes.append(longitude)

# 绘点
plt.figure(figsize=(6, 10))
plt.scatter(longitudes, latitudes, c='blue', marker='o')
plt.grid(True)
plt.show()