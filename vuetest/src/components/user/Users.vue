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
                    <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getUserList"> 
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
                <el-table-column label="地址" prop="address"></el-table-column>
                <el-table-column label="状态" prop="state">
                    <template slot-scope="scope">
                        <el-switch
                            v-model="scope.row.state" @change="userStateChanged(scope.row)"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                        </el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" prop="address" width="300">
                    <template> 
                        <!-- {{scope.row}} -->
                        <el-tooltip effect="dark" content="修改用户" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini"></el-button>
                        </el-tooltip>
                        <el-tooltip effect="dark" content="删除用户" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini"></el-button>
                        </el-tooltip>
                        <el-tooltip effect="dark" content="分配权限" placement="top" :enterable="false">
                            <el-button type="warning" icon="el-icon-setting" size="mini"></el-button>
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
            width="50%">
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
                <el-form-item label="城市">
                    <el-select width="30" v-model="provincevalue" placeholder="请选择省份"
                    @change="chonseProvince">
                        <el-option
                        v-for="item in provinces"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                    <el-select width="30" v-model="cityvalue" placeholder="请选择城市">
                        <el-option
                        v-for="item in cities"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="地址" prop="address">
                    <el-input v-model="streetvalue"></el-input>
                </el-form-item>
            </el-form>
            <!--底部区域-->
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addDialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>


<script>
   export default{
       data(){
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
                    province:'shandongsheng',
                    value:'jinanshi',
                    label:'济南市'
                },{
                    province:'shandongsheng',
                    value:'qingdaoshi',
                    label:'青岛市'
                },{
                    province:'Guangdongsheng',
                    value:'guangzhoushi',
                    label:'广州市'
                }],
                bingcities:[],
                //选择的城市
                cityvalue: '',
                streetvalue: '',
                //获取用户
                queryInfo:{
                   query:'',
                   pagenum:1,
                   pagesize:2
                },
                userlist:[],
                total:0,
                //添加用户对话框
                addDialogVisible:false,
                addForm:{
                   name:'',
                   sex:'男',
                   address:'',
                },
                addFormRules:{
                    name: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    sex: [
                        { required: true, message: '请输入性别', trigger: 'blur' }
                    ],
                    address: [
                        { required: true, message: '请输入地址', trigger: 'blur' }
                    ]
                }
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
            chonseProvince(e){
                console.log(e)
                // this.cities.forEach(function(item,cities){
                //     console.log(item)
                //     if(e === item.province){
                //         this.bingcities.push({
                //             item
                //             }
                //         )
                //         console.log(this.bingcities)
                //     }
                // })
                // for(var pro in this.provinces){
                //     console.log(provinces[pro].label)
                //     if(e === pro.label){
                //         this.bingcities.push(pro)
                //     }
                // }
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
