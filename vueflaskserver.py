from flask import Flask
from flask import request
from flask import make_response
from flask_cors import CORS

from werkzeug.utils import secure_filename
import json
import datetime
import os
import random
import string
import cv2


Server = Flask(__name__)
#解决跨域问题
cors = CORS(Server, supports_credentials=True)

Server.debug=True
accountList=[]
userList=[]
MenuList=[]
roleslist = []
bosspowerlist = []
employeepowerlist = []
categories = []
paramlist = []
goodslist = []
orderlist = []
progresslist = []

Token = 'bearer asdasdasdasdasd1234561234512345132'

#登陆账号
class Account():
    def __init__(self,account,password):
        self.account = account
        self.password = password
    def get_res(self):
        return {"account":self.account, "password":self.password} #dict
    def Print_self(self):
        print("account:"+ self.account + " password:" +self.password)
    def get_account(self):
        return self.account
    def get_password(self):
        return self.password
    def set_account(self,account):
        self.account = account
    def set_password(self,password):
        self.password = password
#用户列表
class User():
    def __init__(self,id,name,sex,email,mobilephone,address,state,option):
        self.id = id
        self.name = name
        self.sex = sex
        self.email = email
        self.mobilephone = mobilephone
        self.address = address
        self.state = state
        self.option = option
    def get_res(self):
        return {"id":self.id, "name":self.name, "sex":self.sex, "email":self.email, "mobilephone":self.mobilephone, "address":self.address, "state":self.state, "option":self.option} 
    def get_id(self):
        return self.id
    def set_Info(self,name,sex,email,mobilephone,address,state,option):
        self.name = name
        self.sex = sex
        self.email = email
        self.mobilephone = mobilephone
        self.address = address
        self.state = state
        self.option = option
    def get_name(self):
        return self.name

#商品
class Goods():
    """docstring for ClassName"""
    def __init__(self, id,name,price,weight,createtime):
        self.id = id
        self.name = name
        self.price = price
        self.weight = weight
        self.createtime = createtime
    def get_res(self):
        return {"id":self.id,"name":self.name,"price":self.price,"weight":self.weight,"createtime":self.createtime}
    def get_id(self):
        return self.id
    def set_Into(self,name,price,weight,createtime):
        self.name = name
        self.price = price
        self.weight = weight
        self.createtime = createtime
    def get_name(self):
        return self.name

#返回的商品列表
class ReultGoods():
    def __init__(self,total,page,goodslist):
        self.total = total
        self.page = page
        self.goodslist = goodslist
    def  get_res(self):
        return {"total":self.total, "page":self.page, "goodslist":self.goodslist}  

#返回用户列表
class UserList():
    def __init__(self,total,page,people):
        self.total = total
        self.page = page
        self.people = people
    def get_res(self):
        return {"total":self.total, "page":self.page, "people":self.people}    
#返回结果
class ResultMsg():
    def __init__(self,code,msg,data):
        self.code = code
        self.msg = msg
        self.data = data
    def get_res(self):
        return {"code":self.code, "msg":self.msg, "data":self.data} 
#菜单列表
class Menu():
    def __init__(self,id,name,path,level,items):
        self.id = id
        self.name = name
        self.path = path
        self.level = level
        self.items = items
    def get_res(self):
        return {"id":self.id, "name":self.name, "path":self.path,"level":self.level, "items":self.items}    
#角色
class Role():
    def __init__(self,id, name,level,description,items):
        self.id = id
        self.name = name
        self.level = level
        self.description = description
        self.items = items
    def get_res(self):
        return {"id":self.id,"name":self.name, "level":self.level, "description":self.description, "items":self.items}    
    def get_id(self):
        return self.id
    def set_Info(self,name,level,description):
        self.name = name
        self.level = level
        self.description = description
#种类
class Category():
    """docstring for Category"""
    def __init__(self, id,name,useful,level,children):
        self.id = id
        self.name = name
        self.useful = useful
        self.level = level
        self.children = children
    def get_res(self):
        return {"id":self.id,"name":self.name, "useful":self.useful, "level":self.level, "children":self.children}    
    def get_id(self):
        return self.id
    def get_items(self):
        return self.children
