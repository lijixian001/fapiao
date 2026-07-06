/**
 * @description Vue应用入口文件
 * 主要功能：
 * 1. 创建Vue应用实例
 * 2. 配置并使用Pinia状态管理、Vue Router路由、Element Plus UI组件库
 * 3. 全局注册Element Plus图标组件
 * 4. 将应用挂载到DOM节点上
 */

// 从vue库中导入createApp函数，用于创建Vue应用实例
import { createApp } from 'vue'
// 从pinia库中导入createPinia函数，用于创建Pinia状态管理实例
import { createPinia } from 'pinia'
// 导入Element Plus UI组件库
import ElementPlus from 'element-plus'
// 导入Element Plus的样式文件
import 'element-plus/dist/index.css'
// 导入Element Plus的所有图标组件，作为一个命名空间对象
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 导入根组件App.vue
import App from './App.vue'
// 导入路由配置
import router from './router'

// 使用createApp函数创建Vue应用实例，传入根组件App
const app = createApp(App)

// 遍历Element Plus图标组件对象，将所有图标组件全局注册到Vue应用中
// 这样在任何组件中都可以直接使用这些图标组件，无需单独导入
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册并使用Pinia状态管理插件
app.use(createPinia())
// 注册并使用Vue Router路由插件
app.use(router)
// 注册并使用Element Plus UI组件库
app.use(ElementPlus)

// 将Vue应用实例挂载到页面上id为app的DOM元素上
app.mount('#app')
