const { Divider } = require("element-ui");

<template>
    <div>
        <!--面包屑导航-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>权限管理</el-breadcrumb-item>
            <el-breadcrumb-item>权限列表</el-breadcrumb-item>
        </el-breadcrumb>
        <!--卡片视图-->
        <el-card>
            <el-table :data="rightslist" border stripe>
                <el-table-column label="#" type="index"></el-table-column>
                <el-table-column label="权限名称" prop="name"></el-table-column>
                <el-table-column label="路径" prop="path"></el-table-column>
                <el-table-column label="权限等级" prop="level">
                    <template slot-scope="scope">
                        <!-- v-if v-else 显示不同的标签-->
                        <el-tag v-if="scope.row.level === 1" type="danger">一级权限</el-tag>
                        <el-tag v-else type="success">二级权限</el-tag>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
    </div>
</template>


<script>
    export default{
        data(){
            return{
                //权限列表
                rightslist:[]
            }
        },
        created(){
            //获取所有权限
            this.getRightsList()
        },
        methods:{
            async getRightsList(){
                const {data:res} = await this.$http.get('GetRights') 
                if(res.code !== 1){
                    return this.$message.error(res.msg);
                }
                this.rightslist = res.data
            }
        }
    }
</script>


<style lang="less" scoped>

</style>