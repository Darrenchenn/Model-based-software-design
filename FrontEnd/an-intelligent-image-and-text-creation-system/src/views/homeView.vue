<script setup>
const userName = localStorage.getItem('username')
</script>

<template>
  <div class="display-5">Welcome Back, {{ userName }}!</div>
</template>

<style scoped></style>
