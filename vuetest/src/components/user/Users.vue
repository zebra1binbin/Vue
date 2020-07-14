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
                    <el-input placeholder="请输入内容" > 
                        <el-button slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <!--添加用户-->
                    <el-button type="primary">添加用户</el-button>
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
                            v-model="scope.row.state"
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
    </div>
</template>


<script>
   export default{
       data(){
           return{
               //
               queryInfo:{
                   query:'',
                   pagenum:1,
                   pagesize:2
               },
               userlist:[],
               total:0
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
            }
       }
   }
</script>

<style lang="less" scoped>

</style>
