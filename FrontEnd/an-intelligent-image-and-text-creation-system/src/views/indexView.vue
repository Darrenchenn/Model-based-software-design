<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  router.replace({ path: '/login' })
})
</script>

<template>
  <div>Placeholder for index view</div>
</template>

<style scoped></style>
