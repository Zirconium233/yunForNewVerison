import json
import os
import random
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

def change_all(path_dir, target_speed:str):
    files = os.listdir(path_dir)
    for file in files:
        target_speed = round(random.uniform(4.5, 5.5), 2)
        change_pace(os.path.join(path_dir, file), target_speed)

if __name__ == "__main__":
    choice = input("你需要修改哪一个tasklist？(All or index)")
    speed = input("你要的配速是多少分钟？(示例：4.5， 输入random在[4.5-5.5]随机)")
    try:
        speed_f = None
        if speed == "random":
            speed_f = round(random.uniform(4.5, 5.5), 2)
        else:
            speed_f = round(float(speed), 2)
        if choice == 'All':
            change_all("./tasks", speed)
        else:
            chi = int(choice)
            change_pace(f"./tasks/tasklist_{chi}.json", speed_f)

    except Exception as e:
        print("错误")
        print(e)
        print("错误退出，如果显示write to，可能已经更改了文件，请自行确认是否可用。")
        input()


    