#参数
class Param():
    def __init__(self,id,name,onlyvalue,items):
       self.id = id 
       self.name = name
       self.onlyvalue = onlyvalue
       self.items = items
    def get_res(self):
        return {"id":self.id,"name":self.name,"onlyvalue":self.onlyvalue,"items":self.items}
    def get_id(self):
        return self.id
    def get_items(self):
        return self.items

#订单
class Order(object):
    """docstring for Order"""
    def __init__(self, id,number,price,paied,send,ordertime):
        self.id = id
        self.number = number
        self.price = price
        self.paied = paied
        self.send = send
        self.ordertime = ordertime
    def get_res(self):
        return {"id":self.id,"number":self.number,"price":self.price,"paied":self.paied,"send":self.send,"ordertime":self.ordertime}   
    def set_Into(self,number,price,paied,send,ordertime):
        self.number = number
        self.price = price
        self.paied = paied
        self.send = send
        self.ordertime = ordertime

#物流
class  Progress(object):
    """docstring for  Progress"""
    def __init__(self, id,time,ftime,context,location):
        self.id = id
        self.time = time
        self.ftime = ftime
        self.context = context
        self.location = location
    def get_res(self):
        return {"id":self.id,"time":self.time,"ftime":self.ftime,"context":self.context,"location":self.location}
        
@Server.route('/')
def hello_world():
    return 'hello_world'

#登录接口(username,password)
@Server.route('/login',methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    for tempaccount in accountList:
        if tempaccount.get_account() == username:
            if tempaccount.get_password() == password:
                return '{"code":1,"msg":"success","data":"","token":"Bearer asdasdasdasdasd1234561234512345132"}'
    return '{"code":0,"msg":"用户名或者密码错误","data":"","token":""}'

#获取主页导航菜单
@Server.route('/GetMenu',methods=['GET'])
def GetMenu():
    yonghutempmenu = []
    yonghuliebiaopower = []
    yonghuliebiaoadd = Menu(111,'用户列表增加','',2,'')
    yonghuliebiaodelete = Menu(112,'用户列表删除','',2,'')
    yonghuliebiaoedit = Menu(113,'用户列表修改','',2,'')
    yonghuliebiaoselect = Menu(114,'用户列表查询','',2,'')
    yonghuliebiaopower.append(yonghuliebiaoadd.get_res())
    yonghuliebiaopower.append(yonghuliebiaodelete.get_res())
    yonghuliebiaopower.append(yonghuliebiaoedit.get_res())
    yonghuliebiaopower.append(yonghuliebiaoselect.get_res())
    yonghuliebiao = Menu(11,'用户列表','Users',2,yonghuliebiaopower)
    yonghutempmenu.append(yonghuliebiao.get_res())
    yonghuguanli = Menu(1,'用户管理','',1,yonghutempmenu)
    
    qunxiantempmenu = []
    jueseliebiao = Menu(21,'角色列表','Roles',2,'')
    qunxiantempmenu.append(jueseliebiao.get_res())
    quanxianliebiao = Menu(22,'权限列表','Rights',2,'')
    qunxiantempmenu.append(quanxianliebiao.get_res())
    quanxianguanli = Menu(2,'权限管理','',1,qunxiantempmenu)

    shangpintempmenu = []
    shangpinliebiao = Menu(31,'商品列表','Goods',2,'')
    shangpintempmenu.append(shangpinliebiao.get_res())
    fenleicanshu = Menu(32,'分类参数','Args',2,'')
    shangpintempmenu.append(fenleicanshu.get_res())
    shangpinfenlei = Menu(33,'商品分类','Categories',2,'')
    shangpintempmenu.append(shangpinfenlei.get_res())
    shangpinguanli = Menu(3,'商品管理','',1,shangpintempmenu)
    diandantempmenu = []
    dingdanliebiao = Menu(41,'订单列表','Orders',2,'')
    diandantempmenu.append(dingdanliebiao.get_res())
    dingdanguanli = Menu(4,'订单管理','',1,diandantempmenu)

    shujutempmenu = []
    shujuliebiao = Menu(51,'数据详情','Datas',2,'')
    shujutempmenu.append(shujuliebiao.get_res())
    shujutongji = Menu(5,'数据统计','',1,shujutempmenu)
    
    templist = []
    templist.append(yonghuguanli.get_res())
    templist.append(quanxianguanli.get_res())
    templist.append(shangpinguanli.get_res())
    templist.append(dingdanguanli.get_res())
    templist.append(shujutongji.get_res())
    ret = ResultMsg(1,'scuuess',templist)
    return json.dumps(ret.get_res(),ensure_ascii=False)
    #return '{"data":[{"id":1,"name":"用户管理","goods":[{"goodsid":11,"goodsname":"用户列表","path":"users"}]},{"id":2,"name":"权限管理","goods":[{"goodsid":21,"goodsname":"权限","path":"authority"}]}],"code":1,"msg":""}'

#获取参数列表
@Server.route('/GetParam',methods=['GET'])
def GetParam():
    #username = request.json.get("username")
    #print()
    ret = ResultMsg(1,'scuuess',paramlist)
    return json.dumps(ret.get_res(),ensure_ascii=False)

#获取商品分类
@Server.route('/GetCategories',methods=['GET'])
def GetCategories():
    ret = ResultMsg(1,'scuuess',categories)
    return json.dumps(ret.get_res(),ensure_ascii=False)

#获取权限列表
@Server.route('/GetRights',methods=['GET'])
def GetRights():
    rightslist = []
    yonghuguanli = Menu(1,'用户管理','',1,'')
    yonghuliebiao = Menu(11,'用户列表','Users',2,'')
    quanxianguanli = Menu(2,'权限管理','',1,'')
    quanxianliebiao = Menu(22,'权限列表','Rights',2,'')
    rightslist.append(yonghuguanli.get_res())
    rightslist.append(yonghuliebiao.get_res())
    rightslist.append(quanxianguanli.get_res())
    rightslist.append(quanxianliebiao.get_res())
    ret = ResultMsg(1,'scuuess',rightslist)
    return json.dumps(ret.get_res(),ensure_ascii=False)

#获取角色列表
@Server.route('/GetRoles',methods=['GET'])
def GetRoles():
    templist = []
    for role in roleslist:
        templist.append(role.get_res())
    ret = ResultMsg(1,'scuuess',templist)
    return json.dumps(ret.get_res(),ensure_ascii=False)

#添加角色
@Server.route('/AddRole',methods=['POST'])
def AddRole():
    id = len(roleslist) + 1
    name = request.json.get("name")
    level = request.json.get("level")
    description = request.json.get("description")
    roleslist.append(Role(id,name,int(level),description,employeepowerlist))
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False)

