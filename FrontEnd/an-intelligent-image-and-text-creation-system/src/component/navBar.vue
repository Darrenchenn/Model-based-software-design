<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const currentRoute = computed(() => {
  return route.name
})

const isNavItemActive = (NavItemRouteName) => {
  if (NavItemRouteName === currentRoute.value) return 'text-white disabled'
  else return 'text-secondary-emphasis'
}
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-warning">
    <div class="container-fluid">
      <span class="navbar-brand text-white">AutoPen</span>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/home" class="nav-link" :class="isNavItemActive('Home')"
              >Home</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              to="/content_create"
              class="nav-link"
              :class="isNavItemActive('Content Create')"
              >Content Create</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              to="/view_create_history"
              class="nav-link"
              :class="isNavItemActive('View Create History')"
              >View History</router-link
            >
          </li>
        </ul>
        <router-link to="/account" class="d-flex nav-link me-3" :class="isNavItemActive('Account')"
          >Account</router-link
        >
      </div>
    </div>
  </nav>
</template>

<style scoped></style>
