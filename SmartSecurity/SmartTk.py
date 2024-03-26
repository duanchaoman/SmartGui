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
root.geometry('400x270')
root.resizable(False,False)

#提示语-ip配置
pro_ipset=tk.Label(root,text='输入地址：')
pro_ipset.place(x=10,y=5)

#文本框-输入ip地址
input_ipadr=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_ipadr.place(x=10,y=25)

#提示语-输入警员账号
pro_Pollab=tk.Label(root,text='输入警员账号：')
pro_Pollab.place(x=10,y=60)

#文本框-输入警员账号
input_Poltext=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_Poltext.place(x=10,y=80)

#提示语-输入登录密码
pro_Pwdlab=tk.Label(root,text='输入登录密码：')
pro_Pwdlab.place(x=10,y=120)

#文本框-输入登录密码
input_Pwdtext=tk.Text(root,height=1, width=20, bd=5, pady=5, padx=5)
input_Pwdtext.place(x=10,y=140)

#文本框-输出消息
out_Magtext=tk.Text(root,height=17, width=25, bd=5, pady=5, padx=5)
out_Magtext.place(x=200,y=10)

#单选按钮-接受收集器-设置默认选中
radio_var=tk.StringVar()
radio_var.set('安防')

#单选按钮-综合安防业务平台
Secbtn=tk.Radiobutton(root,text='综合安防业务平台',variable=radio_var,value='安防')
Secbtn.place(x=10,y=180)

#单选按钮-智慧调度平台
Combtn=tk.Radiobutton(root,text='指挥调度平台',variable=radio_var,value='指挥')
Combtn.place(x=10,y=200)

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

