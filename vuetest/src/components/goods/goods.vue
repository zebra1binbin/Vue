<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>商品列表</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card>
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-input placeholder="请输入商品名称" v-model="queryInfo.query" clearable @clear="getGoodsList()">
                        <el-button slot="append" icon="el-icon-search" @click="getGoodsList()"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="goAddGoodsPage">添加商品</el-button>
                </el-col> 
            </el-row>
            <el-table :data="goodslist" border stripe>
                <el-table-column label="#" type="index"></el-table-column>
                <el-table-column label="商品名称" prop="name"></el-table-column>
                <el-table-column label="商品价格(￥)" prop="price" width="95px"></el-table-column>
                <el-table-column label="商品重量(k)" prop="weight" width="95px"></el-table-column>
                <el-table-column label="创建时间" prop="createtime">
                    <!--修改时间格式-->
                    <template slot-scope="scope">
                        {{scope.row.createtime | dateFormat}}  
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button size="mini" type="primary" icon="el-icon-edit">编辑</el-button>
                        <el-button size="mini" type="danger" icon="el-icon-delete" @click="RemoveGoodsByID(scope.row.id)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.pagenum"
            :page-sizes="[1,2,5,10]"
            :page-size="queryInfo.pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total" background>
            </el-pagination>
        </el-card>
    </div>
</template>

<script>
export default {
    data(){
        return{
            queryInfo:{
                query:'',
                pagenum:1,
                pagesize:10
            },
            total:0,
            goodslist:[]
        }
    },
    created(){
        this.getGoodsList()
    },
    methods:{
        //分页获取goodslist
        async getGoodsList(){
            const {data:res} = await this.$http.get('GetGoods',{params: this.queryInfo})
            if(res.code !== 1){
                return this.$message.error('获取商品列表失败');
            }
            this.goodslist = res.data.goodslist
            this.total = res.data.total
            // return this.$message.success('获取商品列表成功');
        },
        handleSizeChange(newsize){
            //先赋值在获取数据
            this.queryInfo.pagesize = newsize
            this.getGoodsList()
        },
        handleCurrentChange(newnum){
            this.queryInfo.pagenum = newnum
            this.getGoodsList()
        },
        async RemoveGoodsByID(goodsid){
            const confirmResult = await this.$confirm('此操作将永久删除该商品, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).
            catch(err=>err);
            if(confirmResult !== 'confirm'){
                return this.$message.info('已取消删除')
            }
            await this.$http.post('DeleteGoods',{
                id:goodsid
            }).
            then(function (response) {
                if(response.data.code != 1)
                {
                    return this.$message.error('删除商品失败')
                }
            }).catch(function (error) {
                return this.$message.error(error)
            });
            this.getGoodsList()
            return this.$message.success('删除商品成功')
        },
        goAddGoodsPage(){
            this.$router.push('/goods/addgoods');
        }
    }
}
</script>>


<style lang="less" scoped>

</style>>