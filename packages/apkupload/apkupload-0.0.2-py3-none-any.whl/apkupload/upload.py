import configargparse
import argparse
import base64
import hashlib
import hmac
import json
import os
import requests
import time
import urllib.parse
from datetime import datetime
# 解析输入的参数

content_template = """

* 应用名称：{name}
* 下载地址：{url}
* 更新说明：
    {changelog}
* MD5：{md5}
* 版本名称：{version_name}
* 版本号：{version_code}
"""

def parse():
    p = configargparse.ArgParser(
        config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('--config', required=True, is_config_file=True)
    p.add('--version_code', required=True)
    p.add('--version_name', required=True)
    p.add('--send', required=True)
    p.add('--name', required=True)
    p.add('--base', required=True)
    p.add('--input', required=True)
    p.add('--output', required=True)
    p.add('--key', required=True)
    p.add('--password', required=True)
    p.add('--url', required=True)
    p.add('--secret', required=True)
    p.add('--token', required=True)
    p.add('--apk_repository', required=True)
    p.add('--apk_branch', required=True)
    p.add('--user', required=True)
    p.add('--repository', required=True)
    p.add('--github', required=True)
    p.add('--workflow', required=True, )
    p.add('--channels', required=True, nargs="+", )
    p.add('--changelog', required=True, nargs="+")
    p.add('--at', required=True, nargs="+")
    return p.parse_args()


def generate_apk_name():
    now = datetime.strftime(datetime.now(), "%m_%d_%H%M")
    return f"{output}/{name}_{new_version_name}_{now}.apk"


def build_web(md5, size):
    file = f"https://raw.githubusercontent.com/{user}/{apk_repository}/{apk_branch}/"+apk
    content = {
        "version": version_name,
        "url": file,
        "name": name,
        "date": datetime.now().strftime("%Y-%m-%d %H时%M分%S秒"),
        "changelog": changelog
    }
    if md5 != "":
        content["md5"] = md5
        content["size"] = size
    body = {"ref": "main", "inputs": {"content": json.dumps(content)}}
    r = requests.post(
        f"https://api.github.com/repos/{user}/{repository}/actions/workflows/{workflow}/dispatches",
        headers=headers,
        json=body
    )
    # print(r.status_code)


def change_version():
    os.system('rm -rf ' + output)
    os.system('rm -rf ' + input + "/build")
    result = ""
    print(">>>> change version <<<<")
    with open(input + "/apktool.yml", 'r') as f:
        lines = f.readlines()
        for line in lines[:-2]:
            result += line
        result += "  versionCode: '{version_code}'\n".format(
            version_code=version_code)
        result += "  versionName: " + version_name
    with open(input + "/apktool.yml", "w") as f:
        f.write(result)


def build_apk():
    unalign = output + "/unalign.apk"
    unsign = output + "/unsign.apk"
    print(">>>> building apk <<<<")
    os.system(
        'apktool b -o {unalign} {decode}'.format(unalign=unalign, decode=input))
    print(">>>> aligning apk <<<<")
    os.system(
        'zipalign -f 4 {unalign} {unsign}'.format(unalign=unalign, unsign=unsign))
    print(">>>> signing apk <<<<")
    os.system('apksigner sign --ks {key} --ks-pass pass:{password} --out {apk} {unsign}'.format(
        key=key, password=password, apk=apk, unsign=unsign))


def upload_to_github():
    print(">>>> start upload <<<<")
    content = ""
    with open(apk, "rb") as file:
        base64_bytes = base64.b64encode(file.read())
        content = base64_bytes.decode("ascii")
    body = {"message": "upload apk", "content": content}
    apk_name = apk.split("/")[-1]
    r = requests.put(
        f"https://api.github.com/repos/{user}/{apk_repository}/contents/{apk_name}",
        headers=headers,
        json=body,
    )
    print(r.status_code)
    print(r.text)
    if (r.status_code == 200 or r.status_code == 201):
        print(">>>> upload success <<<<")
        if send=='True':
            send_to_dingding()
    else:
        # 上传失败再次上传
        upload_to_github()


def build():
    print(f">>>> start build {apk} <<<<")
    build_web("", "")
    change_version()
    build_apk()
    md5 = hashlib.md5(open(apk, 'rb').read()).hexdigest()
    size = str(os.path.getsize(apk))+"字节"
    build_web(md5, size)
    upload_to_github()


def send_to_dingding():
    md5 = hashlib.md5(open(apk, 'rb').read()).hexdigest()
    print(">>>> send to dingding <<<<")
    content = content_template.format(name=name,url=url,changelog=changelog,md5=md5,version_name=new_version_name,version_code=version_code)
    atMobiles = []
    for i in at:
        atMobiles.append(i)
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url2 = f'https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp=' + \
        timestamp + '&sign=' + sign
    h = {'Content-Type': 'application/json; charset=utf-8'}
    body = {"msgtype": "markdown", "markdown": {"text": content},
            "at": {"atMobiles": atMobiles}, "isAtAll": False}
    r = requests.post(url2, headers=h, data=json.dumps(body))
    print(r.status_code)


if __name__ == "__main__":
    option = parse()
    version_code = option.version_code
    version_name = option.version_name
    name = option.name
    base = option.base
    send = option.send
    print(f"send:{send}")
    channels = option.channels
    input = option.input
    output = option.output
    key = option.key
    password = option.password
    secret = option.secret
    url = option.url
    token = option.token
    changelog = option.changelog
    changelog = [f"> {item}" for item in changelog]
    changelog = "\n".join(changelog)
    print(changelog)
    github = option.github
    workflow = option.workflow
    apk_branch = option.apk_branch
    at = option.at
    user = option.user
    repository = option.repository
    apk_repository = option.apk_repository
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"token {github}"}
    for channel in channels:
        new_version_name = f"{version_name}_{channel}"
        apk = generate_apk_name()
        build()
