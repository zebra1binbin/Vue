<template>
    <div>
        <el-button type="info" @click="loginOut">退出</el-button>
    </div>
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

</style>