import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import { Form,FormItem,Input,Button,Message,Container,Header,Aside,Main } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import Home from '../views/Home.vue'

Vue.use(VueRouter)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Button)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.prototype.$message= Message
Vue.prototype.$http = axios
//请求根路径
axios.defaults.baseURL='http://127.0.0.1:9003/'

const routes = [
  {
    path: '/',
    redirect:'/login'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }

]

const router = new VueRouter({
  routes
})

//路由导航守卫
//to 将要访问的路径
//form 从哪个路径跳转而来
//next 函数
//  next() 放行
//  next('arg') arg强制跳转路径
router.beforeEach((to,form,next)=>{
  if(to.path === '/login'){
    return next();
  }
  //获取token
  const tokenStr = sessionStorage.getItem('token')
  if(!tokenStr){
    return next('/login');
  }
  else{
    return next();
  }
})

export default router