#删除角色
@Server.route('/DeleteRole',methods=['POST'])
def DeleteRole():
    id = request.json.get("id")
    tempindex = 0
    max = len(roleslist)
    for x in range(0,max):
        if roleslist[x].get_id() == int(id):
            tempindex = x
    del roleslist[tempindex]
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False)
#修改角色
@Server.route('/UpdateRole',methods=['POST'])
def UpdateRole():
    id = request.json.get("id")
    name = request.json.get("name")
    level = request.json.get("level")
    description = request.json.get("description")
    for index in range(0,len(roleslist)):
        if roleslist[index].get_id() == int(id):
            roleslist[index].set_Info(name,int(level),description)
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False) 

#获取用户
@Server.route('/Users',methods=['GET'])
def Users():
    retlist = []
    tempretlist = []
    query = str(request.args.get('query'))
    pagenum = int(request.args.get('pagenum'))
    pagesize = int(request.args.get('pagesize'))
    startnum = (pagenum - 1) * pagesize
    endnum = pagenum * pagesize 
    if query is not None or query != '': 
        for queryuser in userList:
            if str(queryuser.get_name()) == query:
                tempretlist.append(queryuser.get_res())
                retlist = UserList(len(userList),pagenum,tempretlist)
                ret = ResultMsg(1,'scuuess',retlist.get_res())
                return json.dumps(ret.get_res(),ensure_ascii=False)
                
    if endnum >= len(userList):
        endnum = len(userList)
    for indexnum in range(startnum,endnum):
        userdata = userList[indexnum].get_res()
        retlist.append(userdata)
    retlist = UserList(len(userList),pagenum,retlist)
    ret = ResultMsg(1,'scuuess',retlist.get_res())
    return json.dumps(ret.get_res(),ensure_ascii=False)
    #return '{"data":{"total":4,"page":1,"people":[{"id":1,"name":"张三","sex":"男","address":"山东省青岛市市北区","state":true},{"id":2,"name":"李四","sex":"男","address":"山东省济南市历下区","state":false}]},"code":1,"msg":"success"}'

