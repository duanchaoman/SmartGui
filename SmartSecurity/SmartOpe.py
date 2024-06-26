import json
import tkinter as tk
from tkinter import Scrollbar,RIGHT,Y
from tkinter import ttk
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
import base64
import requests
from datetime import datetime, timedelta
import random
import codecs
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename

root=tk.Tk()
root.title('监狱-兴义')
root.geometry('1100x800')
root.resizable(False,False)

#全局变量
departId='526101'#警员信息
output_file =codecs.open('dislog.txt','w',encoding='utf-8')

#提示语-ip配置
pro_ipset=tk.Label(root,text='输入IP地址：')
pro_ipset.place(x=10,y=15)

#文本框-输入ip地址
input_ipadr=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_ipadr.place(x=110,y=10)

#提示语-输入警员账号
pro_Pollab=tk.Label(root,text='输入警员账号：')
pro_Pollab.place(x=10,y=55)

#文本框-输入警员账号
input_Poltext=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_Poltext.place(x=110,y=50)

#提示语-输入登录密码
pro_Pwdlab=tk.Label(root,text='输入登录密码：')
pro_Pwdlab.place(x=10,y=95)

#文本框-输入登录密码
input_Pwdtext=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_Pwdtext.place(x=110,y=90)

#文本框-输出消息-添加滚动条
yscrollbar = Scrollbar(root)
yscrollbar.pack(side=RIGHT, fill=Y)
out_Magtext=tk.Text(root,height=58, width=78, bd=5, pady=5, padx=5)
yscrollbar.config(command=out_Magtext.yview)
out_Magtext.config(yscrollcommand=yscrollbar.set)
out_Magtext.place(x=500, y=15)

#单选按钮-接受收集器-设置默认选中
radio_var=tk.StringVar()
radio_var.set('安防')

#单选按钮-综合安防业务平台
Secbtn=tk.Radiobutton(root,text='综合安防业务平台',variable=radio_var,value='安防')
Secbtn.place(x=10,y=120)

#单选按钮-智慧调度平台
Combtn=tk.Radiobutton(root,text='指挥调度平台',variable=radio_var,value='指挥')
Combtn.place(x=150,y=120)

#获取公钥
def getPublicKey():
    uip = input_ipadr.get(1.0, tk.END+"-1c")
    userAccount=input_Poltext.get(1.0, tk.END+"-1c")
    url = "http://" + uip + "/smartSecurityAPI/userLogin/getPublicKey?userAccount="+userAccount
    res = requests.get(url=url).json()
    public = res.get('result')
    publicKey = '-----BEGIN PUBLIC KEY-----\n' + public + '\n-----END PUBLIC KEY-----'
    return publicKey

