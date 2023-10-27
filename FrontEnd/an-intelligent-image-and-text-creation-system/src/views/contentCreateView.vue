<script setup>
import axios from 'axios'
import { computed, ref } from 'vue'
import { onBeforeRouteLeave, useRouter } from 'vue-router'

const router = useRouter()
const serverAddress = import.meta.env.VITE_serverAddress
const finishCreateBtn = ref(null)
const contentTitleInputElement = ref(null)
const confirmSubmitModelBackBtn = ref(null)

const contentTypeInput = ref('illustration')
const promptInput = ref('')
const negativePromptInput = ref('')
const heightInput = ref(520)
const widthInput = ref(520)
const keyInput = ref('')
const contentTitleInput = ref('')

const imgOutput = ref('')
const textOutput = ref('')
const history = ref([])

const isFetchingResult = ref(false)
const isCreateInputInvalid = computed(() => {
  if (promptInput.value && heightInput.value && widthInput.value && keyInput.value) return false
  else return true
})
const showCreateValidationFeedback = ref(false)
const showTitleValidationFeedback = ref(false)

onBeforeRouteLeave((to, from) => {
  if ('id' in to.params) return true
  if (!imgOutput.value && !textOutput.value && history.value.length === 0) return true

  const answer = window.confirm('The canvas and all history will be discarded! Continue?')
  if (!answer) return false
})

const addCurrentOutputToHistory = () => {
  if (!imgOutput.value) return

  history.value.push(imgOutput.value)
  imgOutput.value = ''
  textOutput.value = ''
}

const moveHistoryToCanvas = (id) => {
  addCurrentOutputToHistory()
  imgOutput.value = history.value.filter((historyItem) => historyItem.id === id)[0]
  contentTypeInput.value = imgOutput.value.content_type
  promptInput.value = imgOutput.value.meta.prompt
  negativePromptInput.value = imgOutput.value.meta.negative_prompt
  heightInput.value = imgOutput.value.meta.H
  widthInput.value = imgOutput.value.meta.W
  history.value = history.value.filter((historyItem) => historyItem.id !== id)
  // To:do add textOutput history to textOutput
}

const onClickCreateBtn = () => {
  const datetime = new Date().toLocaleString()
  const contentType = contentTypeInput.value

  if (isFetchingResult.value) return
  if (isCreateInputInvalid.value) {
    showCreateValidationFeedback.value = true
    return
  }

  // Novel writing (GChatGPT)
  // axios.get(serverAddress + '/creator/?prompt=a story about surviving a war')
  // api_key: 'd1hcN8m8Pm0dUy80WUGZ574PviR0gZXfBH2ddXywr9rTlLBmCq3XetMhroHi
  // prompt: 'studying at university of sydney at friday night'

  addCurrentOutputToHistory()
  isFetchingResult.value = true
  showCreateValidationFeedback.value = false
  axios
    .post(serverAddress + '/sd_creator/', {
      api_key: String(keyInput.value),
      prompt: String(contentTypeInput.value + ' ' + promptInput.value),
      width: String(widthInput.value),
      height: String(heightInput.value)
    })
    .then((res) => res.data)
    .then((res) => {
      if (res.status === 'success') {
        imgOutput.value = res
        imgOutput.value['content_type'] = contentType
        imgOutput.value['datetime'] = datetime
        isFetchingResult.value = false
        console.log(JSON.parse(JSON.stringify(imgOutput.value)))
      } else {
        window.alert('Error!')
        isFetchingResult.value = false
        console.log(JSON.parse(JSON.stringify(res)))
      }
    })
    .catch((err) => {
      console.log(err)
      isFetchingResult.value = false
    })
}

