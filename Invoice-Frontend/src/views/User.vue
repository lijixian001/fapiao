<!--
  用户管理页面组件（支持PC+移动端响应式）
  功能说明：
  - 用户列表展示与分页
  - 按关键字（用户名/姓名）搜索用户
  - 新增、编辑、删除用户
  - 用户状态（启用/禁用）管理
  - PC端：搜索栏一行多列，表格正常展示
  - 移动端：搜索栏单列垂直排列，表格横向滑动，弹窗全屏
-->
<template>
  <div class="user-page">
    <el-card class="page-card">
      <!-- 搜索栏：PC端一行多列，移动端单列垂直排列 -->
      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索用户名/姓名"
          clearable
          @keyup.enter="handleSearch"
          class="search-item search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div class="search-buttons">
          <el-button type="primary" @click="handleSearch" class="search-btn">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset" class="search-btn">重置</el-button>
        </div>
        <el-button type="success" @click="handleAdd" class="add-btn">
          <el-icon><Plus /></el-icon>新增用户
        </el-button>
      </div>

      <!-- 用户数据表格：移动端支持横向滑动查看 -->
      <div class="table-wrapper">
        <el-table :data="tableData" v-loading="loading" class="user-table">
          <el-table-column prop="username" label="用户名" width="140" />
          <el-table-column prop="real_name" label="真实姓名" width="140" />
          <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
          <el-table-column prop="phone" label="手机号" width="140" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
                {{ row.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页组件：移动端居中对齐 -->
      <el-pagination
        class="pagination-wrapper"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>

    <!-- 新增/编辑用户对话框：移动端全屏展示 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :fullscreen="isMobile"
      class="user-dialog"
    >
      <el-form :model="formData" label-width="100px" class="user-form">
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
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
// 导入Vue组合式API
import { ref, reactive, onMounted, onUnmounted } from 'vue'
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
// 是否为移动端
const isMobile = ref(false)

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

// 用户列表数据
const tableData = ref([])

// 搜索表单数据
const searchForm = reactive({
  keyword: ''
})

// 分页配置
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 用户表单数据（新增/编辑用）
const formData = reactive({
  username: '',
  password: '',
  real_name: '',
  email: '',
  phone: '',
  status: 1
})

// 获取用户列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await getUserList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined
    })
    tableData.value = res.list
    pagination.total = res.total
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置搜索
const handleReset = () => {
  searchForm.keyword = ''
  pagination.page = 1
  fetchData()
}

// 新增用户
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增用户'
  editId.value = null
  Object.keys(formData).forEach(key => {
    if (key === 'status') {
      formData[key] = 1
    } else {
      formData[key] = ''
    }
  })
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  editId.value = row.id
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    submitLoading.value = true
    const submitData = { ...formData }
    // 将空字符串的整数字段转换为null，避免后端验证失败
    const intFields = ['role_id', 'status']
    intFields.forEach(field => {
      if (submitData[field] === '' || submitData[field] === null || submitData[field] === undefined) {
        submitData[field] = null
      }
    })
    if (isEdit.value) {
      await updateUser(editId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await createUser(submitData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitLoading.value = false
  }
}

// 删除用户
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

// 组件挂载时
onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  fetchData()
})

// 组件卸载时
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 页面卡片容器 */
.page-card {
  width: 100%;
}

/* ========== 搜索栏样式 ========== */
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-item {
  flex-shrink: 0;
}

.search-input {
  width: 300px;
}

.search-buttons {
  display: flex;
  gap: 8px;
}

.add-btn {
  margin-left: auto;
}

/* ========== 表格样式 ========== */
.table-wrapper {
  margin-top: 20px;
  width: 100%;
  overflow-x: auto;
}

.user-table {
  width: 100%;
  min-width: 700px;
}

/* ========== 分页样式 ========== */
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* ========== 对话框底部按钮 ========== */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ========== 移动端响应式样式（<=768px） ========== */
@media screen and (max-width: 768px) {
  /* 搜索栏改为垂直排列 */
  .search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .search-item {
    width: 100% !important;
  }

  .search-buttons {
    width: 100%;
    display: flex;
    gap: 10px;
  }

  .search-btn {
    flex: 1;
    min-height: 44px;
  }

  .add-btn {
    margin-left: 0;
    width: 100%;
    min-height: 44px;
  }

  /* 表格区域调整 */
  .table-wrapper {
    margin-top: 15px;
    margin-left: -12px;
    margin-right: -12px;
    width: calc(100% + 24px);
  }

  .user-table {
    font-size: 13px;
  }

  /* 分页居中 */
  .pagination-wrapper {
    justify-content: center;
    margin-top: 15px;
    overflow-x: auto;
  }

  /* 表单标签宽度调整 */
  .user-form :deep(.el-form-item__label) {
    width: 80px !important;
  }
}

/* ========== 小屏幕适配（<=480px） ========== */
@media screen and (max-width: 480px) {
  .table-wrapper {
    margin-left: -10px;
    margin-right: -10px;
    width: calc(100% + 20px);
  }
}
</style>
