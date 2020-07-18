<template>
    <div>
       <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/goods' }">商品列表</el-breadcrumb-item>
            <el-breadcrumb-item>添加商品</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-alert title="添加商品信息" type="info" center show-icon
            :closable="true"> </el-alert>
            <!--必须是互相类似 "1" => 1  1=>"1"-->
            <!--字符串转成数字  -0  -->
            <!--数字转成字符串  +''  -->
            <el-steps align-center :space="200" :active="activeIndex - 0" 
            finish-status="success">
                <el-step title="基本信息"></el-step>
                <el-step title="商品参数"></el-step>
                <el-step title="商品属性"></el-step>
                <el-step title="商品图片"></el-step>
                <el-step title="商品内容"></el-step>
                <el-step title="完成"></el-step>
            </el-steps>
            <el-form :model="addForm" :rules="addFormRules"
             ref="addFormRef" label-width="100px" label-position="top">
                <!--标签页切换之前的钩子 before-leave-->
                <el-tabs v-model="activeIndex" :tab-position="'left'" 
                :before-leave="beforetabLeave"
                @tab-click="tabClick()">
                    <el-tab-pane label="基本信息" name="0">
                        <el-form-item label="商品名称" prop="name">
                            <el-input v-model="addForm.name"></el-input>
                        </el-form-item>
                        <!--type="number"只能输入数字-->
                        <el-form-item label="商品价格" prop="price">
                            <el-input v-model="addForm.price" type="number"></el-input>
                        </el-form-item>
                         <el-form-item label="商品重量" prop="weight">
                            <el-input v-model="addForm.weight" type="number"></el-input>
                        </el-form-item>
                         <el-form-item label="商品数量" prop="number">
                            <el-input v-model="addForm.number" type="number"></el-input>
                        </el-form-item>
                        <el-form-item label="商品分类" prop="cate">
                            <el-cascader
                            v-model="addForm.cate"
                            :options="catelist"
                            expandTrigger="hover"
                            :props="cateProps"
                            @change="handleChange"
                            clearable>
                            </el-cascader>
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="商品参数" name="1">
                        <el-form-item :label="item.name" v-for="item in manydatalist" :key="item.id">
                            <el-checkbox-group v-model="item.items" >
                                <el-checkbox border :label="it" v-for="it in item.items" :key="it"></el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="商品属性" name="2">
                        <el-form-item :label="item.name" v-for="item in onlydatalist" :key="item.id">
                            <el-input v-model="item.onlyvalue"></el-input>
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="商品图片" name="3">
                        <!--action图像上传的webapi(绝对路径)-->
                        <el-upload
                        :action="uploadurl"
                        :on-preview="handlePreview"
                        :on-remove="handleRemove"
                        list-type="picture"
                        :headers="headerObj"
                        :on-success="UploadSuccess">
                            <el-button size="small" type="primary">点击上传</el-button>
                        </el-upload>
                    </el-tab-pane>
                    <el-tab-pane label="商品内容" name="4">
                        <!--文本编辑器-->
                        <quill-editor
                        v-model="addForm.content"
                        >
                        </quill-editor>
                        <el-button type="primary" class="btnadd" @click="addGoods()">添加商品</el-button>
                    </el-tab-pane>
                </el-tabs>
            </el-form>
        </el-card>


        <el-dialog
        title="图像预览"
        :visible.sync="previewDialogVisible"
        width="50%">
        <img :src="imagepreviewurl" class="previewimage"/>
        </el-dialog>
    </div>
</template>>

<script>
export default {
    data(){
        return{
            activeIndex:'0',
            addForm:{
                name:'',
                price:0,
                weight:0,
                number:0,
                cate:[],
                imageurl:[],
                content:''
            },
            addFormRules:{
                name:[
                    { required: true, message: '请输入商品名称', trigger: 'blur' }
                ],
                price:[
                    { required: true, message: '请输入商品价格', trigger: 'blur' }
                ],
                weight:[
                    { required: true, message: '请输入商品重量', trigger: 'blur' }
                ],
                number:[
                    { required: true, message: '请输入商品数量', trigger: 'blur' }
                ],
                cate:[
                    { required: true, message: '请输入商品分类', trigger: 'blur' }
                ]
            },
            catelist:[],
            cateProps:{
                //看到的
                label:'name',
                //选中的
                value:'id',
                //子标签
                children:'children'
            },
            manydatalist:[],
            onlydatalist:[],
            uploadurl:'http://127.0.0.1:9003/Upload',
            headerObj:{
                Authorization:sessionStorage.getItem('token')
            },
            previewDialogVisible:false,
            imagepreviewurl:''
        }
    },
    created(){
        this.getCategories()
    },
    methods:{
        async getCategories(){
            const {data:res} = await this.$http.get('GetCategories')
            if(res.code !== 1){
                return this.$message.error('获取商品分类失败');
            }
            this.catelist = res.data
        },
        //级联选择器 选中项变化
        handleChange(){

        },
        beforetabLeave(activeName,oldActiveName){
            if(oldActiveName === '0' ){
                if(this.addForm.name.trim().length === 0){
                    this.$message.error('请填写商品名称')
                    return false
                }
                if(this.addForm.cate.length !== 3){
                    this.$message.error('请选择商品分类')
                    return false
                }
            }       
        },
        async tabClick(){
            //1:访问动态参数面板
            if(this.activeIndex === '1'){
                 const {data:res} = await this.$http.get('GetParam')
                if(res.code !== 1){
                    return this.$message.error('获取商品参数失败')
                }
                this.manydatalist = res.data
                // console.log(this.manydatalist)
            }
            else if(this.activeIndex === '2'){
                const {data:res} = await this.$http.get('GetParam')
                if(res.code !== 1){
                    return this.$message.error('获取商品属性失败')
                }
                this.onlydatalist = res.data
                console.log(this.onlydatalist)
            }
        },
        //图像预览
        handlePreview(file){
            this.imagepreviewurl = 'http://127.0.0.1:9003/GetImage?id=' + file.name
            console.log(this.imagepreviewurl)
            this.previewDialogVisible = true
        },
        //删除图像
        handleRemove(file){
            //从图像列表删除图像，避免提交
            const filename =  file.name
            const index = this.addForm.imageurl.findIndex(x => x === filename)
            this.addForm.imageurl.splice(index,1)
            // console.log(this.addForm.imageurl)
        },
        //图像上传成功的事件
        UploadSuccess(response){
            this.addForm.imageurl.push(response.data)
            // console.log(this.addForm.imageurl)
        },
        async addGoods(){
            this.$refs.addFormRef.validate(valid=>{
                if(!valid){
                    return this.$message.error('请填写必要内容')
                }
            })
            const {data:res} = await this.$http.post('AddGoods',this.addForm);
            if(res.code != 1)
            {
                return this.$message.error(res.msg);
            }
            else
            {
                this.$message.success('添加成功');
                this.$router.push('/goods')
            }
        }
    }
}
</script>

<style lang="less" scoped>
.el-checkbox{
    margin: 0 15px 0 0 !important;
}
.previewimage{
    width: 100%;
    height: 600px;
}
.btnadd{
    margin-top: 15px;
}
</style>