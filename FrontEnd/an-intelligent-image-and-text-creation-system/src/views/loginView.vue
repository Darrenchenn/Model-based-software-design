<script setup>
import axios from 'axios'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const serverAddress = import.meta.env.VITE_serverAddress
const activeBtnClass = 'btn-warning text-white'
const disableBtnClass = 'btn-secondary text-secondary-emphasis'

const isSignInSelected = ref(true)
const emailInput = ref('')
const passwordInput = ref('')
const usernameInput = ref('')
const weChatIdInput = ref('')
const identitySelect = ref('creator')
const showValidationFeedback = ref(false)

const onClickSelectLogInBtn = () => {
  isSignInSelected.value = true
  showValidationFeedback.value = false
}

const onClickSelectSignUpBtn = () => {
  isSignInSelected.value = false
  showValidationFeedback.value = false
}

const logInBtnClass = computed(() => {
  if (isSignInSelected.value) return activeBtnClass
  else return disableBtnClass
})

const signUpBtnClass = computed(() => {
  if (isSignInSelected.value) return disableBtnClass
  else return activeBtnClass
})

const onClickLogInBtn = () => {
  if (!usernameInput.value || !passwordInput.value) {
    showValidationFeedback.value = true
    return
  }

  const form = new FormData()
  form.append('username', String(usernameInput.value))
  form.append('password', String(passwordInput.value))

  axios
    .post(serverAddress + '/login_user/', form)
    .then((res) => res.data)
    .then((res) => {
      if ('uuid' in res) {
        localStorage.setItem('userId', res.uuid)
        localStorage.setItem('username', res.username)
        localStorage.setItem('userEmail', res.contact_info.email)
        localStorage.setItem('userWeChatId', res.contact_info.wechat_id)
        localStorage.setItem('identity', res.user_type)
        router.push('/home')
      } else {
        passwordInput.value = ''
        window.alert('Username or password incorrect!')
      }
    })
    .catch((err) => {
      window.alert('Something went wrong. Please try again later!')
      console.log(err)
    })
}

const onClickSignUpBtn = () => {
  if (!usernameInput.value || !passwordInput.value) {
    showValidationFeedback.value = true
    return
  }

  const form = new FormData()
  form.append('username', String(usernameInput.value))
  form.append('password', String(passwordInput.value))
  form.append('email', String(emailInput.value))
  form.append('wechat_id', String(weChatIdInput.value))
  form.append('user_type', String(identitySelect.value))

  axios
    .post(serverAddress + '/register_user/', form)
    .then((res) => {
      return res.data
    })
    .then((res) => {
      if ('uuid' in res) {
        localStorage.setItem('userId', res.uuid)
        localStorage.setItem('username', res.username)
        localStorage.setItem('userEmail', res.contact_info.email)
        localStorage.setItem('userWeChatId', res.contact_info.wechat_id)
        localStorage.setItem('identity', res.user_type)
        router.push('/home')
      } else {
        window.alert('Something went wrong. Please try again later!')
        console.log(res)
      }
    })
    .catch((err) => {
      window.alert('Something went wrong. Please try again later!')
      console.log(err)
    })
}
</script>

<template>
  <div class="container-fluid">
    <div id="fullScreen" class="row justify-content-center align-items-center">
      <div class="col-xl-3 col-lg-4 col-md-5 col-sm-8 col-10">
        <div
          id="loginForm"
          class="px-4 border border-warning border-2 rounded shadow-lg needs-validation"
          :class="showValidationFeedback ? 'was-validated' : ''"
          novalidate
        >
          <!-- Title  -->
          <div class="text-center mt-3 mb-4 text-warning display-5 fw-medium">AutoPen</div>
          <!-- Login or Sign up Button -->
          <div class="btn-group mb-4" role="group">
            <button type="button" class="btn" :class="logInBtnClass" @click="onClickSelectLogInBtn">
              Log in
            </button>
            <button
              type="button"
              class="btn"
              :class="signUpBtnClass"
              @click="onClickSelectSignUpBtn"
            >
              Sign Up
            </button>
          </div>
          <!-- Username -->
          <div class="form-floating mb-3">
            <input
              type="text"
              v-model="usernameInput"
              class="form-control"
              id="usernameInput"
              placeholder="username"
              required
            />
            <label for="usernameInput">
              {{ isSignInSelected ? 'Username' : 'Username*' }}
            </label>
            <div class="invalid-feedback">Username is required!</div>
          </div>
          <!-- Password Input -->
          <div class="form-floating">
            <input
              type="password"
              class="form-control"
              id="passwordInput"
              placeholder="password"
              v-model="passwordInput"
              required
            />
            <label for="passwordInput">{{ isSignInSelected ? 'Password' : 'Password*' }}</label>
            <div class="invalid-feedback">Password is required!</div>
          </div>
          <!-- Extra Input if sign up -->
          <div v-if="!isSignInSelected">
            <!-- Email Input -->
            <div class="form-floating my-3">
              <input
                type="email"
                class="form-control"
                id="emailInput"
                placeholder="name@example.com"
                v-model="emailInput"
              />
              <label for="emailInput"> Email address </label>
            </div>
            <!-- WeChat Id Input -->
            <div class="form-floating mb-3">
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
          <div class="my-4 text-center">
            <button
              id="submitBtn"
              type="submit"
              class="btn btn-outline-warning"
              @click="
                () => {
                  if (isSignInSelected) {
                    onClickLogInBtn()
                  } else {
                    onClickSignUpBtn()
                  }
                }
              "
            >
              {{ isSignInSelected ? 'Log In' : 'Sign Up' }}
            </button>
          </div>
        </div>
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