#增加用户(name,sex,address,state,option)
@Server.route('/AddUser',methods=['POST'])
def AddUser():
    id = len(userList) + 1
    name = request.json.get("name")
    sex = request.json.get("sex")
    email = request.json.get("email")
    mobilephone = request.json.get("mobilephone")
    address = request.json.get("address")
    state = True
    option = ''
    userList.append(User(id,name,sex,email,mobilephone,address,state,option))
    ret = ResultMsg(1,'scuuess',userList[len(userList) - 1].get_res())
    return json.dumps(ret.get_res(),ensure_ascii=False)

#删除用户(id)
@Server.route('/DeleteUser',methods=['POST'])
def DeleteUser():
    id = request.json.get("id")
    tempindex = 0
    count = len(userList)
    for index in range(tempindex,count):
        if userList[index].get_id() == id:
            tempindex = index
    del userList[tempindex]
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False)
    
#修改用户信息(id,name,sex,address,state,option)
@Server.route('/UpdateUser',methods=['POST'])
def UpdateUser():
    id = request.json.get("id")
    name = request.json.get("name")
    sex = request.json.get("sex")
    email = request.json.get("email")
    mobilephone = request.json.get("mobilephone")
    address = request.json.get("address")
    state = request.json.get("state")
    #if request.json.get("state").lower() != 'true':
    #    state = False
    option = request.json.get("option")
    print("id:"+str(id))
    print("name:"+str(name))
    print("sex:"+str(sex))
    print("address:"+str(address))
    print("state:"+str(state))
    print("option:"+str(option))
    for index in range(0,len(userList)):
        if userList[index].get_id() == id:
            userList[index].set_Info(name,sex,email,mobilephone,address,state,option)
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False) 
    
#修改账号密码(username,password)
@Server.route('/UpdateAccount',methods=['POST'])
def UpdateAccount():
    authorization = request.headers.get("Authorization")
    #token验证
    if authorization is None or authorization.lower() != Token: 
        return '',401
    username = request.json.get("username")
    password = request.json.get("password")
    print("post username ：" + username)
    print("post password ：" + password)
    tempjsonaccount = ''
    for tempaccount in accountList:
        if tempaccount.get_account() == username:
            tempaccount.set_password(password)
            tempjsonaccount = tempaccount.get_res()
    ret = ResultMsg(1,'scuuess',tempjsonaccount)
    return json.dumps(ret.get_res())

#获取商品列表(支持分页与按商品名称查询 参考Users)
@Server.route('/GetGoods',methods=['GET'])
def GetGoods():  
    tempretlist= []
    retlist= []
    query = str(request.args.get('query'))
    pagenum = int(request.args.get('pagenum'))
    pagesize = int(request.args.get('pagesize'))
    #开始的index
    startnum = (pagenum - 1) * pagesize
    endnum = pagenum * pagesize 
    if query is not None or query != '': 
        for querygoods in goodslist:
            if str(querygoods.get_name()) == query:
                tempretlist.append(querygoods.get_res())
                retlist = ReultGoods(len(goodslist),pagenum,tempretlist)
                ret = ResultMsg(1,'scuuess',retlist.get_res())
                return json.dumps(ret.get_res(),ensure_ascii=False)
    if endnum >= len(goodslist):
        endnum = len(goodslist)
    for indexnum in range(startnum,endnum):
        retlist.append(goodslist[indexnum].get_res())
    retlist = ReultGoods(len(goodslist),pagenum,retlist)
    ret = ResultMsg(1,'scuuess',retlist.get_res())
    return json.dumps(ret.get_res(),ensure_ascii=False)


