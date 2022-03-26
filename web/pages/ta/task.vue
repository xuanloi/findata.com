<!-- eslint-disable -->
<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}"></TopMenu>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body mt30 px-0">
    <div class="columns is-multiline is-mobile">
        <div class="column is-3 py-0 has-text-centered">
        <span class="has-text-primary"> {{(pagetask? pagetask.origin_api.total_rows : '') + ' kết quả theo ngày giao việc' }} </span>
        </div>
        <div class="column is-1 py-0 has-text-right has-text-grey-dark">
          <span>Từ ngày </span>
        </div>
        <div class="column is-2 py-0">
        <div class="field">
        <div class="control">
        <div :type="errList.find(v=>v==='dob') !==undefined? 'is-danger' : ''" >
          <b-datepicker   size="font-smaller"
            ref="datepicker"
            locale="en-GB"
            placeholder="Chọn ngày"
            v-model="fdate"
          >
          </b-datepicker>
        </div>
        <p class="help is-danger" v-if="errList.find(v=>v==='dob') !==undefined">{{getval(msgList.find(v=>v.name==='dob'),'message')}}</p>
        </div> 
        </div>   
    </div>    
        <div class="column is-1 py-0 has-text-right has-text-grey-dark">
          <span>Đến ngày </span>
        </div>
        <div class="column is-2 py-0">
    <div class="field">
           
    <div class="control">
    <div :type="errList.find(v=>v==='dob') !==undefined? 'is-danger' : ''" >
    <b-datepicker   size="font-smaller"
        ref="datepicker"
        locale="en-GB"
        placeholder="Chọn ngày"
        v-model="tdate"
        >
    </b-datepicker>
    </div>
    <p class="help is-danger" v-if="errList.find(v=>v==='dob') !==undefined">{{getval(msgList.find(v=>v.name==='dob'),'message')}}</p>
    </div> 
    </div>   
    </div>

    <div class="column is-3 py-0">
        <a class="tag is-medium is-primary" @click="approveTask()" v-if="hasRightApprove()===true">Duyệt theo lô</a>
        <a class="tag is-medium is-primary" @click="deleteTask()" v-else-if="hasRightDelete()===true">Xóa theo lô</a>
    </div>
    </div>
    <TableFilter class="mx-4" v-bind="{name: 'pagetask'}" />
    </div>
  </section>
  <Footer></Footer>
