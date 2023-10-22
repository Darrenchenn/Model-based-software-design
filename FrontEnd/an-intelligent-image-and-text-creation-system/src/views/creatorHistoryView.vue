<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const creationHistory = ref(null)

const isFetchingCreationHistory = computed(() => {
  return creationHistory.value === null ? true : false
})

onMounted(() => {
  // To-do: fetch history from server
  creationHistory.value = [
    {
      id: '1',
      datetime: 20231020,
      title: 'example title 1',
      contentType: 'poster',
      imgSrc: 'https://i.pinimg.com/originals/0b/94/33/0b943300e968ba78fb55c6dc16b70631.jpg',
      isAudited: false
    },
    {
      id: '2',
      datetime: 20231021,
      title: 'example title 2',
      contentType: 'social media post',
      textOutput: 'Example text output',
      imgSrc: 'https://i.pinimg.com/originals/95/74/f4/9574f450742dccfac04c15d71d1f638a.jpg',
      isAudited: false
    },
    {
      id: '3',
      datetime: 20231022,
      title: 'example title 3',
      contentType: 'poster',
      imgSrc: 'https://pbs.twimg.com/media/F2XgDoWaYAE5xKP?format=jpg&name=4096x4096',
      isAudited: true,
      supervisor: 'example supervisor 1',
      auditResult: true,
      auditComment: ''
    },
    {
      id: '4',
      datetime: 20231023,
      title: 'example title 4',
      contentType: 'poster',
      imgSrc: 'https://i.pinimg.com/originals/c3/35/ef/c335ef807fa5693f1c05952759ed2436.jpg',
      isAudited: true,
      supervisor: 'example supervisor 2',
      auditResult: false,
      auditComment: 'Your content sucks'
    },
    {
      id: '5',
      datetime: 20231024,
      title: 'example title 5',
      contentType: 'illustration',
      imgSrc: 'https://i.pinimg.com/originals/10/41/52/104152ece82da03225e57a510dcf2b4b.jpg',
      isAudited: false
    }
  ]
  // creationHistory.value = []
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
          v-bind:key="history.id"
          :to="`/view_create_history/${history.id}`"
          class="container col-12 border border-warning rounded mb-4 ps-0"
          id="hideOverflow"
        >
          <div class="row" id="fullHeight">
            <div class="col-4 align-self-center">
              <img :src="history.imgSrc" />
            </div>
            <div class="col-8 py-2 d-flex flex-column">
              <div>Title: {{ history.title }}</div>
              <div>Date: {{ history.datetime }}</div>
              <div class="mb-auto">
                Content type:
                {{ history.contentType[0].toUpperCase() + history.contentType.slice(1) }}
              </div>
              <div class="text-end mb-3 me-2">
                <!-- if not audit -->
                <span
                  v-if="!history.isAudited"
                  class="h5 bg-secondary-subtle text-white rounded text-secondary py-2 px-3"
                  >Not audited</span
                >
                <!-- if audit success -->
                <span
                  v-else-if="history.isAudited && history.auditResult"
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
