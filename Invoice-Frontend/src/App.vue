<!--
  @description Vue应用根组件
  主要功能：
  1. 作为应用的最顶层组件，包含路由视图出口
  2. 提供全局样式重置和基础布局样式
  3. 所有页面组件都会通过 router-view 渲染在此组件内
-->

<template>
  <!-- 路由视图出口组件，用于渲染当前路由匹配的页面组件 -->
  <!-- 根据当前路由地址，动态渲染对应的页面组件 -->
  <router-view />
</template>

<!--
  使用 Vue 3 的 Composition API 语法糖
  script setup 是 Vue 3 的编译时语法糖，让代码更简洁
  此处暂时没有业务逻辑，保持空的 setup 以便后续扩展
-->
<script setup>
</script>

<!--
  全局样式定义
  注意：此处使用的是普通 style 标签（非 scoped），样式会全局生效
-->
<style>
/* 全局样式重置：清除所有元素的默认内外边距，统一盒模型为 border-box */
/* border-box 模式下，元素的宽高包含内边距和边框，便于布局计算 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 设置页面 body 的默认字体族，使用系统字体栈以获得最佳显示效果 */
/* 优先使用苹果系统字体，其次是 Windows 系统字体，最后是通用无衬线字体 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 设置应用根容器的样式，宽度占满全屏，高度占满整个视口高度 */
/* 确保应用始终充满整个浏览器窗口 */
#app {
  width: 100%;
  height: 100vh;
}
</style>
