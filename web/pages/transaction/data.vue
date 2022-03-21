<!-- eslint-disable -->
<template>
<div>
	<TopMenu v-bind="{type: 'tophead', tophead: this.title, enableDownload: true}"></TopMenu>
        <div class="pt60"/>

    <section class="hero is-paddingless is-marginless" v-if="pageitem.record===undefined">
    <div class="hero-body pt5 pb15 pl0 pr0">
        <div class="mx-3"> 
        <TableFilter v-bind="{name: 'pageitem'}" />
        </div>
        </div>
    </section>

    <section class="hero is-paddingless is-marginless"  v-else-if="pageitem.record!==undefined">
    <div class="hero-body pt0">
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
import TableFilter from '@/components/TableFilter'
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
      connection1: this.$connection(),
      items: [],
      title: 'Dữ liệu thống kê Giá'
    }
  },

  head() {
    return {
      title: this.title
    }
  },
    
  created() {
    if(!this.connName) return
    let found = {name: 'reportitem', params: {filter: {company_type: 'KQGD', report_name: this.$route.query.report}}}
    this.connection.getApi([found])
    this.pageitem = {data: [], fields: [], filter: [], record: undefined, action: undefined, enableDelete: false,
    api: {} , origin_api: {}, reload: 0}
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        this.items = this.connection.getbatchData[0].data
        let type = this.login.type
        let filter = (type.code==='staff' || type.code==='ctv')? { task__recipient: this.login.id} : undefined
        if(type.code==='teamlead') filter = { task__recipient: this.login.id, task__assigner: this.login.id}

        let values = 'id,stock_date,company,company__stock_code,task,' + this.items.map(v=> 'f' + v.item).join()
        if(this.connName? this.connName.name==='pricelive' : false) values += ',time'
        let found = this.$copy(this.connName)
        found.params = {filter_or: filter, values: values}
        this.connection1.getApi([found])
      }
    },
    
    'connection1.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
    },
    
    'pageitem.reload': function(newVal, oldVal) {
      if(oldVal===undefined) return
      let found = newVal===0? this.$copy(this.pageitem.origin_api) : this.$copy(this.pageitem.api)
      if(Object.keys(found).length>0) this.connection1.getApi([found])
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
      
    pageitem: {
      get: function() {return this.$store.state.pageitem},
      set: function(val) {this.$store.commit('updatePageItem', {pageitem: val})}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    },
        
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    },

    connName() {
      var val = undefined
      if(this.$route.query.report==='TKGIA') val = this.connection.requirelist.find(v=>v.name==='stockprice')
      else if(this.$route.query.report==='TKLENH') {
        val = this.connection.requirelist.find(v=>v.name==='stockorder')
        this.title = 'Dữ liệu thống kê Đặt lệnh'
      }
      else if(this.$route.query.report==='DTNNLENH') {
        val = this.connection.requirelist.find(v=>v.name==='foreignorder')
        this.title = 'Dữ liệu thống kê Nước ngoài khớp lệnh'
      }
      else if(this.$route.query.report==='DTNNTT') {
        val = this.connection.requirelist.find(v=>v.name==='foreigndeal')
        this.title = 'Dữ liệu thống kê Nước ngoài mua thỏa thuận'
      }
      else if(this.$route.query.report==='GIA') {
        val = this.connection.requirelist.find(v=>v.name==='pricelive')
        this.title = 'Dữ liệu Giá trực tuyến (Live)'
      }
      return val
    }
  },
    
  methods: {
    fillData() {
      let fields = []
      fields.push(mixing.createField('id', 'Id', 'number', false, true))
      fields.push(mixing.createField('stock_date', 'Ngày GD', 'string', false, true))
      if(this.connName? this.connName.name==='pricelive' : false) {
        fields.push(mixing.createField('time', 'Thời gian', 'string', false, true))
      }
      fields.push(mixing.createField('company__stock_code', 'stock_code', 'string', false, true))
      this.items.map(v=>{
         fields.push(mixing.createField('f' + v.item, v.value, 'string', false, true))
      })
      fields.push(mixing.createField('task', 'Mã CV', 'number', false, true))
      fields.push(mixing.createField('action', '', 'string', false, true, '6%', 'select'))
      this.$store.commit('updateState', {name: 'pageitem', key: 'fields', data: fields})
      this.$store.commit('updateState', {name: 'pageitem', key: 'data', data: this.connection1.getbatchData[0].data})
      this.$store.commit('updateState', {name: 'pageitem', key: 'api', data: this.$copy(this.connection1.getbatchStatus[0])})
      this.$store.commit('updateState', {name: 'pageitem', key: 'origin_api', data: this.$copy(this.connection1.getbatchStatus[0])})
    },

    exportData() {
      var _export = new Export()
      let  dataTypes = {id: 'String', stock_date : 'String', stock_code: 'String', task: 'String'}
      let fields = ['id', 'stock_date', 'company__stock_code', 'task']
      this.items.map(v=>{
        dataTypes[v.value] = 'String'
        fields.push('f' + v.item)
      })
      _export.set(this.pageitem.filter, this.$route.query.report, dataTypes, fields)
      _export.exportfile()
    }
  }
}
</script>