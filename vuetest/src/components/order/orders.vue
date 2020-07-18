<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>订单管理</el-breadcrumb-item>
            <el-breadcrumb-item>订单列表</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-input placeholder="请输入订单号" clearable>
                        <el-button slot="append" icon="el-icon-search" ></el-button>
                    </el-input>
                </el-col>
            </el-row>
            <el-table :data="orderslist" border stripe>
                <el-table-column label="#" type="index"></el-table-column>
                <el-table-column label="订单号" prop="number"></el-table-column>
                <el-table-column label="运费" prop="price" width="95px"></el-table-column>
                <el-table-column label="是否已付款" prop="paied">
                    <template slot-scope="scope">
                        <!-- {{scope.row.paied}}   -->
                        <el-tag type="success" v-if="scope.row.paied === true">已付款</el-tag>
                        <el-tag type="danger" v-else>未付款</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="是否已发货" prop="send">
                     <template slot-scope="scope">
                        <!-- {{scope.row.send}}   -->
                        <span  v-if="scope.row.send === true">是</span>
                        <span  v-else>否</span>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间">
                    <!--修改时间格式-->
                    <template slot-scope="scope">
                        {{scope.row.ordertime | dateFormat}}  
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template>
                        <el-button size="mini" type="primary" icon="el-icon-edit"></el-button>
                        <el-button size="mini" type="success" icon="el-icon-location" @click="showProgressBox()"></el-button>
                    </template>
                </el-table-column>
            </el-table>

        </el-card>

        <el-dialog
        title="物流进度"
        :visible.sync="progressDialogVisible"
        width="50%">
              <el-timeline >
                    <el-timeline-item
                    v-for="(activity, index) in progressinfo"
                    :key="index"
                    :timestamp="activity.time">
                        {{activity.context}}
                    </el-timeline-item>
                </el-timeline>
        </el-dialog>
    </div>
</template>>

<script>
export default {
    data(){
        return{
            orderslist:[],
            progressDialogVisible:false,
            progressinfo:[]
        }
    },
    created(){
        this.getOrdersList()
    },
    methods:{
        async getOrdersList(){
            const {data:res} = await this.$http.get('GetOrders')
            if(res.code !== 1){
                return this.$message.error('获取订单列表失败');
            }
            this.orderslist = res.data
        },
        async showProgressBox(){
            const {data:res} = await this.$http.get('GetProgress')
            if(res.code !== 1){
                return this.$message.error('获取物流信息失败');
            }
            this.progressinfo = res.data
            console.log(this.progressinfo)
            this.progressDialogVisible = true
        }
    }    

}
</script>

<style lang="less" scoped>

</style>