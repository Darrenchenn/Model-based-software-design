<script setup>
import { computed, onMounted, ref } from 'vue'

const creationHistory = ref(null)

const isFetchingCreationHistory = computed(() => {
  // return false
  return creationHistory.value === null ? true : false
})

onMounted(() => {
  // To-do: fetch history from server
  creationHistory.value = [
    {
      id: '1',
      title: 'example title 1',
      contentType: 'poster',
      imgSrc: 'https://i.pinimg.com/originals/0b/94/33/0b943300e968ba78fb55c6dc16b70631.jpg',
      isAudited: false
    },
    {
      id: '2',
      title: 'example title 2',
      contentType: 'social media post',
      textOutput: 'Example text output',
      imgSrc: 'https://i.pinimg.com/originals/95/74/f4/9574f450742dccfac04c15d71d1f638a.jpg',
      isAudited: false
    },
    {
      id: '3',
      title: 'example title 3',
      contentType: 'poster',
      imgSrc: 'https://pbs.twimg.com/media/F2XgDoWaYAE5xKP?format=jpg&name=4096x4096',
      isAudited: true,
      auditResult: true,
      auditComment: ''
    },
    {
      id: '4',
      title: 'example title 4',
      contentType: 'poster',
      imgSrc: 'https://i.pinimg.com/originals/c3/35/ef/c335ef807fa5693f1c05952759ed2436.jpg',
      isAudited: true,
      auditResult: false,
      auditComment: 'Your content sucks'
    },
    {
      id: '5',
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
  <div class="container-fluid mx-5 px-5">
    <div class="row mx-5 px-5">
      <div class="col-12 display-4 my-3">History</div>
      <div class="col-12" v-if="isFetchingCreationHistory"></div>
      <div class="col-12 fs-4" v-else-if="creationHistory.length === 0">
        <div>Oops! Look like you don't have any creation yet!</div>
        <div>Go create some!</div>
      </div>
      <div
        v-for="history in creationHistory"
        v-bind:key="history.id"
        class="col-12 border border-warning rounded mb-4 ps-0"
        id="historyItem"
      >
        <img :src="history.imgSrc" />
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  max-height: 200px;
  max-width: 200px;
  height: auto;
  width: auto;
}
</style>
