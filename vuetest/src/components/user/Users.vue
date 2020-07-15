<template>
    <div>
        <!--面包屑导航-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>

        <!--卡片-->
        <el-card class="box-card">
            <el-row :gutter="30">
                <el-col :span="8">
                    <!--搜索-->
                    <el-input placeholder="请输入用户名" v-model="queryInfo.query" clearable @clear="getUserList"> 
                        <el-button slot="append" icon="el-icon-search" @click="getUserList"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <!--添加用户-->
                    <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
                </el-col>
            </el-row>

            <!--用户列表-->
            <el-table :data="userlist" border stripe>
                <el-table-column label="#" type="index"></el-table-column>
                <el-table-column label="姓名" prop="name"></el-table-column>
                <el-table-column label="性别" prop="sex"></el-table-column>
                <el-table-column label="邮箱" prop="email"></el-table-column>
                <el-table-column label="电话" prop="mobilephone"></el-table-column>
                <el-table-column label="地址" prop="address"></el-table-column>
                <el-table-column label="状态" prop="state">
                    <template slot-scope="scope">
                         <!-- {{scope.row}} -->
                        <el-switch
                            v-model="scope.row.state" @change="userStateChanged(scope.row)"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                        </el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" prop="option" width="300">
                    <template slot-scope="scope"> 
                        <!-- {{scope.row}} -->
                        <!-- {{scope.row}} -->
                        <el-tooltip effect="dark" content="修改用户" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row)"></el-button>
                        </el-tooltip>
                        <el-tooltip effect="dark" content="删除用户" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeUserbyID(scope.row.id)"></el-button>
                        </el-tooltip>
                        <el-tooltip effect="dark" content="分配角色" placement="top" :enterable="false">
                            <el-button type="warning" icon="el-icon-setting" size="mini" @click="setRole()"></el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>

            <!--分页区-->
            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.pagenum"
            :page-sizes="[1,2,5,10]"
            :page-size="queryInfo.pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
            </el-pagination>
        </el-card>

        <!--添加用户-->
        <el-dialog
            title="添加用户"
            :visible.sync="addDialogVisible"
            width="50%"
            @close="addDialogClosed">
            <!--内容主题-->
            <el-form :model="addForm" :rules="addFormRules" ref="addFormRef" label-width="70px">
                <el-form-item label="用户名" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="sex">
                    <el-radio-group v-model="addForm.sex" size="medium">
                        <el-radio border label="男"></el-radio>
                        <el-radio border label="女"></el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="addForm.email"></el-input>
                </el-form-item>
                 <el-form-item label="电话" prop="mobilephone">
                    <el-input v-model="addForm.mobilephone"></el-input>
                </el-form-item>
                <el-form-item label="城市">
                    <el-select width="30" v-model="provincevalue" placeholder="请选择省份"
                    @change="changedProvince">
                        <el-option
                        v-for="item in provinces"
                        :key="item.value"
                        :label="item.label"
                        :value="item.label">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                    <el-select width="30" v-model="cityvalue" placeholder="请选择城市">
                        <el-option
                        v-for="item in bingcities"
                        :key="item.value"
                        :label="item.label"
                        :value="item.label">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="地址" prop="address">
                    <el-input v-model="addForm.address"></el-input>
                </el-form-item>
            </el-form>
            <!--底部区域-->
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addUser">确 定</el-button>
            </span>
        </el-dialog>

        <!--修改用户对话框-->
        <el-dialog
        title="修改用户"
        :visible.sync="editDialogVisible"
        width="50%"
        @close="editDialogClosed">
            <el-form ref="editFormRef" :model="editForm" :rules="editFormRules" label-width="80px">
                <el-form-item label="用户ID">
                    <el-input disabled v-model="editForm.id"></el-input>
                </el-form-item>
                <el-form-item label="用户名" prop="name">
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>
                <el-form-item label="用户性别" prop="sex">
                     <el-radio-group v-model="editForm.sex" size="medium">
                        <el-radio border label="男"></el-radio>
                        <el-radio border label="女"></el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="用户邮箱" prop="email">
                    <el-input v-model="editForm.email"></el-input>
                </el-form-item>
                <el-form-item label="用户电话" prop="mobilephone">
                    <el-input v-model="editForm.mobilephone"></el-input>
                </el-form-item>
                <el-form-item label="用户地址" prop="address">
                    <el-input v-model="editForm.address"></el-input>
                </el-form-item>
                <el-form-item label="用户状态">
                 <el-switch v-model="editForm.state" @change="userEditStateChanged(editForm.state)"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                        </el-switch>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editUserInfo">确 定</el-button>
            </span>
        </el-dialog>


        <el-dialog
        title="分配角色"
        :visible.sync="setRoleDialogVisible"
        width="50%">
            <span>该功能API未启用</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="setRoleDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="setRoleDialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>


