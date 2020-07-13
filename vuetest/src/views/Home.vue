<template>
    <el-container class="home-container">
        <!--头布局-->
        <el-header>
            <div class="headerdiv">
                <img class="Icon" src="../assets/logo.png"/>
                <span class="headerspan">管理系统</span>
            </div> 
            <el-button type="info" @click="loginOut">退出</el-button>
        </el-header>
        <!--主体布局-->
        <el-container>
            <!--左布局-->
            <el-aside width="200px">Aside</el-aside>
            <!--右布局-->
            <el-main>Main</el-main>
        </el-container>
    </el-container>
</template>



<script>
export default {
    methods:{
        loginOut()
        {
            //清空token
            sessionStorage.clear();
            this.$message('退出成功');
            this.$router.push('/login');
        }
    }
}
</script>

<style scoped>
.el-header{
    background-color:#373d41 ;
    display: flex;
    justify-content:space-between;
    padding-left: 5;
    align-items: center;
    color: #ffffff;
    font-size: 20px;  
}
.headerdiv{
        display: flex;
        align-items:center;
}
.headerspan{
    margin-left: 15px;
}
.el-aside{
    background-color: #333744;
}
.el-main{
    background-color: #eaedf1;
}
.home-container{
    height: 100%;
}
.Icon{
    height: 50px;
    width: 50px;
}
</style>