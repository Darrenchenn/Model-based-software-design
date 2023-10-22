<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const creationDetail = ref(null)
const supervisorInput = ref('')
const showValidationFeedback = ref(false)

const isFetchingCreationDetail = computed(() => {
  if (!creationDetail.value) return true
  else return false
})

const onClickSubmitAuditionBtn = () => {
  if (!supervisorInput.value) {
    showValidationFeedback.value = true
    return
  }
}

onMounted(() => {
  // id = route.params.id
  // To-do: fetch creation detail from server
  creationDetail.value = {
    id: '4',
    datetime: 20231023,
    title: 'example title 4',
    contentType: 'poster',
    imgSrc: 'https://i.pinimg.com/originals/c3/35/ef/c335ef807fa5693f1c05952759ed2436.jpg',
    isAudited: true,
    auditResult: false,
    auditComment: 'Your content sucks'
  }
})
</script>

<template>
  <div class="container-fluid pt-4">
    <div v-if="isFetchingCreationDetail" class="mt-5 text-center">
      <div class="fs-4 my-3">Retrieving detail...</div>
      <div class="spinner-border text-warning" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else class="row px-3 mx-2 mb-5">
      <div class="col-12 h2 mb-3 px-0">Content Detail</div>
      <div class="col-12 fs-4 border-bottom border-warning mb-3 px-0 pb-3">
        <!-- <div v-if="creationDetail.isAudited">Audit Result</div> -->
        <div>
          <span class="text-secondary me-3 align-middle">
            This content is not submitted for audition
          </span>
          <!-- Button trigger modal -->
          <button
            type="button"
            class="btn btn-warning"
            data-bs-toggle="modal"
            data-bs-target="#auditSubmitBtn"
          >
            Submit for audition
          </button>
          <!-- Modal -->
          <div
            class="modal fade"
            id="auditSubmitBtn"
            data-bs-backdrop="static"
            data-bs-keyboard="false"
            tabindex="-1"
          >
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h1 class="modal-title fs-5">Submit for audition</h1>
                  <button
                    @click="(showValidationFeedback = false), (supervisorInput = '')"
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                  ></button>
                </div>
                <div class="modal-body" style="font-size: 1rem">
                  <div class="my-2">Submit to supervisor for audition</div>
                  <div
                    class="form-floating mb-3 needs-validation"
                    :class="showValidationFeedback ? 'was-validated' : ''"
                    novalidate
                  >
                    <input
                      type="text"
                      class="form-control"
                      id="supervisorIdInput"
                      placeholder="supervisor Id"
                      v-model="supervisorInput"
                      required
                    />
                    <label for="supervisorIdInput">Supervisor id</label>
                    <div class="invalid-feedback">Supervisor id is required</div>
                    <div class="form-text">Contact your supervisor for supervisor id</div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button
                    @click="(showValidationFeedback = false), (supervisorInput = '')"
                    type="button"
                    class="btn btn-outline-warning"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button @click="onClickSubmitAuditionBtn" type="button" class="btn btn-warning">
                    Submit
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-8 border-end border-warning px-0">
        <div class="border text-center me-4">
          <img class="img-fluid" :src="creationDetail.imgSrc" />
        </div>
      </div>
      <div class="col-4">data</div>
    </div>
  </div>
</template>

<style scoped></style>