<script>
   export default{
       data(){
           //验证邮箱
            var checkEmail = (rule,value,callback) => {   
                //验证邮箱的正则表达式
                const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
                if(regEmail.test(value)){
                   return callback()
                }
                callback(new Error('请输入合法邮箱'))
            }

            //验证手机号
            var checkMobilePhone=(rule,value,callback)=>{
                //验证手机的正则表达式
                const regMobilePhone = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/
                if(regMobilePhone.test(value)){
                   return callback()
                }
                callback(new Error('请输入合法手机号码'))
            }
           return{
                //省份
                provinces: [{
                    value: 'shandongsheng',
                    label: '山东省'
                    }, {
                    value: 'Shanghaishi',
                    label: '上海市'
                    }, {
                    value: 'Guangdongsheng',
                    label: '广东省'
                    }],
                //选择的省份
                provincevalue: '',
                //城市
                cities:[{
                    province:'山东省',
                    value:'jinanshi',
                    label:'济南市'
                },{
                    province:'山东省',
                    value:'qingdaoshi',
                    label:'青岛市'
                },{
                    province:'广东省',
                    value:'guangzhoushi',
                    label:'广州市'
                }],
                bingcities:[],
                //选择的城市
                cityvalue: '',
                //获取用户
                queryInfo:{
                   query:'',
                   pagenum:1,
                   pagesize:10
                },
                userlist:[],
                total:0,
                //添加用户对话框
                addDialogVisible:false,
                //修改用户对话框
                editDialogVisible:false,
                addForm:{
                   name:'',
                   sex:'男',
                   email:'',
                   mobilephone:'',
                   address:'',
                },
                addFormRules:{
                    name: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    sex: [
                        { required: true, message: '请选择性别', trigger: 'change' }
                    ],
                    email: [
                        { required: true, message: '请输入邮箱', trigger: 'blur' },
                         //自定义的验证规则
                        {validator:checkEmail, trigger: 'blur'}

                    ],
                    mobilephone: [
                        { required: true, message: '请输入电话', trigger: 'blur' },
                        //自定义的验证规则
                        {validator:checkMobilePhone, trigger: 'blur'}
                    ],
                    address: [
                        { required: true, message: '请输入地址', trigger: 'blur' }
                    ]
                },

                editForm:{

                },
                editFormRules:{
                    name: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    sex: [
                        { required: true, message: '请选择性别', trigger: 'change' }
                    ],
                    email: [
                        { required: true, message: '请输入邮箱', trigger: 'blur' },
                         //自定义的验证规则
                        {validator:checkEmail, trigger: 'blur'}

                    ],
                    mobilephone: [
                        { required: true, message: '请输入电话', trigger: 'blur' },
                        //自定义的验证规则
                        {validator:checkMobilePhone, trigger: 'blur'}
                    ],
                    address: [
                        { required: true, message: '请输入地址', trigger: 'blur' }
                    ]
                },
                validret:false,
                setRoleDialogVisible:false
           }
       },
       created(){
           this.getUserList()
       },
       methods:{
            async getUserList(){
                const {data:res} = await this.$http.get('Users',{params: this.queryInfo})
                if(res.code !== 1){
                    return this.$message.error('获取用户列表失败');
                }
                this.userlist = res.data.people
                this.total = res.data.total
            },
            handleSizeChange(newSize){
                this.queryInfo.pagesize = newSize
                this.getUserList()
            },
            handleCurrentChange(newPage){
                this.queryInfo.pagenum = newPage
                this.getUserList()
            },
            async userStateChanged(userinfo){
                //axios标准请求
                await this.$http.post('UpdateUser',{
                    id:userinfo.id,
                    name:userinfo.name,
                    sex:userinfo.sex,
                    email:userinfo.email,
                    mobilephone:userinfo.mobilephone,
                    address:userinfo.address,
                    state:userinfo.state,
                    option:userinfo.option
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        userinfo.state =!userinfo.state
                        return this.$message.error('更新用户状态失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.$message.success('更新用户状态成功')
            },
            changedProvince(value){
                let _this = this
                // console.log(value)
                _this.cityvalue=''
                _this.bingcities.length = 0
                _this.cities.forEach(function(item){
                    if(value === item.province){
                        _this.bingcities.push(item)
                    }
                })
            },
            //添加用户对话框的关闭事件
            addDialogClosed(){
                this.$refs.addFormRef.resetFields()
            },
            //添加用户确定按钮
            async addUser(){
                //预校验表单
                this.$refs.addFormRef.validate(valid =>{
                    this.validret = valid
                })
                if(!this.validret){
                    return
                }
                await this.$http.post('AddUser',{
                        name:this.addForm.name,
                        sex:this.addForm.sex,
                        email:this.addForm.email,
                        mobilephone:this.addForm.mobilephone,
                        address:this.provincevalue + this.cityvalue + this.addForm.address
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        return this.$message.error('添加用户失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.validret = false
                this.addDialogVisible = false
                this.getUserList()
                this.$message.success('添加用户成功')
            },
            //编辑用户
            showEditDialog(userinfo){
                this.editForm = userinfo
                // console.log(this.editForm)
                this.editDialogVisible = true
            },
            userEditStateChanged(userstate){
                userstate =!userstate
            },
            editDialogClosed(){
                this.$refs.editFormRef.resetFields()
            },
            async editUserInfo(){
                this.$refs.editFormRef.validate(valid =>{
                    this.validret = valid
                })
                if(!this.validret){
                    return
                }
                await this.$http.post('UpdateUser',{
                    id:this.editForm.id,
                    name:this.editForm.name,
                    sex:this.editForm.sex,
                    email:this.editForm.email,
                    mobilephone:this.editForm.mobilephone,
                    address:this.editForm.address,
                    state:this.editForm.state,
                    option:this.editForm.option
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        userinfo.state =!userinfo.state
                        return this.$message.error('修改用户失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.validret = false
                this.editDialogVisible = false
                this.getUserList()
                this.$message.success('修改用户成功')
            },
            //promise返回结果 都可以用异步修饰
            async removeUserbyID(id){
                // console.log(id)
                const confirmResult = await this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).
                catch(err=>err);
                if(confirmResult !== 'confirm'){
                    return this.$message.info('已取消删除')
                }
                await this.$http.post('DeleteUser',{
                    id:id
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        return this.$message.error('删除用户失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.getUserList()
                return this.$message.success('删除用户成功')
            },
            setRole(){
                this.setRoleDialogVisible = true
            }
       }
   }
</script>

<style lang="less" scoped>
.el-select{
    width: 120px;
    margin-right: 10px;
}
</style>
