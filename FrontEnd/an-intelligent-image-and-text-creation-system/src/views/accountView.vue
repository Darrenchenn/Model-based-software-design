<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const userId = localStorage.getItem('userId')
const username = localStorage.getItem('username')
const email = localStorage.getItem('userEmail')
const weChatId = localStorage.getItem('userWeChatId')
const identity = localStorage.getItem('identity')

const onClickSignOutBtn = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<template>
  <div class="container-fluid text-center pt-4">
    <div class="mb-3">userId: {{ userId }}</div>
    <div class="mb-3">username: {{ username }}</div>
    <div class="mb-3">email: {{ email }}</div>
    <div class="mb-3">weChatId: {{ weChatId }}</div>
    <div class="mb-3">identity: {{ identity }}</div>
    <button @click="onClickSignOutBtn" type="button" class="btn btn-warning mb-3">Sign out</button>
  </div>
</template>

<style scoped></style>
