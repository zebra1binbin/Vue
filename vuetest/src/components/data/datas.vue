<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>数据列表</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <div id="main" style="width: 800px;height:600px;"></div>
        </el-card>
    </div>
</template>

<script>
//导入echares
import echarts from 'echarts'
export default {
    data(){
        return{

        }
    },
    created(){
        
    },
    //此时页面元素已经渲染完毕
    mounted(){
        var myChart = echarts.init(document.getElementById('main'));
        var option = {
            title: {
                text: 'ECharts 数据表'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis: {
                data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        };
        myChart.setOption(option);
    },
    methods:{

    }
}
</script>


<style lang="less" scoped>

</style>