const onClickModifyBtn = () => {
  const initImgUrl = imgOutput.value.output[0]
  const datetime = new Date().toLocaleString()
  const contentType = contentTypeInput.value

  if (isFetchingResult.value) return
  if (isCreateInputInvalid.value) {
    showCreateValidationFeedback.value = true
    return
  }

  console.log(`img: ${JSON.stringify(imgOutput.value)}`)

  addCurrentOutputToHistory()
  isFetchingResult.value = true
  showCreateValidationFeedback.value = false
  axios
    .post(serverAddress + '/sd_creator/', {
      api_key: String(keyInput.value),
      prompt: String(contentTypeInput.value + ' ' + promptInput.value),
      width: String(widthInput.value),
      height: String(heightInput.value),
      init_image: String(initImgUrl)
    })
    .then((res) => res.data)
    .then((res) => {
      if (res.status === 'success') {
        imgOutput.value = res
        imgOutput.value['content_type'] = contentType
        imgOutput.value['datetime'] = datetime
        isFetchingResult.value = false
        console.log(JSON.parse(JSON.stringify(imgOutput.value)))
      } else {
        window.alert('Error!')
        isFetchingResult.value = false
        console.log(JSON.parse(JSON.stringify(res)))
      }
    })
    .catch((err) => {
      console.log(err)
      isFetchingResult.value = false
    })
}

const onClickFinishCreateBtn = () => {
  if (isFetchingResult.value) return
  finishCreateBtn.value.click()
}

const onClickConfirmCreate = () => {
  if (isFetchingResult.value) return
  isFetchingResult.value = true

  if (!contentTitleInput.value) {
    showTitleValidationFeedback.value = true
    contentTitleInputElement.value.focus()
    return
  }

  const product = {}
  product.content = JSON.parse(JSON.stringify(imgOutput.value))
  product.content.title = String(contentTitleInput.value)
  product.creator_uuid = localStorage.getItem('userId')
  product.creator_name = localStorage.getItem('username')
  product.audition_status = 'no_submitted_for_audition'

  axios
    .post(serverAddress + '/insert_product/', product)
    .then((res) => res.data)
    .then((res) => {
      confirmSubmitModelBackBtn.value.click()
      router.push(`/view_create_history/${res}`)
    })
    .catch((err) => {
      console.log(err)
      window.alert('Something went wrong, please try again later!')
    })
}
</script>

