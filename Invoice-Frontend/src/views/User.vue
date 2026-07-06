<!--
  用户管理页面组件
  功能说明：
  - 用户列表展示与分页
  - 按关键字（用户名/姓名）搜索用户
  - 新增、编辑、删除用户
  - 用户状态（启用/禁用）管理
-->
<template>
  <div class="user-page">
    <el-card>
      <!-- 搜索栏：包含关键字搜索、搜索/重置按钮、新增用户按钮 -->
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索用户名/姓名"
          style="width: 300px"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" style="margin-left: auto" @click="handleAdd">
          <el-icon><Plus /></el-icon>新增用户
        </el-button>
      </div>

      <!-- 用户数据表格：展示用户列表，包含用户基本信息、状态、操作列 -->
      <el-table :data="tableData" style="width: 100%; margin-top: 20px" v-loading="loading">
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="real_name" label="真实姓名" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件：控制当前页码、每页条数，显示总记录数 -->
      <el-pagination
        style="margin-top: 20px; justify-content: flex-end; display: flex"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>

    <!-- 新增/编辑用户对话框：包含用户信息表单 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="formData.username" :disabled="isEdit" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码">
          <el-input v-model="formData.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="formData.real_name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="formData.email" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="formData.phone" />
        </el-form-item>
        <el-form-item v-if="isEdit" label="状态">
          <el-switch v-model="formData.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
// 导入Vue组合式API
import { ref, reactive, onMounted } from 'vue'
// 导入Element Plus消息提示和确认对话框组件
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入用户相关API接口函数
import { getUserList, createUser, updateUser, deleteUser } from '@/api/user'

// 表格数据加载状态
const loading = ref(false)
// 表单提交加载状态
const submitLoading = ref(false)
// 新增/编辑对话框显示状态
const dialogVisible = ref(false)
// 对话框标题
const dialogTitle = ref('')
// 是否为编辑模式
const isEdit = ref(false)
// 当前编辑的用户ID
const editId = ref(null)
// 用户列表数据
const tableData = ref([])

// 搜索表单数据
const searchForm = reactive({
  keyword: ''  // 搜索关键字（用户名/姓名）
})

// 分页配置
const pagination = reactive({
  page: 1,       // 当前页码
  page_size: 10, // 每页条数
  total: 0       // 总记录数
})

// 用户表单数据（新增/编辑用）
const formData = reactive({
  username: '',   // 用户名
  password: '',   // 密码（仅新增时使用）
  real_name: '',  // 真实姓名
  email: '',      // 邮箱
  phone: '',      // 手机号
  status: 1       // 状态（1：启用，0：禁用）
})

// 获取用户列表数据
const fetchData = async () => {
  loading.value = true
  try {
    // 调用API获取用户列表，传入分页和搜索参数
    const res = await getUserList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined
    })
    // 更新表格数据和总记录数
    tableData.value = res.list
    pagination.total = res.total
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理：重置为第一页并重新获取数据
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置搜索：清空搜索条件，重置为第一页并重新获取数据
const handleReset = () => {
  searchForm.keyword = ''
  pagination.page = 1
  fetchData()
}

// 新增用户：打开新增对话框，重置表单数据
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增用户'
  editId.value = null
  // 重置表单数据，根据字段类型设置默认值
  Object.keys(formData).forEach(key => {
    if (key === 'status') {
      formData[key] = 1
    } else {
      formData[key] = ''
    }
  })
  dialogVisible.value = true
}

// 编辑用户：打开编辑对话框，填充当前行数据
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  editId.value = row.id
  // 将当前行数据合并到表单中
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 提交表单：根据isEdit判断是新增还是编辑
const handleSubmit = async () => {
  try {
    submitLoading.value = true
    if (isEdit.value) {
      // 编辑模式：调用更新接口
      await updateUser(editId.value, formData)
      ElMessage.success('更新成功')
    } else {
      // 新增模式：调用创建接口
      await createUser(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    // 刷新列表数据
    fetchData()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitLoading.value = false
  }
}

// 删除用户：弹出确认框，确认后调用删除接口
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除这个用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

// 组件挂载时获取用户列表
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* 搜索栏样式：弹性布局，元素间距12px，垂直居中，允许换行 */
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
</style>
