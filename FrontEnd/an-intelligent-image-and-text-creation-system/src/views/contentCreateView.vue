<script setup>
import axios from 'axios'
import { ref } from 'vue'

const serverAddress = import.meta.env.VITE_serverAddress

const contentTypeInput = ref('illustration')
const promptInput = ref('')
const negativePromptInput = ref('')
const heightInput = ref(720)
const widthInput = ref(720)
const keyInput = ref('')

const imgOutput = ref('')
const textOutput = ref('')

const onClickCreateBtn = () => {
  if (!promptInput.value || !keyInput.value) {
    alert('prompt or key input empty!')
    return
  }

  axios
    .post(serverAddress + '/sd_creator/', {
      prompt: promptInput.value,
      // prompt: 'studying at university of sydney at friday night',
      api_key: keyInput.value,
      // api_key: 'd1hcN8m8Pm0dUy80WUGZ574PviR0gZXfBH2ddXywr9rTlLBmCq3XetMhroHi'
      width: String(widthInput.value),
      height: String(heightInput.value)
    })
    .then((res) => {
      console.log(res.data)
      console.log(res.status)
      console.log(res.statusText)
      console.log(res.headers)
      console.log(res.config)
      return res
    })
    .then((res) => {
      // console.log(JSON.stringify(res))
      // return res.json()
      imgOutput.value = res.data.output[0]
    })
    .then()
    .catch((err) => {
      console.log(err)
    })

  // axios.get(serverAddress + '/creator/?prompt=a story about surviving a war')

  // fetch('http://40.76.249.160:8000/sd_creator/', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({
  //     prompt: 'studying at university of sydney at friday night',
  //     api_key: 'd1hcN8m8Pm0dUy80WUGZ574PviR0gZXfBH2ddXywr9rTlLBmCq3XetMhroHi'
  //   })
  // })
  //   .then((res) => res.json())
  //   .then((res) => console.log(res))
  //   .catch((err) => console.log(err))
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
            <!-- Input prompt -->
            <div class="form-floating mb-3 col-12 p-0">
              <textarea
                v-model="promptInput"
                class="form-control"
                placeholder="Prompt"
                id="promptInput"
              ></textarea>
              <label for="promptInput">Describe your requirements*</label>
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
              />
              <label for="heightInput">Height* (in pixels)</label>
            </div>
            <!-- Width -->
            <div class="form-floating mb-3 pe-0 col-6">
              <input
                v-model="widthInput"
                type="number"
                class="form-control"
                id="widthInput"
                placeholder="name@example.com"
              />
              <label class="ms-2" for="widthInput">Width* (in pixels)</label>
            </div>
            <!-- Key (for developer) -->
            <div class="form-floating mb-3 col-12 p-0">
              <input
                v-model="keyInput"
                type="text"
                class="form-control"
                id="Key"
                placeholder="name@example.com"
              />
              <label for="Key">Key*</label>
            </div>
            <!-- Submit Button -->
            <div class="mb-3 col-3 p-0 mb-3">
              <button @click="onClickCreateBtn" class="btn btn-outline-warning" id="submitBtn">
                Create
              </button>
            </div>
            <div class="col-12 mb-3 px-0">To-do: History</div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="container-fluid">
          <div class="row">
            <!-- Output Image -->
            <div class="col-12 border text-center mb-3 px-0">
              <div v-if="!imgOutput" id="placeHolder"></div>
              <img v-else class="img-fluid" :src="imgOutput" />
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
#submitBtn {
  width: 100%;
}
#submitBtn:hover {
  color: white;
}
</style>
