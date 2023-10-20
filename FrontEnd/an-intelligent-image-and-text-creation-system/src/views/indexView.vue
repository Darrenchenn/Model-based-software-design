<script setup></script>

<template>
  <div class="container-fluid">
    <div id="loadingScreen" class="row justify-content-center align-items-center">
      <div class="text-center">
        <div class="display-1 text-center text-warning">AutoPen</div>
        <div class="spinner-border text-primary text-warning mt-5" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#loadingScreen {
  height: 100vh;
  width: 100vw;
}

.spinner-border {
  width: 5rem;
  height: 5rem;
}
</style>