#增加商品
@Server.route('/AddGoods',methods=['POST'])
def  AddGoods():
    id = len(goodslist) + 1
    name = request.json.get("name")
    price = int(request.json.get("price"))
    weight = int(request.json.get("weight"))
    goodslist.append((Goods(id,name,price,weight,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))
    ret = ResultMsg(1,'scuuess',goodslist[len(goodslist) - 1].get_res())
    return json.dumps(ret.get_res(),ensure_ascii=False)
#删除商品信息
@Server.route('/DeleteGoods',methods=['POST'])
def DeleteGoods():
    id = request.json.get("id")
    tempindex = 0
    count = len(goodslist)
    for index in range(tempindex,count):
        if goodslist[index].get_id() == id:
            tempindex = index
    del goodslist[tempindex]
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False)

#修改商品信息
@Server.route('/UpdateGoods',methods=['POST'])
def  UpdateGoods():
    id = request.json.get("id")
    name = request.json.get("name")
    price = request.json.get("price")
    weight = request.json.get("weight")
    for index in range(0,len(goodslist)):
        if goodslist[index].get_id() == id:
            goodslist[index].set_Info(name,price,weight,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ret = ResultMsg(1,'scuuess','')
    return json.dumps(ret.get_res(),ensure_ascii=False) 

#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@Server.route("/Upload", methods=['POST'])
def Upload():
    authorization = request.headers.get("Authorization")
    print(authorization)
    f = request.files['file']
    if not (f and allowed_file(f.filename)):
        return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
    user_input = request.form.get("name")
    basepath = os.path.dirname(__file__) 
    # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  
    print(upload_path)
    f.save(upload_path)
    # 使用Opencv转换一下图片格式和名称
    #img = cv2.imread(upload_path)
    #cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
    ret = ResultMsg(1,'success',f.filename)
    return  json.dumps(ret.get_res(),ensure_ascii=False) 

#返回图像
@Server.route('/GetImage',methods=['GET'])
def GetImage():
    import base64
    id = request.args.get("id")
    basepath = os.path.abspath(os.curdir)
    imagepath = basepath + '\\static\\images\\' + id
    print(imagepath)
    image_data = open(imagepath, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@Server.route('/GetOrders',methods=['GET'])
def GetOrders():
    templist = []
    for order in orderlist:
        templist.append(order.get_res())
    ret = ResultMsg(1,'scuuess',templist)
    return json.dumps(ret.get_res(),ensure_ascii=False)


@Server.route('/GetProgress',methods=['GET'])
def GetProgress():
    ret = ResultMsg(1,'scuuess',progresslist)
    return json.dumps(ret.get_res(),ensure_ascii=False)

#创建登录账号
def CreateAccount():
    accountList.append(Account('123','123'))
    accountList.append(Account('admin','123456'))
    
#创建用户列表
def CreateUsers():
    userList.append(User(1,'123','男','123@qq.com','11111111111','这是一个测试的账号，切勿改名',True,''))
    userList.append(User(2,'李四','男','456@qq.com','22222222222','山东省济南市历城区',False,''))
    userList.append(User(3,'王五','男','789@qq.com','33333333333','山东省潍坊市坊子区',True,''))
    userList.append(User(4,'李签','女','111@qq.com','44444444444','山东省青岛市市南区',True,''))
    userList.append(User(5,'张三','男','123@qq.com','11111111111','山东省青岛市市北区',True,''))


#创建角色列表
def CreateRoles():
 
    yonghutempmenu = []
    yonghuliebiaopower = []
    yonghuliebiaoadd = Menu(111,'用户列表增加','',2,'')
    yonghuliebiaodelete = Menu(112,'用户列表删除','',2,'')
    yonghuliebiaoedit = Menu(113,'用户列表修改','',2,'')
    yonghuliebiaoselect = Menu(114,'用户列表查询','',2,'')
    yonghuliebiaopower.append(yonghuliebiaoadd.get_res())
    yonghuliebiaopower.append(yonghuliebiaodelete.get_res())
    yonghuliebiaopower.append(yonghuliebiaoedit.get_res())
    yonghuliebiaopower.append(yonghuliebiaoselect.get_res())
    yonghuliebiao = Menu(11,'用户列表','Users',2,yonghuliebiaopower)
    yonghutempmenu.append(yonghuliebiao.get_res())
    yonghuguanli = Menu(1,'用户管理','',1,yonghutempmenu)
    qunxiantempmenu = []
    jueseliebiao = Menu(21,'角色列表','Roles',2,'')
    qunxiantempmenu.append(jueseliebiao.get_res())
    quanxianliebiao = Menu(22,'权限列表','Rights',2,'')
    qunxiantempmenu.append(quanxianliebiao.get_res())
    quanxianguanli = Menu(2,'权限管理','',1,qunxiantempmenu)
    bosspowerlist.append(yonghuguanli.get_res())
    bosspowerlist.append(quanxianguanli.get_res())
    employeepowerlist.append(quanxianguanli.get_res())
    roleslist.append(Role(1,'主管',1,'最高权限所有者',bosspowerlist))
    roleslist.append(Role(2,'员工',2,'一般权限所有者',employeepowerlist))

#创建商品分类列表
def CreateCategories():
    phonetemp = []
    xiaomi = Category(111,'小米',True,3,'')
    apple =  Category(112,'苹果',True,3,'')
    phonetemp.append(xiaomi.get_res())
    phonetemp.append(apple.get_res())
    phone = Category(11,'手机',True,2,phonetemp)

    cameratemp = []
    sony = Category(121,'索尼',True,3,'')
    cameratemp.append(sony.get_res())
    camera= Category(12,'相机',True,2,cameratemp)
    digitallist = []
    digitallist.append(phone.get_res())
    digitallist.append(camera.get_res())
    digital = Category(1,'电子设备',True,1,digitallist)

    bedtemp = []
    ximengsi = Category(211,'席梦思',True,3,'')
    bedtemp.append(ximengsi.get_res())
    bed = Category(21,'床',True,2,bedtemp)
    furniturelist = []
    furniturelist.append(bed.get_res())
    furniture = Category(2,'家具',False,1,furniturelist)
    categories.append(digital.get_res())
    categories.append(furniture.get_res())

#创建参数列表
def CreateParam():
    colorlist = []
    colorlist.append('红色')
    colorlist.append('蓝色')
    colorlist.append('绿色')
    color = Param(1,'颜色','颜色的值',colorlist)
    sizelist = []
    sizelist.append('小')
    sizelist.append('中')
    sizelist.append('大')
    size = Param(2,'大小','大小的值',sizelist)
    paramlist.append(color.get_res())
    paramlist.append(size.get_res())
    
#创建商品列表
def CreateGoods():
    #日期格式 2020-07-18 00:00:00
    goodslist.append(Goods(1,'苹果七',5600,100,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    goodslist.append(Goods(2,'苹果八',5700,100,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    goodslist.append(Goods(3,'苹果九',5800,100,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

#创建订单
def CreateOrders():
    orderlist.append(Order(1,'sf4541231546645',40,True,True,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    orderlist.append(Order(2,'sf4541231584646',40,False,False,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    orderlist.append(Order(3,'sf4541231546495',40,False,False,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    orderlist.append(Order(4,'sf4541231546644',40,False,False,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    orderlist.append(Order(5,'sf4541231546641',40,True,True,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    orderlist.append(Order(6,'sf4541231546642',40,True,True,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def  CreateProgress():
    p1 = Progress(1,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达A','')
    p2 = Progress(2,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达B','')
    p3 = Progress(3,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达C','')
    p4 = Progress(4,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达D','')
    p5 = Progress(5,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达E','')
    p6 = Progress(6,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'快件到达F','')
    progresslist.append(p1.get_res())
    progresslist.append(p2.get_res())
    progresslist.append(p3.get_res())
    progresslist.append(p4.get_res())
    progresslist.append(p5.get_res())
    progresslist.append(p6.get_res())

if __name__ == '__main__':
    CreateAccount()
    CreateUsers()
    CreateRoles()
    CreateCategories()
    CreateParam()
    CreateGoods()
    CreateOrders()
    CreateProgress()
    print (' * '+ os.path.abspath(os.curdir)) 
    Server.run(host='127.0.0.1',port=9003)

    
    


