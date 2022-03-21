<template>
  <div class="columns is-centered px-0 mx-0 mt-6">
    <div class="column is-4" style="border: solid 1px hsl(0, 0%, 86%)">
      <section class="hero">
        <div class="hero-body px-5 pt30 pb20">
          <div class="field is-grouped mt10">
            <div class="control is-expanded">
              <span class="title is-size-3">Đăng nhập</span>
            </div>
            <div class="control">
              <nuxt-link to="/">
                <span class="icon">
                  <i class="mdi mdi-home-import-outline is-size-2" />
                </span>
              </nuxt-link>
            </div>
          </div>

          <div class="field mt40">
            <label class="label">Tài khoản</label>
            <div class="control">
              <input class="input" type="text" placeholder v-model="username" />
            </div>
            <p
              class="help is-danger"
              v-if="errors.find(v=>v.name==='username')"
            >{{errors.find(v=>v.name==='username').text}}</p>
          </div>

          <div class="field mt30">
            <label class="label">Mật khẩu</label>
            <div class="field-body">
              <div class="field has-addons">
                <p class="control is-expanded">
                  <input
                    class="input"
                    :type="showpass? 'text' : 'password'"
                    placeholder
                    v-model="password"
                  />
                </p>
                <p class="control">
                  <a class="button" @click="showpass=!showpass">
                    <span class="icon">
                      <i
                        :class="showpass? 'mdi mdi-eye-outline has-text-dark fs22' : 'mdi mdi-eye-off-outline has-text-dark fs22'"
                      />
                    </span>
                  </a>
                </p>
              </div>
            </div>
            <p
              class="help is-danger"
              v-if="errors.find(v=>v.name==='password')"
            >{{errors.find(v=>v.name==='password').text}}</p>
          </div>

          <div class="field is-grouped mt40">
            <div class="control is-expanded">
              <button class="button is-primary" @click="signin()">Đăng nhập</button>
            </div>
              <div class="control">
              <a class="is-primary" @click="accountRecovery()">Quên mật khẩu?</a>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
/* eslint-disable */

import mixing from "@/assets/js/mixing.js";

export default {
  props: ['modal'],

  data() {
    return {
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(),
      connection2: this.$connection(),
      username: undefined,
      password: undefined,
      retypePassword: undefined,
      errors: [],
      showpass: false,
      registers: [],
      type: undefined,
    }
  },

  head() {
    return {
      title: 'Đăng nhập vào hệ thống'
    }
  },

  watch: {
    "connection1.getdataReady": function(newVal) {
      if (newVal==="success") {
        let data = this.connection1.getbatchData.find(v => v.name==="login").data
        this.fillData(data)
      } else if(newVal==='error') this.$router.push({path: '/error'})
    },

    "connection2.getdataReady": function(newVal) {
      if (newVal==="success") {
        let data = this.connection2.getbatchData.find(v=>v.name==='rights').data
        data.filter(v=>v.category==='function').map(v=>{
          let found = this.api.find3var('functions','admin', v.classify)
          if(found? (found.enable? !data.find(x=>x.id===found.id): false) : false) data.push(found)
        })
        mixing.multiSort(data, {index: 'asc'})
        this.rights = data

        data = this.connection2.getbatchData.find(v=>v.name==='news').data
        if(data.length>0) this.hasnews = true
        this.notification = this.connection2.getbatchData.find(v=>v.name==='notification').data
        this.redirectUrl()
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit("updateApi", {api: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit('updateLogin', {login: val})}
    },
    
    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    },

    rights: {
      get: function() {return this.$store.state.rights},
      set: function(val) {this.$store.commit('updateRights', {rights: val})}
    },

    hasnews: {
      get: function() {return this.$store.state.hasnews},
      set: function(val) {this.$store.commit('updateHasNews', {hasnews: val})}
    },

    notification: {
      get: function() {return this.$store.state.notification},
      set: function(val) {this.$store.commit('updateNotification', {notification: val})}
    }
  },

  mounted() {
    let self = this;
    window.addEventListener("keyup", function(ev) {
      if(ev.key==='Enter' && self.$route.name==='signin') self.signin()
    })
  },

  methods: {
    checkError() {
      this.errors = []
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

      if (!this.$empty(this.username)) {
        this.username = this.username.trim().toLowerCase();
      }
      if (this.$empty(this.username)) {
        this.errors.push({
          name: "username",
          text: "Email hoặc số điện thoại di động không được bỏ trống."
        });
      } else if (
        !re.test(String(this.username).toLowerCase()) &&
        !mixing.isNumber(this.username)
      ) {
        this.errors.push({
          name: "username",
          text: "Email hoặc số điện thoại di động không hợp lệ."
        });
      } else if (
        mixing.isNumber(this.username) &&
        (this.username.length < 9 || this.username.length > 11)
      ) {
        this.errors.push({
          name: "username",
          text: "Số điện thoại di động không hợp lệ."
        })
      }

      if (this.$empty(this.password)) {
        this.errors.push({
          name: "password",
          text: "Mật khẩu không được bỏ trống."
        });
      } 
      /*
      else if (this.password.length < 6) {
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
      }*/
      return this.errors.length>0? true  : false
    },

    signin() {
      if(this.checkError()) return
      const ele = {
        name: "login",
        url: "login/",
        params: {
          filter: {
            email: this.username,
            password: this.password,
            type: this.$empty(this.$route.query.type)
              ? ""
              : this.$route.query.type
          }
        }
      };
      this.connection1.getApi([ele]);
    },

    redirectUrl() {
      if(this.modal) {
        this.menuaction = {id: mixing.id(), action: 'close-login'}
      }
      else if(this.$route.query.to) {
        let params = JSON.parse(this.$route.query.params)
        this.$router.push({ path: this.$route.query.to, query: params})
      }
      else this.$router.push({ path: "/" })
    },

    fillData(data) {
      if(!data) {
        const text = 'Tài khoản hoặc mật khẩu không chính xác'
        this.errors.push({name: "username", text: text})
        this.errors.push({ name: "password", text: text})  
      } else if(!data.enable) {
        this.errors.push({name: "username", text: 'Tài khoản đang bị khóa. Đăng nhập không thành công'})
      } else if(data.approve? data.approve.code!=='yes' : false) {
        this.errors.push({name: "username", text: 'Tài khoản chưa được phê duyệt. Đăng nhập không thành công'})
      }
      if(this.errors.length>0) return
      this.login = data
      if(this.modal) this.redirectUrl()
      else {
        let connlist = [{name: 'rights', url: 'data/Classification',
          params: {sort: 'index', filter: {function__account_type: data.type.id, function__enable: 1, enable: 1}}},
          {name : 'news', url: 'data/News', params: {page: 1, onpage: 1, create_time__gt: new Date(Date.now() - 7*24*3600*1000)}},
          {name: 'notification', url: 'data/Notification', params: {page: 1, onpage: 10, sort:'-id', filter: {receiver: this.login.id},
          values: 'id,sender,sender__name,sender__avatar,receiver,type,type__value,seen,refid,link,create_time'}}
        ]
        this.connection2.getApi(connlist)
      } 
    },

    accountRecovery() {
      this.$router.push({path: '/account-recovery'})
    }
  }
}
</script>