#功能-登录
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
        login_name="\n当前登录用户：\n"+userName
        Level=res.get('result').get('user').get('accountLevel')
        accountLevel="\n当前用户级别：\n"+str(Level)
        person= res.get('result').get('person').get('personId')
        token = res.get('result').get('token')
        userId = res.get('result').get('user').get('userId')
        guestCode = res.get('result').get('user').get('guestCode')
        user_guestCode = "\nguestCode:\n"+str(guestCode)
        out_Magtext.delete('1.0','end')
        out_Magtext.insert('1.0',login_name)
        out_Magtext.insert('1.0',accountLevel)
        out_Magtext.insert('1.0',user_guestCode)
        #打开安防业务平台
        anfang_window=tk.Toplevel(root)
        anfang_window.title('安防业务平台------当前登录：'+userName)
        anfang_window.geometry('1680x860')
        anfang_window.resizable(False, False)

        #文本框-安防输出消息
        yscrollbar = Scrollbar(anfang_window)
        anfang_outmag=tk.Text(anfang_window,height=60, width=80, bd=5, pady=5, padx=5)
        yscrollbar.pack(side=RIGHT, fill=Y)
        yscrollbar.config(command=anfang_outmag.yview)
        anfang_outmag.config(yscrollcommand=yscrollbar.set)
        anfang_outmag.place(x=1100,y=50)

        #提示语-人工接警
        pro_aas=tk.Label(anfang_window,text='人工接警')
        pro_aas.place(x=10,y=10)

        #打开未处置警情页面
        def nodis():
            nodis_window=tk.Toplevel(anfang_window)
            nodis_window.title('未处置')
            nodis_window.geometry('650x450')
            nodis_window.resizable(False, False)
            #提示语-报警时间
            pro_distime=tk.Label(nodis_window,text='输入报警时间（格式：2024-03-12 11:05:42）')
            pro_distime.place(x=10,y=10)

            #文本框-报警时间输入框
            input_distext=tk.Text(nodis_window,height=1, width=20, bd=5, pady=5, padx=5)
            input_distext.place(x=10,y=30)

            #功能-此刻
            def now_time():
                curr_time = datetime.now()
                now_time = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                input_distext.delete('1.0','end')
                input_distext.insert('1.0',now_time)
                return now_time

            #按钮-此刻
            btn_addtime=tk.Button(nodis_window,text='此刻',height=1, width=8,command=lambda :now_time())
            btn_addtime.place(x=180,y=30)

            #提示语-报警地点
            pro_plcadd=tk.Label(nodis_window,text='报警地点')
            pro_plcadd.place(x=10,y=60)

            #单选按钮-报警地点
            radio_plcadd = tk.StringVar()

            jian1_btn = tk.Radiobutton(nodis_window, text='监一栋', variable=radio_plcadd, value='监一栋')
            jian1_btn.place(x=10, y=80)
            jian2_btn = tk.Radiobutton(nodis_window, text='监一栋/1楼/103', variable=radio_plcadd, value='监一栋/1楼/103')
            jian2_btn.place(x=70, y=80)
            jian3_btn = tk.Radiobutton(nodis_window, text='监二栋', variable=radio_plcadd,value='监二栋')
            jian3_btn.place(x=180, y=80)
            jian4_btn = tk.Radiobutton(nodis_window, text='监二栋/1楼/101', variable=radio_plcadd, value='监二栋/1楼/101')
            jian4_btn.place(x=240, y=80)
            jian5_btn = tk.Radiobutton(nodis_window, text='监三栋', variable=radio_plcadd,value='监三栋')
            jian5_btn.place(x=350, y=80)
            jian6_btn = tk.Radiobutton(nodis_window, text='监三栋/3楼/301', variable=radio_plcadd, value='监三栋/3楼/301')
            jian6_btn.place(x=410, y=80)

            # 提示语-报警说明
            pro_plcmag = tk.Label(nodis_window, text='报警说明')
            pro_plcmag.place(x=10, y=110)

            # 单选按钮-报警说明
            radio_plcmag=tk.StringVar()

            plcmag1_btn=tk.Radiobutton(nodis_window,text='区域入侵',variable=radio_plcmag,value='区域入侵')
            plcmag1_btn.place(x=10,y=130)
            plcmag2_btn = tk.Radiobutton(nodis_window, text='非法翻越', variable=radio_plcmag, value='非法翻越')
            plcmag2_btn.place(x=90, y=130)
            plcmag3_btn = tk.Radiobutton(nodis_window, text='浪费食物', variable=radio_plcmag, value='浪费食物')
            plcmag3_btn.place(x=180, y=130)
            plcmag4_btn = tk.Radiobutton(nodis_window, text='打架斗殴', variable=radio_plcmag, value='打架斗殴')
            plcmag4_btn.place(x=270, y=130)
            plcmag5_btn = tk.Radiobutton(nodis_window, text='其他警情', variable=radio_plcmag, value='其他警情')
            plcmag5_btn.place(x=360, y=130)

            # 提示语-报警级别
            pro_plcleve = tk.Label(nodis_window, text='报警级别')
            pro_plcleve.place(x=10, y=160)

            # 单选按钮-报警级别
            radio_plcleve=tk.StringVar()

            plcleve1_btn=tk.Radiobutton(nodis_window,text='一级',variable=radio_plcleve,value='01')
            plcleve1_btn.place(x=10,y=180)
            plcleve2_btn = tk.Radiobutton(nodis_window, text='二级', variable=radio_plcleve, value='02')
            plcleve2_btn.place(x=80, y=180)
            plcleve3_btn = tk.Radiobutton(nodis_window, text='三级', variable=radio_plcleve, value='03')
            plcleve3_btn.place(x=160, y=180)
            plcleve4_btn = tk.Radiobutton(nodis_window, text='四级', variable=radio_plcleve, value='04')
            plcleve4_btn.place(x=230, y=180)

            #提示语-报警人姓名
            pro_plcname=tk.Label(nodis_window,text='报警人姓名')
            pro_plcname.place(x=10,y=220)

            #文本框-输入报警人姓名
            input_plcname=tk.Text(nodis_window,height=1, width=20, bd=5, pady=5, padx=5)
            input_plcname.place(x=10,y=240)

            # 提示语-报警描述
            pro_plcdes=tk.Label(nodis_window,text='报警描述')
            pro_plcdes.place(x=10,y=280)

            #文本框-输入报警描述
            input_plcdes=tk.Text(nodis_window,height=1, width=40, bd=5, pady=5, padx=5)
            input_plcdes.place(x=10,y=300)

            #功能-提交接警
            def subplc():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                url ='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/addRecord'
                headers={'Content-Type':'application/json','token':token,'guestCode':guestCode}
                get_alrtime=input_distext.get(1.0, tk.END+"-1c")
                get_plcname=input_plcname.get(1.0, tk.END+"-1c")
                get_plcdes=input_plcdes.get(1.0, tk.END+"-1c")
                data_front={
                    "createTime": " ",
                    "handledTime": "",
                    "alarmTime":get_alrtime,
                    "address":radio_plcadd.get(),
                    "alarmMemo":radio_plcmag.get(),
                    "alarmLevelCode":radio_plcleve.get(),
                    "alarmPerson":get_plcname,
                    "alarmDescription":get_plcdes,
                    "receiverUserId":userId
                }
                #监1栋警情
                if radio_plcadd.get() =='监一栋':
                    data_after = {
                        "result": "",
                        "positionCode": "5223010030090300080020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91866657470413,\"latitude\":25.13827024150108,\"altitude\":65.78820653240608}",
                        "inRoom": 2,
                        "addressId": "522301-f05257da869443379d54b6117c7e9ca2",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    add_data={**data_front,**data_after}
                    data=json.dumps(add_data)
                    res=requests.post(url=url,headers=headers,data=data).json()
                    anfang_outmag.delete('1.0','end')
                    anfang_outmag.insert('1.0',res)

                #监一栋/1楼/103
                if radio_plcadd.get() =='监一栋/1楼/103':
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
                    add_data = {**data_front, **data_after}
                    data = json.dumps(add_data)
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

                # 监二栋
                if radio_plcadd.get() =='监二栋':
                    data_after ={
                        "result": "",
                        "positionCode": "5223010030090300250020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91812442487351,\"latitude\":25.13657776364555,\"altitude\":65.83604369036267}",
                        "inRoom": 2,
                        "addressId": "522301-e6e7fdd97a004c4dbfe1ae18dff1dc44",
                        "alarmSourceCode": "02",
                        "status": "0"
                        }
                    add_data = {**data_front, **data_after}
                    data = json.dumps(add_data)
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

                #监二栋/1楼/101
                if radio_plcadd.get() =='监二栋/1楼/101':
                    data_after ={
                        "result": "",
                        "positionCode": "5223010030090300250020010010101007200000",
                        "alarmAddressFloorId": "522301-bfbe31d4762e4481ad12faca722f7187",
                        "alarmCoordinate": "[0.3997897837903417,-2.149987578392025,4.64088885716837]",
                        "inRoom": 1,
                        "addressId": "522301-DCEE86EAA6C64A48B72397A105F07176",
                        "alarmSourceCode": "02",
                        "status": "0"
                        }
                    add_data = {**data_front, **data_after}
                    data = json.dumps(add_data)
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

                #监三栋
                if radio_plcadd.get() =='监三栋':
                    data_after = {
                        "result": "",
                        "positionCode": "5223010030090300110020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91928082206817,\"latitude\":25.138360192747538,\"altitude\":65.78392642732317}",
                        "inRoom": 2,
                        "addressId": "522301-82db70c673bc463db4bf74dc936ffaa8",
                        "alarmSourceCode": "02",
                        "status": "0"
                         }
                    add_data = {**data_front, **data_after}
                    data = json.dumps(add_data)
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

                    #监三栋/3楼/301
                if radio_plcadd.get() =='监三栋/3楼/301':
                    data_after ={
                            "result": "",
                            "positionCode": "5223010030090300030020030030101006300000",
                            "alarmAddressFloorId": "522301-d484a2818a6a479caf35366dfbe7148a",
                            "alarmCoordinate": "[-2.968560094905736,-1.6307787381579555,12.603140276020165]",
                            "inRoom": 1,
                            "addressId": "522301-3a8d121100e94a349e95a5ca3a61c28f",
                            "alarmSourceCode": "02",
                            "status": "0"
                        }
                    add_data = {**data_front, **data_after}
                    data = json.dumps(add_data)
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

            #按钮-接警
            btn_accplc=tk.Button(nodis_window,text='接警',height=2, width=16,command=lambda :subplc())
            btn_accplc.place(x=100,y=350)

        #按钮-未处置
        btn_nodis=tk.Button(anfang_window,text='未处置',height=1, width=8,command=lambda :nodis())
        btn_nodis.place(x=10,y=30)

        # 打开补录页面
        def addrec():
            window_addrec=tk.Toplevel(anfang_window)
            window_addrec.title('补录')
            window_addrec.geometry('650x550')
            window_addrec.resizable(False, False)

            #提示语-处警时间
            pro_handtime=tk.Label(window_addrec,text='处警时间(非必填 )')
            pro_handtime.place(x=10,y=10)

            #文本框-开始时间
            input_startime=tk.Text(window_addrec,height=1, width=20, bd=5, pady=5, padx=5)
            input_startime.place(x=10,y=30)

            #提示语-开始时间结束时间
            pro_time=tk.Label(window_addrec,text='开始时间---格式：2024-03-12 11:00:00---结束时间')
            pro_time.place(x=180,y=35)

            # 文本框-结束时间
            input_endtime=tk.Text(window_addrec,height=1, width=20, bd=5, pady=5, padx=5)
            input_endtime.place(x=480,y=30)

            #提示语-报警时间
            pro_plctime=tk.Label(window_addrec,text='报警时间（格式：2024-03-12 11:00:00）')
            pro_plctime.place(x=10,y=60)

            #文本框-报警时间
            input_plctext=tk.Text(window_addrec,height=1, width=20, bd=5, pady=5, padx=5)
            input_plctext.place(x=10,y=80)

            # 功能-此刻
            def now_time():
                curr_time = datetime.now()
                now_time = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                input_plctext.delete('1.0', 'end')
                input_plctext.insert('1.0', now_time)
                return now_time

            # 按钮-此刻
            btn_addtime = tk.Button(window_addrec, text='此刻', height=1, width=8, command=lambda: now_time())
            btn_addtime.place(x=180, y=80)

            #提示语-报警地点
            pro_plcadd=tk.Label(window_addrec,text='报警地点')
            pro_plcadd.place(x=10,y=110)

            # 单选按钮-报警地点
            radio_plcadd = tk.StringVar()

            jian1_btn = tk.Radiobutton(window_addrec, text='监一栋', variable=radio_plcadd, value='监一栋')
            jian1_btn.place(x=10, y=130)
            jian2_btn = tk.Radiobutton(window_addrec, text='监一栋/1楼/103', variable=radio_plcadd,value='监一栋/1楼/103')
            jian2_btn.place(x=70, y=130)
            jian3_btn = tk.Radiobutton(window_addrec, text='监二栋', variable=radio_plcadd, value='监二栋')
            jian3_btn.place(x=180, y=130)
            jian4_btn = tk.Radiobutton(window_addrec, text='监二栋/1楼/101', variable=radio_plcadd,value='监二栋/1楼/101')
            jian4_btn.place(x=240, y=130)
            jian5_btn = tk.Radiobutton(window_addrec, text='监三栋', variable=radio_plcadd, value='监三栋')
            jian5_btn.place(x=350, y=130)
            jian6_btn = tk.Radiobutton(window_addrec, text='监三栋/3楼/301', variable=radio_plcadd,value='监三栋/3楼/301')
            jian6_btn.place(x=410, y=130)

            # 提示语-报警说明
            pro_plcmag = tk.Label(window_addrec, text='报警说明')
            pro_plcmag.place(x=10, y=160)

            # 单选按钮-报警说明
            radio_plcmag = tk.StringVar()

            plcmag1_btn = tk.Radiobutton(window_addrec, text='区域入侵', variable=radio_plcmag, value='区域入侵')
            plcmag1_btn.place(x=10, y=180)
            plcmag2_btn = tk.Radiobutton(window_addrec, text='非法翻越', variable=radio_plcmag, value='非法翻越')
            plcmag2_btn.place(x=90, y=180)
            plcmag3_btn = tk.Radiobutton(window_addrec, text='浪费食物', variable=radio_plcmag, value='浪费食物')
            plcmag3_btn.place(x=180, y=180)
            plcmag4_btn = tk.Radiobutton(window_addrec, text='打架斗殴', variable=radio_plcmag, value='打架斗殴')
            plcmag4_btn.place(x=270, y=180)

            # 提示语-报警级别
            pro_plcleve = tk.Label(window_addrec, text='报警级别')
            pro_plcleve.place(x=10, y=210)

            # 单选按钮-报警级别
            radio_plcleve = tk.StringVar()

            plcleve1_btn = tk.Radiobutton(window_addrec, text='一级', variable=radio_plcleve, value='01')
            plcleve1_btn.place(x=10, y=230)
            plcleve2_btn = tk.Radiobutton(window_addrec, text='二级', variable=radio_plcleve, value='02')
            plcleve2_btn.place(x=80, y=230)
            plcleve3_btn = tk.Radiobutton(window_addrec, text='三级', variable=radio_plcleve, value='03')
            plcleve3_btn.place(x=160, y=230)
            plcleve4_btn = tk.Radiobutton(window_addrec, text='四级', variable=radio_plcleve, value='04')
            plcleve4_btn.place(x=230, y=230)

            # 提示语-报警人姓名
            pro_plcname = tk.Label(window_addrec, text='报警人姓名')
            pro_plcname.place(x=10, y=250)

            # 文本框-输入报警人姓名
            input_plcname = tk.Text(window_addrec, height=1, width=20, bd=5, pady=5, padx=5)
            input_plcname.place(x=10, y=270)

            # 提示语-报警描述
            pro_plcdes = tk.Label(window_addrec, text='报警描述')
            pro_plcdes.place(x=10, y=310)

            # 文本框-输入报警描述
            input_plcdes = tk.Text(window_addrec, height=1, width=40, bd=5, pady=5, padx=5)
            input_plcdes.place(x=10, y=330)

            # 提示语-处警结果
            pro_plcres=tk.Label(window_addrec,text='处警结果')
            pro_plcres.place(x=10,y=370)

            # 文本框-处警结果
            input_plcres=tk.Text(window_addrec, height=1, width=40, bd=5, pady=5, padx=5)
            input_plcres.place(x=10,y=390)

            def plcsave():
                uip=input_ipadr.get(1.0, tk.END + "-1c")
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/addRecord'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                starttime=input_startime.get(1.0, tk.END + "-1c")
                endtime=input_endtime.get(1.0,tk.END+"-1c")
                thistime=input_plctext.get(1.0, tk.END + "-1c")
                get_plcname=input_plcname.get(1.0, tk.END + "-1c")
                get_plcadd=radio_plcadd.get()
                get_plcmag=radio_plcmag.get()
                get_plcleve=radio_plcleve.get()
                get_plcdes=input_plcdes.get(1.0, tk.END + "-1c")
                get_plcres=input_plcres.get(1.0, tk.END + "-1c")
                data_front = {
                    "createTime": starttime,
                    "handledTime": endtime,
                    "alarmTime":thistime,
                    "address": get_plcadd,
                    "alarmMemo":get_plcmag,
                    "alarmLevelCode": get_plcleve,
                    "alarmPerson": get_plcname,
                    "alarmDescription": get_plcdes,
                    "receiverUserId": userId,
                    "result":get_plcres
                }
                if get_plcadd =='监一栋':
                    add_info = {
                        "positionCode": "5223010030090300080020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91866657470413,\"latitude\":25.13827024150108,\"altitude\":65.78820653240608}",
                        "inRoom": 2,
                        "addressId": "522301-f05257da869443379d54b6117c7e9ca2",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data=json.dumps({**data_front,**add_info})
                    res=requests.post(url=url,headers=headers,data=data).json()
                    anfang_outmag.delete('1.0','end')
                    anfang_outmag.insert('1.0',res)
                elif get_plcadd == '监一栋/1楼/103':
                    add_info = {
                        "positionCode": "5223010030090300010020010010301006500000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "[-2.338444465518915,-1.6307756742432518,4.991408488774528]",
                        "inRoom": 1,
                        "addressId": "522301-f9dfcc084f294fc5a959efe69465e555",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data = json.dumps({**data_front, **add_info})
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)
                elif get_plcadd == '监二栋':
                    add_info ={
                        "positionCode": "5223010030090300250020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91812442487351,\"latitude\":25.13657776364555,\"altitude\":65.83604369036267}",
                        "inRoom": 2,
                        "addressId": "522301-e6e7fdd97a004c4dbfe1ae18dff1dc44",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data = json.dumps({**data_front, **add_info})
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)
                elif get_plcadd == '监二栋/1楼/101':
                    add_info = {
                        "result": "",
                        "positionCode": "5223010030090300250020010010101007200000",
                        "alarmAddressFloorId": "522301-bfbe31d4762e4481ad12faca722f7187",
                        "alarmCoordinate": "[0.3997897837903417,-2.149987578392025,4.64088885716837]",
                        "inRoom": 1,
                        "addressId": "522301-DCEE86EAA6C64A48B72397A105F07176",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data = json.dumps({**data_front, **add_info})
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)
                elif get_plcadd == '监三栋':
                    add_info = {
                        "positionCode": "5223010030090300110020000000001000000000",
                        "alarmAddressFloorId": "",
                        "alarmCoordinate": "{\"longitude\":104.91928082206817,\"latitude\":25.138360192747538,\"altitude\":65.78392642732317}",
                        "inRoom": 2,
                        "addressId": "522301-82db70c673bc463db4bf74dc936ffaa8",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data = json.dumps({**data_front, **add_info})
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)
                elif get_plcadd == '监三栋/3楼/301':
                    add_info = {
                        "result": "",
                        "positionCode": "5223010030090300030020030030101006300000",
                        "alarmAddressFloorId": "522301-d484a2818a6a479caf35366dfbe7148a",
                        "alarmCoordinate": "[-2.968560094905736,-1.6307787381579555,12.603140276020165]",
                        "inRoom": 1,
                        "addressId": "522301-3a8d121100e94a349e95a5ca3a61c28f",
                        "alarmSourceCode": "02",
                        "status": "0"
                    }
                    data = json.dumps({**data_front, **add_info})
                    res = requests.post(url=url, headers=headers, data=data).json()
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', res)

            # 按钮-接警
            btn_plcsave=tk.Button(window_addrec,text='接警',height=2, width=16,command=lambda :plcsave())
            btn_plcsave.place(x=290,y=450)



        #按钮-补录
        btn_addre=tk.Button(anfang_window,text='补录',height=1, width=10,command=lambda :addrec())
        btn_addre.place(x=90,y=30)

        # 一键创建处理查询
        def credoit():
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
            twores=str(twoleveres.get('code'))
            foures=str(fourleveres.get('code'))
            if twores and foures =='200':
                twores='二级报警创建成功，result:'+str(twoleveres.get('result'))
                foures='四级报警创建成功，result:'+str(fourleveres.get('result'))
                anfang_outmag.delete('1.0', 'end')
                anfang_outmag.insert('end', twores+'\n')
                anfang_outmag.insert('end',foures+'\n')
                # 处理新增二级警情
                query_url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=2024-03-12+00:00:00&endDate=2024-03-19+23:59:59&address=&importantEquip='
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
                    mag='处理成功：'
                    twodo_result = 'msg：' + twolevegnore_res.get('msg') + '   result：' + twolevegnore_res.get('result')
                    anfang_outmag.insert('end',twodo_mag + '\n')
                    anfang_outmag.insert('end',mag+ '\n')
                    anfang_outmag.insert('end',twodo_result + '\n')

                elif twolevegnore_res.get('msg') != 'OK':
                    erromag='二级警情创建失败，检查'
                    btn_credoit.configure(bg='red')
                    anfang_outmag.delete('1.0', 'end')
                    anfang_outmag.insert('1.0', erromag)

                #四级警情（未作）



                # 查询-处理历史-一二三级
                beginDate = str((curr_time - timedelta(days=30)).date())
                endDate=datetime.strftime(curr_time, '%Y-%m-%d')
                otturl='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+beginDate+'+00:00:00&endDate='+endDate+'+23:59:59&positionCode=&pushStatus='
                ott_res = requests.get(url=otturl,headers=headers,params=None).json()
                ottrecords = ott_res.get('result').get('records')
                res_mag='处置历史最新数据：'
                anfang_outmag.insert('end', res_mag + '\n')
                ottnew ='一二三级警情：'+str(ottrecords[0])
                anfang_outmag.insert('end', ottnew+'\n')
                # 查询-处理历史-四级
                foururl='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+beginDate+'+00:00:00&endDate='+endDate+'+23:59:59&positionCode=&pushStatus='
                four_res=requests.get(url=foururl,headers=headers,params=None).json()
                fourrecords = four_res.get('result').get('records')
                fournew='四级警情：'+str(fourrecords[0])
                anfang_outmag.insert('end', fournew + '\n')






                btn_credoit.configure(bg='green')



            elif twores != '200':
                erromag='二级警情创建失败，检查创建警情参数配置'
                btn_credoit.configure(bg='red')
                anfang_outmag.delete('1.0', 'end')
                anfang_outmag.insert('1.0', erromag)


            elif foures != '200':
                erromag = '四级警情创建失败，检查创建警情参数配置'
                btn_credoit.configure(bg='red')
                anfang_outmag.delete('1.0', 'end')
                anfang_outmag.insert('1.0', erromag)










        # 按钮-一键创建
        btn_credoit=tk.Button(anfang_window,text='一键创建处理警情',height=1,width=20,command=lambda :credoit())
        btn_credoit.place(x=190,y=30)











        #提示语-警情中心
        pro_plccenter=tk.Label(anfang_window,text='警情中心')
        pro_plccenter.place(x=10,y=70)

        #提示语-实时警情
        pro_plccurr=tk.Label(anfang_window,text='------实时警情')
        pro_plccurr.place(x=10,y=90)

        #功能-警情查询
        def plcquery():
            window_plcquery=tk.Toplevel(anfang_window)
            window_plcquery.title('警情查询')
            window_plcquery.geometry('1050x700')
            window_plcquery.resizable(False, False)

            #文本框-输出查询消息-添加滚动条
            yscrollbar=Scrollbar(window_plcquery)
            yscrollbar.pack(side=RIGHT, fill=Y)
            out_plcquerymag=tk.Text(window_plcquery,height=50, width=70, bd=5, pady=5, padx=5)
            yscrollbar.config(command=out_plcquerymag.yview)
            out_plcquerymag.config(yscrollcommand=yscrollbar.set)
            out_plcquerymag.place(x=500,y=10)

            # 提示语-单一查询
            pro_sinquery=tk.Label(window_plcquery,text='单一查询')
            pro_sinquery.place(x=10,y=10)

            # 提示语-时间段
            pro_timequery=tk.Label(window_plcquery,text='------时间段（当前时间）,一二三级')
            pro_timequery.place(x=10,y=30)

            #功能-当天
            def todayquery():
                uip=input_ipadr.get(1.0, tk.END + "-1c")
                headers={'Content-Type':'application/json','token':token,'guestCode':guestCode}
                star=datetime.now()
                star1=datetime.strftime(star, '%Y-%m-%d')
                var1='+00:00:00'
                startime=star1+var1
                end=datetime.now()
                end1=datetime.strftime(end, '%Y-%m-%d')
                var2='+23:59:59'
                endtime=end1+var2
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+startime+'&endDate='+endtime+'&address=&importantEquip='
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0','end')
                out_plcquerymag.insert('1.0',res)

            #按钮-当天
            btn_today=tk.Button(window_plcquery,text='当天',height=1, width=10,command=lambda :todayquery())
            btn_today.place(x=10,y=60)

            #功能-7天内
            def weekquery():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtinme=datetime.now()
                upweektime=datetime.strftime(nowtinme - timedelta(days=nowtinme.weekday() + 7),'%Y-%m-%d')
                var1='+00:00:00'
                out_upweek=upweektime+var1
                currtime=datetime.strftime(nowtinme,'%Y-%m-%d')
                var2='+23:59:59'
                out_currtime=currtime+var2
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + out_upweek + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-7天内
            btn_week=tk.Button(window_plcquery,text='7天内',height=1, width=10,command=lambda :weekquery())
            btn_week.place(x=90,y=60)

            #功能-30天内
            def monthquery():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1='+00:00:00'
                thirty_days_ago=thirty_days+var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + thirty_days_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-30天内
            btn_month=tk.Button(window_plcquery,text='30天内',height=1, width=10,command=lambda :monthquery())
            btn_month.place(x=170,y=60)

            # 提示语-报警来源（默认30天）
            pro_plccome = tk.Label(window_plcquery, text='------报警来源（当前时间前30天内）,一二三级')
            pro_plccome.place(x=10, y=90)

            #功能-报警来源-查询设备
            def devicequery():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmSourceCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&'+alarmSourceCode+'&alarmLevelCode=&alarmMemo=&beginDate='+thirty_days_ago+'&endDate='+out_currtime+'&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-报警来源-设备
            btn_device=tk.Button(window_plcquery,text='设备',height=1, width=10,command=lambda :devicequery())
            btn_device.place(x=10,y=120)

            #提示语
            pro_oneleve = tk.Label(window_plcquery, text='------报警级别（当前时间前30天内）,一二三级')
            pro_oneleve.place(x=10, y=150)

            #功能-一级
            def oneleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + thirty_days_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-一级
            btn_oneleve=tk.Button(window_plcquery,text='一级',height=1, width=10,command=lambda :oneleve())
            btn_oneleve.place(x=10,y=180)

            #提示语-报警地点
            pro_plcadd = tk.Label(window_plcquery, text='------报警地点（当前时间前30天内）,一二三级')
            pro_plcadd.place(x=10, y=210)

            #功能-监一栋
            def onebuil():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                address='%E7%9B%91%E4%B8%80%E6%A0%8B'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + thirty_days_ago + '&endDate=' + out_currtime + '&address=' + address + '&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            # 按钮-监一栋
            btn_onebuil=tk.Button(window_plcquery,text='监一栋',height=1, width=10,command=lambda :onebuil())
            btn_onebuil.place(x=10,y=240)

            # 提示语-时间段
            pro_timequery = tk.Label(window_plcquery, text='------时间段（当前时间）,四级')
            pro_timequery.place(x=10, y=300)

            #功能-4级当天
            def fourtoday():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                star = datetime.now()
                star1 = datetime.strftime(star, '%Y-%m-%d')
                var1 = '+00:00:00'
                startime = star1 + var1
                end = datetime.now()
                end1 = datetime.strftime(end, '%Y-%m-%d')
                var2 = '+23:59:59'
                endtime = end1 + var2
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+startime+'&endDate='+endtime+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            # 按钮-4级当天
            btn_fourtoday=tk.Button(window_plcquery,text='当天',height=1, width=10,command=lambda :fourtoday())
            btn_fourtoday.place(x=10,y=330)

            #功能-4级7天内
            def fourweek():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtinme = datetime.now()
                upweektime = datetime.strftime(nowtinme - timedelta(days=nowtinme.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                out_upweek = upweektime + var1
                currtime = datetime.strftime(nowtinme, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+out_upweek+'&endDate='+out_currtime+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-4级7天内
            btn_fourweek=tk.Button(window_plcquery,text='7日内',height=1, width=10,command=lambda :fourweek())
            btn_fourweek.place(x=90,y=330)

            #功能-4级30天内
            def fourmonth():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+thirty_days_ago+'&endDate='+out_currtime+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-4级30天内
            btn_fourmonth=tk.Button(window_plcquery,text='30日内',height=1, width=10,command=lambda :fourmonth())
            btn_fourmonth.place(x=170,y=330)

            # 提示语-4报警来源（默认30天）
            pro_fourcome = tk.Label(window_plcquery, text='------报警来源（当前时间前30天内）,四级')
            pro_fourcome.place(x=10, y=360)

            #功能-报警来源-查询设备
            def fourdevice():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmSourceCode = '01'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode='+alarmSourceCode+'&alarmLevelCode=&alarmMemo=&beginDate='+thirty_days_ago+'&endDate='+out_currtime+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            # 按钮-报警来源-设备
            btn_fourdevice = tk.Button(window_plcquery, text='设备', height=1, width=10,command=lambda :fourdevice())
            btn_fourdevice.place(x=10, y=390)

            # 提示语-报警级别-四级
            pro_fourleve = tk.Label(window_plcquery, text='------报警级别（当前时间前30天内）,四级')
            pro_fourleve.place(x=10, y=420)

            #功能-报警级别-四级
            def fourleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '04'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=01&alarmLevelCode='+alarmLevelCode+'&alarmMemo=&beginDate='+thirty_days_ago+'&endDate='+out_currtime+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-报警等级-四级
            btn_fourleve=tk.Button(window_plcquery,text='四级', height=1, width=10,command=lambda :fourleve())
            btn_fourleve.place(x=10,y=450)

            # 提示语-报警地点-四级
            pro_fouradd = tk.Label(window_plcquery, text='------报警地点（当前时间前30天内）,四级')
            pro_fouradd.place(x=10, y=480)

            #功能-报警地点(监1栋)-四级
            def fouradd():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                thirty_days = str((nowtime - timedelta(days=30)).date())
                var1 = '+00:00:00'
                thirty_days_ago = thirty_days + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                address='%E7%9B%91%E4%B8%80%E6%A0%8B'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+thirty_days_ago+'&endDate='+out_currtime+'&address='+address+'&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            # 按钮-报警地点-四级
            btn_fouradd=tk.Button(window_plcquery,text='监一栋',height=1, width=10,command=lambda :fouradd())
            btn_fouradd.place(x=10,y=510)

        #按钮-警情查询
        btn_plcquery=tk.Button(anfang_window,text='警情查询',command=lambda :plcquery())
        btn_plcquery.place(x=10,y=110)

        #功能-警情处理
        def plchandwin():
            window_plchand=tk.Toplevel(anfang_window)
            window_plchand.title('警情处理')
            window_plchand.geometry('1050x700')
            window_plchand.resizable(False, False)

            # 文本框-输出处理结果-添加滚动条
            yscrollbar = Scrollbar(window_plchand)
            yscrollbar.pack(side=RIGHT, fill=Y)
            out_plchandmag=tk.Text(window_plchand,height=50, width=70, bd=5, pady=5, padx=5)
            yscrollbar.config(command=out_plchandmag.yview)
            out_plchandmag.config(yscrollcommand=yscrollbar.set)
            out_plchandmag.place(x=500, y=10)

            #提示语-一二三四级警情处理
            pro_otthand=tk.Label(window_plchand,text='一二三四级警情处理')
            pro_otthand.place(x=10,y=10)

            #提示语-预案
            pro_plan=tk.Label(window_plchand,text='----预案')
            pro_plan.place(x=10,y=30)

            def getplan():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                url='http://'+uip+'/smartSecurityAPI/sheme/queryPage?pageSize=1000'
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', res)

            #按钮-当前预案
            btn_getplan=tk.Button(window_plchand,text='预案信息',height=1, width=10,command=lambda :getplan())
            btn_getplan.place(x=10,y=60)











            #提示语-一级警情处理
            pro_onelevehand=tk.Label(window_plchand,text='----一级警情')
            pro_onelevehand.place(x=10,y=90)

            #功能-查询最新一级警情
            def plconeleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime=datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7),'%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', res)

            #按钮-最新一级警情
            btn_plconeleve=tk.Button(window_plchand,text='最新',height=1, width=10,command=lambda :plconeleve())
            btn_plconeleve.place(x=10,y=120)

            #功能-处置一级警情-忽略
            def oneleveignore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI= alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult='http://'+uip+'/smartSecurityAPI/alarmHandler/alarmHandled'
                data=json.dumps({
                        "alarmHandlingCode": "0",
                        "handleResult": "忽略",
                        "action": 0,
                        "alarmId": alarmId
                        })
                gnore_res=requests.post(url=urlresult,headers=headers,data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            #按钮-处置一级警情默认最新一条-忽略
            btn_plcdoleve=tk.Button(window_plchand,text='忽略',height=1,width=10,command=lambda :oneleveignore())
            btn_plcdoleve.place(x=90,y=120)

            #功能-处置一级警情-处置
            def onelevedis():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "1",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            #按钮-处置一级警情默认最新一条-处置
            btn_plcdolevedis=tk.Button(window_plchand,text='处置',height=1,width=10,command=lambda :onelevedis())
            btn_plcdolevedis.place(x=170,y=120)

            # 功能-处置一级警情-处置并上报
            def plcdolevedisesc():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '01'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "2",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置一级警情默认最新一条-处置并上报
            btn_plcdolevedisesc=tk.Button(window_plchand,text='处置并上报',height=1,width=10,command=lambda :plcdolevedisesc())
            btn_plcdolevedisesc.place(x=250,y=120)

            # 提示语-二级警情处理
            pro_twolevehand =tk.Label(window_plchand,text='----二级警情')
            pro_twolevehand.place(x=10,y=150)

            # 功能-查询最新二级警情
            def plctwoleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '02'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', res)

            # 按钮-最新二级警情
            btn_twolevehand=tk.Button(window_plchand,text='最新',height=1,width=10,command=lambda :plctwoleve())
            btn_twolevehand.place(x=10,y=180)

            # 功能-处置二级警情-忽略
            def twoleveignore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '02'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "0",
                    "handleResult": "忽略",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置二级警情默认最新一条-忽略
            btn_twoleveignore=tk.Button(window_plchand,text='忽略',height=1,width=10,command=lambda :twoleveignore())
            btn_twoleveignore.place(x=90,y=180)

            #处置二级警情-处置
            def twolevedis():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '02'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "1",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置二级警情默认最新一条-处置
            btn_twolevedis=tk.Button(window_plchand,text='处置',height=1,width=10,command=lambda :twolevedis())
            btn_twolevedis.place(x=170,y=180)

            # 功能-处置二级警情-处置并上报
            def twolevedisesc():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '02'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "2",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置二级警情默认最新一条-处置并上报
            btn_twolevedisesc=tk.Button(window_plchand,text='处置并上报',height=1,width=10,command=lambda :twolevedisesc())
            btn_twolevedisesc.place(x=250,y=180)

            # 提示语-三级警情处理
            pro_threehand=tk.Label(window_plchand,text='----三级警情')
            pro_threehand.place(x=10,y=210)

            # 功能-查询最新三级警情
            def plcthreeleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '03'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', res)

            # 按钮-最新三级警情
            btn_threelevehand=tk.Button(window_plchand,text='最新',height=1,width=10,command=lambda :plcthreeleve())
            btn_threelevehand.place(x=10,y=240)

            # 功能-处置三级警情-忽略
            def threelevegnore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '03'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "0",
                    "handleResult": "忽略",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置三级警情默认最新一条-忽略
            btn_threelevegnore=tk.Button(window_plchand,text='忽略',height=1,width=10,command=lambda :threelevegnore())
            btn_threelevegnore.place(x=90,y=240)

            # 功能-处置三级警情默认最新一条-处置
            def threelevedis():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '03'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "1",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置三级警情默认最新一条-处置
            btn_threelevedis=tk.Button(window_plchand,text='处置',height=1,width=10,command=lambda :threelevedis())
            btn_threelevedis.place(x=170,y=240)

            # 功能-处置三级警情-处置并上报
            def threelevedisesc():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '03'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "2",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置三级警情默认最新一条-处置并上报
            btn_threelevedisesc=tk.Button(window_plchand,text='处置并上报',height=1,width=10,command=lambda :threelevedisesc())
            btn_threelevedisesc.place(x=250,y=240)

            # 提示语-四级警情处理
            pro_fourlevehand=tk.Label(window_plchand,text='----四级警情')
            pro_fourlevehand.place(x=10,y=270)

            # 功能-查询最新四级警情
            def fourlevehand():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '04'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', res)

            # 按钮-最新四级警情
            btn_fourlevehand=tk.Button(window_plchand,text='最新',height=1,width=10,command=lambda :fourlevehand())
            btn_fourlevehand.place(x=10,y=300)

            # 功能-处置四级警情-忽略
            def fourlevegnore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '04'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "0",
                    "handleResult": "忽略",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置四级警情默认最新一条-忽略
            btn_fourlevegnore=tk.Button(window_plchand,text='忽略',height=1,width=10,command=lambda :fourlevegnore())
            btn_fourlevegnore.place(x=90,y=300)

            # 功能-处置四级警情默认最新一条-处置
            def fourlevedis():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '04'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "1",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置四级警情默认最新一条-处置
            btn_fourlevedis=tk.Button(window_plchand,text='处置',height=1,width=10,command=lambda :fourlevedis())
            btn_fourlevedis.place(x=170,y=300)

            # 功能-处置三级警情-处置并上报
            def fourlevedisesc():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                nowtime = datetime.now()
                upweektime = datetime.strftime(nowtime - timedelta(days=nowtime.weekday() + 7), '%Y-%m-%d')
                var1 = '+00:00:00'
                week_ago = upweektime + var1
                currtime = datetime.strftime(nowtime, '%Y-%m-%d')
                var2 = '+23:59:59'
                out_currtime = currtime + var2
                alarmLevelCode = '04'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&pushStatus=0,1&alarmSourceCode=&alarmLevelCode=' + alarmLevelCode + '&alarmMemo=&beginDate=' + week_ago + '&endDate=' + out_currtime + '&address=&importantEquip='
                res = requests.get(url=url, headers=headers, params=None).json()
                alarm = res.get('result').get('records')
                alarmI = alarm[0]
                alarmId = str(alarmI.get('alarmId'))
                urlresult = 'http://' + uip + '/smartSecurityAPI/alarmHandler/alarmHandled'
                data = json.dumps({
                    "alarmHandlingCode": "2",
                    "handleResult": "处置",
                    "action": 0,
                    "alarmId": alarmId
                })
                gnore_res = requests.post(url=urlresult, headers=headers, data=data).json()
                out_plchandmag.delete('1.0', 'end')
                out_plchandmag.insert('1.0', gnore_res)

            # 按钮-处置四级警情默认最新一条-处置并上报
            btn_fourlevedisesc=tk.Button(window_plchand,text='处置并上报',height=1,width=10,command=lambda :fourlevedisesc())
            btn_fourlevedisesc.place(x=250,y=300)

        #按钮-警情处理
        btn_plchand=tk.Button(anfang_window,text='警情处理',command=lambda :plchandwin())
        btn_plchand.place(x=80,y=110)

        # 提示语-处警历史查询
        pro_plcdishic = tk.Label(anfang_window, text='------处警历史')
        pro_plcdishic.place(x=10,y=150)


        # 功能-警情查询
        def plcdishic():
            window_plcdishic = tk.Toplevel(anfang_window)
            window_plcdishic.title('警情查询')
            window_plcdishic.geometry('1050x700')
            window_plcdishic.resizable(False, False)

            # 文本框-输出查询消息-添加滚动条
            yscrollbar = Scrollbar(window_plcdishic)
            yscrollbar.pack(side=RIGHT, fill=Y)
            out_plcquerymag = tk.Text(window_plcdishic, height=50, width=70, bd=5, pady=5, padx=5)
            yscrollbar.config(command=out_plcquerymag.yview)
            out_plcquerymag.config(yscrollcommand=yscrollbar.set)
            out_plcquerymag.place(x=500, y=10)

            #提示语—单一查询
            pro_onesele=tk.Label(window_plcdishic,text='单一查询')
            pro_onesele.place(x=10,y=10)

            #提示语-时间段
            pro_timeslot=tk.Label(window_plcdishic,text='------时间段（当前时间），一二三级')
            pro_timeslot.place(x=10,y=30)

            #功能-当天
            def plctoday():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_time=datetime.strftime(datetime.now(),'%Y-%m-%d')
                url ='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_time+'+00:00:00&endDate='+plc_time+'+23:59:59&positionCode=&pushStatus='
                headers={'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0','end')
                out_plcquerymag.insert('1.0',res)

            #按钮-当天
            btn_plctoday=tk.Button(window_plcdishic,text='当天',height=1, width=10,command=lambda :plctoday())
            btn_plctoday.place(x=10,y=60)

            #功能-7天内
            def plcweek():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_weekago = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday() + 7),'%Y-%m-%d')
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_weekago + '+00:00:00&endDate=' + plc_today + '+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0','end')
                out_plcquerymag.insert('1.0',res)

            #按钮-7天内
            btn_plcweek=tk.Button(window_plcdishic,text='7天内',height=1, width=10,command=lambda :plcweek())
            btn_plcweek.place(x=90,y=60)

            #功能-30天内
            def plcmonth():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago=str((datetime.now() - timedelta(days=30)).date())
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_monthago + '+00:00:00&endDate=' + plc_today + '+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0','end')
                out_plcquerymag.insert('1.0',res)

            #按钮-30天内
            btn_plcmonth=tk.Button(window_plcdishic,text='30天内',height=1, width=10,command=lambda :plcmonth())
            btn_plcmonth.place(x=170,y=60)

            #提示语-报警来源
            pro_plcsou=tk.Label(window_plcdishic,text='------报警来源（当前时间30天内），一二三级')
            pro_plcsou.place(x=10,y=90)

            #功能-设备
            def plcdevice():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                alarmSourceCode='01'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode='+alarmSourceCode+'&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-设备
            btn_plcdevice=tk.Button(window_plcdishic,text='设备',height=1, width=10,command=lambda :plcdevice())
            btn_plcdevice.place(x=10,y=120)

            #提示语-报警级别
            pro_plcleve=tk.Label(window_plcdishic,text='------报警级别（当前时间前30天内），一二三级')
            pro_plcleve.place(x=10,y=150)

            #功能-一级
            def plconeleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                alarmLevelCode='01'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode='+alarmLevelCode+'&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-一级
            btn_plconeleve=tk.Button(window_plcdishic,text='一级',height=1, width=10,command=lambda :plconeleve())
            btn_plconeleve.place(x=10,y=180)

            #提示语-报警地点
            pro_plcadd=tk.Label(window_plcdishic,text='------报警地点（当前时间前30天内），一二三级')
            pro_plcadd.place(x=10,y=210)

            #功能-监一栋
            def plconeadd():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                positionCode = '5223010030090300080020000000001000000000'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode='+positionCode+'&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-监一栋
            btn_plconeadd=tk.Button(window_plcdishic,text='监一栋',height=1, width=10,command=lambda :plconeadd())
            btn_plconeadd.place(x=10,y=240)

            #提示语-处置状态
            pro_plcdista=tk.Label(window_plcdishic,text='------处置状态（当前时间前30天内），一二三级')
            pro_plcdista.place(x=10,y=270)

            #功能-忽略
            def plcignore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                pushStatus = '2'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&pushStatus='+pushStatus
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-忽略
            btn_plcignore=tk.Button(window_plcdishic,text='忽略',height=1, width=10,command=lambda :plcignore())
            btn_plcignore.place(x=10,y=300)

            #功能-已处置
            def plcdispos():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                pushStatus = '3'
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_monthago + '+00:00:00&endDate=' + plc_today + '+23:59:59&pushStatus=' + pushStatus
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-已处置
            btn_plcdispos=tk.Button(window_plcdishic,text='已处置',height=1, width=10,command=lambda :plcdispos())
            btn_plcdispos.place(x=90,y=300)

            #提示语-时间端（4级）
            pro_fourtimelot=tk.Label(window_plcdishic,text='------时间段（当前时间）,四级')
            pro_fourtimelot.place(x=10,y=380)

            #功能-当天（4级）
            def plcfourtoday():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_today+'+00:00:00&endDate='+plc_today+'+23:59:59&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-当天（4级）
            btn_plcfourtoday=tk.Button(window_plcdishic,text='当天',height=1, width=10,command=lambda :plcfourtoday())
            btn_plcfourtoday.place(x=10,y=410)

            #功能-7天内（4级）
            def plcfourweekago():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_weekago = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday() + 7),'%Y-%m-%d')
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_weekago + '+00:00:00&endDate=' + plc_today + '+23:59:59&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-7天内（4级）
            btn_plcfourweekago=tk.Button(window_plcdishic,text='7天内',height=1, width=10,command=lambda :plcfourweekago())
            btn_plcfourweekago.place(x=90,y=410)

            #功能-30天内（4级）
            def plcfourmonth():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_monthago + '+00:00:00&endDate=' + plc_today + '+23:59:59&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-30天内（4级）
            btn_plcfourmonth=tk.Button(window_plcdishic,text='30天内',height=1, width=10,command=lambda :plcfourmonth())
            btn_plcfourmonth.place(x=170,y=410)

            #提示语-报警来源（4级）
            pro_plcfoursou=tk.Label(window_plcdishic,text='------报警来源（当前时间30天内），四级')
            pro_plcfoursou.place(x=10,y=440)

            #功能-设备（4级）
            def plcfourdevice():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                alarmSourceCode = '01'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode='+alarmSourceCode+'&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-设备（4级）
            btn_plcfourdevice=tk.Button(window_plcdishic,text='设备',height=1, width=10,command=lambda :plcfourdevice())
            btn_plcfourdevice.place(x=10,y=470)

            #提示语-报警级别（4级）
            pro_plcfourleve=tk.Label(window_plcdishic,text='------报警级别（当前时间30天内），四级')
            pro_plcfourleve.place(x=10,y=500)

            #功能-四级（4级）
            def plcfourleve():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                alarmLevelCode = '04'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode='+alarmLevelCode+'&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode=&pushStatus='
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-一级（4级）
            btn_plcfourleve=tk.Button(window_plcdishic,text='四级',height=1, width=10,command=lambda :plcfourleve())
            btn_plcfourleve.place(x=10,y=530)

            #提示语-报警地点（4级）
            pro_plcfouradd=tk.Label(window_plcdishic,text='------报警地点（当前时间30天内），四级')
            pro_plcfouradd.place(x=10,y=560)

            #功能-监一栋（4级）
            def plcfouroneadd():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                positionCode='5223010030090300080020000000001000000000'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&positionCode='+positionCode
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-监一栋（4级）
            btn_plcfouroneadd=tk.Button(window_plcdishic,text='监一栋',height=1, width=10,command=lambda :plcfouroneadd())
            btn_plcfouroneadd.place(x=10,y=590)

            #提示语-处置状态（4级）
            pro_plcfourdista=tk.Label(window_plcdishic,text='------处置状态（当前时间30天内），四级')
            pro_plcfourdista.place(x=10,y=620)

            #功能-忽略（4级）
            def plcfourignore():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                pushStatus = '2'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate='+plc_monthago+'+00:00:00&endDate='+plc_today+'+23:59:59&pushStatus='+pushStatus
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-忽略（4级）
            btn_plcfourignore=tk.Button(window_plcdishic,text='忽略',height=1, width=10,command=lambda :plcfourignore())
            btn_plcfourignore.place(x=10,y=650)

            #功能-已处置（4级）
            def plcfourdispos():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                plc_monthago = str((datetime.now() - timedelta(days=30)).date())
                pushStatus = '3'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                url = 'http://' + uip + '/smartSecurityAPI/alarmMessages/alarm/getFourLevelAlarmMessages?currentPage=1&pageSize=10&alarmSourceCode=&alarmLevelCode=&alarmMemo=&beginDate=' + plc_monthago + '+00:00:00&endDate=' + plc_today + '+23:59:59&pushStatus=' + pushStatus
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-已处置（4级）
            btn_plcfourdispos=tk.Button(window_plcdishic,text='已处置',height=1, width=10,command=lambda :plcfourdispos())
            btn_plcfourdispos.place(x=90,y=650)

        #按钮-处置历史
        btn_plcdishic=tk.Button(anfang_window,text='处置历史',command=lambda :plcdishic())
        btn_plcdishic.place(x=10,y=170)

        #功能-警情分析
        def plcana():
            window_plcana=tk.Toplevel(anfang_window)
            window_plcana.title('警情分析')
            window_plcana.geometry('1050x700')
            window_plcana.resizable(False,False)

            #文本框-输出分析结果-添加滚动条
            yscrollbar = Scrollbar(window_plcana)
            yscrollbar.pack(side=RIGHT, fill=Y)
            out_plcquerymag = tk.Text(window_plcana, height=50, width=70, bd=5, pady=5, padx=5)
            yscrollbar.config(command=out_plcquerymag.yview)
            out_plcquerymag.config(yscrollcommand=yscrollbar.set)
            out_plcquerymag.place(x=500, y=10)

            #提示语-天周月年
            pro_dayweemon=tk.Label(window_plcana,text='------按照当天/本周/本月/本年进行查询')
            pro_dayweemon.place(x=10,y=10)

            #功能-当天
            def today():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                plc_today=datetime.strftime(datetime.now(),'%Y-%m-%d')
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=day&beginTime='+plc_today+'+00:00:00&endTime='+plc_today+'+23:59:59'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res=requests.get(url=url,headers=headers,params=None).json()
                out_plcquerymag.delete('1.0','end')
                out_plcquerymag.insert('1.0',res)

            #按钮-当天
            btn_today=tk.Button(window_plcana,text='当天',height=1, width=10,command=lambda :today())
            btn_today.place(x=10,y=40)

            #功能-本周
            def week():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday()), '%Y-%m-%d')
                this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()),'%Y-%m-%d')
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=week&beginTime='+this_week_start+'+00:00:00&endTime='+this_week_end+'+23:59:59'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-本周
            btn_week=tk.Button(window_plcana,text='本周',height=1, width=10,command=lambda :week())
            btn_week.place(x=90,y=40)

            #功能-当月
            def month():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                this_month_start = datetime.strftime(datetime(datetime.now().year, datetime.now().month, 1), '%Y-%m-%d')
                this_month_end = datetime.strftime(datetime(datetime.now().year, datetime.now().month + 1, 1) - timedelta(days=1),'%Y-%m-%d')
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=month&beginTime='+this_month_start+'+00:00:00&endTime='+this_month_end+'+23:59:59'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-当月
            btn_month=tk.Button(window_plcana,text='当月',height=1, width=10,command=lambda :month())
            btn_month.place(x=170,y=40)

            #功能-本年
            def year():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                this_year_start = datetime.strftime(datetime(datetime.now().year, 1, 1), '%Y-%m-%d')
                this_year_end = datetime.strftime(datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1),'%Y-%m-%d')
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/queryAlarmCount?address=&fixTime=year&beginTime='+this_year_start+'&endTime='+this_year_end+'+23:59:59'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)

            #按钮-本年
            btn_year=tk.Button(window_plcana,text='当年',height=1, width=10,command=lambda :year())
            btn_year.place(x=250,y=40)

            #提示语-报警地点
            pro_plcadd=tk.Label(window_plcana,text='报警地点(默认查询本周)')
            pro_plcadd.place(x=10,y=70)

            #功能-监一栋
            def plcone():
                uip = input_ipadr.get(1.0, tk.END + "-1c")
                this_week_start = datetime.strftime(datetime.now() - timedelta(days=datetime.now().weekday()),'%Y-%m-%d')
                this_week_end = datetime.strftime(datetime.now() + timedelta(days=6 - datetime.now().weekday()),'%Y-%m-%d')
                address = '522301-f05257da869443379d54b6117c7e9ca2'
                url='http://'+uip+'/smartSecurityAPI/alarmMessages/queryAlarmCount?address='+address+'&fixTime=week&beginTime='+this_week_start+'+00:00:00&endTime='+this_week_end+'+23:59:59'
                headers = {'Content-Type': 'application/json', 'token': token, 'guestCode': guestCode}
                res = requests.get(url=url, headers=headers, params=None).json()
                out_plcquerymag.delete('1.0', 'end')
                out_plcquerymag.insert('1.0', res)




            #按钮-监一栋
            btn_plcone=tk.Button(window_plcana,text='监一栋',height=1, width=10,command=lambda :plcone())
            btn_plcone.place(x=10,y=100)









        #按钮-警情分析
        btn_plcana=tk.Button(anfang_window,text='警情分析',command=lambda :plcana())
        btn_plcana.place(x=80,y=170)








    # if radio_var == '指挥':

#按钮-登录
Logbtn=tk.Button(root,text='登录',height=1, width=8,command=lambda :login())
Logbtn.place(x=10,y=230)

#功能-重置
def Btn_resetting():
    input_Poltext.delete('1.0','end')
    input_Pwdtext.delete('1.0','end')
    out_Magtext.delete('1.0','end')
    input_ipadr.delete('1.0','end')

#按钮-重置
Resbtn=tk.Button(root,text='重置',height=1, width=8,command=lambda :Btn_resetting())
Resbtn.place(x=100,y=230)

root.mainloop()