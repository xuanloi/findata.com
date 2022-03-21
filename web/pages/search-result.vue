<!-- eslint-disable -->
<template>
<div>
  <TopMenu v-bind="{type: 'search', tophead: this.tophead, enableDownload: true}"></TopMenu>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body mt30 px-0">
    <div class="columns is-multiline is-mobile">
      <div class="column is-3 py-0 has-text-centered">
        <span class="has-text-primary"> {{(pagetask? pagetask.api.total_rows : '') + ' bản ghi được tìm thấy.'}} </span>
      </div>

    <div class="column is-3 py-0">
      <button class="button is-primary is-outlined font-smaller" @click="approveTask()" v-if="hasRightApprove()===true">Duyệt theo lô</button>
      <button class="button is-primary is-outlined font-smaller" @click="deleteTask()" v-else-if="hasRightDelete()===true">Xóa theo lô</button>
    </div>
    </div>
      <div class="mx-3" v-if="pagetask"> 
        <TableFilter v-bind="{name: 'pagetask'}" > </TableFilter>
      </div>
    </div>
    </section>

  <Footer></Footer>
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'

import mixing from '@/assets/js/mixing.js'
import TableFilter from '@/components/TableFilter.vue'
import Export from '@/assets/js/export.js'

export default {
  components: {
    TopMenu,
    Footer,
    TableFilter
  },

  data () {
      return {
        connection: this.$connection(),
        data: [],
        fields: [],
        errList: [],
        msgList: [],
        tophead: 'Kết quả tìm kiếm',
        message: '',
        reload: false
      }
    },

    head() {
      return {
        title: this.tophead
      }
    },
    
    created() {
      this.connectData()
      let fields = []
      fields.push(mixing.createField('id', 'Id', 'number', false, true))
      let field = mixing.createField('company__stock_code', 'Công ty', 'string', false, true)
      field.tooltip = {position: 'is-right', field: 'company__name', class: 'tag is-rounded is-light'}
      fields.push(field)

      fields.push(mixing.createField('company__type__code', 'Loại', 'string', false, true))
      fields.push(mixing.createField('report_period__value', 'Kỳ BC', 'string', false, true))
      fields.push(mixing.createField('year', 'Năm', 'string', false, true))
      fields.push(mixing.createField('report_name__code', 'Báo cáo', 'string', false, true))
      
      field = mixing.createField('report_type__code', 'Loại BC', 'string', false, true)
      field.tooltip = {position: 'is-right', field: 'report_type__value', class: 'tag is-rounded is-light'}
      fields.push(field)

      fields.push(mixing.createField('assigner__name', 'Người giao việc', 'string', false, true))
      fields.push(mixing.createField('recipient__name', 'Người nhận việc', 'string', false, true))

      fields.push(mixing.createField('assign_date', 'Ngày giao', 'string', false, true))
      let status = this.$route.query.status===undefined? undefined : this.api.getbyid(parseInt(this.$route.query.status)).code
      if(status==='waiting-approve') {
          var text = 'Ngày nộp'
          var name = 'waiting1_time'
      }
      else if(status==='waiting-approve-2') {
          var text = 'Ngày duyệt 1'
          var name = 'waiting2_time'
      }
      else if(status==='approved') {
          var text = 'Ngày lưu kho'
          var name = 'approve_time'
      }
      else {
          var text = 'Ngày đến hạn'
          var name = 'due_date'
      }

      fields.push(mixing.createField(name, text, 'string', false, true))
      fields.push(mixing.createField('percentage', 'Tỷ lệ', 'string', false, true))
      fields.push(mixing.createField('priority', 'Ưu tiên', 'string', false, true))
      
      field = mixing.createField('status__value', 'Trạng thái', 'string', false, true)
      field.style = {list: [{value: 'not-yet-entered', class: 'button is-small is-primary is-outlined'},
        {value: 'entered', class: 'button is-small is-info is-outlined'},
        {value: 'approved', class: 'button is-small is-success is-outlined'},
        {value: 'waiting-approve', class: 'button is-small is-link is-outlined'},
        {value: 'waiting-approve-2', class: 'button is-small is-link is-outlined'},
        {value: 'retype', class: 'button is-small is-danger is-outlined'}], condition: 'status__code', click: true}
      fields.push(field)

      let type = this.login.type
      if(type.code==='admin' || type.code==='manager' || type.code==='teamlead') {
        field = mixing.createField('action', '', 'string', false, true, '7%', 'select, edit')
        fields.push(field)
      }
      this.fields = fields
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true, enableApprove: true,
      api: {} , origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
    },

    watch: {
      "connection.getdataReady": function(newVal) {
        if (newVal === "success") this.fillData()    
      },

      'pagetask.record': function(newVal) {
        if(newVal) {
          if(this.pagetask.action==='edit') {
            let routeData = this.$router.resolve({ path: '/finance/task-edit', query: {task: newVal.id}})
             window.open(routeData.href, '_blank')
          } 
          else if(this.pagetask.action==='show') {
            let routeData = this.$router.resolve({ path: '/finance/data-entry', query: {task: newVal.id, type: newVal.company__type__code, company: newVal.company, report: newVal.report_name__code}})
             window.open(routeData.href, '_blank')
          } 
          this.$store.commit("updateState", {name: "pagetask", key: "record", data: undefined})
          this.$store.commit("updateState", {name: "pagetask", key: "action", data: undefined})
        }
      },

      '$route.query' : function(newVal) {
        this.connectData()
      },
      
      menuaction : function(newVal) {
        if(newVal? newVal.action==='download': false) this.exportData()
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.getters.api },
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },
      
      pagetask: {
        get: function() {return this.$store.state.pagetask},
        set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
      },
      
      companylist: {
        get: function() {return this.$store.state.companylist},
        set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
      },

      accountlist: {
        get: function() {return this.$store.state.accountlist},
        set: function(val) {this.$store.commit('updateAccountList', {accountlist: val})}
      },

      login: {
        get: function() {return this.$store.state.login},
        set: function(val) {this.$store.commit("updateLogin", { login: val })}
      },

      menuaction: {
        get: function() {return this.$store.state.menuaction},
        set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
      }
    },
    
    methods: {
      hasRightDelete() {
        let code = this.login.type.code
        if(this.$route.query.status==='158') {
          if(code==='admin' || code==='manager') return true
        }
        return false
      },

      hasRightApprove() {
        let code = this.login.type.code
        if(this.$route.query.status==='677') {
          if(code==='admin' || code==='manager') return true
        }
        else if(this.$route.query.status=='171') {
          if(code==='admin' || code==='manager' || code==='teamlead') return true
        }
      },

      approveTask() {
        this.$router.push({name: 'import-batch-approve', query: {status: this.api.getbyid(parseInt(this.$route.query.status)).code}})
      },

      deleteTask() {
        this.$router.push({name: 'delete-task'})
      },

      connectData() {
        let values = 'id,company,company__name,company__stock_code,company__type__code,report_type,report_period,report_period__code,report_period__value,year,report_name,report_name__code,report_type__code,report_type__value,'
        values += 'assigner,assigner__name,recipient,recipient__name,assign_date,due_date,percentage,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time,marked_fields'
          
        let found = {name: 'tasklist', url: 'data/Task/', params: {}}
        let filter = this.$route.query.type==='company'? {company: this.$route.query.keyword} : 
        (this.$route.query.type==='task'? {id: this.$route.query.keyword} : {recipient: this.$route.query.keyword})

        //check right
        let type = this.login.type
        if(type.code==='staff' || type.code==='ctv') filter.recipient = this.login.id

        //check filter by status
        if(this.$route.query.status!==undefined) filter.status = this.$route.query.status
        found.params = {values: values, filter: filter, sort: '-update_time,-priority'}    
        this.connection.getApi([found])
      },

      fillData() {
        let data = this.$copy(this.connection.getbatchData[0].data)
        data.map(v=>{
          v.assign_date = mixing.yyyymmdd(new Date(v.assign_date))
          v.due_date = mixing.yyyymmdd(new Date(v.due_date))
          v.entry_time = this.$empty(v.entry_time)===true? 'n/a' : v.entry_time.substring(0,10)
          v.waiting1_time = this.$empty(v.waiting1_time)===true? 'n/a' : v.waiting1_time.substring(0,10)
          v.waiting2_time = this.$empty(v.waiting2_time)===true? 'n/a' : v.waiting2_time.substring(0,10)
          v.approve_time = this.$empty(v.approve_time)===false? v.approve_time.substring(0,10) : undefined
        })
        this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        if(Object.keys(this.pagetask.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
        }

        if(this.reload) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'filter', data: data})
          this.reload = false
          this.exportData()
        }
      },

      updateTask(task) {
        task.assign_date = mixing.yyyymmdd(new Date(task.assign_date))
        task.due_date = mixing.yyyymmdd(new Date(task.due_date))
        task.entry_time = this.$empty(task.entry_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.entry_time))
        task.waiting1_time = this.$empty(task.waiting1_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting1_time))
        task.waiting2_time = this.$empty(task.waiting2_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting2_time))
        task.approve_time = this.$empty(task.approve_time)===false? mixing.yyyymmdd(new Date(task.approve_time)) : undefined
        let index = this.pagetask.data.findIndex(v=>v.id===task.id)
        let self = this
        
        if(index>=0) {
          let copy = this.$copy(this.pagetask.data)
          copy[index] = task
          mixing.arrayMove(copy,index,0)
          if(this.pagetask.currentFilter? this.pagetask.currentFilter.length>0 : false) {
           this.$store.commit('updateState', {name: 'pagetask', key: 'filterby', data: this.$copy(this.pagetask.currentFilter)})
          }
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
          mixing.delay(function(newVal) {
            self.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
          },100)
        }
        else {
          if(this.pagetask.currentFilter? this.pagetask.currentFilter.length>0 : false) return
          //check right
          if(this.login.id===task.assigner || this.login.id===task.recipient) {var isOK = true} 
          else if(this.login.type.code==='admin' || this.login.type.code==='manager') {var isOK = true}
          if(isOK===undefined) return //exit
          let copy = this.$copy(this.pagetask.data)
          copy.data.splice(0, 0, task)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
          mixing.delay(function(newVal) {
            self.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
          },100)
        }
      },

      exportData() {
        if(!this.pagetask.api.full_data) {
          this.reload = true
          let found = this.$copy(this.pagetask.api)
          found.params.page = -1
          this.connection.getApi([found])
          return
        }

        var _export = new Export()
        let status = this.$route.query.status===undefined? undefined : this.api.getbyid(parseInt(this.$route.query.status)).code
        let  dataTypes = {
          id: 'String', 
          company: 'String',
          company_type : 'String',
          report_period: 'String',
          year: 'String',
          report_type: 'String',
          report_name: 'String',
          assigner: 'String',
          recipient: 'String',
          assign_date: 'String',
          due_date: 'String',
          priority : 'String',
          percentage : 'String',
          status : 'String',
          report : 'String',
          approve: 'String',
          entry_time: 'String',
          waiting1_time: 'String',
          waiting2_time: 'String',
          approve_time: 'String'
        }
        
      let fields = ['id', 'company__stock_code', 'company__type__code', 'report_period__value', 'year', 'report_type__code', 'report_name__code', 
      'assigner__name', 'recipient__name', 'assign_date', 'due_date','priority', 'percentage', 'status__value', 'report', 'approve', 'entry_time', 'waiting1_time', 'waiting2_time', 'approve_time']
        _export.set(this.pagetask.filter, this.tophead, dataTypes, fields)
        _export.exportfile()
      }
  }
}
</script>

<style scoped
  src="bulma-extensions/bulma-tooltip/dist/css/bulma-tooltip.min.css">
</style>