<!-- eslint-disable -->
<template>
<div class="columns is-centered mt-6 mx-3">
    <div class="column is-6" style="border: solid 1px hsl(0, 0%, 86%)">
        <div class="mb-3 mt-2">
           <figure class="image is-64x64">
              <nuxt-link to="/"> <img v-lazy="require(`~/assets/images/logo.png`)" width="160"/> </nuxt-link>
          </figure>
        </div>
      <section class="hero">
        <div class="hero-body px-4 pt-4 pb40">
          <template v-if="!action">
            <article class="message is-primary">
            <div class="message-body fs18  has-background-white">
            Vui lòng nhập các thông tin dưới đây để cập nhật mật khẩu.
            </div>
            </article>
            
  <div class="field is-horizontal mt10">
    <div class="field-body">
      <div class="field">
        <label class="label has-text-dark"> Nhập mật khẩu mới </label>
        <div class="control">
         <input class="input is-primary" :type="showpass? 'text' : 'password'" placeholder="Từ 6 kí tự bao gồm chữ và số " v-model="password" ref="inputcode" />
        </div>
         <p class="help is-danger"
              v-if="errors.find(v=>v.name==='password')"
            >{{errors.find(v=>v.name==='password').text}}</p>
      </div>
      <div class="field">
        <label class="label has-text-dark"> Nhắc lại mật khẩu </label>
        <div class="control">
           <input class="input is-primary" :type="showpass? 'text' : 'password'" v-model="retypePassword"/>
        </div>
         <p class="help is-danger"
              v-if="errors.find(v=>v.name==='retypePassword')"
            >{{errors.find(v=>v.name==='retypePassword').text}}</p>
        </div>
      </div>
    </div>
    <p> 
      <a class="button" @click="showpass=!showpass">
          <span class="icon">
            <i
              :class="showpass? 'mdi mdi-eye-outline has-text-dark fs22' : 'mdi mdi-eye-off-outline has-text-dark fs22'"
            />
          </span>
        </a> 
      </p>
          <div class="field mt30">
            <p class="control has-text-centered">
              <a class="button is-primary" @click="getPassword()"> Cập nhật mật khẩu</a>
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
      connection3: this.$connection(),
      code: undefined,
      errors: [],
      user: undefined,
      message: undefined,
      success: undefined,
      action: undefined,
      password: undefined,
      retypePassword: undefined,
      link: undefined,
      showpass: false
    }
  },

  head() {
    return {
      title: 'Tạo mật khẩu mới'
    }
  },

  mounted() {
    let found = {name: 'account', url: 'data/Account', params: {filter: {id: this.$route.query.id}}}
    let ele = {name: 'link', url: 'data/Link', params: {filter: {guid: this.$route.query.token}}}
    this.connection.getApi([found, ele])
    if(this.$refs.inputcode) this.$refs.inputcode.focus()
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        let data = this.connection.getbatchData.find(v=>v.name==='link').data
        this.link = data.length>0? data[0] : undefined
        if(this.link? this.link.expiry : 1<0) this.invalidLink()
        data = this.connection.getbatchData.find(v=>v.name==='account').data
        this.user = data.length>0? data[0] : undefined
        if(!this.user) this.invalidLink()
      } else if(newVal===false) this.invalidLink()
    },

    'connection1.getdataReady' : function(newVal) {
      if(newVal==='success') {
        this.user.password = this.connection1.getbatchData.find(v=>v.name==='hash').data[0]
        this.user.update_time = new Date()
        this.connection2.update('accountlist', this.user)
      } 
    },

    'connection2.getupdateStatus' : function(newVal) {
      if(newVal) {
        this.message = 'Cập nhật mật khẩu thành công.' 
        this.success = true
        this.action = {name: 'login', to: {path: '/login'}, text: 'Đi tới trang đăng nhập'}
        this.link.enable = false
        this.link.update_time = new Date()
        this.connection3.update('link', this.link)
      } else if(newVal===false) {
        this.message = 'Có lỗi xẩy ra. Hãy thử lại một lần nữa.' 
        this.success = false
      }
    }
  },

  methods: {
    checkError() {
      this.errors = []
      if (this.$empty(this.password)) {
        this.errors.push({
          name: "password",
          text: "Mật khẩu không được bỏ trống."
        });
      } else if (this.password.length < 6) {
        this.errors.push({
          name: "password",
          text: "Mật khẩu gồm 6 kí tự trở nên bao gồm chữ và số ."
        });
      } else if (
        !(/\d/.test(this.password) && /[a-zA-Z]/.test(this.password))
      ) {
        this.errors.push({
          name: "password",
          text: "Mật khẩu gồm 6 kí tự trở nên bao gồm chữ và số ."
        })
      }
      else if(this.password!==this.retypePassword) {
        this.errors.push({
          name: "retypePassword",
          text: "Nhắc lại mật khẩu phải giống với mật khẩu mới."
        })
      }
      return this.errors.length>0? true : false 
    },

    invalidLink() {
      this.message = 'Đường link không hợp lệ'
      this.success = false
      this.action = {name: 'index', to: {path: '/'}, text: 'Đi tới trang chủ'}
    },
  
    getPassword() {
      this.success = undefined
      this.message = undefined
      this.action = undefined
      this.errors = []
      if(this.checkError()) return
      let ele = {name: 'hash', url: 'get-hash/' + this.password, params: {}}
      this.connection1.getApi([ele])
    }
  }
}
</script>
