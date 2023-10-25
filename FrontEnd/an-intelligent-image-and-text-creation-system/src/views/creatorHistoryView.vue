<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const serverAddress = import.meta.env.VITE_serverAddress
const userId = localStorage.getItem('userId')

const creationHistory = ref(null)

const isFetchingCreationHistory = computed(() => {
  return creationHistory.value === null ? true : false
})

onMounted(() => {
  axios
    .get(serverAddress + `/get_product/?creator_uuid=${userId}`)
    .then((res) => res.data)
    .then((res) => {
      creationHistory.value = res
    })
    .catch((err) => {
      console.log(err)
    })
})
</script>

<template>
  <div class="container-fluid">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-6 container-fluid row">
        <div class="col-12 display-4 my-3">History</div>
        <div v-if="isFetchingCreationHistory" class="col-12 mt-3 text-center">
          <div class="mb-3 fs-4">Retrieving history...</div>
          <div class="spinner-border text-warning" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else-if="creationHistory.length === 0" class="col-12 fs-4">
          <div>Oops! Look like you don't have any creation yet!</div>
          <div>Go create some!</div>
        </div>
        <RouterLink
          v-else
          v-for="history in creationHistory"
          v-bind:key="history.uuid"
          :to="`/view_create_history/${history.uuid}`"
          class="container col-12 border border-warning rounded mb-4 ps-0"
          id="hideOverflow"
        >
          <div class="row" id="fullHeight">
            <div class="col-4 align-self-center">
              <img :src="history.content.output[0]" />
            </div>
            <div class="col-8 py-2 d-flex flex-column">
              <div>Title: {{ history.content.title }}</div>
              <div>Date: {{ history.content.datetime }}</div>
              <div class="mb-auto">
                Content type:
                {{
                  history.content.content_type === 'illustration'
                    ? 'Illustration'
                    : history.content.content_type === 'poster'
                    ? 'Poster'
                    : history.content.content_type === 'icon'
                    ? 'Icon'
                    : 'Social media post'
                }}
              </div>
              <div class="text-end mb-3 me-2">
                <!-- if not audit -->
                <span
                  v-if="history.audition_status === 'no_submitted_for_audition'"
                  class="h5 bg-secondary-subtle text-white rounded text-secondary py-2 px-3"
                  >Not audited</span
                >
                <!-- if audit success -->
                <span
                  v-else-if="history.audition_status === 'pass'"
                  class="h5 bg-success text-white rounded text-success py-2 px-3"
                  >Pass
                </span>
                <!-- if audit fail -->
                <span v-else class="h5 bg-danger text-white rounded text-danger py-2 px-3"
                  >Fail</span
                >
              </div>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
#hideOverflow {
  overflow: hidden;
}
#fullHeight {
  height: 200px;
}
img {
  overflow: hidden;
  max-height: 200px;
  max-width: 200px;
  height: auto;
  width: auto;
}
a {
  text-decoration: none;
  color: black;
}
</style>
