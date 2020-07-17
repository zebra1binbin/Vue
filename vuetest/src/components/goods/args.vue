<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>分类参数</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card>
            <el-alert show-icon :closable="false" title="注意：只允许为第三级分类设置相关参数！" type="warning"> </el-alert>
            <el-row class="cat_opt">
                <el-col>
                    <span>选择商品分类：</span>
                    <el-cascader
                    v-model="selectedKeys"
                    :options="catelist"
                    expandTrigger="hover"
                    :props="cascaderProps"
                    @change="handleChange"
                    clearable
                    ></el-cascader>
                </el-col>
            </el-row>

            <el-tabs v-model="activeName" @tab-click="handleTabClick()">
                <el-tab-pane label="动态参数" name="many">
                    <el-button :disabled="isBtnDisable" type="primary" size="mini" @click="addDialogVisible = true">添加参数</el-button>
                    <el-table :data="manyTableData" border stripe>
                        <el-table-column type="expand">  
                            <template slot-scope="scope">
                                <!-- {{scope.row.items[0]}} -->
                                <el-tag v-for="item1 in scope.row.items" :key="item1" style="margin:10px" closable @close="reDescriptionById(item1)">
                                    {{item1}}
                                </el-tag>

                                <el-input
                                class="input-new-tag"
                                v-if="scope.row.inputVisible"
                                v-model="scope.row.inputValue"
                                ref="saveTagInput"
                                size="small"
                                @keyup.enter.native="handleInputConfirm(scope.row)"
                                @blur="handleInputConfirm(scope.row)"
                                >
                                </el-input>
                                <el-button v-else class="button-new-tag" size="small" @click="showInput(scope.row)">+ New Tag</el-button>
                            </template>
                        </el-table-column>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="参数名称" prop="name"></el-table-column>
                        <el-table-column label="操作">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" icon="el-icon-edit" @click="showEditDialog(scope.row.name)">编辑</el-button>
                                <el-button type="danger" size="mini"  icon="el-icon-delete" @click="DeleteClick()">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="静态属性" name="only">
                    <el-button :disabled="isBtnDisable" type="primary" size="mini" @click="addDialogVisible = true">添加属性</el-button>
                    <el-table :data="onlyTableData" border stripe>
                        <el-table-column type="expand">  
                            <template slot-scope="scope">
                                <!-- {{scope.row.items[0]}} -->
                                <el-tag v-for="item1 in scope.row.items" :key="item1" style="margin:10px ;0px" closable @close="reDescriptionById(item1)">
                                    {{item1}}
                                </el-tag>
                                <el-input
                                class="input-new-tag"
                                v-if="scope.row.inputVisible"
                                v-model="scope.row.inputValue"
                                ref="saveTagInput"
                                size="small"
                                @keyup.enter.native="handleInputConfirm(scope.row)"
                                @blur="handleInputConfirm(scope.row)"
                                >
                                </el-input>
                                <el-button v-else class="button-new-tag" size="small" @click="showInput(scope.row)">+ New Tag</el-button>
                            </template>
                        </el-table-column>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="属性名称" prop="name"></el-table-column>
                        <el-table-column label="操作">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" icon="el-icon-edit" @click="showEditDialog(scope.row.name)">编辑</el-button>
                                <el-button type="danger" size="mini"  icon="el-icon-delete" @click="DeleteClick()">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>

        </el-card>

        <el-dialog
        :title="'添加'+TitleText"
        :visible.sync="addDialogVisible"
        width="50%"
        @close="addDialogClosed()">
            <el-form ref="addFormRef" 
            :model="addForm" 
            :rules="addFormRules" 
            label-width="100px">
                <el-form-item :label="TitleText" prop='name'>
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addParams()">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
        :title="'修改'+TitleText"
        :visible.sync="editDialogVisible"
        width="50%"
        @close="editDialogClosed()">
            <el-form ref="editFormRef" 
            :model="editForm" 
            :rules="editFormRules" 
            label-width="100px">
                <el-form-item :label="TitleText" prop='name'>
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editParams()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data(){
        return{
            catelist:[],
            cascaderProps:{
                //选中的
                value:'id',
                //看到的
                label:'name',
                //子标签
                children:'children'
            },
            selectedKeys:[],
            //被激活的页签的名称
            activeName:'many',
            manyTableData:[],
            onlyTableData:[],
            addDialogVisible:false,
            editDialogVisible:false,
            addForm:{
                name:''
            },
            addFormRules:{
                name:[
                    { required: true, message: '请输入参数名称', trigger: 'blur' }
                ]
            },
            editForm:{
                name:''
            },
            editFormRules:{
                name:[
                    { required: true, message: '请输入参数名称', trigger: 'blur' }
                ]
            },
            //默认隐藏文本输入框
            inputVisible:false,
            //输入内容
            inputValue:''
        }
    },
    created(){
        this.getCateList()
    },
    methods:{
        async getCateList(){
            const {data:res} = await this.$http.get('GetCategories',{params: this.queryinfo})
            // console.log(res)
            if(res.code !== 1){
                return this.$message.error('获取商品分类失败');
            }
            this.catelist = res.data
        },
        handleChange(){
           this.getParamList()
        },
        handleTabClick(){
            console.log(this.activeName)
            this.getParamList()
        },
        async getParamList(){
            if(this.selectedKeys.length !==3){
                this.selectedKeys = []
                this.manyTableData = []
                this.onlyTableData = []
                return
            }
            const {data:res} = await this.$http.get('GetParam')
            if(res.code !== 1){
                 return this.$message.error('获取商品分类失败')
            }

            //inputVisible
            //inputValue
            //在这里会出现 多个items共用一个inputVisible、inputValue的bug
            res.data.forEach(element => {
                console.log('for' + element.items)
                //为每一行数据赋予自己inputVisible、inputValue
                element.inputVisible = false
                element.inputValue = ''
            });
            if(this.activeName === 'many'){
                this.manyTableData = res.data
            }
            else{
                this.onlyTableData = res.data
            }
            console.log(res.data)
        },
        addDialogClosed(){
            this.$refs.addFormRef.resetFields()
        },
        addParams(){
            this.$message.success('API未启用,添加成功')
            this.addDialogVisible = false
        },
        DeleteClick(){
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
        },
        showEditDialog(name){
            this.editForm.name = name
            this.editDialogVisible = true
        },
        editDialogClosed(){
            this.$refs.editFormRef.resetFields()
        },
        editParams(){
            this.$message.success('API未启用,修改成功')
            this.editDialogVisible = false
        },
        reDescriptionById(name)
        {
                this.$confirm('该API未启用, 是否继续删除:'+ name + '?', '提示', {
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
        },
        //文本框失去焦点、或摁下enter都会触发
        handleInputConfirm(row){
            if(row.inputValue.trim().length === 0){
                row.inputValue = ''
                row.inputVisible = false
                return
            }
            //调用web
            let _this = this
            _this.islike = false
            row.items.forEach(it => {
                if(it === row.inputValue.trim())
                {
                    _this.islike = true
                }
            })
            if(_this.islike){
                return this.$message.error('该参数已经存在')
            }
            else{
                row.items.push(row.inputValue.trim())
                row.inputValue = ''
                row.inputVisible = false
                this.$message.success('添加参数成功')
            }
            // console.log('ok')
        },
        showInput(row){
            row.inputVisible = true;
            //自动获取焦点
            //nextTick 当页面元素被重新渲染之后，才会指定回调函数中的代码
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        }
    },
    computed:{
        isBtnDisable(){
            if(this.selectedKeys.length !==3){
                return true
            }
            else{
                return false
            }
        },
        cateID(){
            if(this.selectedKeys.length ===3){
                return this.selectedKeys[2]
            }
            else{
                return null
            }
        },
        //动态计算标题文本
        TitleText(){
            if(this.activeName === 'many'){
                return '动态参数'
            }
            else{
                return '静态属性'
            }
        }
    }
}
</script>>


<style lang="less" scoped>
.cat_opt{
    margin: 15px 0;
}
.input-new-tag{
    width: 120px;
}
</style>>