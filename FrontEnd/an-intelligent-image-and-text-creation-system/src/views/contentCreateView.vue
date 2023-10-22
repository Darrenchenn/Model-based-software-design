<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

const serverAddress = import.meta.env.VITE_serverAddress

const contentTypeInput = ref('illustration')
const promptInput = ref('')
const negativePromptInput = ref('')
const heightInput = ref(520)
const widthInput = ref(520)
const keyInput = ref('')

const imgOutput = ref('')
const textOutput = ref('')
const history = ref([])

const isFetchingResult = ref(false)
const isInputInvalid = computed(() => {
  if (promptInput.value && heightInput.value && widthInput.value && keyInput.value) return false
  else return true
})
const showValidationFeedback = ref(false)

onBeforeRouteLeave((to, from) => {
  if (!imgOutput.value && !textOutput.value && history.value.length === 0) return true

  const answer = window.confirm('The canvas and all history will be discarded! Continue?')
  if (!answer) return false
})

onMounted(() => {
  const placeHolder = {
    content_type: 'illustration',
    status: 'success',
    generationTime: 1.3200268745422363,
    id: 12202888,
    output: ['https://pbs.twimg.com/media/Fa7BgJ7VsAIELjd?format=jpg&name=large'],
    meta: {
      H: 512,
      W: 512,
      enable_attention_slicing: 'true',
      file_prefix: 'e5cd86d3-7305-47fc-82c1-7d1a3b130fa4',
      guidance_scale: 7.5,
      model: 'runwayml/stable-diffusion-v1-5',
      n_samples: 1,
      negative_prompt:
        ' ((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs))',
      outdir: 'out',
      prompt:
        'ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black eyeliner)) DSLR photography, sharp focus, Unreal Engine 5, Octane Render, Redshift, ((cinematic lighting)), f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame',
      revision: 'fp16',
      safetychecker: 'no',
      seed: 3499575229,
      steps: 20,
      vae: 'stabilityai/sd-vae-ft-mse'
    }
  }
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value.push(JSON.parse(JSON.stringify(placeHolder)))
  history.value[0].id = 12202888
  history.value[0].content_type = 'illustration'
  history.value[0].output[0] =
    'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/e5cd86d3-7305-47fc-82c1-7d1a3b130fa4-0.png'
  history.value[1].id = 1
  history.value[1].content_type = 'socialMediaPost'
  history.value[1].output[0] =
    'https://i.pinimg.com/originals/0b/94/33/0b943300e968ba78fb55c6dc16b70631.jpg'
  history.value[2].id = 2
  history.value[2].content_type = 'icon'
  history.value[2].output[0] =
    'https://i.pinimg.com/originals/95/74/f4/9574f450742dccfac04c15d71d1f638a.jpg'
  history.value[3].id = 3
  history.value[3].content_type = 'icon'
  history.value[3].output[0] =
    'https://pbs.twimg.com/media/F2XgDoWaYAE5xKP?format=jpg&name=4096x4096'
  history.value[4].id = 4
  history.value[4].content_type = 'poster'
  history.value[4].output[0] =
    'https://i.pinimg.com/originals/c3/35/ef/c335ef807fa5693f1c05952759ed2436.jpg'
  history.value[5].id = 5
  history.value[5].content_type = 'poster'
  history.value[5].output[0] =
    'https://i.pinimg.com/originals/10/41/52/104152ece82da03225e57a510dcf2b4b.jpg'
  imgOutput.value = JSON.parse(JSON.stringify(placeHolder))
  imgOutput.value.id = 6
})

const addCurrentOutputToHistory = () => {
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
  const contentType = contentTypeInput.value

  if (isFetchingResult.value) return
  if (isInputInvalid.value) {
    showValidationFeedback.value = true
    return
  }

  // Novel writing (GChatGPT)
  // axios.get(serverAddress + '/creator/?prompt=a story about surviving a war')
  // api_key: 'd1hcN8m8Pm0dUy80WUGZ574PviR0gZXfBH2ddXywr9rTlLBmCq3XetMhroHi
  // prompt: 'studying at university of sydney at friday night'

  try {
    addCurrentOutputToHistory()
    isFetchingResult.value = true
    showValidationFeedback.value = false
    axios
      .post(serverAddress + '/sd_creator/', {
        api_key: String(keyInput.value),
        prompt: String(promptInput.value),
        width: String(widthInput.value),
        height: String(heightInput.value)
      })
      .then((res) => res.data)
      .then((res) => {
        imgOutput.value = res
        imgOutput.value['content_type'] = contentType
        // console.log(JSON.stringify(res))
      })
  } catch (err) {
    console.log(err)
  } finally {
    isFetchingResult.value = false
  }
}

const onClickModifyBtn = () => {
  const contentType = contentTypeInput.value

  if (isFetchingResult.value) return
  if (isInputInvalid.value) {
    showValidationFeedback.value = true
    return
  }

  try {
    addCurrentOutputToHistory()
    isFetchingResult.value = true
    showValidationFeedback.value = false
    axios
      .post(serverAddress + '/sd_creator/', {
        api_key: String(keyInput.value),
        prompt: String(promptInput.value),
        width: String(widthInput.value),
        height: String(heightInput.value),
        init_image: String(imgOutput.value.output[0])
      })
      .then((res) => res.data)
      .then((res) => {
        imgOutput.value = res
        imgOutput.value['content_type'] = contentType
        // console.log(JSON.stringify(res))
      })
  } catch (err) {
    console.log(err)
  } finally {
    isFetchingResult.value = false
  }
}

const onClickFinishCreateBtn = () => {
  if (isFetchingResult.value) return
  // To do: submit content to server
}
</script>

<template>
  <div class="container-fluid pt-4">
    <div class="row px-3">
      <div class="col-12 col-lg-6 mb-3">
        <div class="container-fluid p">
          <div class="row">
            <!-- Select which type of content -->
            <label for="createIllustration" class="form-label d-block col-12 px-0"
              >What are we creating today?</label
            >
            <div class="form-check col-12 col-xl-3">
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
            <div class="form-check col-12 col-xl-3">
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
            <div class="form-check col-12 col-xl-3">
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
            <div class="form-check col-12 col-xl-3 mb-3">
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
            </div>
            <form
              class="col-12 container-fluid row needs-validation"
              :class="showValidationFeedback ? 'was-validated' : ''"
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
            <hr v-if="history.length !== 0" class="col-12 mb-2 px-0" />
            <div v-if="history.length !== 0" class="h2 col-12 mb-3 px-0">History</div>
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
