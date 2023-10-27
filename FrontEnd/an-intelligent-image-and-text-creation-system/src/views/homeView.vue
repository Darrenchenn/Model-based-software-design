<script setup>
import axios from 'axios'
import { ref } from 'vue'

const userName = localStorage.getItem('username')
const serverAddress = import.meta.env.VITE_serverAddress

const personalUrlInput = ref('')
const isFetching = ref(false)

const onClickWeChatForwarding = () => {
  if (isFetching.value) return
  isFetching.value = true

  axios
    .get(
      serverAddress +
        `/forward/wechat?username=${userName}&title=Testing&message=Test message from AutoPen&url=${personalUrlInput.value}`
    )
    .then((res) => {
      if (res.status === 200) {
        personalUrlInput.value = ''
        isFetching.value = false
      }
    })
    .catch((err) => {
      console.log(err)
      isFetching.value = false
    })
}
</script>

<template>
  <div class="container-fluid mx-5">
    <div class="mt-3 display-5">Welcome Back, {{ userName }}!</div>
    <div class="mt-3">
      <div class="mb-3">
        If you want to receive WeChat forwarding from others, please follow the steps below:
      </div>
      <div class="mb-3">
        1. Visit <a href="https://push.showdoc.com.cn/#/">https://push.showdoc.com.cn/#/</a>
      </div>
      <div class="mb-3">2. Click "登录" on the top right hand corner</div>
      <div class="mb-3">3. Scan the QR code on the screen</div>
      <div class="mb-3"></div>
      <div class="mb-3">4. Log in in WeChat</div>
      <div class="mb-3">5. Copy your personal url</div>
      <div class="mb-3">6. Input your personal url below and click submit</div>
      <div class="form-floating mb-3">
        <input
          v-model="personalUrlInput"
          type="text"
          class="form-control"
          id="floatingInput"
          placeholder="Personal url"
        />
        <label for="floatingInput">Personal url</label>
        <button
          :disabled="isFetching"
          @click="onClickWeChatForwarding"
          class="mt-2 btn btn-outline-warning align-middle text-center"
        >
          <div v-if="isFetching" class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div v-else>Submit</div>
        </button>
      </div>
      <div class="mb-3">7. You should receive test message on your WeChat</div>
      <div class="mb-3">
        You are good to go! Others can forward content to you with your username!
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
