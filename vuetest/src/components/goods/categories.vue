<template>
    <div>
        <!--面包屑导航-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>商品分类</el-breadcrumb-item>
        </el-breadcrumb>
        <!--卡片视图-->
        <el-card>
            <el-row>
                <el-col>
                    <el-button type="primary" >添加分类</el-button>
                </el-col>
            </el-row>
            <tree-table :show-row-hover="false" border show-index index-text="#" :expand-type="false" :selection-type="false" :data="catelist" :columns="columns">

            </tree-table>
        </el-card>
    </div>
</template>

<script>
    export default{
        data(){
            return{
                //商品分类数据
                catelist:[],
                queryinfo:{
                    pagenum:1,
                    pagesize:1
                },
                total:0,
                //table列的定义
                columns:[
                    {
                        label:'分类名称',
                        prop:'name'
                    }
                ]
            }
        },
        created(){
            this.getCategories()
        },
        methods:{
            async getCategories(){
                const {data:res} = await this.$http.get('GetCategories',{params: this.queryinfo})
                console.log(res)
                if(res.code !== 1){
                    return this.$message.error('获取商品分类失败');
                }
                this.catelist = res.data
                this.total = 2
            }
        }
    }

</script>


<style lang="less" scoped>

</style>