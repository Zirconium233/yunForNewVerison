#自动获取token等信息，点进跑步信息自动保存跑步记录tasklist
#安装mitmproxy 运行mitmproxy -s proxy.py
#手机代理设置为电脑ip:8080
import mitmproxy
import json
import subprocess
import configparser

def decode(key_enc,data,use_gzip):
    use_gzip_str = str(use_gzip).lower()
    result = subprocess.run(
        ['java', '-jar', 'decrypt.jar', key_enc, data, use_gzip_str],
        capture_output=True,
        text=True
    )
    print(result.args)
    print(result.stdout)
    print(result.stderr)
    output = result.stdout.split("\n")
    
    decrypted_key = output[0].split(": ")[1]
    decrypted_text = output[1].split(": ")[1]
    return decrypted_key, decrypted_text

def match_str(str,patterns):
    for pattern in patterns:
        if pattern in str:
            return True
    return False

fields_to_keep = [
    "recordMileage",
    "recodePace",
    "recodeCadence",
    "recodeDislikes",
    "duration",
    "pointsList",
    "schoolId",
    "manageList"
]

class Yun:
    saved = False
    count = 0

    def request(flow: mitmproxy.http.HTTPFlow) -> None:
        if "210.45.246.53:8080" not in flow.request.pretty_url:
            flow.live = False

    def response(self, flow: mitmproxy.http.HTTPFlow):
        
        req_url = flow.request.url
        if "210.45.246.53:8080" in req_url :
            if(self.saved == False and match_str(req_url,["getStudentInfo","AppSysMsgApi","homePageApi","crsReocordInfo"])):
                config = configparser.ConfigParser()
                config.read('config.ini')
                config.set('User', 'token', flow.request.headers.get("token",""))
                config.set('User', 'device_Id', flow.request.headers.get("deviceId",""))
                config.set('User', 'device_Name', flow.request.headers.get("deviceName",""))
                config.set('User', 'uuid', flow.request.headers.get("uuid",""))
                config.set('User', 'utc', flow.request.headers.get("utc",""))
                config.set('User', 'sign', flow.request.headers.get("sign",""))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                print("token: "+flow.request.headers.get("token",""))
                print("deviceId: "+flow.request.headers.get("deviceId",""))
                print("deviceName: "+flow.request.headers.get("deviceName",""))
                print("uuid: "+flow.request.headers.get("uuid",""))
                print("utc: "+flow.request.headers.get("utc",""))
                print("sign: "+flow.request.headers.get("sign",""))
                self.saved = True
            if("crsReocordInfo" in req_url) :
                request_body = json.loads(flow.request.text)
                cipher_key = request_body.get('cipherKey', '')
                response_text = flow.response.text.strip('"')
                print(cipher_key)
                _,tasklist_raw = decode(cipher_key,response_text,True)
                tasklist_json = json.loads(tasklist_raw)
                data = tasklist_json['data']
                
                if 'pointsList' in data:
                    for point in data['pointsList']:
                        if 'ts' in point:
                            del point['ts']
                filtered_data = {key: value for key, value in data.items() if key in fields_to_keep}
                tasklist_json['data'] = filtered_data
                with open(f"tasklist_{self.count}.json", 'w', encoding='utf-8') as file:
                    json.dump(tasklist_json, file, ensure_ascii=False, indent=4)
                self.count = self.count + 1
        else:
            flow.live = False
addons = [
    Yun()
]