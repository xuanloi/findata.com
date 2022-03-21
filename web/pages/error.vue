<template>
<div>
<TopMenu v-bind="{type: 'tophead', tophead: 'Thông báo lỗi'}" />
<section class="hero mt60">
  <div class="hero-body">
    <div class="container">
      <p class="notification fs20 fb500">
          Đã có lỗi xẩy ra khi kết nối dữ liệu. Thành thật xin lỗi về sự bất tiện này.
      </p>
    </div>
  </div>
</section>
</div>
</template>

<script>
/* eslint-disable */
export default {
  head () {
    return {
      title: 'Thông báo lỗi.'
    }
  }
}
</script>
