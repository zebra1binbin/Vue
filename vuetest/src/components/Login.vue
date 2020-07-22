<template>
    <div class="login_container">
        <div class="login_box">
            <!--头像-->
            <div class="avatar_box">
                <img src="../assets/logo.png"/>
            </div>
            <!--登陆表单-->
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" class="login_form">
                <!--用户名-->
                <el-form-item prop="username">
                  <el-input
                    v-model="loginForm.username"
                    placeholder="请输入账号"
                    prefix-icon="el-icon-user">
                   </el-input>
                </el-form-item>
                  <!--密码-->
                 <el-form-item prop="password">
                  <el-input
                    type="password"
                    v-model="loginForm.password"
                    placeholder="请输入密码"
                    prefix-icon="el-icon-lock">
                    </el-input>
                </el-form-item>
                <!--按钮-->
                 <el-form-item class="btns">
                   <el-button type="primary" @click="Login">登录</el-button>
                   <el-button type="info" @click="resetLoginForm">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            //登录表单的数据对象
            loginForm:{
                username:'',
                password:''
            },
            //验证规则
            loginFormRules: {
                username: [
                    { required: true, message: '请输入账号', trigger: 'blur' },
                    { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'change' }
                ]
          }
        }
    },
    created(){
        document.onkeyup = (e) => {
            //Enter ： keyCode= 13
            // console.log(e.keyCode)
            if (e.keyCode === 13) {
               this.Login()
            }
        }
    }
    ,
    methods:{
        //重置
        resetLoginForm(){
            this.$refs.loginFormRef.resetFields();
        },
        //登录
        //localstorage 持久化
        //sessionstorage 会话（可保存token）
        Login(){
            this.$refs.loginFormRef.validate(async (valid)=>{
                if(!valid)
                {
                    return this.$message.error('格式错误');
                }
                const {data:res} = await this.$http.post('login',this.loginForm);
                if(res.code != 1)
                {
                    return this.$message.error(res.msg);
                }
                else
                {
                    this.$message.success('欢迎登陆');
                }
                sessionStorage.setItem('token',res.token);
                //页面跳转
                this.$router.push('/home');
            });
        }
    }
}
</script>

<style lang="less" scoped>
.login_container{
    background-color:cadetblue;
    height: 100%;
}

.login_box{
    width: 450px;
    height: 300px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%); 

    .avatar_box{
    height: 130px;
    width: 130px;
    border:1px solid #eee;
    border-radius: 50%;
    padding:10px;
    box-shadow:0 0 10px #ddd;
    position: absolute;
    left: 50%;
    transform: translate(-50%,-50%); 
    background-color:#fff;
    img{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: #eee;
        }
    }
}
.btns{
    display: flex;
    justify-content: flex-end;
}

.login_form{
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
}

</style>