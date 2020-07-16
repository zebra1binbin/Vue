<template>
    <div>
        <!--面包屑导航-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>权限管理</el-breadcrumb-item>
            <el-breadcrumb-item>角色列表</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card>
            <el-row>
                <el-col>
                    <el-button type="primary" @click="addRoleDialogVisible = true">添加角色</el-button>
                </el-col>
            </el-row>
            <el-table :data="roleslist" border stripe>
                <!--展开列-->
                <el-table-column type="expand">
                    <template slot-scope="scope">
                         <!--分为24列-->
                        <el-row :class="['bdbottom' , i1 ===0 ? 'bdtop' : 'bdbottom','vcenter']" v-for="(item1,i1) in scope.row.items" 
                        :key="item1.id">
                            <!--一级权限-->
                            <el-col :span="5">
                                <el-tag type="danger" closable @close="removeRightById(item1.id)">
                                    {{item1.name}}
                                </el-tag>
                                <!--小图标-->
                                <i class="el-icon-caret-right"></i>
                            </el-col>
                             <!--二、三级权限-->
                            <el-col :span="19">
                                <!--for循环 嵌套渲染二级权限-->
                                <el-row :class="[i2 === 0 ? '':'bdtop','vcenter']" v-for="(item2,i2) in item1.items" :key="item2.id">
                                    <el-col :span="6">
                                        <el-tag type="success" closable @close="removeRightById(item2.id)">
                                            {{item2.name}}
                                        </el-tag>
                                        <!--小图标-->
                                        <i class="el-icon-caret-right"></i>
                                    </el-col>
                                     <el-col :span="18">
                                        <!--closable 关闭小图标-->
                                        <el-tag closable v-for="(item3) in item2.items" :key="item3.id" type="warning" @close="removeRightById(item3.id)">
                                            {{item3.name}}
                                        </el-tag>
                                     </el-col>
                                </el-row>
                            </el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <!--索引列-->
                <el-table-column label="#" type="index"></el-table-column>
                <el-table-column label="角色名称" prop="name"></el-table-column>
                <el-table-column label="角色描述" prop="description"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <!-- {{scope.row}} -->
                        <el-tooltip effect="dark" content="编辑" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row)">编辑</el-button>
                        </el-tooltip>
                        <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeUserbyID(scope.row.id)">删除</el-button>
                        </el-tooltip>
                        <!--提交树最底层的数组的id实现 树的默认选中节点(default-checked-keys)-->
                        <el-tooltip effect="dark" content="分配权限" placement="top" :enterable="false">
                            <el-button type="warning" icon="el-icon-setting" size="mini" @click="showSetRightDialog(scope.row)">分配权限</el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>


        <el-dialog
        title="添加角色"
        :visible.sync="addRoleDialogVisible"
        width="50%"
         @close="addDialogClosed()">
             <el-form :model="addForm" :rules="addFormRules" ref="addFormRef" label-width="80px">
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
                <el-form-item label="角色等级" prop="level">
                    <el-select width="30" v-model="levelvalue" placeholder="请选择等级" @change="levelChanged">
                        <el-option
                        v-for="item in levels"
                        :key="item.value"
                        :label="item.label"
                        :value="item.label">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="角色描述">
                    <el-input v-model="addForm.description"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addRoleDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addRole()">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
        title="编辑角色"
        :visible.sync="editRoleDialogVisible"
        width="50%"
         @close="editDialogClosed()">
             <el-form :model="editForm" :rules="editFormRules" ref="editFormRef" label-width="80px">
                <el-form-item label="角色ID" prop="id">
                    <el-input v-model="editForm.id" disabled=""></el-input>
                </el-form-item>
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>
                <el-form-item label="角色等级" prop="level">
                    <el-select width="30" v-model="editlevelvalue" placeholder="请选择等级" @change="editlevelChanged">
                        <el-option
                        v-for="item in levels"
                        :key="item.value"
                        :label="item.label"
                        :value="item.label">
                            <span style="float: left">{{ item.label }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="角色描述">
                    <el-input v-model="editForm.description"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editRoleDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editRole()">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
        title="分配权限"
        :visible.sync="setRightDialogVisible"
        width="50%"
        @close="setRightDialogClosed"
        >
            <!--树形组件-->
            <span>该功能API未启用</span>
            <el-tree 
            :data="rightlist" 
            :props="treeProps" 
            show-checkbox node-key="id" 
            default-expand-all
            :default-checked-keys="defKeys">
            </el-tree>
            <span slot="footer" class="dialog-footer">
                <el-button @click="setRightDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editRight">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>


<script>
    export default{
        data(){
            return{
                roleslist:[],
                addRoleDialogVisible:false,
                editRoleDialogVisible:false,
                addForm:{
                    name:'',
                    level:'',
                    description:''
                },
                 addFormRules:{
                    name: [
                        { required: true, message: '请输入角色名称', trigger: 'blur' }
                    ],
                    level: [
                        { required: true, message: '请选择权限级别', trigger: 'change' }
                    ]
                },
                editForm:{
 
                },
                editFormRules:{
                    name: [
                        { required: true, message: '请输入角色名称', trigger: 'blur' }
                    ],
                    level: [
                        { required: true, message: '请选择权限级别', trigger: 'change' }
                    ]
                },
                levels: [{
                    value: '最高级别权限',
                    label: '1'
                    }, {
                    value: '一般级别权限',
                    label: '2'    
                }],
                levelvalue:'',
                editlevelvalue:'',
                validret:false,
                setRightDialogVisible:false,
                rightlist:[],
                //树形控件的绑定对象
                treeProps:{
                    children: 'items',
                    label: 'name'
                },
                //默认选中的id
                defKeys:[]
            }
        },
        created(){
            this.getRolesList()
        },
        methods:{
            async getRolesList(){
                const {data:res} = await this.$http.get('GetRoles') 
                if(res.code !== 1){
                    return this.$message.error(res.msg);
                }
                this.roleslist = res.data
            },
            async removeRightById(id){
                await this.$confirm('该功能API未启用', '提示', {
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
            levelChanged(){
                this.addForm.level = this.levelvalue
            },
            editlevelChanged(){
                this.editForm.level = this.editlevelvalue
            },
            addDialogClosed(){
                this.$refs.addFormRef.resetFields()
            },
            editDialogClosed(){
                this.$refs.editFormRef.resetFields()
            },
            async addRole(){
                this.$refs.addFormRef.validate(valid =>{
                    this.validret = valid
                })
                if(!this.validret){
                    return
                }
                await this.$http.post('AddRole',{
                        name:this.addForm.name,
                        level:this.addForm.level,
                        description:this.addForm.description
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        return this.$message.error('添加用户失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.validret = false
                this.addRoleDialogVisible = false
                this.getRolesList()
                this.$message.success('添加角色成功')
            },
            showEditDialog(roseinfo){
                let _this = this
                _this.levels.forEach(function(item){
                    //str化
                    if(roseinfo.level + '' === item.label){
                        _this.editlevelvalue = item.label
                    }
                })
                this.editForm = roseinfo
                this.editRoleDialogVisible = true
            },
            async editRole(){
                this.$refs.editFormRef.validate(valid =>{
                    this.validret = valid
                })
                if(!this.validret){
                    return
                }
                await this.$http.post('UpdateRole',{
                    id:this.editForm.id,
                    name:this.editForm.name,
                    level:this.editForm.level,
                    description:this.editForm.description
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        return this.$message.error('修改角色失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.validret = false
                this.editRoleDialogVisible = false
                this.getRolesList()
                this.$message.success('修改角色成功')
            },
            async removeUserbyID(id){
                // console.log(id)
                const confirmResult = await this.$confirm('此操作将删除该角色, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).
                catch(err=>err);
                if(confirmResult !== 'confirm'){
                    return this.$message.info('已取消删除')
                }
                await this.$http.post('DeleteRole',{
                    id:id
                }).
                then(function (response) {
                    if(response.data.code != 1)
                    {
                        return this.$message.error('删除角色失败')
                    }
                }).catch(function (error) {
                    return this.$message.error(error)
                });
                this.getRolesList()
                return this.$message.success('删除角色成功')
            },
            async showSetRightDialog(row){
                const {data:res} = await this.$http.get('GetMenu')
                if(res.code !== 1){
                    return this.$message.error(res.msg);
                }
                this.rightlist = res.data
                // console.log(row)
                this.getLeafKeys(row,this.defKeys)
                // console.log(this.rightlist)
                this.setRightDialogVisible = true
            },
            //递归获取所有底层数组的id，并保存到defKeys
            getLeafKeys(node,arr){
                //底层节点的id长度为3
                if(node.id >= 100 ){
                    // console.log("push值：" + node.id)
                    return arr.push(node.id)
                }
                // console.log(node.items)
                if(node.items.length > 0){
                    node.items.forEach(item=>
                        this.getLeafKeys(item,arr)
                    )
                }
               
            },
            setRightDialogClosed(){
                this.defKeys.length = 0
            },
            editRight(){
                this.setRightDialogVisible = false
                return this.$message.success('删除权限成功')
            }
        }
    }
</script>


<style lang="less" scoped>
.el-tag{
    margin: 7px;

}

.bdtop{
    border-top: 1px solid#eee;
}

.bdbottom{
    border-bottom: 1px solid#eee;
}

.vcenter{
    display: flex;
    align-items: center;
}

</style>