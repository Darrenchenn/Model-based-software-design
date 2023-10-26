<script setup>
const userName = localStorage.getItem('username')
</script>

<template>
  <div class="container-fluid">
    <div class="mt-3 display-5">Welcome Back, {{ userName }}!</div>

    <div class="mt-5">
      <div class="mb-3">
        If you want to receive WeChat forwarding from others, please follow the steps below:
      </div>
      <div class="mb-3">
        1. Visit <a href="https://push.showdoc.com.cn/#/">https://push.showdoc.com.cn/#/</a>
      </div>
      <div class="mb-3">2. Click "登录" on the top right hand corner</div>
      <img src="../assets/image/img_sign_in.png" />
      <div class="mb-3">
        3. Visit <a href="https://push.showdoc.com.cn/#/">https://push.showdoc.com.cn/#/</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  width: auto;
  height: 100px;
}
</style>
