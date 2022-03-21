<!-- eslint-disable -->
<template>
  <nav class="panel my-4" v-if="selectedRows">
    <div class="columns is-multiline">
      <div class="column is-1 is-offset-1"></div>
      <div class="column is-3">
        <span class="has-text-primary fb500">{{selectedlist.length + ' bản ghi được chọn' }}</span>
      </div>
      <div class="column is-5">
          <a v-if="pagetask? pagetask.enableDelete : false"
            class="tag is-medium is-danger"
            @click="selectedAction('delete')"
          >Xóa dữ liệu</a>

          <a v-if="pagetask? pagetask.enableApprove : false"
            class="tag is-medium is-primary ml-3"
            @click="selectedAction('approved')"
          >Duyệt dữ liệu</a>

           <a
            class="tag is-medium is-primary is-light ml-3"
            @click="selectedAction('opentab')"
          >Mở tab</a>

           <a v-if="pagetask? pagetask.api.url==='data/Task/' : false"
            class="tag is-medium is-primary is-light ml-3"
            @click="selectedAction('download')"
          >Tải dữ liệu</a>
      </div>
      <div class="column is-2">
        <a class="delete is-medium has-background-grey" @click="clearSelect()"></a>
      </div>

    <div class="column is-10 is-offset-1" v-if="actionType==='delete'">
  <article class="message is-primary">
  <div class="message-body has-background-light">
  <nav class="level" v-if="selectedRows.filter(v=>v.status__code==='not-yet-entered').length>0">
  <!-- Left side -->
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code==='not-yet-entered').length}} </span> 
          <span> Báo cáo chưa nhập, <strong>sẵn sàng để xóa</strong> </span>
      </p>
      </div>
      <div class="level-item">
          <p class="ml40">
          <a class="tag is-medium is-danger" @click="confirmDeleteTask('available')"> Thực hiện</a>
          </p>
      </div>
  </div>
  <div class="level-right">
  <div class="level-item">
      <span :class="msgInfo.find(v=>v.name==='available').type" v-if="msgInfo.find(v=>v.name==='available')"> {{msgInfo.find(v=>v.name==='available').message}} </span>
  </div>
  </div>
  </nav>

  <nav class="level" v-if="selectedRows.filter(v=>v.status__code!=='not-yet-entered' && v.status__code!=='approved').length>0">
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code!=='not-yet-entered' && v.status__code!=='approved').length}}  </span> 
          <span> Báo cáo đang nhập, <strong>nhưng chưa duyệt</strong>. </span>
      </p>
      </div>
      <div class="level-item">
        <p class="ml40">
          <a class="tag is-medium is-danger" @click="confirmDeleteTask('relate')"> Thực hiện </a>
        </p>
      </div>
  </div>
    <div class="level-right">
      <div class="level-item">
          <span :class="msgInfo.find(v=>v.name==='relate').type" v-if="msgInfo.find(v=>v.name==='relate')"> {{msgInfo.find(v=>v.name==='relate').message}} </span>
      </div>
    </div>
  </nav>

  <nav class="level" v-if="selectedRows.filter(v=>v.status__code==='approved').length>0">
    <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code==='approved').length}}  </span> 
          <span> Báo cáo đã duyệt, <strong>đăng nhập để xóa</strong>. </span>
      </p>
      </div>
      <div class="level-item">
        <p class="ml40">
          <a class="tag is-medium is-danger" @click="confirmDeleteTask('approved')" v-if="loggedin"> Thực hiện </a>
          <a class="tag is-medium is-primary" @click="loginForm=true" v-else> Đăng nhập </a>
        </p>
      </div>
    </div>
        <div class="level-right">
      <div class="level-item">
          <span :class="msgInfo.find(v=>v.name==='approved').type" v-if="msgInfo.find(v=>v.name==='approved')"> {{msgInfo.find(v=>v.name==='approved').message}} </span>
      </div>
    </div>
  </nav>
  </div>
  </article>
  </div>

  <div class="column is-10 is-offset-1" v-else-if="actionType==='approved'">
  <article class="message is-primary">
  <div class="message-body has-background-light">

  <nav class="level" v-if="selectedRows.filter(v=>v.status__code==='waiting-approve').length>0">
  <!-- Left side -->
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code==='waiting-approve').length}} </span> 
          <span> Bản ghi trạng thái <strong>Chờ duyệt 1 </strong> -> chuyển sang <strong>Chờ duyệt 2</strong></span>
      </p>
      </div>
      <div class="level-item">
          <p class="ml40">
            <a class="tag is-medium is-primary" @click="confirmApprove('waiting-approve')"> Thực hiện </a>
          </p>
      </div>
  </div>
  <div class="level-right">
  <div class="level-item">
      <span :class="msgInfo.find(v=>v.name==='waiting-approve').type" v-if="msgInfo.find(v=>v.name==='waiting-approve')"> {{msgInfo.find(v=>v.name==='waiting-approve').message}} </span>
  </div>
  </div>
  </nav>

  <nav class="level" v-if="selectedRows.filter(v=>v.status__code==='waiting-approve-2').length>0">
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code==='waiting-approve-2').length}} </span> 
          <span> Bản ghi trạng thái <strong>chờ duyệt 2</strong> -> chuyển sang <strong>Đồng ý</strong></span>
      </p>
      </div>
      <div class="level-item">
          <p class="ml40">
            <a class="tag is-medium is-primary" @click="confirmApprove('waiting-approve-2')" 
              v-if="login.type.code==='manager' || login.type.code==='admin'"> Thực hiện
          </a>
          </p>
      </div>
  </div>
    <div class="level-right">
      <div class="level-item">
          <span :class="msgInfo.find(v=>v.name==='waiting-approve-2').type" v-if="msgInfo.find(v=>v.name==='waiting-approve-2')"> {{msgInfo.find(v=>v.name==='waiting-approve-2').message}} </span>
      </div>
    </div>
  </nav>

  <nav class="level" v-if="selectedRows.filter(v=>v.status__code!=='waiting-approve' && v.status__code!=='waiting-approve-2').length>0">
  <div class="level-left">
      <div class="level-item">
      <p class="ml20">
          <span class="tag is-primary is-medium mr20"> {{selectedRows.filter(v=>v.status__code!=='waiting-approve' && v.status__code!=='waiting-approve-2').length}}  </span> 
          <span> Bản ghi ở các <strong>trạng thái khác</strong> -> không thể phê duyệt </span>
      </p>
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
/* eslint-disable */
import Vue from "vue";
import mixing from "@/assets/js/mixing.js";
import Connection from "@/assets/js/connection.js"
import login from '@/pages/login.vue'
import Export from '@/assets/js/export.js'

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
    "connection.getupdateStatus": function(newVal) {
      if(newVal===true) {
        var data = this.$copy(this.connection.getupdateRecord);
        var message = "Dữ liệu xóa thành công sẽ biến mất trên màn hình sau 5s";
        const num_error = data.filter(v => v.error).length

        let text =
          (num_error===0 ? "Hoàn thành." : "Có lỗi.") +
          " Đã xoá " +
          data.filter(v => v.error === undefined).length +
          "/" +
          data.length;
        let type = num_error===0 ? "has-text-primary" : "has-text-danger";
        this.msgInfo = [{name: this.deleteType,  message: text, type: type }];
        const datalist = this.$copy(this.pagetask.data)

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
              if (index >= 0) this.$delete(datalist, index)
            }
          })
      
        let self = this
        mixing.delay(function() {
          self.$store.commit("updateState", {name: 'pagetask', key: "data", data: datalist})
        }, 5000)
      }
    },

    "connection1.getupdateStatus": function(newVal) {
      if(newVal===true) {
        var data = this.$copy(this.connection1.getupdateRecord);
        var message = "Dữ liệu sẽ thay đổi trên màn hình sau 5s";
        const num_error = data.filter(v => v.error).length

        let text =
          (num_error===0 ? "Hoàn thành." : "Có lỗi.") +
          " Đã duyệt " +
          data.filter(v => v.error === undefined).length +
          "/" +
          data.length;
        let type = num_error===0 ? "has-text-primary" : "has-text-danger";
        this.msgInfo = [{name: this.taskStatus,  message: text, type: type }];
        const datalist = this.$copy(this.pagetask.data)

        if (data.filter(v => v.error === undefined).length > 0)
          this.$buefy.snackbar.open({
            duration: 5000,
            message: message,
            type: "is-success",
            position: "is-bottom"
          });

          data.forEach(v => {
            if(!v.error) {
              v.assign_date = mixing.yyyymmdd(new Date(v.assign_date))
              v.due_date = mixing.yyyymmdd(new Date(v.due_date))
              let index = datalist.findIndex(x => x.id === v.id)
              if (index >= 0) datalist[index] = v
            }
          })
      
        let self = this
        mixing.delay(function() {
          self.$store.commit("updateState", {name: 'pagetask', key: "data", data: datalist})
        }, 5000)
      }
    },

    menuaction: function(newVal) {
      if(newVal===undefined) return
      else if(newVal.action==='close-login') {
        this.loggedin = true
        this.loginForm = undefined
      }
    },

    "connection2.getdataReady": function(newVal) {
      if (newVal === "success") {
        let reportitem = this.connection2.getbatchData.find(v=>v.name==='reportitem').data
        let filter = this.connection2.getbatchData.filter(v=>v.name!=='reportitem')
        filter.map(v=>{
          let row = v.data.length>0? v.data[0] : undefined
          if(row) {
            let task = this.selectedRows.find(x=>x.id===row.task)
            if(task) {
              let data = this.$copy(reportitem.filter(x=>x.company_type===task.company__type__code && x.report_name===task.report_name__code.replace('-LK', '')))
              data.map(y=>{
                y.input = row['f' + y.item]? mixing.numbertoString(row['f' + y.item]) : undefined
              })
              var _export = new Export()
              var filename  = task.company__stock_code  + '-' + task.company__type__code + '-' + task.year + '-Q' + task.report_period__code  + '-' + task.report_type__code + '-' + task.report_name__code
              _export.set(data, filename)
              _export.exportReport()
            }
          }
        })
      } else if(newVal==='error') {
          let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: 'Lỗi. Tải dữ liệu không thành công.'}
          this.$buefy.notification.open(info)
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
    
    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
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
    confirmDeleteTask(name) {
      if(name==='available')
        var data = this.selectedRows.filter(v=>v.status__code==='not-yet-entered')
      else if(name==='relate')
        var data = this.selectedRows.filter(v=>v.status__code!=='not-yet-entered' && v.status__code!=='approved')
      else if(name==='approved')
        var data = this.selectedRows.filter(v=>v.status__code==='approved')
      
      this.deleteType = name
      this.connection.delete(this.pagetask.api.name, data)
    },
    
    confirmApprove(name) {
      this.taskStatus = name
      let data = this.$copy(this.selectedRows.filter(v=>v.status__code===name))
      data.map(v=>{
        let found = name==='waiting-approve'?  this.api.find3var('list', 'task-status', 'waiting-approve-2')
        : this.api.find3var('list', 'task-status', 'approved')

        v.status = found.id
        v.status__code = found.code
        v.status__value = found.value

        v.assign_date = new Date(v.assign_date)
        v.due_date = new Date(v.due_date)
        v.entry_time = v.entry_time? new Date(v.entry_time) : undefined
        v.waiting1_time = v.waiting1_time? new Date(v.waiting1_time) : undefined

        if(name==='waiting-approve') v.waiting2_time = new Date()
        else if(v.waiting2_time) v.waiting2_time = new Date(v.waiting2_time)
        
        if(name==='waiting-approve-2') v.approve_time = new Date()
        else if(v.approve_time) v.approve_time = new Date(v.approve_time)
      })
      this.connection1.insert(this.pagetask.api.name, data, this.pagetask.api.params.values)
    },

    selectedAction(type) {
      this.selectedRows = []
      this.pagetask.models.forEach((element, id) => {
        if (element === true) {
          let found = this.pagetask.data.find(v => parseInt(v.id) === parseInt(id));
          this.selectedRows.push(found);
        }
      })

      if(type==='opentab') this.openTab()
      else if(type==='download') this.download()
      this.msgInfo = []
      this.actionType = type
    },

    openTab() {
      if(this.selectedRows.length>20) {
        let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: 'Lỗi. Chỉ mở được tối đa 20 tab.'}
        this.$buefy.notification.open(info)
        return
      }

      let urlList = []
      this.selectedRows.map(newVal=>{
        let routeData = this.$router.resolve({ path: '/finance/data-entry', query: {task: newVal.id, type: newVal.company__type__code, company: newVal.company, report: newVal.report_name__code}})
        this.pagetask.api.url==='data/Task_Stock'? routeData = this.$router.resolve({ path: '/transaction/data-entry', query: {task: newVal.id, report: newVal.report_name__code}}) : false
        urlList.push(routeData.href) 
      })
      let i = -1;
      let int = setInterval(() => {
        i++
        if (i>= urlList.length) clearInterval(int)
        else window.open(urlList[i], "_blank")
      }, 500)
    },

    download() {
      if(this.selectedRows.length>20) {
        let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: 'Lỗi. Chỉ tải được tối đa 20 file.'}
        this.$buefy.notification.open(info)
        return
      }
      let connlist = [{name: 'reportitem', url: 'data/Report_Item', params: {page: -1, sort: 'index', filter: {enable: 1}}}]
      this.selectedRows.map(v=>{
        let name = mixing.connection(v.report_name__code, v.company__type__code)
        let found = {name: name.toUpperCase(), url: 'data/' + name.toUpperCase(), params: {filter:{task: v.id}}}
        connlist.push(found)
      })
      this.connection2.getApi(connlist)
    },

    clearSelect() {
      this.$store.commit("updateState", {name: "pagetask", key: "data", data: this.$copy(this.pagetask.data)})
    }
  }
}
</script>