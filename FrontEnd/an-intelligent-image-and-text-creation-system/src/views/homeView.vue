<script setup>
const userName = localStorage.getItem('userName')
</script>

<template>
  <div class="display-5">Welcome Back, {{ userName }}!</div>
</template>

<style scoped></style>
