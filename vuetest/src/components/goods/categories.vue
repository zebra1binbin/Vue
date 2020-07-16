<template>
    <div>
        <!--面包屑导航-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>商品分类</el-breadcrumb-item>
        </el-breadcrumb>
        <!--卡片视图-->
        <el-card>
            <el-row>
                <el-col>
                    <el-button type="primary" @click="showAddCateDialog()">添加分类</el-button>
                </el-col>
            </el-row>
            <tree-table class="treetable" :data="catelist" 
            :columns="columns" :show-row-hover="false" 
            border show-index index-text="#" 
            :expand-type="false" :selection-type="false" treeType>
                <!--是否有效-->
                <template slot="isok" slot-scope="scope">
                    <i class="el-icon-success" v-if="scope.row.useful === true"
                    style="color:lightgreen;"></i>
                    <i class="el-icon-error" v-else
                    style="color:red;"></i>
                </template>
                <!--排序-->
                <template slot="order" slot-scope="scope">
                    <el-tag size="mini" v-if="scope.row.level === 1">一级</el-tag>
                    <el-tag type="success" size="mini" v-else-if="scope.row.level === 2">二级</el-tag>
                    <el-tag type="warning" size="mini" v-else>三级</el-tag>
                </template>
                 <!--操作-->
                <template slot="option">
                    <el-button size="mini" type="primary" icon="el-icon-edit">编辑</el-button>
                    <el-button size="mini" type="danger" icon="el-icon-delete" @click="open">删除</el-button>
                </template>
            </tree-table>


            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryinfo.pagenum"
            :page-sizes="[1, 2, 3, 4]"
            :page-size="queryinfo.pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">

            </el-pagination>
        </el-card>

        <el-dialog
        title="添加分类"
        :visible.sync="addCateDialogVisible"
        width="50%"
        @close="addCateDialogClose()">
            <el-form :model="addCateForm" :rules="addCateFormRules" ref="addCateFormRef"
             label-width="100px">
                <el-form-item label="分类名称：" prop="name">
                    <el-input v-model="addCateForm.name"></el-input>
                </el-form-item>
                <el-form-item label="父级分类">
                    <!--options数据源-->
                    <!--props指定配置对象-->
                    <el-cascader
                    v-model="selectedKeys"
                    :options="parentCategoriesList"
                    expandTrigger="hover"
                    :props="cascaderProps"
                    @change="handleChange"
                    clearable
                    change-on-select>
                    </el-cascader>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addCateDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addCate()">确 定</el-button>
            </span>
        </el-dialog>



    </div>
</template>

<script>
    export default{
        data(){
            return{
                //商品分类数据
                catelist:[],
                queryinfo:{
                    pagenum:1,
                    pagesize:1
                },
                total:0,
                //table列的定义
                columns:[
                    {
                        //标题
                        label:'分类名称',
                        //绑定属性
                        prop:'name'
                    },
                    {
                        label:'是否有效',
                        type:'template',
                        template:'isok'
                    },
                    {
                        label:'排序',
                        type:'template',
                        template:'order'
                    },
                    {
                        label:'操作',
                        type:'template',
                        template:'option'
                    }
                ],
                addCateDialogVisible:false,
                //添加分类的表单数据对象
                addCateForm:{
                    name:'',
                    //父级id
                    pid:0,
                    //等级
                    level:1
                },
                addCateFormRules:{
                    name: [
                        { required: true, message: '请输入分类名称', trigger: 'change' }
                    ]
                },
                parentCategoriesList:[],
                //制定级联选择器的配置对象
                cascaderProps:{
                    //选中的
                    value:'id',
                    //看到的
                    label:'name',
                    //子标签
                    children:'children'
                },
                //选中的分类id
                selectedKeys:[]
            }
        },
        created(){
            this.getCategories()
        },
        methods:{
            async getCategories(){
                const {data:res} = await this.$http.get('GetCategories',{params: this.queryinfo})
                // console.log(res)
                if(res.code !== 1){
                    return this.$message.error('获取商品分类失败');
                }
                this.catelist = res.data
                this.total = 2
            },
            //监听pagesize
            handleSizeChange(newSize){
                this.queryinfo.pagesize = newSize
                this.$message.success('该API未启用分页');
            },
            //监听pagenum
            handleCurrentChange(newPage){
                this.queryinfo.pagesize = newPage
                this.$message.success('该API未启用分页');
            },
            showAddCateDialog(){
                this.getParentCategories()
                this.addCateDialogVisible = true
            },
            async getParentCategories(){
                const {data:res} = await this.$http.get('GetCategories')
                if(res.code !== 1){
                    return this.$message.error('获取父级分类数据失败');
                }
                console.log(res)
                this.parentCategoriesList = res.data
            },
            //选择项发生变化
            handleChange(){
                //selectedKeys长度大于零证明有选择
                if(this.selectedKeys.length > 0){
                    this.addCateForm.pid = this.selectedKeys[this.selectedKeys.length - 1]
                    this.addCateForm.level = this.selectedKeys.length
                }
                else{
                    this.addCateForm.pid = 0
                    this.addCateForm.level = 0
                }
            },
            addCate(){
                this.$message.success('pid:' + this.addCateForm.pid + ' level:' + this.addCateForm.level + 'API未启用');
                this.addCateDialogVisible = false
            },
            addCateDialogClose(){
                this.$refs.addCateFormRef.resetFields()
                this.selectedKeys.length = 0
                this.addCateForm.pid = 0
                this.addCateForm.level = 0
            },
            open() {
                this.$confirm('该API未启用, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
                }).catch(() => {
                    this.$message({
                    type: 'info',
                    message: '已取消删除'
                });          
            });
        }
        }
    }

</script>


<style lang="less" scoped>
.treetable{
    margin-top: 15px;
}
.el-cascader{
    width: 100%;
}
</style>