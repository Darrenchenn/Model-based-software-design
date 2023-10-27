<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const serverAddress = import.meta.env.VITE_serverAddress

const userId = localStorage.getItem('userId')
const username = localStorage.getItem('username')
const identity = localStorage.getItem('identity')

const isFetching = ref(true)
const history = ref(null)

const isCreator = computed(() => identity === 'creator')

const onClickSignOutBtn = () => {
  localStorage.clear()
  router.push('/')
}

onMounted(() => {
  axios
    .get(
      serverAddress +
        (isCreator.value
          ? `/get_product/?creator_uuid=${userId}`
          : `/get_product/?responsible_supervisor_uuid=${userId}`)
    )
    .then((res) => res.data)
    .then((res) => {
      history.value = res
      console.log(JSON.stringify(history.value))
      isFetching.value = false
    })
    .catch((err) => {
      console.log(err)
    })
})
</script>

<template>
  <div class="container-fluid mx-5 mt-4">
    <div class="h1 mb-3">Account detail:</div>
    <div>
      <div class="mb-3">User id: {{ userId }}</div>
      <div class="mb-3">Username: {{ username }}</div>
      <div class="mb-3">Identity: {{ identity }}</div>
    </div>
    <div>
      <div v-if="!isFetching">
        <div>
          <div class="mb-3">
            {{
              (isCreator
                ? `No. of content created: `
                : `No. of content submitted to you for audition: `) + history.length
            }}
          </div>
          <div class="mb-3">
            No. of passed content:
            {{ history.filter((itm) => itm.audition_status === 'pass').length }}
          </div>
          <div class="mb-3">
            No. of failed content:
            {{ history.filter((itm) => itm.audition_status === 'false').length }}
          </div>
        </div>
      </div>
    </div>
    <button @click="onClickSignOutBtn" type="button" class="btn btn-warning mb-3">Sign out</button>
  </div>
</template>

<style scoped></style>
