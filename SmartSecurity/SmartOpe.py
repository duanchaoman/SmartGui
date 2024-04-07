import json
import tkinter as tk
from tkinter import Scrollbar,RIGHT,Y
from tkinter import ttk
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
import base64
import requests
from datetime import datetime, timedelta

root=tk.Tk()
root.title('监狱-兴义')
root.geometry('1000x800')
root.resizable(False,False)

#全局变量
departId='526101'#警员信息

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
out_Magtext.place(x=400, y=15)

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
        userName=res.get('result').get('user').get('userName')
        login_name="\n当前登录用户："+userName
        Level=res.get('result').get('user').get('accountLevel')
        accountLevel="\n当前用户级别："+str(Level)
        person= res.get('result').get('person').get('personId')
        user_departId=res.get('result').get('person').get('departId')
        token = res.get('result').get('token')
        userId = res.get('result').get('user').get('userId')
        guestCode = res.get('result').get('user').get('guestCode')
        user_guestCode = "\nGuestCode:"+str(guestCode)
        out_Magtext.delete('1.0','end')
        out_Magtext.insert('end',login_name)
        out_Magtext.insert('end',accountLevel)
        out_Magtext.insert('end',user_guestCode)

        # 提示语-警情中心
        tk.Label(root,text='------警情中心').place(x=10,y=200)

        #功能-一键接警
        def creat():
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/addRecord'
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            curr_time = datetime.now()
            alrtime = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            twolevedata_front = {
                "createTime": " ",
                "handledTime": "",
                "alarmTime": alrtime,
                "address": "监一栋/1楼/103",
                "alarmMemo": "非法翻越",
                "alarmLevelCode": "02",
                "alarmPerson": "报警人姓名",
                "alarmDescription": "报警描述",
                "receiverUserId": userId
            }
            fourlevedata_front = {
                "createTime": " ",
                "handledTime": "",
                "alarmTime": alrtime,
                "address": "监一栋/1楼/103",
                "alarmMemo": "非法翻越",
                "alarmLevelCode": "04",
                "alarmPerson": "报警人姓名",
                "alarmDescription": "报警描述",
                "receiverUserId": userId
            }
            data_after = {
                "result": "",
                "positionCode": "5223010030090300010020010010301006500000",
                "alarmAddressFloorId": "",
                "alarmCoordinate": "[-2.338444465518915,-1.6307756742432518,4.991408488774528]",
                "inRoom": 1,
                "addressId": "522301-f9dfcc084f294fc5a959efe69465e555",
                "alarmSourceCode": "02",
                "status": "0"
            }
            twoadd_data = {**twolevedata_front, **data_after}
            twodata = json.dumps(twoadd_data)
            twoleveres = requests.post(url=url, headers=headers, data=twodata).json()
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

            elif tworesmsg.get('msg') != 'OK':
                erromag = '二级警情创建失败，检查'
                btn_credoit.configure(bg='red')
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('1.0', erromag)

            elif fouresmsg.get('msg') != 'OK':
                erromag = '四级警情创建失败，检查'
                btn_credoit.configure(bg='red')
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('1.0', erromag)


        # 按钮-一键创建
        btn_credoit=tk.Button(root,text='一键接警',height=1,width=20,command=lambda :creat())
        btn_credoit.place(x=10,y=230)

        #功能-一键处警
        def plcdis():
            # 二级警情
            uip = input_ipadr.get(1.0, tk.END + "-1c")
            query_url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=2024-03-12+00:00:00&endDate=2024-03-19+23:59:59&address=&importantEquip='
            headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
            query_res = requests.get(url=query_url, headers=headers, params=None).json()
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
            if twolevegnore_res.get('msg') == 'OK':
                twodo_mag = '二级警情处置结果：'
                mag = '处理成功：'
                twodo_result = 'msg：' + twolevegnore_res.get('msg') + '   result：' + twolevegnore_res.get('result')
                out_Magtext.delete('1.0','end')
                out_Magtext.insert('end', twodo_mag + '\n')
                out_Magtext.insert('end', mag)
                out_Magtext.insert('end', twodo_result + '\n')
                btn_plcdis.configure(bg='green')

            elif twolevegnore_res.get('msg') != 'OK':
                erromag = '二级警情创建失败，检查'
                btn_plcdis.configure(bg='red')
                out_Magtext.delete('1.0', 'end')
                out_Magtext.insert('1.0', erromag)
            #4级警情处置接口存在问题

        #按钮-一键处警
        btn_plcdis=tk.Button(root,text='一键处警',height=1,width=20,command=lambda :plcdis())
        btn_plcdis.place(x=180,y=230)

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
            else:
                btn_ott.configure(bg='red')

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
            else:
                btn_four.configure(bg='red')

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
                btn_week.configure(bg='green')
            else:
                btn_week.configure(bg='red')

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

        # 按钮-巡更日志
        btn_plclog=tk.Button(root,text='巡更日志',height=1,width=10)
        btn_plclog.place(x=10,y=500)

        # 按钮-统计分析





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