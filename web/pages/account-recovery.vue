<!-- eslint-disable -->
<template>
<div class="columns is-centered mt-6 mx-3">
    <div class="column is-6" style="border: solid 1px hsl(0, 0%, 86%)">
        <div class="mb-3 mt-2">
           <figure class="image is-64x64">
              <nuxt-link to="/"> <img v-lazy="require(`~/assets/images/logo.png`)"/> </nuxt-link>
          </figure>
        </div>

      <section class="hero">
        <div class="hero-body px-3 pt-3">
          <template v-if="!action">
            <article class="message is-primary">
            <div class="message-body fs18  has-background-white">
            <strong> Để lấy lại mật khẩu </strong> vui lòng nhập thông tin tài khoản (username) và mã kiểm tra. Nếu thông tin là hợp lệ chúng tôi đã gửi cho bạn một email chứa đường link để thay đổi mật khẩu.
            </div>
            </article>
            
  <div class="field is-horizontal mt10">
    <div class="field-body">
      <div class="field">
        <label class="label has-text-dark"> Nhập username </label>
        <div class="control">
         <input class="input is-primary" type="text" placeholder="Nhập email vào đây." v-model="username" ref="inputcode" @change="checkInfo()" />
        </div>
         <p class="help is-danger"
              v-if="errors.find(v=>v.name==='username')"
            >{{errors.find(v=>v.name==='username').text}}</p>
      </div>
      <div class="field is-narrow">
        <label class="label has-text-dark"> Mã kiểm tra : {{refcode}} </label>
        <div class="control">
           <input class="input is-primary" type="text" :placeholder="'Nhập ' + refcode + ' vào đây'"  v-model="code"/>
        </div>
         <p class="help is-danger"
              v-if="errors.find(v=>v.name==='code')"
            >{{errors.find(v=>v.name==='code').text}}</p>
        </div>
      </div>
    </div>
  
          <div class="field mt30" v-if="isPhone">
            <label class="label has-text-dark"> Vui lòng cung cấp email để nhận link </label>
            <div class="control">
              <input class="input is-primary" type="text" placeholder="Nhập email" v-model="email" @change="checkEmail()"  />
            </div>
            <p class="help is-danger mt5 fs13"
              v-if="errors.find(v=>v.name==='email')"
            >{{errors.find(v=>v.name==='email').text}}</p>
          </div>

          <div class="field mt30">
            <p class="control has-text-centered">
              <a class="button is-primary" @click="getPassword()"> Lấy lại mật khẩu</a>
            </p>
          </div>
          </template>

        <template v-else>
            <article class="message" :class="success? 'is-primary' : 'is-danger'" v-if="success!==undefined">
          <div class="message-body fs18 has-background-white">
            {{message}}
          </div>
          </article>

        <div class="field mt30">
            <p class="control has-text-centered">
              <nuxt-link class="button is-primary" :to="action.to"> 
                {{action.text}}
              </nuxt-link>
            </p>
          </div>
        </template>

        </div>
      </section>
    </div>
    </div>
</template>

<script>
/* eslint-disable */
import Connection from "@/assets/js/connection.js"
import mixing from "@/assets/js/mixing.js"

export default {
  data() {
    return {
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(),
      code: undefined,
      errors: [],
      user: undefined,
      message: undefined,
      success: undefined,
      action: undefined,
      code: undefined,
      refcode: undefined,
      username: undefined,
      isPhone: false,
      email: undefined,
      authcode: undefined
    }
  },

  head() {
    return {
      title: 'Lấy lại mật khẩu truy cập'
    }
  },

  mounted() {
    this.refcode = mixing.id().substring(0,4)
    if(this.$refs.inputcode) this.$refs.inputcode.focus()
    let self = this
    window.addEventListener("keyup", function(ev) {
      if(ev.key==='Enter') {
        if(self.success===undefined) self.getPassword()
      }
    })
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        let data = this.connection.getbatchData[0].data
        if(data.length===0) {
          this.errors.push({name: 'username', text: 'Tài khoản không tồn tại'})
          return
        }

        this.user = data[0]
        this.authcode = mixing.guid()
        let routeData = this.$router.resolve({path: '/get-password', query: {id: this.user.id, token: this.authcode}});
        var href = window.location.href 
        href = href.substring(0, href.indexOf(this.$route.path)) + routeData.href

        var ele =  {
          'guid' : this.authcode,
          'route_name': 'account-recovery',
          'query': 'token: ' + this.authcode,
          'link': href,
          'valid_from':  new Date(),
          'valid_to':  new Date(Date.now() + 2 * 24*60*60*1000),
          'action_result': this.api.getval(this.api.find3var('list','action-result','initialize'), 'id'),
          'detail': 'Account recovery link'
        }
        this.connection1.insert('link', ele)
      }
    },

   'connection1.getupdateStatus': function(newVal) {
      if(newVal) {
        let routeData = this.$router.resolve({path: '/get-password', query: {id: this.user.id, token: this.authcode}})
        let path = window.location.origin + routeData.href
        let content = 'Hãy click vào đường link đưới đây để  lấy lại mật khẩu.' + '\n'
        content += path + '\n\n' +  'Cảm ơn,' + '\n' + 'Findata'
        let data = {subject: 'Phục hồi tài khoản', content: content, to: this.email? this.email : this.username}
        let found = {name: 'sendemail', url: 'send-email/', method: 'post', data: data, params: {}}
        this.connection2.getApi([found])
      }
    },

    'connection2.getdataReady' : function(newVal) {
      if(newVal==='success') {
        this.message = 'Thành công. Hãy mở email của bạn để  lấy lại  mật khẩu.' 
        this.success = true
        this.action = {name: 'login', to: {path: '/login'}, text: 'Đi tới trang đăng nhập'}
      } else if(newVal===false) {
        this.message = 'Có lỗi xẩy ra. Hãy thử lại một lần nữa.' 
        this.success = false
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit("updateApi", {api: val})}
    }
  },
  
  methods: {
    checkInfo() {
      this.errors = []
      let result = mixing.checkEmailPhone(this.username)
      if(result.text) this.errors.push({name: 'username', text: result.text })
      else this.isPhone = this.username.indexOf('@')>=0? false : true
    },

    checkEmail() {
      this.errors = []
      let result = mixing.checkEmailPhone(this.email)
      if(result.text? 1>0 : this.email.indexOf('@') <0) {
        this.errors.push({name: 'email', text: 'Email không hợp lệ' })
      }
    },

    getPassword() {
      this.success = undefined
      this.message = undefined
      this.action = undefined
      this.errors = []
      
      let result = mixing.checkEmailPhone(this.username)
      if(result.text) this.errors.push({name: 'username', text: result.text})
      if(this.$empty(this.code)) this.errors.push({name: 'code', text: 'Chưa nhập mã kiểm tra'})
      else if(this.refcode!==this.code) this.errors.push({name: 'code', text: 'Mã kiểm tra không đúng'})
      if(this.isPhone) {
        result = mixing.checkEmailPhone(this.email)
        if(result.text? 1>0 : this.email.indexOf('@')<0) this.errors.push({name: username, text: 'Email không hợp lệ'})
      }
      if(this.errors.length>0) return
      let found = {name: 'user', url: 'data/Account', params: {filter: {email: this.username}}}
      this.connection.getApi([found])
    }
  }
}
</script>
