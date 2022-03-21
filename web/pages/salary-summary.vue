<!-- eslint-disable -->
<template>
<div>
<TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}"></TopMenu>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body mt30 px-0">
    <div class="columns is-multiline is-mobile">
        <div class="column is-3 py-0 has-text-centered">
        <span class="has-text-primary">  {{this.data.length + ' kết quả theo ngày giao việc'}} </span>
        </div>
        <div class="column is-1 pt0 has-text-right has-text-grey-dark">
             <span>Từ ngày </span>
        </div>
        <div class="column is-2 pt0">
    <div class="field">
           
    <div class="control">
    <div :type="errList.find(v=>v==='dob') !==undefined? 'is-danger' : ''" >
        <b-datepicker   size="font-smaller"
            ref="datepicker"
            placeholder="Chọn ngày"
            v-model="fdate"
            >
        </b-datepicker>
    </div>
    <p class="help is-danger" v-if="errList.find(v=>v==='dob') !==undefined">{{getval(msgList.find(v=>v.name==='dob'),'message')}}</p>
    </div> 
    </div>   
    </div>    
        <div class="column is-1 pt0 has-text-right has-text-grey-dark">
             <span>Đến ngày </span>
        </div>
        <div class="column is-2 pt0">
    <div class="field">
           
    <div class="control">
    <div :type="errList.find(v=>v==='dob') !==undefined? 'is-danger' : ''" >
    <b-datepicker   size="font-smaller"
        ref="datepicker"
        placeholder="Chọn ngày"
        v-model="tdate"
        >
    </b-datepicker>
    </div>
    <p class="help is-danger" v-if="errList.find(v=>v==='dob') !==undefined">{{getval(msgList.find(v=>v.name==='dob'),'message')}}</p>
    </div> 
    </div>   
    </div>

    <div class="column is-3 pt0">
        <b-checkbox type='is-primary' class="mr40" v-model="salcal"><span class="ml5 has-text-primary"> Tính lương </span></b-checkbox>
    </div>
    </div>
        <div class="mx-3"> 
            <TableFilter v-bind="{name: 'pagetask'}" > </TableFilter>
        </div>
    </div>
    </section>
<Footer></Footer>
</div>
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import TableFilter from '@/components/TableFilter'
import Export from '@/assets/js/export.js'

