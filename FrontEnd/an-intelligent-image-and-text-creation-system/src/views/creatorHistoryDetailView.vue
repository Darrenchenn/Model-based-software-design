<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const serverAddress = import.meta.env.VITE_serverAddress
let supervisorName = ''

const creationDetail = ref(null)
const supervisorIdInput = ref('')
const supervisorIdInputInvalidFeedback = ref('Supervisor Id is required!')
const showValidationFeedback = ref(false)

const isFetchingCreationDetail = computed(() => {
  if (!creationDetail.value) return true
  else return false
})

const isAudited = computed(() => {
  if (!creationDetail.value) return false

  if (
    creationDetail.value.audition_status === 'no_submitted_for_audition' ||
    creationDetail.value.audition_status === 'await_audition'
  )
    return false
  else return true
})

const isAwaitAudition = computed(() => {
  if (!creationDetail.value) return false
  else if (creationDetail.value.audition_status === 'await_audition') return true
  return false
})

const isNotSubmittedForAudition = computed(() => {
  if (!creationDetail.value) return false
  else if (creationDetail.value.audition_status === 'no_submitted_for_audition') return true
  return false
})

const auditResult = computed(() => {
  if (!creationDetail.value) return false

  if (creationDetail.value.audition_status === 'pass') return true
  else return false
})

const isSupervisorIdValid = async (supervisorId) => {
  let result

  await axios
    .get(serverAddress + `/verify_supervisor/${supervisorId}`)
    .then((res) => res.data)
    .then((res) => {
      if (res.message === 'success') {
        supervisorName = res.supervisor_namae
        result = true
      } else result = false
    })
    .catch((err) => {
      console.log(err)
      result = false
    })

  return result
}

const onClickSubmitAuditionBtn = async () => {
  if (!supervisorIdInput.value) {
    supervisorIdInputInvalidFeedback.value = 'Supervisor Id is required!'
    showValidationFeedback.value = true
    return
  }

  const isValid = await isSupervisorIdValid(supervisorIdInput.value)

  if (!isValid) {
    supervisorIdInputInvalidFeedback.value = 'Supervisor Id is incorrect!'
    supervisorIdInput.value = ''
    showValidationFeedback.value = true
    return
  }

  axios
    .post(serverAddress + '/update_product/', {
      uuid: String(creationDetail.value.uuid),
      creator_uuid: String(creationDetail.value.creator_uuid),
      creator_name: String(creationDetail.value.creator_name),
      responsible_supervisor_uuid: String(supervisorIdInput.value),
      responsible_supervisor_name: String(supervisorName),
      audition_status: String('await_audition'),
      audit_comment: '',
      content: creationDetail.value.content
    })
    .then((res) => {
      if (res.status === 200) {
        router.go()
      } else {
        console.log(JSON.parse(JSON.stringify(res)))
        window.alert('Something went wrong. Please try again later!')
      }
    })
    .catch((err) => {
      console.log(err)
      window.alert('Something went wrong. Please try again later!')
    })
}

onMounted(() => {
  // id = route.params.id
  axios
    .get(serverAddress + `/get_product/?uuid=${route.params.id}`)
    .then((res) => res.data)
    .then((res) => {
      creationDetail.value = res
      console.log(JSON.parse(JSON.stringify(creationDetail.value)))
    })
    .catch((err) => {
      console.log(err)
    })
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
      <div class="col-12 border-bottom border-warning mb-3 px-0 pb-3">
        <!-- if audited -->
        <div v-if="isAudited">
          <div class="fs-4">Audit Result</div>
          <div>
            <span> Audit: </span>
            <span v-if="auditResult" class="text-success fs-5 fw-bold"> Success </span>
            <span v-else class="text-danger fs-5 fw-bold"> Fail </span>
          </div>
          <div>Auditor: {{ creationDetail.responsible_supervisor_name }}</div>
          <div>Auditor Id: {{ creationDetail.responsible_supervisor_uuid }}</div>
          <div class="d-flex">
            <div class="me-1">Comment:</div>
            <div>{{ creationDetail.audit_comment }}</div>
          </div>
          <!-- If fail, show modify btn -->
          <div v-if="!auditResult">To-do: modify btn</div>
        </div>
        <div v-else-if="isAwaitAudition">
          <div class="text-warning fs-4 me-3 align-middle">Awaiting audition</div>
          <div>Auditor: {{ creationDetail.responsible_supervisor_name }}</div>
          <div>Auditor Id: {{ creationDetail.responsible_supervisor_uuid }}</div>
        </div>
        <!-- If not submitted for audition -->
        <div v-else-if="isNotSubmittedForAudition">
          <span class="text-secondary fs-4 me-3 align-middle">
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
                    @click="(showValidationFeedback = false), (supervisorIdInput = '')"
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                  ></button>
                </div>
                <div class="modal-body">
                  <div class="my-2">Submit to your supervisor for audition</div>
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
                      v-model="supervisorIdInput"
                      required
                    />
                    <label for="supervisorIdInput">Supervisor Id</label>
                    <div class="invalid-feedback">{{ supervisorIdInputInvalidFeedback }}</div>
                    <div class="form-text">Contact your supervisor for supervisor Id</div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button
                    @click="(showValidationFeedback = false), (supervisorIdInput = '')"
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
          <img class="img-fluid" :src="creationDetail.content.output[0]" />
        </div>
      </div>
      <div class="col-4 pe-0">
        <div class="container-fluid row pe-0">
          <div class="col-12 mb-3">
            <label for="contentType" class="form-label">Content type</label>
            <input
              class="form-control"
              id="contentType"
              :value="
                creationDetail.content.content_type === 'illustration'
                  ? 'Illustration'
                  : creationDetail.content.content_type === 'poster'
                  ? 'Poster'
                  : creationDetail.content.content_type === 'icon'
                  ? 'Icon'
                  : 'Social media post'
              "
              disabled
              readonly
            />
          </div>
          <div class="col-12 mb-3">
            <label for="title" class="form-label">Title</label>
            <input
              class="form-control"
              id="title"
              :value="creationDetail.content.title"
              disabled
              readonly
            />
          </div>
          <div class="col-12 mb-3">
            <label for="datetime" class="form-label">Date</label>
            <input
              class="form-control"
              id="datetime"
              :value="creationDetail.content.datetime"
              disabled
              readonly
            />
          </div>
          <div class="col-12 mb-3">
            <label for="historyPrompt" class="form-label">Prompt</label>
            <textarea
              class="form-control"
              id="historyPrompt"
              :value="creationDetail.content.meta.prompt"
              rows="5"
              disabled
              readonly
            >
            </textarea>
          </div>
          <div class="col-12 mb-3">
            <label for="historyNegativePrompt" class="form-label">Negative Prompt</label>
            <textarea
              class="form-control"
              id="historyNegativePrompt"
              :value="creationDetail.content.meta.negative_prompt"
              rows="5"
              disabled
              readonly
            >
            </textarea>
          </div>
          <div class="col-6 mb-3">
            <label for="historyHeight" class="form-label">Height</label>
            <input
              class="form-control"
              id="historyHeight"
              :value="creationDetail.content.meta.H"
              disabled
              readonly
            />
          </div>
          <div class="col-6 mb-3">
            <label for="historyWidth" class="form-label">Width</label>
            <input
              class="form-control"
              id="historyWidth"
              :value="creationDetail.content.meta.W"
              disabled
              readonly
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