</div>
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import Export from '@/assets/js/export.js'
export default {
    data () {
      return {
        connection: this.$connection(this.$buefy),
        data: [],
        fields: [],
        errList: [],
        msgList: [],
        fdate: new Date(Date.now() -15*24*3600*1000),
        tdate: new Date(),
        tophead: '',
      }
    },

    head() {
      return {
        title: 'Danh sách công việc nhập báo cáo giao dịch'
      }
    },

    created() {
      this.connectData()
      let fields = []
      fields.push(mixing.createField('id', 'Id', 'number', false, true))
      fields.push(mixing.createField('stock_date', 'Ngày dữ liệu', 'string', false, true))
      let field = mixing.createField('report_name__code', 'Báo cáo', 'string', false, true)
      field.tooltip = {position: 'is-right', field: 'report_name__value', class: 'tag is-rounded is-light'}
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
      let isAllow = (type.code==='admin' || type.code==='manager' || type.code==='teamlead')? true : false
      field = mixing.createField('action', '', 'string', false, true, '7%', isAllow? 'select, edit' : 'select')
      fields.push(field)
      this.fields = fields
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
      enableDelete: type.code==='admin' || type.code==='manager'? true : false, 
      enableApprove: isAllow, api: {} , origin_api: {}, reload: 0}
    },

    watch: {
      "connection.getdataReady": function(newVal) {
        if (newVal === "success") this.fillData()    
      },

      'pagetask.reload': function(newVal, oldVal) {
        if(oldVal===undefined) return
        let found = newVal===0? this.$copy(this.pagetask.origin_api) : this.$copy(this.pagetask.api)
        if(Object.keys(found).length>0) this.connection.getApi([found])
      },

      'pagetask.record': function(newVal) {
        if(newVal) {
          if(this.pagetask.action==='edit') {
            let routeData = this.$router.resolve({ path: '/ta/task-edit', query: {task: newVal.id}})
            window.open(routeData.href, '_blank')
          } 
          else if(this.pagetask.action==='show') {
            let routeData = this.$router.resolve({ path: '/ta/data-entry', query: {task: newVal.id, report: newVal.report_name__code}})
            window.open(routeData.href, '_blank')
          } 
          this.$store.commit("updateState", {name: "pagetask", key: "record", data: undefined})
        }
      },

      fdate: function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.$store.commit("updateState", {name: "pagetask", key: "origin_api", data: {}})
        this.connectData()
      },

      tdate: function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.$store.commit("updateState", {name: "pagetask", key: "origin_api", data: {}})
        this.connectData()
      },
        
      menuaction: function(newVal) {
        if(newVal? newVal.action==='download': false) this.exportData()
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
        this.$router.push({path: '/import', query: {type: 'batch-approve', status: this.api.getbyid(parseInt(this.$route.query.status)).code}})
      },

      deleteTask() {
        this.$router.push({path: '/import', query: {type: 'delete-task'}})
      },

      connectData() {
        let values = 'id,stock_date,report_name,report_name__code,report_name__value,assigner,assigner__name,recipient,recipient__name,assign_date,due_date,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time'
        let nextdate = new Date(new Date(this.tdate).getTime()+(1*24*60*60*1000))
        
        let found = {name: 'tasktaindex', url: 'data/Task_Taindex', params: {}}
        let filter = {assign_date__gte: mixing.yyyymmdd(this.fdate), assign_date__lt:mixing.yyyymmdd(nextdate)}

        //check right
        let type = this.login.type
        if(type.code==='staff' || type.code==='ctv') {
          filter = {assign_date__gte: mixing.yyyymmdd(this.fdate), assign_date__lt:mixing.yyyymmdd(nextdate), recipient: this.login.id}
        }

        //check filter by status
        if(this.$route.query.status!==undefined) filter.status = this.$route.query.status
        found.params = {values: values, filter: filter, sort: '-update_time'}    
        this.connection.getApi([found])
        this.getHeader()
      },

      updateTask(task) {
        task.assign_date = mixing.yyyymmdd(new Date(task.assign_date))
        task.due_date = mixing.yyyymmdd(new Date(task.due_date))
        task.entry_time = this.$empty(task.entry_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.entry_time))
        task.waiting1_time = this.$empty(task.waiting1_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting1_time))
        task.waiting2_time = this.$empty(task.waiting2_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting2_time))
        task.approve_time = this.$empty(task.approve_time)===false? mixing.yyyymmdd(new Date(task.approve_time)) : undefined
        let index = this.pagetask.data.findIndex(v=>task.id===task.id)
       
        if(index>=0) {
          let copy = this.$copy(this.pagetask.data)
          copy[index] = task
          mixing.arrayMove(copy,index,0)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
          this.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
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
          this.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
        }
      },

      fillData() {
        let data = this.$copy(this.connection.getbatchData[0].data)
        data.map(v=>{
          v.assign_date = mixing.yyyymmdd(new Date(v.assign_date))
          v.due_date = mixing.yyyymmdd(new Date(v.due_date))
          v.entry_time = this.$empty(v.entry_time)===true? 'n/a' : mixing.yyyymmdd(new Date(v.entry_time))
          v.waiting1_time = this.$empty(v.waiting1_time)===true? 'n/a' : mixing.yyyymmdd(new Date(v.waiting1_time))
          v.waiting2_time = this.$empty(v.waiting2_time)===true? 'n/a' : mixing.yyyymmdd(new Date(v.waiting2_time))
          v.approve_time = this.$empty(v.approve_time)===false? mixing.yyyymmdd(new Date(v.approve_time)) : undefined
        })
        this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        if(Object.keys(this.pagetask.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
        }
      },

      getHeader() {  
        this.tophead = 'Danh sách công việc nhập báo cáo Dữ liệu giao dịch'
      },

      exportData() {
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