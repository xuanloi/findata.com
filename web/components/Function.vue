<!-- eslint-disable -->

<template>
  <div>
       <p class="title is-size-4 ml5 mb30">Tạo mới chức năng </p>
      <div class="field is-horizontal">
  <div class="field-label is-normal">
    <label class="label">Mã, tên chức năng</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Mã chức năng" v-model="item">
      </p>
    </div>

        <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Tên chức năng" v-model="value">
      </p>
    </div>
  </div>
</div>

      <div class="field is-horizontal mt20">
  <div class="field-label is-normal">
    <label class="label">Cấp độ, cấp trên</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Cấp độ" v-model="level">
      </p>
    </div>
        <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Cấp trên" v-model="parent">
      </p>
    </div>
  </div>
</div>
      <div class="field is-horizontal mt20">
  <div class="field-label is-normal">
    <label class="label">Thứ tự, biểu tượng</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Thứ tự" v-model="index">
      </p>
    </div>
        <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Biểu tượng" v-model="icon">
      </p>
    </div>
  </div>
</div>
      <div class="field is-horizontal mt20">
  <div class="field-label is-normal">
    <label class="label">Hình ảnh</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Hình ảnh" v-model="image">
      </p>
    </div>
  </div>
</div>
      <div class="field is-horizontal mt20">
  <div class="field-label is-normal">
    <label class="label">Đường dẫn</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Đường dẫn" v-model="link">
      </p>
    </div>
  </div>
</div>

<div class="field is-horizontal mt30">
  <div class="field-label">
    <!-- Left empty for spacing -->
  </div>
  <div class="field-body">
    <div class="field">
      <div class="control">
        <button class="button is-primary" @click="update()">
          {{label}}
        </button>
      </div>
    </div>
  </div>
</div>
    </div>
</template>

<script>
/* eslint-disable */

import mixing from "@/assets/js/mixing.js"

export default {
  data () {
    return {
      connection: this.$connection(this.$buefy),
      item: undefined,
      value: undefined,
      level: undefined,
      index: undefined,
      parent: undefined,
      icon: undefined,
      image: undefined,
      link: undefined,
      label: 'Tạo mới'
    }
  },

  created () {
    const record = this.pagefunction.record
    if(record===undefined) return
    this.item = record.item
    this.value = record.value
    this.level = record.level
    this.index = record.index
    this.parent = record.parent
    this.label = 'Cập nhật'
    this.link = record.link
    this.icon = record.icon
  },

  watch: {
    query: function(newVal) {
      if(newVal) {
        let copy = this.$copy(this.pagefunction)
        copy.data = newVal
        this.pagefunction = copy
      }
    }
  },

  computed: {
    query() {
      return this.$store.state[this.$route.query.type]
    },

    pagefunction: {
      get: function() {return this.$store.state.pagefunction},
      set: function(val) {this.$store.commit('updatePageFunction', {pagefunction: val})}
    }
  },

  methods: {
    update () {
      let data = { item: this.item, value: this.value, level: this.level, parent: this.parent, index: this.index,
      icon: this.icon, image: this.image, link: this.link }
      data = mixing.resetEmptyString(data)
      
      const record = this.pagefunction.record
      if(this.pagefunction.action==='insert') this.connection.insert(this.pagefunction.api.name, data)
      else {
        data.id = record.id
        data.update_time = new Date()
        this.connection.update(this.pagefunction.api.name, data)
      }
    }
  }
}
</script>
