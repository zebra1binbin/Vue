import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Welcome from '../components/Welcome.vue'
import Users from '../components/user/Users.vue'
import { 
  Form,
  FormItem,
  Input,
  Button,
  Message,
  Container,
  Header,
  Aside,
  Main,
  Menu,
  Submenu,
  MenuItemGroup,
  MenuItem,
  Breadcrumb,
  BreadcrumbItem,
  Card,
  Row,
  Col,
  Table,
  TableColumn,
  Switch,
  Tooltip,
  Pagination } 
  from 'element-ui'
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
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItemGroup)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.prototype.$message= Message
Vue.prototype.$http = axios
//请求根路径
axios.defaults.baseURL='http://127.0.0.1:9003/'
//每个请求都会验证
axios.interceptors.request.use(config => {
  config.headers.Authorization = sessionStorage.getItem('token')
  //固定写法
  return config
})

const routes = [
  {
    path: '/',
    redirect:'/login'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    redirect:'/welcome',
    children:[
      {
        path: '/welcome',
        name: 'welcome',
        component: Welcome
      },
      {
        path: '/users',
        name: 'users',
        component: Users
      },
      {
        //临时的
        path: '/authority',
        name: 'welcome',
        component: Welcome
      }
    ]
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

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

export default router
