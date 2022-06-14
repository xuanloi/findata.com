<template>
<div>
<TopMenu v-bind ="{type: 'tophead', tophead: tophead}" />
<div class="pt80"/>
      <div class="columns">
      <div class="column is-4"/>
          <div class="column is-4">   
          <div class="box">
              <div class="field">
                    <label class="label has-text-left">Email</label>
              <div class="control">
                  <input  class="input" type="text" v-model="email" readonly>
                  </div>
                  <p class="help is-danger" v-if="errList.find(v=>v==='email')">{{getval(msgList.find(v=>v.name==='email'), 'message')}}</p>
              </div>   
                  <div class="field mt-5">
                    <label class="label has-text-left">Mật khẩu cũ</label>
                <div class="field-body">
                  <div class="field has-addons">
              <div class="control is-expanded">
                  <input  class="input" :type="showpass? 'text' : 'password'" v-model="password" :class="errList.find(v=>v==='password')? 'is-danger' : ''">
                  <p class="help is-danger" v-if="errList.find(v=>v==='password')">{{getval(msgList.find(v=>v.name==='password'), 'message')}}</p>
                  </div> 
              <div class="control">
                <a class="button" @click="showpass=!showpass">
                  <span class="icon">
                    <i
                      :class="showpass? 'mdi mdi-eye-outline has-text-dark fs22' : 'mdi mdi-eye-off-outline has-text-dark fs22'"
                    />
                  </span>
                </a>
              </div>
              </div>
                </div>   

              </div>
              <div class="field mt-5">
                    <label class="label has-text-left">Mật khẩu mới</label>
              <div class="control">
                  <input  class="input" :type="showpass? 'text' : 'password'" v-model="newpassword" :class="errList.find(v=>v==='newpassword')? 'is-danger' : ''">
                  <p class="help is-danger" v-if="errList.find(v=>v==='newpassword')">{{getval(msgList.find(v=>v.name==='newpassword'), 'message')}}</p>
                  </div> 
              </div>   
              <div class="field">
                    <label class="label has-text-left">Nhập lại mật khẩu mới</label>
              <div class="control">
                  <input  class="input" :type="showpass? 'text' : 'password'" v-model="retypepassword" :class="errList.find(v=>v==='retypepassword')? 'is-danger' : ''">
                  <p class="help is-danger" v-if="errList.find(v=>v==='retypepassword')">{{getval(msgList.find(v=>v.name==='retypepassword'), 'message')}}</p>
                  </div> 
              </div>   
      <div class="field mt-5">
          <a class="button is-primary" @click="changePassword()">
              <span class="font-smaller">Đổi mật khẩu</span>
          </a>
      </div>
      </div>
      </div>
    </div>
    <Footer class="mt60"></Footer>
</div>
</template>

<script>
import mixing from "@/assets/js/mixing.js";
export default {
    data() {
      return {
        tophead: 'Đổi mật khẩu truy cập',
        email: '',
        password: '',
        newpassword: '',
        retypepassword: '',
        errList: [],
        msgList: [],
        connection: this.$connection(),
        connection1: this.$connection(),
        hash: undefined,
        showpass: false
      }
    },
    head() {
      return {
        title: 'Đổi mật khẩu'
      }
    },
    created() {
      this.email = this.login.email
    },
    watch: {
      'connection.getdataReady' : function(newVal) {
        if (newVal==='success') this.checkLogin()
        else if(newVal==='error') this.$router.push({path: '/error'})
      },

      'connection1.getupdateStatus' : function(newVal) {
        if(newVal) {
          this.password = ''
          this.newpassword = ''
          this.retypepassword = ''
          this.$buefy.snackbar.open({
              duration: 4000,
              message: 'Đổi mật khẩu thành công. Bạn cần đăng nhập lại để sử dụng.',
              type: 'is-dark',
              position: 'is-bottom',
          })
          let self = this
          mixing.delay(function(){
            self.login = undefined
            self.$router.push({name: 'login'})}, 4000)
        }
        else if(newVal===false) {
            this.$buefy.snackbar.open(`Lỗi. Thay đổi mật khẩu thất bại`);
        }
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.state.api },
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },

      login: {
        get: function() {return this.$store.state.login},
        set: function(val) {this.$store.commit("updateLogin", { login: val })}
      }
    },

    methods: {
      checkLogin() {
        this.hash = this.connection.getbatchData.find(v=>v.name==='hash').data[0]
        let account = this.connection.getbatchData.find(v => v.name==="login").data
        //Check account was disable
        if(account===undefined) {
          this.errList.push('email')
          this.msgList.push({name: 'email', message:  this.api.getval(this.api.find3var('login','form','message'), 'value')})   
          return
        }
        else if(account.enable === false) {
          this.errList.push('email')
          this.msgList.push({name: 'email', message: this.api.getval(this.api.find3var('inform','login','account-disable'), 'value')})   
          return   
        }
        let copy = this.$copy(account)
        copy.password = this.hash
        if(copy.approve) copy.approve = copy.approve.id
        if(copy.bank) copy.bank = copy.bank.id
        if(copy.city) copy.city = copy.city.id
        if(copy.team) copy.team = copy.team.id
        if(copy.type) copy.type = copy.type.id
        this.connection1.update('accountlist', copy)
      },

      validate() {
        this.errList = []
        this.msgList = []

        if(this.password===null || this.password==='') {
          this.errList.push('password')
          this.msgList.push({name: 'password', message: 'Mật khẩu không được bỏ trống'})
        } 
        else if(this.password.length<6) {
          this.errList.push('password')
          this.msgList.push({name: 'password', message: 'Mật khẩu phải có độ dài từ 6 kí tự trở lên'})
        } 
        
        if(this.newpassword===null || this.newpassword==='') {
          this.errList.push('newpassword')
          this.msgList.push({name: 'newpassword', message: 'Mật khẩu mới không được bỏ trống'})
        } 
        else if(this.newpassword.length<6) {
          this.errList.push('newpassword')
          this.msgList.push({name: 'newpassword', message: 'Mật khẩu mới phải có độ dài từ 6 kí tự trở lên'})
        } 

        if(this.retypepassword===null || this.retypepassword==='') {
          this.errList.push('retypepassword')
          this.msgList.push({name: 'retypepassword', message: 'Mật khẩu nhắc lại không được bỏ trống'})
        } 
        else if(this.retypepassword.length<6) {
          this.errList.push('retypepassword')
          this.msgList.push({name: 'retypepassword', message: 'Mật khẩu nhắc lại phải có độ dài từ 6 kí tự trở lên'})
        }
        else if(this.newpassword!==this.retypepassword) {
          this.errList.push('retypepassword')
          this.msgList.push({name: 'retypepassword', message: 'Mật khẩu nhắc lại phải giống với mật khẩu mới'})
        } 
        else if(this.password===this.newpassword) {
          this.errList.push('newpassword')
          this.msgList.push({name: 'newpassword', message: 'Mật khẩu mới phải khác mật khẩu cũ'})
        }
        return this.errList.length>0? false : true
      },

      changePassword() {
        if(!this.validate()) return
        let found = {name: 'hash', url: 'get-hash/' + this.newpassword, params: {}}
        const ele = {name: "login", url: "login/", params: {filter: {email: this.email, password: this.password}, type: 'serializer'}}
        this.connection.getApi([found,ele])
      },  

      getval (obj, field) {
        if (obj === undefined || obj === null) return ''
        return obj[field]===undefined? '' : obj[field]
      }
    }
}
</script>