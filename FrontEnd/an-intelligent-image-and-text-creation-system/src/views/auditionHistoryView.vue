<script setup>
import {computed, onMounted, ref} from "vue";
import axios from "axios";
const supervisor_username = localStorage.getItem('username')
const superviosr_userid = localStorage.getItem('userId')
const products = ref([])             // 未审核产品列表
const showReviewDialog = ref(false)  // 是否显示审核与评论对话框
const selectedProduct = ref(null)    // 选中的产品
const reviewText = ref('')            // 评论内容
const auditStatus = ref("false");      // 默认选择审核通过
const audit_cont_null=ref('');


onMounted(() => {
  axios.get('http://127.0.0.1:8000/get_product/')
      .then((res) => res.data)
      .then((res) => {
        products.value = res
        console.log(res)
      }).catch((err) => {
    console.log(err)
  });
})

const filteredProducts = computed(() => {
  // 使用 computed 属性来过滤产品列表
  return products.value.filter(product => {
    return (
      product.responsible_supervisor_uuid === superviosr_userid
    );
  });
});

const submitReview = () => {
  const reviewData = {
    uuid: selectedProduct.value.uuid,
    audit_comment: reviewText.value,
    audition_status: auditStatus.value,
  };

  axios.post('http://127.0.0.1:8000/update_product/', reviewData)
    .then((res) => {
      // 处理成功响应，可以根据后端返回的数据进行操作
      console.log('Review submitted successfully');
      // 更新前端产品列表或其他操作
      // 例如，刷新产品列表
      getProducts1();
      // 关闭评论对话框
      showReviewDialog.value = false;
    })
    .catch((error) => {
      // 处理错误响应，例如网络错误或后端验证失败
      console.error('Review submission error:', error);
      // 可以根据错误情况执行适当的操作
    });
};

const openReviewDialog = (product) => {
  // 打开审核与评论对话框
  selectedProduct.value = product;
  showReviewDialog.value = true;
}

const getProducts = () => {
  //获取更新列表
  axios.get('http://127.0.0.1:8000/get_product/')
      .then((res) => res.data)
      .then((res) => {
        products.value = res
        console.log(res)
      }).catch((err) => {
    console.log(err)
  });
}

const cancelAudition = (product) => {
  if (product) {
    console.log("Before clearing audit_comment:", product.audit_comment);
    product.audit_comment = '';
    console.log("After clearing audit_comment:", product.audit_comment);

    console.log("Before changing audition_status:", product.audition_status);
    product.audition_status = 'await_audition';
    console.log("After changing audition_status:", product.audition_status);

    // 清空 reviewText 的值
    reviewText.value = '';
    const cancelAudition = (product) => {
  if (product) {
    console.log("Before clearing audit_comment:", product.audit_comment);
    product.audit_comment = '';
    console.log("After clearing audit_comment:", product.audit_comment);

    console.log("Before changing audition_status:", product.audition_status);
    product.audition_status = 'no_submitted_for_audition';
    console.log("After changing audition_status:", product.audition_status);

    // 清空 reviewText 的值
    console.log("Before clearing reviewText:", reviewText.value);
    reviewText.value = '';
    console.log("After clearing reviewText:", reviewText.value);

    // 向后端发送请求以更新产品的审核状态和评论内容
    axios.post('http://127.0.0.1:8000/update_product/', {
      uuid: product.uuid,
      audit_comment: '',
      audition_status: 'no_submitted_for_audition'
    })
      .then((res) => {
        // 处理成功响应，可以根据后端返回的数据进行操作
        console.log('Audition Cancelled successfully');
        // 更新前端产品列表或其他操作
        // 例如，刷新产品列表
        getProducts1();
        // 关闭评论对话框
        showReviewDialog.value = false;
      })
      .catch((error) => {
        // 处理错误响应，例如网络错误或后端验证失败
        console.error('Audition Cancellation Error:', error);
        // 可以根据错误情况执行适当的操作
      });
  }
};

    // 向后端发送请求以更新产品的审核状态和评论内容
    axios.post('http://127.0.0.1:8000/update_product/', {
      uuid: product.uuid,
      audit_comment: '',
      audition_status: 'await_audition'
    })
      .then((res) => {
        // 处理成功响应，可以根据后端返回的数据进行操作
        console.log('Audition Cancelled successfully');
        // 更新前端产品列表或其他操作
        // 例如，刷新产品列表
        getProducts1();
        // 关闭评论对话框
        showReviewDialog.value = false;
      })
      .catch((error) => {
        // 处理错误响应，例如网络错误或后端验证失败
        console.error('Audition Cancellation Error:', error);
        // 可以根据错误情况执行适当的操作
      });
  }
};