export default {
  components: {
    TableFilter
  },

  data () {
    return {
        connection: this.$connection(),
        data: [],
        fields: [],
        errList: [],
        msgList: [],
        fdate: new Date(Date.now() -15*24*3600*1000),
        tdate: new Date(),
        tophead: 'Tổng hợp tiền công',
        salcal: undefined
      }
    },

    head() {
      return {
        title: this.tophead
      }
    },
    
    created() {
      this.pagetask = {data: [], fields: [], filter: [], record: undefined, action: undefined, enableDelete: true,
      api: {} , origin_api: {}, reload: 0}
      this.connectData()
    },

    watch: {
      'connection.getdataReady' : function(newVal) {
        if(newVal==='success') this.fillData()
        else if (newVal==='error') this.$router.push({path: '/error'})
      },

      'pagetask.record' : function(newVal) {
        if(newVal!==undefined) {
          let routeData = this.$router.resolve({ name: 'data-entry', query: {task: newVal.id, company_type: newVal.company_type, company: newVal.company}}) 
          window.open(routeData.href, '_blank')
          this.pagetask.record = undefined
        }
      },

      fdate : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.connectData(true)
      },

      tdate : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.connectData(true)
      },

      salcal : function(newVal) {
        if(newVal===undefined) return
        this.connectData()
      },

      menuaction : function(newVal) {
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
      },
    },
    
    methods: {
      connectData() {
        let nextdate = new Date(new Date(this.tdate).getTime()+(1*24*60*60*1000))
        let url = (this.salcal===true? 'salary-calculation/' : 'salary-summary/') +  mixing.yyyymmdd(this.fdate).replace(/-/g, '') + ',' + mixing.yyyymmdd(nextdate).replace(/-/g, '')     
        let obj = {name: 'salcal', url: url, params: {}}
        this.connection.getApi([obj])
      },

      fillData() {
        let data = this.connection.getbatchData[0].data
        data.forEach(element => {
          if(this.salcal===true) {
            element.fdate = mixing.yyyymmdd(this.fdate)
            element.tdate = mixing.yyyymmdd(this.tdate)
            element.bank_account_name = element.recipient.bank_account_name
            element.bank_account = element.recipient.bank_account
            element.bank = this.$empty(element.recipient.bank)===false? this.api.getbyid(element.recipient.bank).value : undefined
            element.point = this.$empty(element.point)===false? element.point.toFixed(2) : undefined
            element.reality = this.$empty(element.reality)===false? mixing.numbertoString(element.reality) : undefined
            element.pay_date = undefined
            element.detail = undefined
          }
          else {
            element.recipient_name = element.recipient.id + ' | ' + element.recipient.name
            element.company_type = this.api.getbyid(element.type_id).code
            element.report_name_code = element.report_name.code
            element.point = this.$empty(element.point)===false? element.point.toFixed(2) : undefined
            element.expectation = this.$empty(element.expectation)===false? mixing.numbertoString(element.expectation) : undefined
            element.reality = this.$empty(element.reality)===false? mixing.numbertoString(element.reality) : undefined
          }
        })
        this.data = data
        this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        if(Object.keys(this.pagetask.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
        }
        this.getFields()
      },

      getFields() {
          let fields = []
          if(this.salcal!==true) {
            fields.push(mixing.createField('id', 'Id', 'number', false, true))
            let field = mixing.createField('recipient_name', 'Người nhập', 'string', false, true)
            fields.push(field)
            fields.push(mixing.createField('company_type', 'Loại doanh nghiệp', 'string', false, true))
            fields.push(mixing.createField('report_name_code', 'Báo cáo', 'string', false, true))
            fields.push(mixing.createField('count', 'Số lượng', 'number', false, true))
            fields.push(mixing.createField('expectation', 'TC dự kiến', 'number', false, true))
            fields.push(mixing.createField('reality', 'TC thực tế', 'number', false, true))
            fields.push(mixing.createField('point', 'Điểm GT', 'number', false, true))
          }
          else {
            fields.push(mixing.createField('id', 'Id', 'number', false, true))
            let field = mixing.createField('fdate', 'Từ ngày', 'string', false, true)
            fields.push(field)
            fields.push(mixing.createField('tdate', 'Đến ngày', 'string', false, true))
            fields.push(mixing.createField('reality', 'Tiền công', 'number', false, true))
            fields.push(mixing.createField('point', 'Điểm GT', 'number', false, true))
            fields.push(mixing.createField('bank_account_name', 'Tên tài khoản', 'string', false, true))
            fields.push(mixing.createField('bank_account', 'Tài khoản', 'number', false, true))
            fields.push(mixing.createField('bank', 'Ngân hàng', 'number', false, true))
            fields.push(mixing.createField('pay_date', 'Ngày trả lương', 'number', false, true))
            fields.push(mixing.createField('detail', 'Chi tiết', 'number', false, true))
          }
          
          this.fields = fields
          this.$store.commit('updateState', {name: 'pagetask', key: 'fields', data: fields})
        },

       exportData() {
        var _export = new Export()
        let dataTypes = {}
        let fields = []

        this.fields.forEach(element => {
            dataTypes[element.name] = 'String'
            fields.push(element.name)
        })

        _export.set(this.pagetask.filter===undefined? this.pagetask.data : this.pagetask.filter, 'salary-summary', dataTypes, fields)
        _export.exportfile()
      }
    }
}
</script>

<style scoped
  src="bulma-extensions/bulma-tooltip/dist/css/bulma-tooltip.min.css">
</style>