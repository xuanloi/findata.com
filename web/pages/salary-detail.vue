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
            locale="it-IT"
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
        locale="it-IT"
        placeholder="Chọn ngày"
        v-model="tdate"
        >
    </b-datepicker>
    </div>
    <p class="help is-danger" v-if="errList.find(v=>v==='dob') !==undefined">{{getval(msgList.find(v=>v.name==='dob'),'message')}}</p>
    </div> 
    </div>   
    </div>
    </div>
    <TableFilter class="mx-4" v-bind="{name: 'pagetask'}" />
    </div>
  </section>
  <Footer></Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
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
        connection: this.$connection(this.$buefy),
        data: [],
        fields: [],
        errList: [],
        msgList: [],
        fdate: new Date(Date.now() -15*24*3600*1000),
        tdate: new Date(),
        tophead: '',
        reload: false
      }
    },

    head() {
      return {
        title: 'Chi tiết tiền công'
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
      fields.push(mixing.createField('recipient__name', 'Người nhận việc', 'string', false, true))

      fields.push(mixing.createField('assign_date', 'Ngày giao', 'string', false, true))
      fields.push(mixing.createField('approve_time', 'Ngày duyệt', 'string', false, true))
      
      fields.push(mixing.createField('company__factor', 'Hệ số DN', 'string', false, true))
      fields.push(mixing.createField('unit_price', 'Đơn giá', 'string', false, true))
      fields.push(mixing.createField('into_money', 'TC dự kiến', 'string', false, true))
      fields.push(mixing.createField('reality', 'TC thực tế', 'string', false, true))
      fields.push(mixing.createField('point', 'Điểm GT', 'string', false, true))
      
      field = mixing.createField('status__value', 'Trạng thái', 'string', false, true)
      field.style = {list: [{value: 'not-yet-entered', class: 'button is-small is-primary is-outlined'},
        {value: 'entered', class: 'button is-small is-info is-outlined'},
        {value: 'approved', class: 'button is-small is-success is-outlined'},
        {value: 'waiting-approve', class: 'button is-small is-link is-outlined'},
        {value: 'waiting-approve-2', class: 'button is-small is-link is-outlined'},
        {value: 'retype', class: 'button is-small is-danger is-outlined'}], condition: 'status__code', click: true}
      fields.push(field)

      this.fields = fields
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true, enableApprove: true,
      api: {} , origin_api: {}, reload: 0}
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
          if(this.pagetask.action==='show') {
            var routeData = this.$router.resolve({ path: '/finance/data-entry', query: {task: newVal.id, type: newVal.company__type__code, company: newVal.company, report: newVal.report_name__code}})
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
        let values = 'id,company,company__name,company__stock_code,company__type__code,report_type,report_period,report_period__value,year,report_name,report_name__code,report_type__code,report_type__value,company__factor,unit_price,into_money,'
        values += 'assigner,assigner__name,recipient,recipient__name,assign_date,due_date,percentage,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time,marked_fields'
        let nextdate = new Date(new Date(this.tdate).getTime()+(1*24*60*60*1000))
        
        let found = {name: 'tasklist', url: 'data/Task', params: {}}
        let filter = {assign_date__gte: mixing.yyyymmdd(this.fdate), assign_date__lt:mixing.yyyymmdd(nextdate)}

        //check right
        let type = this.login.type
        if(type.code==='staff' || type.code==='ctv') {
          filter = {assign_date__gte: mixing.yyyymmdd(this.fdate), assign_date__lt:mixing.yyyymmdd(nextdate), recipient: this.login.id}
        }

        //check filter by status
        if(this.$route.query.status!==undefined) filter.status = this.$route.query.status
        found.params = {values: values, filter: filter}    
        this.connection.getApi([found])
        this.getHeader()
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
          v.point = this.$empty(v.percentage)===false? (mixing.formatNumber(v.percentage)/100.00).toFixed(2) : undefined
          v.percentage = v.percentage===null? undefined : v.percentage + '%'
          v.reality = v.status__code==='approved'? v.into_money : undefined
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

      getHeader() {
        let status = this.$route.query.status
        if(status!==undefined) status = this.api.getbyid(parseInt(status)).code

        if(status===undefined) this.tophead = 'Danh sách công việc'
        else if(status==='not-yet-entered') this.tophead = 'Danh sách công việc chưa nhập'
        else if(status==='entered') this.tophead = 'Danh sách công việc đang nhập'
        else if(status==='waiting-approve') this.tophead = 'Danh sách công việc chờ duyệt 1'
        else if(status==='waiting-approve-2') this.tophead = 'Danh sách công việc chờ duyệt 2'
        else if(status==='approved') this.tophead = 'Danh sách công việc đã duyệt'
        else if(status==='retype') this.tophead = 'Danh sách công việc sửa lại'
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
          company_factor: 'String',
          unit_price: 'String',
          expectation: 'String',
          reality: 'String',
          point: 'String',
          approve_time: 'String'
        }

        let fields = ['id', 'company__stock_code', 'company__type__code', 'report_period__value', 'year', 'report_type__code', 'report_name__code', 
        'assigner__name', 'recipient__name', 'assign_date', 'due_date','priority', 'percentage', 'status__value', 'company__factor', 'unit_price', 'into_money', 'reality', 'point','approve_time']
      _export.set(this.pagetask.filter, 'salary-list', dataTypes, fields)
      _export.exportfile()
      }
    }
}
</script>