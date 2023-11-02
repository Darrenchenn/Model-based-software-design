<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const supervisor_username = localStorage.getItem('username')
// const supervisor_userId = localStorage.getItem('userId')
const templates = ref([]) // 模板列表
const showReviewDialog = ref(false)
const selectedTemplate = ref(null)
const reviewText = ref('')
const auditStatus = ref('') // 添加审核状态变量
const pageSize = ref('10')
const currentPage = ref('0')
const serverAddress = import.meta.env.VITE_serverAddress

onMounted(() => {
  axios
    .get(
      serverAddress + `/get_all_templates/?page=${currentPage.value}&page_size=${pageSize.value}`
    )
    .then((res) => {
      templates.value = res.data
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
})

const newTemplateContent = ref('') // 用于存储新模板的内容

// 创建一个函数，用于添加新模板
const addTemplate = () => {
  if (newTemplateContent.value.trim() === '') {
    // 检查模板内容是否为空
    console.error('Template content is required')
    return
  }

  const newTemplateData = new FormData() // 使用 FormData 对象来构建 POST 数据
  newTemplateData.append('content', newTemplateContent.value) // 将 content 添加到 FormData 对象中

  axios
    .post(serverAddress + '/create_template/', newTemplateData, {
      headers: {
        'Content-Type': 'multipart/form-data' // 设置请求头
      }
    })
    .then((res) => {
      if (res.data.message === 'Template created successfully') {
        console.log(newTemplateData)
        // 清空输入框
        newTemplateContent.value = ''
        // 更新模板列表
        getTemplates()
      } else {
        console.error('Failed to add template')
      }
    })
    .catch((err) => {
      console.error('Error adding template:', err)
    })
}

const submitReview = () => {
  if (selectedTemplate.value) {
    const reviewData = new FormData() // 使用 FormData 对象来构建 POST 数据
    reviewData.append('content', reviewText.value)

    axios
      .post(serverAddress + `update_template_by_uuid/${selectedTemplate.value.uuid}/`, reviewData)
      .then((res) => {
        console.log('Review submitted successfully')
        getTemplates() // 更新模板列表
        showReviewDialog.value = false
      })
      .catch((error) => {
        console.error('Review submission error:', error)
      })
  }
}

// const openReviewDialog = (template) => {
//   selectedTemplate.value = template
//   showReviewDialog.value = true
//   reviewText.value = template.content // 在打开对话框时填充内容
// }

const deleteTemplate = () => {
  if (
    selectedTemplate.value &&
    selectedTemplate.value.uuid !== null &&
    selectedTemplate.value.uuid !== undefined
  ) {
    // 使用 HTTP DELETE 请求来删除模板
    console.log(selectedTemplate.value.uuid)
    axios
      .get(serverAddress + `/delete_template/${selectedTemplate.value.uuid}`)
      .then((res) => {
        if (res.status === 200) {
          console.log('Template deleted successfully')
          getTemplates() // 更新模板列表
          showReviewDialog.value = false
        } else {
          console.error('Failed to delete template')
        }
      })
      .catch((err) => {
        console.error('Error deleting template:', err)
      })
  } else {
    console.error('No template selected for deletion')
  }
}

const getTemplates = () => {
  console.log(`currentPage = ${currentPage.value}`)
  console.log(`pageSize = ${pageSize.value}`)
  axios
    .get(
      serverAddress + `/get_all_templates/?page=${currentPage.value}&page_size=${pageSize.value}`
    )
    .then((res) => {
      templates.value = res.data
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}
const changePage = (newPage) => {
  if (newPage >= 0) {
    currentPage.value = newPage
    getTemplates()
  } else {
    getTemplates()
  }
}
const toggleReviewDialog = (template) => {
  if (template === selectedTemplate.value && showReviewDialog) {
    selectedTemplate.value = null
    showReviewDialog.value = false
    reviewText.value = ''
  } else {
    selectedTemplate.value = template
    showReviewDialog.value = true
    reviewText.value = template.content // 在打开对话框时填充内容
    auditStatus.value = '' // 重置审核状态
  }
}
</script>

<template>
  <div class="div_a">
    <h1 class="h1_c">WELCOME Supervisor: {{ supervisor_username }}</h1>
    <h2 class="h1_d">Create new template for creator</h2>

    <!-- 显示模板列表 -->
    <div class="list-container">
      <div class="add_class">
        <textarea
          class="ta_b"
          v-model="newTemplateContent"
          placeholder="New Template Content"
        ></textarea>
        <div class="button-container">
          <button style="" @click="addTemplate">Add Template</button>
        </div>
      </div>
      <ul style="width: 100%; padding-top: 20px">
        <div class="div_b">
          <li v-for="template in templates" :key="template.uuid" class="li_a">
            <div class="list-item" @click="() => toggleReviewDialog(template)">
              <div class="list-item-content">
                <div class="list-item-left">
                  <p>Template ID: {{ template.uuid }}</p>
                  <p>Template Content:</p>
                  <p class="p1_a">{{ template.content }}</p>
                </div>
              </div>
            </div>
            <!-- 审核与评论对话框 -->
            <div v-if="template === selectedTemplate && showReviewDialog" class="review-dialog">
              <div style="display: flex; width: 100%">
                <textarea class="ta_a" v-model="reviewText"></textarea>
                <div style="display: flex; flex-direction: column; padding-left: 5%">
                  <button @click="submitReview">CONFIRM</button>
                  <button @click="deleteTemplate">DELETE</button>
                </div>
              </div>
            </div>
          </li>
        </div>
      </ul>
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage.value === 0">
          Previous
        </button>
        <button @click="changePage(currentPage + 1)">Next</button>
      </div>
    </div>
    <div style="height: 400px"></div>
  </div>
</template>

<style scoped>
body {
  background-color: #15171e !important;
  margin: 0;
  padding: 0;
}
.add_class {
  border-radius: 3px;
  width: 80%;
  background-color: #28334c;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
}
.p1_a {
  background-color: #939497;
  padding: 10px;
  border-radius: 3px;
}
.h1_c {
  padding-top: 10px;
  padding-bottom: 5px;
  padding-left: 10%;
  font-size: 30px;
  background-color: #15171e;
  color: #ffffff;
}
.h1_d {
  margin: 0 auto;
  width: 80%;
  color: #939497;
  font-size: 15px;
}
.div_a {
  background-color: #15171e;
}
.div_b {
  border-radius: 3px;
  padding: 10px 5px;
  width: 80%;
  border-top: 2px solid #939497; /* 上边框 */
  border-right: 2px solid #939497;
  border-left: 2px solid #939497;
}
.li_a {
  border-bottom: 2px solid #939497;
  padding-right: 10px;
  width: 100%;
  /* border: 2px solid #939497; */
}
.ta_a {
  width: 80%;
  background-color: #303237;
  color: #939497;
  border-radius: 3px;
}
.ta_b {
  width: 98%;
  margin: 0 auto;
  background-color: #303237;
  color: #939497;
  border-radius: 3px;
}

ul {
  list-style-type: none;
  padding: 0;
}

.list-item {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  cursor: pointer;
}

.list-item-content {
  padding-top: 5px;
  padding-left: 10px;
  display: flex;
  align-items: stretch;
  width: 100%; /* 占用 80% 的宽度 */
}

.list-item-left {
  padding-top: 5px;
  background-color: #23252b;
  color: #ffffff;
  width: 100%;
  border-radius: 3px;
  word-wrap: break-word;
  padding-left: 10px;
  padding-right: 10px;
  right: 5px;
}

.list-item-right {
  align-items: center;
  width: 50%;
  margin: 0 auto;
  display: flex;
}

.product-image {
  max-height: 200px;
  width: auto;
  justify-content: center;
  margin: 0 auto;
}

.review-dialog {
  margin-top: 10px;
  padding: 10px;
  /* 显示在下方 */

  width: 100%;
}
.list-container {
  padding-top: 10px;
  width: 80%;
  margin: 0 auto;
  box-sizing: border-box;
}
.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 其他样式规则 */
</style>
