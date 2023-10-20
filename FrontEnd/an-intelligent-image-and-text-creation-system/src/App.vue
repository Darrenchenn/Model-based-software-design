<script setup>
import { useRoute } from 'vue-router'
import NavBar from './component/navBar.vue'

const route = useRoute()
</script>

<template>
  <NavBar v-if="!route.meta.hideNavBar"></NavBar>
  <router-view></router-view>
</template>

<style scoped></style>
