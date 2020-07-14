<template>
    <el-container class="home-container">
        <!--头布局-->
        <el-header>
            <div class="headerdiv">
                <img class="Icon" src="../assets/logo.png"/>
                <span class="headerspan">商品管理系统</span>
            </div> 
            <el-button type="info" @click="loginOut">退出</el-button>
        </el-header>
        <!--主体布局-->
        <el-container>
            <!--左布局-->
            <el-aside :width="isCollapse ? '64px' : '200px'">
                <div class="toggle-button" @click="toggleCollapse">|||</div>
                <!--侧边栏 (:属性绑定的标志)-->
                <el-menu background-color="#333744" text-color="#fff"  active-text-color="#409eff" :unique-opened="true" :collapse="isCollapse" :collapse-transition="false" :router="true" :default-active="activePath">
                        <!--一级菜单 如果index报错可以拼接一个''空字符串-->
                        <el-submenu :index="menuitem.id + ''" v-for="menuitem in menulist" :key="menuitem.id">
                            <!--一级菜单模板-->
                            <template slot="title">
                                <!--图标-->
                                <i :class="iconsobj[menuitem.id]"></i>
                                <!--文本-->
                                <span>{{menuitem.name}}</span>
                            </template>
                            <!--二级菜单-->
                            <el-menu-item :index="'/' + subitem.path" v-for="subitem in menuitem.goods" :key="subitem.goodsid" @click="saveNavState('/' + subitem.path)">
                                <!--图标-->
                                <i class="el-icon-menu"></i>
                                <!--文本-->
                                <span>{{subitem.goodsname}}</span>
                            </el-menu-item>
                        </el-submenu>
                </el-menu>
            </el-aside>
            <!--右布局-->
            <el-main>
                <!--路由占位符-->
                 <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>



<script>
export default {
    data(){
        return{
            //菜单数据
            menulist:[],
            iconsobj:{
                '1':'el-icon-goods',
                '2':'el-icon-warning-outline'
            },
            //折叠标志
            isCollapse:false,
            //被激活的地址
            activePath:''
        }
    },
    created(){
        this.getMenuList()
        this.activePath = sessionStorage.getItem('activePath')
    },
    methods:{
        loginOut(){
            //清空token
            sessionStorage.clear();
            this.$message('退出成功');
            this.$router.push('/login');
        },
        async getMenuList(){
           const {data:res} = await this.$http.get('GetGoods')
           if(res.code !== 1){
               return this.$message.error(res.msg);
           }
           this.menulist = res.data
        },
        //点击按钮切换菜单折叠、展开
        toggleCollapse(){
            this.isCollapse = !this.isCollapse
        },
        //保存当前链接
        saveNavState(activePath){
            sessionStorage.setItem('activePath',activePath)
            this.activePath = activePath
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
.el-menu {
        border-right: 0;
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

.iconfont{
    margin-right: 10px;
}
.toggle-button{
    background-color: #4a5064;
    font-size: 10px;
    line-height: 24px;
    color: #fff;
    text-align: center;
    letter-spacing: 0.2em;
    cursor: pointer;
}
</style>