<template>
  <div class="container-fluid pt-4">
    <div class="row px-3">
      <!-- Finish Create Button -->
      <button
        v-if="imgOutput"
        ref="finishCreateBtn"
        type="button"
        class="btn btn-primary d-none"
        data-bs-toggle="modal"
        data-bs-target="#finishCreateStaticBackdrop"
      >
        Launch static backdrop modal
      </button>
      <!-- Finish Create Modal -->
      <div
        v-if="imgOutput"
        class="modal fade"
        id="finishCreateStaticBackdrop"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
      >
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Finish create confirmation</h1>
              <button
                @click="(contentTitleInput = ''), (showTitleValidationFeedback = false)"
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body row">
              <div class="col-7 text-center">
                <img class="img-fluid" :src="imgOutput.output[0]" />
              </div>
              <div class="col-5 container-fluid">
                <div class="row">
                  <div class="col-12 mb-3">
                    <div
                      class="form-floating needs-validation"
                      :class="showTitleValidationFeedback ? 'was-validated' : ''"
                      novalidate
                    >
                      <input
                        ref="contentTitleInputElement"
                        v-model="contentTitleInput"
                        type="text"
                        class="form-control"
                        id="contentTitleInputElement"
                        placeholder="Title"
                        required
                      />
                      <label for="contentTitleInputElement" class="form-label"
                        >Content Title*</label
                      >
                      <div class="invalid-feedback">Title is required!</div>
                    </div>
                  </div>
                  <div class="col-12 mb-3">
                    <label for="historyContentType" class="form-label">Content Type</label>
                    <input
                      class="form-control"
                      id="historyContentType "
                      :value="
                        imgOutput.content_type[0].toUpperCase() + imgOutput.content_type.slice(1)
                      "
                      disabled
                      readonly
                    />
                  </div>
                  <div class="col-12 mb-3">
                    <label for="historyPrompt" class="form-label">Prompt</label>
                    <textarea
                      class="form-control"
                      id="historyPrompt"
                      :value="imgOutput.meta.prompt"
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
                      :value="imgOutput.meta.negative_prompt"
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
                      :value="imgOutput.meta.H"
                      disabled
                      readonly
                    />
                  </div>
                  <div class="col-6 mb-3">
                    <label for="historyWidth" class="form-label">Width</label>
                    <input
                      class="form-control"
                      id="historyWidth"
                      :value="imgOutput.meta.W"
                      disabled
                      readonly
                    />
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                @click="(contentTitleInput = ''), (showTitleValidationFeedback = false)"
                ref="confirmSubmitModelBackBtn"
                type="button"
                class="btn btn-outline-warning"
                data-bs-dismiss="modal"
              >
                Back
              </button>
              <button
                :disabled="isFetchingResult"
                @click="onClickConfirmCreate"
                type="button"
                class="btn btn-warning"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6 mb-3 border-end border-warning">
        <div class="container-fluid p">
          <div class="row">
            <!-- Select which type of content -->
            <label for="createIllustration" class="form-label d-block col-12 px-0"
              >What are we creating today?</label
            >
            <div class="form-check col-12 col-xl-4">
              <input
                v-model="contentTypeInput"
                class="form-check-input"
                type="radio"
                name="selectContentType"
                id="createIllustration"
                value="illustration"
              />
              <label class="form-check-label" for="createIllustration"> Illustration </label>
            </div>
            <div class="form-check col-12 col-xl-4">
              <input
                v-model="contentTypeInput"
                class="form-check-input"
                type="radio"
                name="selectContentType"
                id="createPoster"
                value="poster"
              />
              <label class="form-check-label" for="createPoster"> Poster </label>
            </div>
            <div class="form-check col-12 col-xl-4">
              <input
                v-model="contentTypeInput"
                class="form-check-input"
                type="radio"
                name="selectContentType"
                id="createIcon"
                value="icon"
              />
              <label class="form-check-label" for="createIcon"> Icon </label>
            </div>
            <!-- <div class="form-check col-12 col-xl-3 mb-3">
              <input
                v-model="contentTypeInput"
                class="form-check-input"
                type="radio"
                name="selectContentType"
                id="createSocialMediaPost"
                value="socialMediaPost"
              />
              <label class="form-check-label" for="createSocialMediaPost">
                Social Media Post
              </label>
            </div> -->
            <form
              class="col-12 container-fluid row needs-validation"
              :class="showCreateValidationFeedback ? 'was-validated' : ''"
              novalidate
            >
              <!-- Input prompt -->
              <div class="form-floating col-12 mb-3 p-0">
                <textarea
                  v-model="promptInput"
                  class="form-control"
                  placeholder="Prompt"
                  id="promptInput"
                  required
                ></textarea>
                <label for="promptInput">Describe your requirements*</label>
                <div class="invalid-feedback">Prompt is required!</div>
              </div>
              <!-- Negative input prompt -->
              <div class="form-floating mb-3 col-12 p-0">
                <textarea
                  v-model="negativePromptInput"
                  class="form-control"
                  placeholder="Negative Prompt"
                  id="negativePromptInput"
                ></textarea>
                <label for="promptInput">What you don't want in the content</label>
              </div>
              <!-- Height -->
              <div class="form-floating mb-3 ps-0 col-6">
                <input
                  v-model="heightInput"
                  type="number"
                  class="form-control"
                  id="heightInput"
                  placeholder="Height"
                  required
                />
                <label for="heightInput">Height* (in pixels)</label>
                <div class="invalid-feedback">Height is required!</div>
              </div>
              <!-- Width -->
              <div class="form-floating mb-3 pe-0 col-6">
                <input
                  v-model="widthInput"
                  type="number"
                  class="form-control"
                  id="widthInput"
                  placeholder="name@example.com"
                  required
                />
                <label class="ms-2" for="widthInput">Width* (in pixels)</label>
                <div class="invalid-feedback">Width is required!</div>
              </div>
              <!-- Key (for developer) -->
              <div class="form-floating mb-3 col-12 p-0">
                <input
                  v-model="keyInput"
                  type="text"
                  class="form-control"
                  id="Key"
                  placeholder="afwegwerbiuebr"
                  required
                />
                <label for="Key">Key*</label>
                <div class="invalid-feedback">Key is required!</div>
              </div>
            </form>
            <!-- Create Button -->
            <div class="col-4 mb-5">
              <button
                :disabled="isFetchingResult"
                @click="onClickCreateBtn"
                class="btn btn-outline-warning"
                id="btnInheritWidth"
              >
                {{ imgOutput ? 'Create new content' : 'Create' }}
              </button>
            </div>
            <!-- Modify existing content button -->
            <div v-if="imgOutput" class="col-4">
              <button
                :disabled="isFetchingResult"
                @click="onClickModifyBtn"
                class="btn btn-outline-warning"
                id="btnInheritWidth"
              >
                Modify Content
              </button>
            </div>
            <!-- Finish create button -->
            <div v-if="imgOutput" class="col-4">
              <button
                :disabled="isFetchingResult"
                @click="onClickFinishCreateBtn"
                class="btn btn-warning"
                id="btnInheritWidth"
              >
                Finish create
              </button>
            </div>
            <!-- History -->
            <div
              v-if="history.length !== 0"
              class="h2 col-12 border-top border-warning mb-3 pt-3 px-0"
            >
              History
            </div>
            <div
              v-for="historyContent in history"
              v-bind:key="historyContent.id"
              class="col-4 mb-3"
            >
              <img
                id="imgBtn"
                class="img-fluid p-0 rounded-0"
                :src="historyContent.output[0]"
                data-bs-toggle="modal"
                :data-bs-target="'#id_' + String(historyContent.id)"
              />
              <!-- Modal -->
              <div class="modal fade" :id="'id_' + String(historyContent.id)" tabindex="-1">
                <div class="modal-dialog modal-xl">
                  <div class="modal-content container-fluid px-0">
                    <div class="modal-body row">
                      <div class="col-7 text-center">
                        <img class="img-fluid" :src="historyContent.output[0]" />
                      </div>
                      <div class="col-5 container-fluid">
                        <div class="row">
                          <div class="col-12 mb-3">
                            <label for="historyContentType" class="form-label">Content Type</label>
                            <input
                              class="form-control"
                              id="historyContentType "
                              :value="
                                historyContent.content_type[0].toUpperCase() +
                                historyContent.content_type.slice(1)
                              "
                              disabled
                              readonly
                            />
                          </div>
                          <div class="col-12 mb-3">
                            <label for="historyPrompt" class="form-label">Prompt</label>
                            <textarea
                              class="form-control"
                              id="historyPrompt"
                              :value="historyContent.meta.prompt"
                              rows="5"
                              disabled
                              readonly
                            >
                            </textarea>
                          </div>
                          <div class="col-12 mb-3">
                            <label for="historyNegativePrompt" class="form-label"
                              >Negative Prompt</label
                            >
                            <textarea
                              class="form-control"
                              id="historyNegativePrompt"
                              :value="historyContent.meta.negative_prompt"
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
                              :value="historyContent.meta.H"
                              disabled
                              readonly
                            />
                          </div>
                          <div class="col-6 mb-3">
                            <label for="historyWidth" class="form-label">Width</label>
                            <input
                              class="form-control"
                              id="historyWidth"
                              :value="historyContent.meta.W"
                              disabled
                              readonly
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-outline-warning" data-bs-dismiss="modal">
                        Close
                      </button>
                      <button
                        @click="moveHistoryToCanvas(historyContent.id)"
                        type="button"
                        class="btn btn-warning"
                        data-bs-dismiss="modal"
                      >
                        Move to canvas
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="container-fluid">
          <div class="row">
            <!-- Canvas -->
            <div class="col-12 px-0 h2">Canvas</div>
            <!-- Output Image -->
            <div class="col-12 border text-center mb-3 px-0">
              <div
                v-if="!imgOutput"
                class="d-flex align-content-center justify-content-center"
                id="placeHolder"
              >
                <div
                  v-if="isFetchingResult"
                  class="align-self-center spinner-border text-warning"
                  role="status"
                >
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <img v-else class="img-fluid" :src="imgOutput.output[0]" />
            </div>
            <!-- Output Text (if social media post is selected) -->
            <div v-if="textOutput" class="col-12 border mb-3">{{ textOutput }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#placeHolder {
  width: 100%;
  height: 500px;
}
#imgBtn:hover {
  cursor: pointer;
}
.btn-outline-warning:hover {
  color: white;
}
#btnInheritWidth {
  width: 100%;
}
</style>
