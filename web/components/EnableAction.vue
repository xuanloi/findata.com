<!-- eslint-disable -->
<template>
  <nav class="panel my-4" v-if="selectedRows">
    <div class="columns is-multiline">
      <div class="column is-1 is-offset-1"></div>
      <div class="column is-3">
        <span class="has-text-primary fb500">{{selectedlist.length + ' bản ghi được chọn' }}</span>
      </div>
      <div class="column is-5">
          <a class="tag is-medium is-primary ml-3" @click="selectedAction('enable-disable')" v-if="login.type.code==='admin'">Cho phép / Vô hiệu</a>
      </div>
      <div class="column is-2">
        <a class="delete is-medium has-background-grey" @click="clearSelect()"></a>
      </div>

  <div class="column is-10 is-offset-1" v-if="actionType==='enable-disable'">
  <article class="message is-primary">
  <div class="message-body has-background-light">

  <nav class="level" v-if="selectedRows.filter(v=>v.enable).length>0">
  <!-- Left side -->
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.enable).length}} </span> 
          <span> Bản ghi <strong>Có hiệu lực </strong> -> chuyển sang <strong>Vô hiệu lực</strong></span>
      </p>
      </div>
      <div class="level-item">
          <p class="ml40">
            <a class="tag is-medium is-danger" @click="confirmAction('disable')" v-if="loggedin"> Thực hiện</a>
          <a class="tag is-medium is-primary" @click="loginForm=true" v-else> Đăng nhập </a>
          </p>
      </div>
  </div>
  <div class="level-right">
  <div class="level-item">
      <span :class="msgInfo.find(v=>v.name==='disable').type" v-if="msgInfo.find(v=>v.name==='disable')"> {{msgInfo.find(v=>v.name==='disable').message}} </span>
  </div>
  </div>
  </nav>

  <nav class="level" v-if="selectedRows.filter(v=>!v.enable).length>0">
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>!v.enable).length}} </span> 
          <span> Bản ghi <strong>Vô hiệu lực</strong> -> chuyển sang <strong>Có hiệu lực</strong></span>
      </p>
      </div>
      <div class="level-item">
          <p class="ml40">
          <a class="tag is-medium is-danger" @click="confirmAction('enable')" v-if="loggedin"> Thực hiện</a>
          <a class="tag is-medium is-primary" @click="loginForm=true" v-else> Đăng nhập </a>
          </p>
      </div>
  </div>
    <div class="level-right">
      <div class="level-item">
        <span :class="msgInfo.find(v=>v.name==='enable').type" v-if="msgInfo.find(v=>v.name==='enable')"> {{msgInfo.find(v=>v.name==='enable').message}} </span>
      </div>
    </div>
  </nav>
  </div>
  </article>
  </div>
  <div class="modal" :class="loginForm!==undefined? 'is-active' : ''" v-if="loginForm!==undefined">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content my-0 py-0">
    <loginform v-bind="{modal: true}"> </loginform>
    </div>
    <button class="modal-close is-large has-background-dark" aria-label="close" @click="loginForm=undefined"></button>
  </div>
    </div>
  </nav>
</template>

<script>
import Vue from "vue";
import mixing from "@/assets/js/mixing.js";
import login from '@/pages/login.vue'
Vue.component('loginform', login)
export default {
  props: ["selectedlist"],

  data() {
    return {
      loginForm: undefined,
      loggedin: undefined,
      msgInfo: [],
      deleteType: undefined,
      taskStatus: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      actionType: undefined,
      selectedRows: []
    }
  },

  watch: {
    "connection1.getupdateStatus": function(newVal) {
      if(newVal===true) {
        var data = this.$copy(this.connection1.getupdateRecord);
        var message = "Dữ liệu sẽ thay đổi trên màn hình sau 5s";
        const num_error = data.filter(v => v.error).length

        let text =
          (num_error===0 ? "Hoàn thành." : "Có lỗi.") +
          " Đã cập nhật " +
          data.filter(v => v.error === undefined).length +
          "/" +
          data.length;
        let type = num_error===0 ? "has-text-primary" : "has-text-danger";
        this.msgInfo = [{name: this.taskStatus,  message: text, type: type }];
        const datalist = this.$copy(this.pageitem.data)

        if (data.filter(v => v.error === undefined).length > 0)
          this.$buefy.snackbar.open({
            duration: 5000,
            message: message,
            type: "is-success",
            position: "is-bottom"
          });

          data.forEach(v => {
            if(!v.error) {
              let index = datalist.findIndex(x => x.id === v.id)
              if (index >= 0) datalist[index] = v
            }
          })
      
        let self = this
        mixing.delay(function() {
          self.$store.commit("updateState", {name: 'pageitem', key: "data", data: datalist})
        }, 5000)
      }
    },

    menuaction: function(newVal) {
      if(newVal===undefined) return
      else if(newVal.action==='close-login') {
        this.loggedin = true
        this.loginForm = undefined
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
    
    pageitem: {
      get: function() {return this.$store.state.pageitem},
      set: function(val) {this.$store.commit('updatePageItem', {pageitem: val})}
    },
    
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    }
  },

  methods: { 
    confirmAction(name) {
      this.taskStatus = name
      let data = this.$copy(this.selectedRows.filter(v=>v.enable===(name==='enable'? false : true)))
      data.map(v=>{v.enable = name==='enable'? true : false})
      this.connection1.insert('reportitem', data)
    },

    selectedAction(type) {
      this.selectedRows = []
      this.pageitem.models.forEach((element, id) => {
        if (element === true) {
          let found = this.pageitem.data.find(v => parseInt(v.id) === parseInt(id));
          this.selectedRows.push(found);
        }
      })
      this.msgInfo = []
      this.actionType = type
    },

    clearSelect() {
      this.$store.commit("updateState", {name: "pageitem", key: "data", data: this.$copy(this.pageitem.data)})
    }
  }
}
</script>