const getProducts1 = () => {
  // 获取更新列表，并筛选出特定条件的产品
  axios.get('http://127.0.0.1:8000/get_product/')
    .then((res) => res.data)
    .then((res) => {
      // 使用 filter 方法筛选产品
      const filteredProducts = res.filter(product => {
        return (
          product. responsible_supervisor_uuid === superviosr_userid
        );
      });

      // 将筛选后的产品保存到 products 变量
      products.value = filteredProducts;
    })
    .catch((err) => {
      console.log(err);
    });
};


const auditStatusText = computed(() => {
  // 计算属性，根据审核状态返回相应文本
  return (status) => {
    if (status === "await_audition") {
      return "UNAUDITED";
    } else if (status === "pass") {
      return "PASS";
    } else if (status === "false") {
      return "NOT PASS";
    } else {
      return "未知状态";
    }
  };
});

// 添加一个方法，用于打开或关闭审核与评论对话框
const toggleReviewDialog = (product) => {
  if (product === selectedProduct && showReviewDialog) {
    selectedProduct.value = null
    showReviewDialog.value = false;
     reviewText.value = '';
  } else {
    selectedProduct.value = product;
    showReviewDialog.value = true;
     reviewText.value = '';
  }
};

</script>

<template>
  <div class="div_a">
    <h1 class="h1_c">WELCOME Supervisor :  {{supervisor_username}}</h1>
    <h2 class="h1_d">Please click one row to audit</h2>

    <!-- 显示产品列表 -->
    <div class="list-container">
      <ul style="width: 100%">
        <li v-for="product in filteredProducts" :key="product.uuid" class="li_a">
          <div class="list-item" @click="() => toggleReviewDialog(product)" >
            <div class="list-item-content">
              <div class="list-item-left">
                <h3>{{ product.name }}</h3>
                <p>Creator :</p>
                <p class="p1_a"> {{ product.creator_name }}</p>
                <p>Audition Content: </p>
                <p class="p1_a">{{ product.audit_comment ? product.audit_comment : 'No Comment Yet' }}</p>
                <p>Audition Status: </p>
                <p class="p1_a">{{ auditStatusText(product.audition_status) }}</p>
              </div>
              <div class="list-item-right">
                <!-- 显示图片 -->
                <img
                  :src="product.content.output[0]"
                  alt="Product Image"
                  :class="{ 'product-image': !selectedProduct || selectedProduct !== product }"
                  :style="{ width: selectedProduct === product ? '80%' : 'auto' ,margin: selectedProduct === product ? '0 auto' : '0 auto' }"
                  @click.stop
                />
              </div>
            </div>
          </div>
          <!-- 审核与评论对话框 -->
          <div v-if="product === selectedProduct && showReviewDialog" class="review-dialog">
            <div style="display: flex; width: 100%;">
              <textarea class="ta_a" v-model="reviewText" :placeholder="product.audit_comment ? product.audit_comment : 'Please comment'"></textarea>
              <div style="display: flex; flex-direction: column;padding-left: 5%">
                <select id="auditStatusSelect" v-model="auditStatus" style="padding-bottom: 5px;background-color: #303237;color: white;border-radius: 3px;">
                  <option value="pass">PASS</option>
                  <option value="false">NOT PASS</option>
                </select>
                <button @click="submitReview" style="background-color: #303237;color: white;border-radius: 3px;">CONFIRM</button>
                <button @click="cancelAudition(product)" style="background-color: #303237;color: white;border-radius: 3px;">Audition Cancel</button>
              </div>
            </div>
          </div>
        </li>
      </ul>
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
   .p1_a{
     background-color: #939497;
     padding: 10px;
     border-radius: 3px;

   }
  .h1_c{
    padding-top: 10px;
    padding-bottom: 5px;
    padding-left:10%;
    font-size: 30px;
    background-color: #15171e;
    color:#ffffff;
  }
  .h1_d{
    margin: 0 auto;
    width: 80%;
    color:#939497;
    font-size: 15px;
  }
  .div_a{

    background-color: #15171e;
  }
  .li_a{
    width:100%;
    border: 2px solid #939497;
  }
  .ta_a{
    width: 80%;
    background-color: #303237;
    color:#939497;
    border-radius: 3px;

  }
  .clickable-item {

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
    border-top: 2px solid #939497; /* 上边框 */
    margin-bottom: 10px;
    padding: 10px 2px;
    cursor: pointer;
  }

  .list-item-content {
    padding-left: 10px;
    display: flex;
    align-items: stretch;
    width: 100%; /* 占用 80% 的宽度 */
  }

  .list-item-left {

    background-color: #23252b;
    color:#ffffff;
    width: 50%;
    border-radius: 3px;
    word-wrap: break-word;
    padding-left: 10px;
    padding-right: 10px;
    right: 5px;
  }

  .list-item-right {
    align-items: center;
    width:50%;
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


  /* 其他样式规则 */
</style>
