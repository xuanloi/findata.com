<!-- eslint-disable -->
<template>
  <div class="ml10 mr10">
    <p class="title">Báo cáo vi phạm </p>
    <div class="field is-horizontal mt40 mb40">
      <div class="field-body">
      <div class="field">
      <label class="label">Họ tên của bạn</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="fullname">
      </div>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='fullname')">{{errors.find(v=>v.name==='fullname').text}}</p>
    </div>
    <div class="field">
      <label class="label">Điện thoại di động / Email </label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="contact">
      </div>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='contact')">{{errors.find(v=>v.name==='contact').text}}</p>
    </div>
    </div>
    </div>

      <template v-if="violatetype">
      <div class="field mt10" v-for="(v,i) in violatetype" :key="i">
             <b-radio v-model="radio"
                :native-value="v.id">
                {{v.value}}
            </b-radio>
      </div>
      <p class="help is-danger" v-if="errors.find(v=>v.name==='radio')">{{errors.find(v=>v.name==='radio').text}}</p>
      </template>

      <p class="mt30 mb30">
        <a class="button is-primary" @click="send()"> Gửi đi </a>
      </p>
  </div>
</template>

<script>
/* eslint-disable */

import mixing from '@/assets/js/mixing.js'

export default {
  props: ['comment', 'name'],

  data() {
    return {
      errors: [],
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(),
      radio: undefined,
      fullname: undefined,
      contact: undefined,
      violatetype: undefined
    }
  },

  created() {
    this.violatetype = this.api.filter2var('list', 'violate')
    this.fullname = this.login.name
    this.contact = this.login.email
  },

  watch: {
    'connection.getupdateStatus': function(newVal) {
      if(newVal) {
        let data = this.$copy(this.comment)
        data.deleted = true
        if(this.name==='help') this.connection1.update('helpcomment', data)
        else if(this.name==='news') this.connection1.update('newscomment', data)
        this.action = {name: 'close', date: new Date()}
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit('updateLogin', {login: val})}
    },

    violatehandle: {
      get: function() {return this.$store.state.violatehandle},
      set: function(val) {this.$store.commit('updateViolateStatus', {violatehandle: val})}
    },

    action: {
      get: function() {return this.$store.state.action},
      set: function(val) {this.$store.commit('updateAction', {action: val})}
    }
  },

  methods: {
    checkError() {
      this.errors = []
      if(this.$empty(this.radio)) this.errors.push({name: 'radio', text: 'Bạn chưa chọn loại vi phạm'})
      let contactCheck = mixing.checkEmailPhone(this.contact)
      if(contactCheck.text) this.errors.push({name: 'contact', text: contactCheck.text})
      if(this.$empty(this.fullname)) this.errors.push({name: 'fullname', text: 'Họ và tên không được bỏ trống'})
      return this.errors.length>0? true : false
    },

    send() {
      if(this.checkError()) return
      let content = mixing.stripHtml(this.comment.comment)
      if(content.length>200) content = content.substring(0,200) + '...'  
      let message = {success: 'Thành công. Cảm ơn bạn thông tin cho chúng tôi.',
      error: 'Có lỗi xảy ra. Hãy thử lại một lần nữa'}

      let data = {reporter: this.login.id, type: this.radio, link: this.$route.fullPath, refid: this.comment.id, 
      poster: this.comment.creator, handle_method: this.api.find3var('list', 'violate-handle', 'not-show').id, content: content}
      this.connection.insert('violate', data, undefined, undefined, undefined, message)
    }
  }
}
</script>