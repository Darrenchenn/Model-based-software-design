<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeBtnClass = 'btn-warning text-white'
const disableBtnClass = 'btn-secondary text-secondary-emphasis'

const isSignInSelected = ref(true)
const emailInput = ref('')
const passwordInput = ref('')
const weChatIdInput = ref('')
const identitySelect = ref('creator')

const onClickLogInBtn = () => {
  isSignInSelected.value = true
}

const onClickSignUpBtn = () => {
  isSignInSelected.value = false
}

const logInBtnClass = computed(() => {
  if (isSignInSelected.value) return activeBtnClass
  else return disableBtnClass
})

const signUpBtnClass = computed(() => {
  if (isSignInSelected.value) return disableBtnClass
  else return activeBtnClass
})

const onClickSubmitBtn = () => {
  // To-Do 連結後端登入/註冊
  localStorage.setItem('userName', 'example user name')
  localStorage.setItem('identity', identitySelect.value)
  router.push('/home')
}
</script>

<template>
  <div class="container-fluid">
    <div id="fullScreen" class="row justify-content-center align-items-center">
      <div class="col-xl-3 col-lg-4 col-md-5 col-sm-8 col-10">
        <form
          id="loginForm"
          class="text-center px-4 border border-warning border-2 rounded shadow-lg"
        >
          <!-- Title  -->
          <div class="mt-3 mb-4 text-warning display-5 fw-medium">AutoPen</div>
          <!-- Login or Sign up Button -->
          <div class="btn-group mb-4" role="group">
            <button type="button" class="btn" :class="logInBtnClass" @click="onClickLogInBtn">
              Log in
            </button>
            <button type="button" class="btn" :class="signUpBtnClass" @click="onClickSignUpBtn">
              Sign Up
            </button>
          </div>
          <!-- Email Input -->
          <div class="form-floating mb-3">
            <input
              type="email"
              class="form-control"
              id="emailInput"
              placeholder="name@example.com"
              v-model="emailInput"
            />
            <label for="emailInput">
              {{ isSignInSelected ? 'Email address' : 'Email address*' }}
            </label>
          </div>
          <!-- Password Input -->
          <div class="form-floating">
            <input
              type="password"
              class="form-control"
              id="passwordInput"
              placeholder="password"
              v-model="passwordInput"
            />
            <label for="passwordInput">{{ isSignInSelected ? 'Password' : 'Password*' }}</label>
          </div>
          <!-- Extra Input if sign up -->
          <div v-if="!isSignInSelected">
            <!-- WeChat Id Input -->
            <div class="form-floating my-3">
              <input
                type="text"
                class="form-control"
                id="weChatIdInput"
                placeholder="WeChat ID"
                v-model="weChatIdInput"
              />
              <label for="weChatIdInput">WeChat ID</label>
            </div>
            <!-- Select creator or supervisor -->
            <div class="input-group mb-3">
              <span class="input-group-text">I am a</span>
              <select class="form-select" v-model="identitySelect">
                <option value="creator" selected>Creator</option>
                <option value="supervisor">Supervisor</option>
              </select>
            </div>
          </div>
          <!-- Submit Button -->
          <div class="my-4">
            <button
              id="submitBtn"
              type="submit"
              class="btn btn-outline-warning"
              @click="onClickSubmitBtn"
            >
              {{ isSignInSelected ? 'Log In' : 'Sign Up' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
#fullScreen {
  height: 100vh;
  width: 100vw;
}
.btn-group {
  width: 100%;
}
#submitBtn {
  width: 40%;
}
#submitBtn:hover {
  color: white;
}
</style>