# 加密处理
def encrpt(password,public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()

def login():
    if radio_var.get()=='安防':
        #登录逻辑
        set_ip=input_ipadr.get(1.0, tk.END+"-1c")
        url='http://'+set_ip+'/smartSecurityAPI/userLogin/login'
        headers={'Content-Type':'application/json'}
        set_userAccount=input_Poltext.get(1.0, tk.END+"-1c")
        get_pwd=input_Pwdtext.get(1.0, tk.END+"-1c")
        set_pwd=encrpt(get_pwd, getPublicKey())
        payload = json.dumps({
            "userAccount": set_userAccount,
            "password": set_pwd
        })
        res=requests.post(url=url,headers=headers,data=payload).json()
        if res.get('msg') == 'OK':
            userName=res.get('result').get('user').get('userName')
            login_name="\n当前登录用户："+userName
            Level=res.get('result').get('user').get('accountLevel')
            accountLevel="\n当前用户级别："+str(Level)
            person= res.get('result').get('person').get('personId')
            user_departId=res.get('result').get('person').get('departId')
            user_deptName = res.get('result').get('deptName')
            token = res.get('result').get('token')
            userId = res.get('result').get('user').get('userId')
            guestCode = res.get('result').get('user').get('guestCode')
            roleId = res.get('result').get('user').get('roleId')
            user_guestCode = "\nGuestCode:"+str(guestCode)
            out_Magtext.delete('1.0','end')
            out_Magtext.insert('end',login_name)
            out_Magtext.insert('end',accountLevel)
            out_Magtext.insert('end',user_guestCode)
            output_file.write('登录用户信息；'+json.dumps(res)+'\n')
        else:
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('end', res)
            output_file.write('登录失败，检查用户信息：'+json.dumps(res)+'\n')

        # 提示语-警情中心
        tk.Label(root,text='------警情中心').place(x=10,y=200)

        #功能-一键接警
        def creat():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/addRecord'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            curr_time = datetime.now()
            alrtime = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            twoleve_data=json.dumps(
                {
                    "createTime": "",
                    "handledTime": "",
                    "alarmTime": alrtime,
                    "address": "监一栋",
                    "alarmMemo": "区域入侵",
                    "alarmLevelCode": "02",
                    "alarmPerson": "报警人姓名",
                    "alarmPersonTel": "12333333333",
                    "alarmDescription": "描述",
                    "receiverUserId": userId,
                    "result": "",
                    "positionCode": "5223010030090300080020000000001000000000",
                    "alarmAddressFloorId": "",
                    "alarmCoordinate": "{\"longitude\":104.91867520732873,\"latitude\":25.138250882693978,\"altitude\":65.82954917621814}",
                    "inRoom": 2,
                    "addressId": "522301-f05257da869443379d54b6117c7e9ca2",
                    "alarmSourceCode": "02",
                    "status": "0"
                }
            )

            fourlevedata_front = {
                "createTime": " ",
                "handledTime": "",
                "alarmTime": alrtime,
                "address": "监一栋/1楼/103",
                "alarmMemo": "非法翻越",
                "alarmLevelCode": "04",
                "alarmPerson": "报警人姓名",
                "alarmPersonTel": "13111111111",
                "alarmDescription": "报警描述",
                "receiverUserId": userId
            }
            data_after = {
                "result": "",
	            "positionCode": "5223010030090300010020010010301006500000",
                "alarmAddressFloorId": "522301-6ebac410cd6145eead50f90d6cbb2bd8",
                "alarmCoordinate": "[-2.825569540095187,-1.6307759843888676,5.376916993914214]",
                "inRoom": 1,
                "addressId": "522301-f9dfcc084f294fc5a959efe69465e555",
                "alarmSourceCode": "02",
                "status": "0"
                    }
            twoleveres = requests.post(url=url, headers=headers, data=twoleve_data).json()
            fouradd_data={**fourlevedata_front, **data_after}
            fourdata=json.dumps(fouradd_data)
            fourleveres=requests.post(url=url,headers=headers,data=fourdata).json()
            tworesmsg=twoleveres.get('msg')
            fouresmsg=fourleveres.get('msg')
            if tworesmsg and fouresmsg =='OK':
                twores='二级报警创建成功，result:'+str(twoleveres.get('result'))
                foures='四级报警创建成功，result:'+str(fourleveres.get('result'))
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('end', twores+'\n')
                out_Magtext.insert('end',foures+'\n')
                btn_credoit.configure(bg='green')
                output_file.write('二级警情添加结果：' + json.dumps(twoleveres) + '\n')
                output_file.write('四级警情添加结果：' + json.dumps(fourleveres) + '\n')
            elif tworesmsg.get('msg') != 'OK':
                erromag = '二级警情创建失败，检查'
                btn_credoit.configure(bg='red')
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('1.0', erromag)
                output_file.write('二级警情添加失败：'+json.dumps(twoleveres)+'\n')

            elif fouresmsg.get('msg') != 'OK':
                erromag = '四级警情创建失败，检查'
                btn_credoit.configure(bg='red')
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('1.0', erromag)
                output_file.write('四级警情添加失败：'+json.dumps(fourleveres)+'\n')

        # 按钮-一键创建
        btn_credoit=tk.Button(root,text='一键接警',height=1,width=10,command=lambda :creat())
        btn_credoit.place(x=10,y=230)

        # 功能-最新一二三级警情
        def lastott():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday()), '%Y-%m-%d')
            this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()), '%Y-%m-%d')
            url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+this_week_start+'+00:00:00&endDate='+this_week_end+'+23:59:59&address=&importantEquip='
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0','end')
            out_Magtext.insert('1.0',res)
            if res.get('msg') == 'OK':
                btn_lastott.configure(bg='green')
                output_file.write('警情添加结果：' + json.dumps(res) + '\n')
            else:
                btn_lastott.configure(bg='red')
                output_file.write('警情添加失败'+json.dumps(res)+'\n')

        # 按钮-最新一二三级警情
        btn_lastott=tk.Button(root,text='最新一二三级',height=1,width=10,command=lambda :lastott())
        btn_lastott.place(x=90,y=230)

        # 功能-最新四级
        def lastfour():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday()), '%Y-%m-%d')
            this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()), '%Y-%m-%d')
            url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+this_week_start+'+00:00:00&endDate='+this_week_end+'+23:59:59&address=&importantEquip='
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_lastfour.configure(bg='green')
                output_file.write('四级警情查询结果：' + json.dumps(res) + '\n')
            else:
                btn_lastfour.configure(bg='red')
                output_file.write('四级警情查询失败：'+json.dumps(res)+'\n')

        # 按钮-最新四级
        btn_lastfour=tk.Button(root,text='最新四级',height=1,width=10,command=lambda :lastfour())
        btn_lastfour.place(x=170,y=230)

        #功能-一键处警
        def plcdis():
            # 二级警情
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            this_startime = datetime.strftime(datetime.now(),'%Y-%m-%d')
            this_endtime = datetime.strftime(datetime.now(),'%Y-%m-%d')
            query_url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+this_startime+'+00:00:00&endDate='+this_endtime+'+23:59:59&address=&importantEquip='
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            query_res = requests.get(url=query_url, headers=headers, params=None).json()
            get_toal = query_res.get('result').get('total')
            four_url ='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+this_startime+'+00:00:00&endDate='+this_endtime+'+23:59:59&address=&importantEquip='
            four_res = requests.get(url=four_url,headers=headers,params=None).json()
            get_fourtoal = four_res.get('result').get('total')
            if get_toal and get_fourtoal > 0:
                alarm = query_res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                twodo_url = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                twoleve_data = json.dumps({
                    "alarmHandlingCode": "2",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                twolevegnore_res = requests.post(url=twodo_url, headers=headers, data=twoleve_data).json()
                # 四级警情处置
                four_alarm =four_res.get('result').get('records')
                four_alarmI =four_alarm[0]
                four_alarmId =str(four_alarmI.get('alarmId'))
                fourleve_url = 'http://'+uip+'/smartSecurityAPI/alarmHandler/alarmHandled'
                fourleve_data =json.dumps(
                    {
                        "alarmHandlingCode": "0",
                        "handleResult": "123",
                        "action": 1,
                        "alarmId": four_alarmId
                    }
                )
                fourleve_res =requests.post(url=fourleve_url,headers=headers,data=fourleve_data).json()

                if twolevegnore_res.get('msg') and fourleve_res.get('msg') == 'OK':
                    twodo_mag = '二级警情处置结果：'
                    fourdo_mag = '四级警情处置结果：'
                    out_Magtext.delete('1.0','end')
                    out_Magtext.insert('end', twodo_mag + '\n'+json.dumps(twolevegnore_res)+'\n')
                    out_Magtext.insert('end',fourdo_mag + '\n'+json.dumps(fourleve_res)+'\n')
                    btn_plcdis.configure(bg='green')
                    output_file.write('二级警情处理成功：' + json.dumps(twolevegnore_res) + '\n')
                    output_file.write('四级警情处置成功：'+json.dumps(fourleve_res)+'\n')

                elif twolevegnore_res.get('msg') or fourleve_res.get('msg') != 'OK':
                    two_erromag = '二级警情处置失败：'
                    four_erromag = '四级警情处置失败：'
                    btn_plcdis.configure(bg='red')
                    out_Magtext.delete('1.0', 'end')
                    out_Magtext.insert('1.0',json.dumps(two_erromag+twolevegnore_res)+'\n')
                    out_Magtext.insert('1.0',json.dumps(four_erromag+fourleve_res)+'\n')
                    output_file.write('二级警情处理失败：'+json.dumps(twolevegnore_res)+'\n')
                    output_file.write('四级警情处置失败：'+json.dumps(fourleve_res)+'\n')

            else:
                erromag = '未查询到警情信息，检查服务器配置'
                btn_plcdis.configure(bg='red')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',erromag)
                output_file.write(erromag)

        #按钮-一键处警
        btn_plcdis=tk.Button(root,text='一键处警',height=1,width=10,command=lambda :plcdis())
        btn_plcdis.place(x=250,y=230)

        #功能-设备报警
        def plcdriver():
            url = 'http://192.168.1.251:1777/eventRcv'
            headers = {}


        #按钮 - 设备报警
        btn_plcdriver=tk.Button(root,text='设备报警',height=1,width=10)
        btn_plcdriver.place(x=330,y=230)






        # 提示语-处警历史
        tk.Label(root,text='------处警历史').place(x=10,y=260)

        #功能-查询一二三级
        def ott():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday() + 7),'%Y-%m-%d')
            this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()), '%Y-%m-%d')
            otturl = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + this_week_start + '+00:00:00&endDate=' + this_week_end + '+23:59:59&positionCode=&pushStatus='
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            ott_res = requests.get(url=otturl, headers=headers, params=None).json()
            out_Magtext.delete('1.0','end')
            out_Magtext.insert('end', ott_res)
            if ott_res.get('msg') == 'OK':
                btn_ott.configure(bg='green')
                output_file.write('一二三级警情查询结果：' + json.dumps(ott_res) + '\n')
            else:
                btn_ott.configure(bg='red')
                output_file.write('未查询到一二三级警情数据'+json.dumps(ott_res)+'\n')
        #按钮-一二三级
        btn_ott=tk.Button(root,text='一二三级',height=1,width=20,command=lambda :ott())
        btn_ott.place(x=10,y=290)

        # 功能-四级
        def four():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday() + 7),'%Y-%m-%d')
            this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()), '%Y-%m-%d')
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + this_week_start + '&endDate=' + this_week_end + '&importantEquip='
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_four.configure(bg='green')
                output_file.write('查询四级警情信息：'+json.dumps(res)+'\n')
            else:
                btn_four.configure(bg='red')
                output_file.write('未查询到四级警情：'+json.dumps(res)+'\n')

        # 按钮-四级
        btn_four=tk.Button(root,text='四级',height=1,width=20,command=lambda :four())
        btn_four.place(x=180,y=290)


        # 提示语-警情分析
        tk.Label(root,text='------警情分析').place(x=10,y=320)

        # 功能-本周
        def week():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday()), '%Y-%m-%d')
            this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()), '%Y-%m-%d')
            url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=week&beginTime=' + this_week_start + '+00:00:00&endTime=' + this_week_end + '+23:59:59'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                if len(res.get('result')) == 0:
                    btn_week.configure(bg='yellow')
                    output_file.write('本周无数据：'+json.dumps(res)+'\n')
                else:
                    btn_week.configure(bg='green')
                    output_file.write('本周警情分析数据：'+json.dumps(res)+'\n')
            else:
                btn_week.configure(bg='red')
                output_file.write('本周处警信息查询失败，检查配置信息'+json.dumps(res)+'\n')
        # 按钮-本周
        btn_week=tk.Button(root,text='本周',height=1,width=20,command=lambda :week())
        btn_week.place(x=10,y=350)

        # 功能-当月
        def month():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            this_month_start = datetime.strftime(datetime(datetime.now().year, datetime.now().month, 1), '%Y-%m-%d')
            this_month_end = datetime.strftime(
                datetime(datetime.now().year, datetime.now().month + 1, 1) - timedelta(days=1), '%Y-%m-%d')
            url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=month&beginTime=' + this_month_start + '+00:00:00&endTime=' + this_month_end + '+23:59:59'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                if len(res.get('result')) == 0:
                    btn_month.configure(bg='yellow')
                else:
                    btn_month.configure(bg='green')
            else:
                btn_month.configure(bg='red')

        # 按钮-本月
        btn_month=tk.Button(root,text='当月',height=1,width=20,command=lambda :month())
        btn_month.place(x=180,y=350)

        # 提示语-警员管理
        tk.Label(root,text='------警员管理').place(x=10,y=380)

        # 功能-民警信息
        def plcinfo():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://'+uip+'/smartSecurityAPI/bus/person/findAll?departId='+departId
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_plcinfo.configure(bg='green')
            else:
                btn_plcinfo.configure(bg='red')

        # 按钮-民警信息
        btn_plcinfo=tk.Button(root,text='民警信息',height=1,width=10,command=lambda :plcinfo())
        btn_plcinfo.place(x=10,y=410)

        # 功能-实时警力
        def plcreal():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://'+uip+'/smartSecurityAPI/zxw/getZxwBuildFloorTree'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_plcreal.configure(bg='green')
            else:
                btn_plcreal.configure(bg='red')

        # 按钮-实时警力
        btn_plcreal=tk.Button(root,text='实时警力',height=1,width=10,command=lambda :plcreal())
        btn_plcreal.place(x=130,y=410)

        # 功能-警情分析
        def plcana():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip +'/smartSecurityAPI/bus/dept/queryDepartStatistics'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url, headers=headers, params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') =='OK':
                btn_plcana.configure(bg='green')
            else:
                btn_plcana.configure(bg='red')

        # 按钮-警情分析
        btn_plcana=tk.Button(root,text='警情分析',height=1,width=10,command=lambda :plcana())
        btn_plcana.place(x=250,y=410)

        # 提示语-日常巡更
        tk.Label(root,text='------日常巡更').place(x=10,y=440)

        # 功能-新增巡更路线
        def plcparo():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip +'/smartSecurityAPI/patrol/path/save'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            pathNode = "[{\"id\":\"xgpoint3748\",\"type\":0,\"currentTreeId\":\"000\",\"url\":\"\",\"positionCode\":\"5223010030090300270020000000001000000000\",\"videoArr\":[],\"position\":{\"longitude\":104.91964972549191,\"latitude\":25.136245142355815,\"altitude\":65.6849678889957}},{\"id\":\"xgpoint0468\",\"type\":0,\"currentTreeId\":\"000\",\"url\":\"\",\"positionCode\":\"5223010030090300270020000000001000000000\",\"videoArr\":[],\"position\":{\"longitude\":104.919499419485,\"latitude\":25.136890583330715,\"altitude\":65.66221604181243}},{\"id\":\"xgpoint8076\",\"type\":0,\"currentTreeId\":\"000\",\"url\":\"\",\"positionCode\":\"5223010030090300270020000000001000000000\",\"videoArr\":[],\"position\":{\"longitude\":104.92004081159351,\"latitude\":25.13702465293982,\"altitude\":65.6669518570738}}]"
            data = json.dumps({
                "pathName": "日常巡更路线",
                "pathNode": pathNode

            })
            res = requests.post(url=url, headers=headers, data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_plcparo.configure(bg='green')
            else:
                btn_plcparo.configure(bg='red')

        # 按钮-新增巡更路线
        btn_plcparo=tk.Button(root,text='新增巡更路线',height=1,width=10,command= lambda :plcparo())
        btn_plcparo.place(x=10,y=470)

        # 功能 -新增巡更任务
        def plcpata():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            # 获取巡更路线信息
            getlisturl = 'http://' + uip + '/smartSecurityAPI/patrol/path/list'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=getlisturl, headers=headers, params=None).json()
            result=res.get('result')
            path = result[0]
            pathId = path.get('pathId')
            url= 'http://' + uip + '/smartSecurityAPI/patrol/task/save'
            data=json.dumps({
                    "pathId": pathId,
                    "taskName": "日常巡更任务",
                    "departId": user_departId,
                    "taskType": "0",
                    "taskTimes": 1,
                    "taskTime": 5
            })
            patares=requests.post(url=url,headers=headers,data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', patares)
            if patares.get('msg') == 'OK' :
                btn_plcpata.configure(bg='green')
            else:
                btn_plcpata.configure(bg='red')

        # 按钮-新增巡更任务
        btn_plcpata=tk.Button(root,text='新增巡更任务',height=1,width=10,command=lambda :plcpata())
        btn_plcpata.place(x=130,y=470)

        # 功能-执行巡更任务
        def plcimp():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            # 获取巡更路线列表
            getlist_url='http://' + uip +'/smartSecurityAPI/patrol/task/getTodayPatrolTaskDetails?taskType=0'
            getlist_res=requests.get(url=getlist_url,headers=headers,params=None).json()
            result=getlist_res.get('result')
            result_0=result[0]
            taskId=result_0.get('taskId')
            #执行巡更任务
            taskStartTime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            taskEndTime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            url='http://' + uip +'/smartSecurityAPI/patrol/rec/save'
            data=json.dumps({
                    "recResult": 1,
                    "recRemark": "",
                    "taskId": taskId,
                    "taskStartTime": taskStartTime,
                    "taskEndTime": taskEndTime
            })
            res=requests.post(url=url,headers=headers,data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_plcimp.configure(bg='green')
            else:
                btn_plcimp.configure(bg='red')

        # 按钮-执行巡更任务
        btn_plcimp=tk.Button(root,text='执行巡更任务',height=1,width=10,command=lambda :plcimp())
        btn_plcimp.place(x=250,y=470)

        # 功能-新增定时巡更任务
        def setimetask():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            patrol_url ='http://' + uip +'/smartSecurityAPI/patrol/path/list'
            patrol_res = requests.get(url=patrol_url,headers=headers,params=None).json()
            get_pathId = ((patrol_res.get('result'))[0]).get('pathId')
            task_url = 'http://'+uip+'/smartSecurityAPI/patrol/task/save'
            task_data=json.dumps(
                {
                    "pathId": get_pathId,
                    "taskName": "定时",
                    "departId": user_departId,
                    "taskType": "1",
                    "taskTimes": 1,
                    "taskTime": 5,
                    "taskRange": "[{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]},{\"arr\":[\"00:00-23:59\"]}]"
                }
            )
            task_res=requests.post(url=task_url,headers=headers,data=task_data).json()
            if task_res.get('msg') == 'OK':
                btn_setimetask.configure(bg='green')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',task_res)
            else:
                btn_setimetask.configure(bg='red')
                msg='错误，请检查'
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',msg)

        # 按钮-新增定时巡更任务
        btn_setimetask=tk.Button(root,text='新增定时巡更',height=1,width=10,command=lambda :setimetask())
        btn_setimetask.place(x=370,y=470)

        # 功能-执行定时巡更任务
        def dotimetask():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            TaskDetails_url='http://'+uip+'/smartSecurityAPI/patrol/task/getTodayPatrolTaskDetails?taskType=1'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            TaskDetails_res=requests.get(url=TaskDetails_url,headers=headers,params=None).json()
            taskID =((TaskDetails_res.get('result'))[0]).get('taskId')
            url = 'http://'+uip+'/smartSecurityAPI/patrol/rec/save'
            this_startime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            this_endtime = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            data = json.dumps(
                {
                    "recResult": 1,
                    "recRemark": "",
                    "taskId": taskID,
                    "taskStartTime":this_startime,
                    "taskEndTime": this_endtime
                }
            )
            res = requests.post(url=url,headers=headers,data=data).json()
            if res.get('msg') == 'OK':
                btn_dotimetask.configure(bg='green')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',res)
            else:
                msg='错误，请检查'
                btn_dotimetask.configure(bg='red')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',msg)




        # 按钮-执行定时巡更任务
        btn_dotimetask=tk.Button(root,text='执行定时巡更',height=1,width=10,command=lambda :dotimetask())
        btn_dotimetask.place(x=370,y=500)

        # 功能-巡更日志
        def plclog():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            taskStartTime = datetime.strftime(datetime.now(),'%Y-%m-%d')
            taskEndTime = datetime.strftime(datetime.now(),'%Y-%m-%d')
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url='http://' + uip +'/smartSecurityAPI/patrol/rec/list?taskStartTime='+taskStartTime+'+00:00:00&taskEndTime='+taskEndTime+'+23:59:59'
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_plclog.configure(bg='green')
            else:
                btn_plclog.configure(bg='red')

        # 按钮-巡更日志
        btn_plclog=tk.Button(root,text='巡更日志',height=1,width=10,command=lambda :plclog())
        btn_plclog.place(x=10,y=500)

        # 功能-统计分析
        def plcstaana():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            beginDat = datetime.strftime(datetime.now(),'%Y-%m-%d')
            endDate = datetime.strftime(datetime.now(),'%Y-%m-%d')
            url='http://' + uip +'/smartSecurityAPI/patrol/path/pathStatistics?beginDate='+beginDat+'+00:00:00&endDate='+endDate+'+23:59:59'
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK' :
                btn_plcstaana.configure(bg='green')
            else:
                btn_plcstaana.configure(bg='red')

        # 按钮-统计分析
        btn_plcstaana=tk.Button(root,text='统计分析',height=1,width=10,command=lambda :plcstaana())
        btn_plcstaana.place(x=130,y=500)

        # 提示语-应急处突
        tk.Label(root,text='------应急处突').place(x=10,y=540)

        # 功能-罪犯监管
        def crimag():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url ='http://' + uip +'/smartSecurityAPI/criminal/findAll?roomJqname=&roomNo='
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_crimag.configure(bg='green')
            else:
                btn_crimag.configure(bg='red')

        # 按钮-罪犯监管
        btn_crimag=tk.Button(root,text='罪犯监管',height=1,width=10,command=lambda :crimag())
        btn_crimag.place(x=10,y=570)

        # 功能-应急资源
        def emeres():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            getgroup_url='http://' + uip +'/smartSecurityAPI/emergency/group'
            getgroup_res=requests.get(url=getgroup_url,headers=headers,params=None).json()
            result=getgroup_res.get('result')
            result_1=result[0]
            emergencyGroupId=result_1.get('emergencyGroupId')
            url ='http://'+ uip +'/smartSecurityAPI/emergency/member?emergencyGroupId='+emergencyGroupId
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_emeres.configure(bg='green')
            else:
                btn_emeres.configure(bg='red')

        # 按钮-应急资源
        btn_emeres=tk.Button(root,text='应急资源',height=1,width=10,command=lambda :emeres())
        btn_emeres.place(x=130,y=570)

        # 功能-应急物资
        def ememat():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url ='http://' + uip +'/smartSecurityAPI/emergency/store/list?storeStrutsCode=&keyWord='
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_ememat.configure(bg='green')
            else:
                btn_ememat.configure(bg='red')

        #按钮-应急物资
        btn_ememat=tk.Button(root,text='应急物资',height=1,width=10,command=lambda :ememat())
        btn_ememat.place(x=250,y=570)

        # 提示语-应急演练
        tk.Label(root,text='------应急演练').place(x=10,y=600)

        # 功能-新增应急预案
        def emeplan():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url ='http://' + uip +'/smartSecurityAPI/preplan/save'
            numb=str(random.randint(1,1000))
            data=json.dumps(
                {
                    "departId":user_departId,
                    "deptName": user_deptName,
                    "preplanName": "应急预案"+numb,
                    "preplanNo": "0000001",
                    "eventId": "510107-e5bec9e25883431f9c869dc63596fc1d",
                    "preplanLevel": "1",
                    "nodeEntityList": [{
                        "nodeName": "声音报警",
                        "nodeText": "01",
                        "nodeDescr": "123",
                        "nodeId": "5942_0"
                    }],
                    "preplanFile": "[]"
                }
            )
            res=requests.post(url=url,headers=headers,data=data).json()#新增应急预案
            sle_url='http://' + uip +'/smartSecurityAPI/preplan?currentPage=1&pageSize=10&keyWord=%E5%BA%94%E6%80%A5%E9%A2%84%E6%A1%88'+numb
            sle_res=requests.get(url=sle_url,headers=headers,params=None).json()
            sle_result=sle_res.get('result').get('records')
            sle_result_1 = sle_result[0]
            preplanId = sle_result_1.get('preplanId')
            app_url ='http://'+ uip +'/smartSecurityAPI/preplan/approval'
            app_data =json.dumps(
                {
                    "preplanId":preplanId,
                    "describle":"null",
                    "status": "102"
                }
            )
            requests.post(url=app_url,headers=headers,data=app_data).json()#审批
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_emeplan.configure(bg='green')
            else:
                btn_emeplan.configure(bg='red')

        # 按钮-新增应急预案
        btn_emeplan=tk.Button(root,text='新增应急预案',height=1,width=10,command=lambda :emeplan())
        btn_emeplan.place(x=10,y=630)

        # 功能-新增演练计划
        def emplan():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            currtinme=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            sel_url = 'http://' + uip +'/smartSecurityAPI/preplan?departId=526132&pageSize=1000'
            sel_res =requests.get(url=sel_url,headers=headers,params=None).json()
            records =sel_res.get('result').get('records')
            records_1 = records[0]
            preplanId = records_1.get('preplanId')
            url = 'http://' + uip +'/smartSecurityAPI/rehearsal/save'
            data=json.dumps(
                {
                    "rehearsalName": "演练计划",
                    "rehearsalPlantime": currtinme,
                    "preplanId":preplanId
                }
            )

            res = requests.post(url=url,headers=headers,data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_emplan.configure(bg='green')
            else:
                btn_emplan.configure(bg='red')

        # 按钮-新增演练计划
        btn_emplan=tk.Button(root,text='新增演练计划',height=1,width=10,command=lambda :emplan())
        btn_emplan.place(x=130,y=630)

        # 功能-新增方案
        def proadd():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            # 获取rehearsalId
            rehearsal_url='http://' + uip +'/smartSecurityAPI/rehearsal/queryPage?pageSize=1000'
            rehearsal_res=requests.get(url=rehearsal_url,headers=headers,params=None).json()
            rehearsal=rehearsal_res.get('result').get('records')
            rehearsal_1=rehearsal[0]
            rehearsalId=rehearsal_1.get('rehearsalId')
            # 获取schemePlaceId,schemeGroup
            scheme_url='http://'+ uip +'/smartSecurityAPI/sheme/queryPage?schemeName=&pageSize=1000'
            scheme_res=requests.get(url=scheme_url,headers=headers,params=None).json()
            scheme =scheme_res.get('result').get('records')
            scheme_1=scheme[0]
            schemePlaceType='building'
            schemePlaceId=scheme_1.get('schemePlaceId')
            schemeGroup=scheme_1.get('schemeGroup')
            # 新增方案
            url='http://' + uip + '/smartSecurityAPI/sheme/save'
            data=json.dumps(
                {
                    "schemeName": "方案名称",
                    "rehearsalId":rehearsalId,
                    "schemePurpose": "演练目的",
                    "schemePlace": "监一栋",
                    "schemePlaceType":schemePlaceType,
                    "schemePlaceId":schemePlaceId,
                    "schemeMan": "[\"f9e31355c63947339940b59b178f9a84\",\"27788f69c9974dda81bb31c80c00cf62\",\"ec306071c2614a36855b23b26549a513\"]",
                    "schemeGroup":schemeGroup,
                    "schemeLabour": "职责分工",
                    "schemeStand": "演练前准备",
                    "schemeDemands": "具体要求"
                }
            )
            res=requests.post(url=url,headers=headers,data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_proadd.configure(bg='green')
            else:
                btn_proadd.configure(bg='red')

        # 按钮-新增方案
        btn_proadd=tk.Button(root,text='新增演习方案',height=1,width=10,command=lambda :proadd())
        btn_proadd.place(x=250,y=630)

        # 功能-执行演练
        def impdri():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            # 获取所有方案信息
            sheme_url='http://' + uip +'/smartSecurityAPI/sheme/queryPage?schemeName=&pageSize=1000'
            sheme_res=requests.get(url=sheme_url,headers=headers,params=None).json()
            records=sheme_res.get('result').get('records')
            records_1=records[0]
            schemeId=records_1.get('schemeId')
            # 执行演练
            endtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            url='http://' + uip +'/smartSecurityAPI/shemeRec/save'
            data=json.dumps(
                {
                    "endTime": endtime,
                    "schemeId": schemeId,
                    "schemeMemo": "演练完毕",
                    "startTime": endtime
                }
            )
            res=requests.post(url=url,headers=headers,data=data).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_impdri.configure(bg='green')
            else:
                btn_impdri.configure(bg='red')

        # 按钮-执行演练
        btn_impdri=tk.Button(root,text='执行演练',height=1,width=10,command=lambda :impdri())
        btn_impdri.place(x=10,y=660)

        # 功能-演练记录
        def drirec():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            url='http://' + uip +'/smartSecurityAPI/shemeRec/queryPage?pageSize=1000'
            res=requests.get(url=url,headers=headers,params=None).json()
            out_Magtext.delete('1.0', 'end')
            out_Magtext.insert('1.0', res)
            if res.get('msg') == 'OK':
                btn_drirec.configure(bg='green')
            else:
                btn_drirec.configure(bg='red')

        # 按钮-演练记录
        btn_drirec=tk.Button(root,text='演练记录',height=1,width=10,command=lambda :drirec())
        btn_drirec.place(x=130,y=660)

        #提示语 -全监总览
        tk.Label(root,text='全监总览').place(x=10,y=690)

        #功能 -当日值班
        def todayduty():
            beginDate = datetime.strftime(datetime.now(),'%Y-%m-%d')
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip +'/smartSecurityAPI/xingyiduty/getDutyOnDay?beginDate='+beginDate
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res = requests.get(url=url,headers=headers,params=None).json()
            if res.get('msg') == 'OK':
                btn_todayduty.configure(bg='green')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',res)
            else:
                msg='接口错误，请检查'
                btn_todayduty.configure(bg='red')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',msg+res)

        #按钮 -当日值班
        btn_todayduty=tk.Button(root,text='当日值班',height=1,width=10,command=lambda :todayduty())
        btn_todayduty.place(x=10,y=710)

        #功能 - 全监总览
        def allinfo():
            this_day = datetime.strftime(datetime.now(), '%Y-%m-%d')
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip +'/smartSecurityAPI/dutyOverview/searchData?day='+this_day
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            res =requests.get(url=url,headers=headers,params=None).json()
            if res.get('msg') == 'OK':
                btn_allinfo.configure(bg='green')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',res)
            else:
                msg = '接口错误，请检查：'
                btn_allinfo.configure(bg='red')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',msg+res)

        #按钮 - 全监总览
        btn_allinfo=tk.Button(root,text='全监总览',height=1,width=10,command=lambda :allinfo())
        btn_allinfo.place(x=130,y=710)

        #提示语 -值班排班
        tk.Label(root,text='值班排班').place(x=10,y=740)

        #功能-上传和文件选择
        def load():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://'+uip+'/smartSecurityAPI/xingyiduty/import'
            selectFile = tk.filedialog.askopenfilename()
            entry1.insert(0,selectFile)
            files = {"file": (selectFile, open(selectFile, "rb"),
                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}  # 文件上传需要填写的文件参数

            data = {}
            heards = {'token': token, 'guestCode': guestCode}
            res = requests.post(url=url, files=files, data=data, headers=heards).json()
            if res.get('msg') == 'OK':
                btn_load.configure(bg='green')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',res)
            else:
                msg = '值班表上传失败，检查配置'
                btn_load.configure(bg='red')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('1.0',msg+res)

        #按钮-上传和文件选择
        btn_load=tk.Button(root,text='上传值班表',height=1,width=10,command=lambda :load())
        btn_load.place(x=10,y=760)
        entry1=tk.Entry(root,width=20)
        entry1.place(x=100,y=765)






        # 功能-一键执行所有功能
        def allfunction():
            for ram in range(0,27):
                if ram == 0:
                    creat()
                elif ram == 1:
                    lastott()
                elif ram == 2:
                    lastfour()
                elif ram == 3:
                    plcdis()
                elif ram == 4:
                    ott()
                elif ram == 5:
                    four()
                elif ram == 6:
                    week()
                elif ram == 7:
                    month()
                elif ram == 8:
                    plcinfo()
                elif ram == 9:
                    plcreal()
                elif ram == 10:
                    plcana()
                elif ram == 11:
                    plcparo()
                elif ram == 12:
                    plcpata()
                elif ram == 13:
                    plcimp()
                elif ram == 14:
                    plclog()
                elif ram == 15:
                    plcstaana()
                elif ram == 16:
                    crimag()
                elif ram == 17:
                    emeres()
                elif ram == 18:
                    ememat()
                elif ram == 19:
                    emeplan()
                elif ram == 20:
                    emplan()
                elif ram == 21:
                    proadd()
                elif ram == 22:
                    impdri()
                elif ram == 23:
                    drirec()
                elif ram == 24:
                    todayduty()
                elif ram == 25:
                    allinfo()
                elif ram == 26:
                    load()

        # 按钮-一键执行所有功能
        btn_allfunction = tk.Button(root, text='一键执行', height=1, width=10, command=lambda: allfunction())
        btn_allfunction.place(x=250, y=150)

#按钮-登录
Logbtn=tk.Button(root,text='登录',height=1, width=8,command=lambda :login())
Logbtn.place(x=50,y=150)

#功能-重置
def Btn_resetting():
    input_Poltext.delete('1.0','end')
    input_Pwdtext.delete('1.0','end')
    out_Magtext.delete('1.0','end')
    input_ipadr.delete('1.0','end')

#按钮-重置
Resbtn=tk.Button(root,text='重置',height=1, width=8,command=lambda :Btn_resetting())
Resbtn.place(x=150,y=150)






root.mainloop()