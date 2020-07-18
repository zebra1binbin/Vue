import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Welcome from '../components/Welcome.vue'
import Users from '../components/user/Users.vue'
import Rights from '../components/authority/Rights.vue'
import Roles from '../components/authority/Roles.vue'
import Categories from '../components/goods/categories.vue'
import Args from '../components/goods/args.vue'
import Goods from '../components/goods/goods.vue'
import AddGoods from '../components/goods/addgoods.vue'
import Orders from '../components/order/orders.vue'
import Datas from '../components/data/datas.vue'

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
  Pagination,
  Dialog,
  RadioGroup,
  Radio,
  Select,
  Option,
  MessageBox,
  Tag,
  Tree,
  Cascader,
  Alert,
  TabPane,
  Tabs,
  Steps,
  Step,
  Checkbox,
  CheckboxGroup,
  Upload,
  Timeline,
  TimelineItem } 
  from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import Home from '../views/Home.vue'
import TreeTable from 'vue-table-with-tree-grid'

import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css' // import styles
import 'quill/dist/quill.snow.css' // for snow theme
import 'quill/dist/quill.bubble.css' // for bubble theme


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
Vue.use(Dialog)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(Select)
Vue.use(Option)
Vue.use(Tag)
Vue.use(Tree)
Vue.use(Cascader)
Vue.use(Alert)
Vue.use(TabPane)
Vue.use(Tabs)
Vue.use(Step)
Vue.use(Steps)
Vue.use(Checkbox)
Vue.use(CheckboxGroup)
Vue.use(Upload)
Vue.use(Timeline)
Vue.use(TimelineItem)
Vue.use(VueQuillEditor)
Vue.prototype.$message= Message
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$http = axios
//全局可用组件
Vue.component('tree-table',TreeTable)

//全局过滤器 orihinVal需要处理的时间格式
Vue.filter('dateFormat',function(orihinVal){
  const dt = new Date(orihinVal)
  const y = dt.getFullYear()
  const m = (dt.getMonth() + 1 + '').padStart(2,'0')
  const d = (dt.getDate() + '').padStart(2,'0')

  const hh = (dt.getHours() + '').padStart(2,'0')
  const mm = (dt.getMinutes() + '').padStart(2,'0')
  const ss = (dt.getSeconds() + '').padStart(2,'0')
  return `${y}-${m}-${d} ${hh}:${mm}:${ss}`
})

//请求根路径
axios.defaults.baseURL='http://127.0.0.1:9003/'
//每个请求都会加一个验证
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
    //routeview中的跳转组件
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
        path: '/rights',
        name: 'rights',
        component: Rights
      },
      {
        path: '/roles',
        name: 'Roles',
        component: Roles
      },
      {
        path:'/categories',
        name: 'Categories',
        component: Categories
      },
      {
        path:'/args',
        name:'args',
        component:Args
      },
      {
        path:'/goods',
        name:'goods',
        component:Goods
      },
      {
        path:'/goods/AddGoods',
        name:'addgoods',
        component:AddGoods
      },
      {
        path:'/orders',
        name:'orders',
        component:Orders
      },
      {
        path:'/datas',
        name:'datas',
        component:Datas
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
