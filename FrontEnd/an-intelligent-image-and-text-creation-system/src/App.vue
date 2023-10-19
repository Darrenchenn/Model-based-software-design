<script setup>
// import { onMounted, ref } from 'vue'
// import axios from 'axios'

// const isLogin = ref(null)

// const fetchLoginStatus = () => {
//   // axios.get('').then(() => {})
//   setTimeout(() => {
//     isLogin.value = false
//     // isLogin.value = true
//   }, 2000)
// }

// onMounted(() => {
//   // fetchLoginStatus()
// })
</script>

<template>
  <router-view></router-view>
  <!-- <div v-if="isLogin === null" class="container-fluid">
    <div id="loadingScreen" class="row justify-content-center align-items-center">
      <div class="text-center">
        <div class="display-1 text-center text-warning">AutoPen</div>
        <div class="spinner-border text-primary text-warning mt-5" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="isLogin === false">
    <div>Login in page</div>
  </div>
  <div v-else>HomePage</div> -->
</template>

<style scoped>
/* #loadingScreen {
  height: 100vh;
  width: 100vw;
}

.spinner-border {
  width: 5rem;
  height: 5rem;
} */
</style>
