<!-- eslint-disable -->
<template>
<div>
	<topmenu v-bind="{type: 'tophead', tophead: 'Danh sách chỉ tiêu báo cáo', enableDownload: true}"></topmenu>
        <div class="pt60"/>

    <section class="hero is-paddingless is-marginless" v-if="pageitem.record===undefined">
    <div class="hero-body pt5 pb15 pl0 pr0">
        <div class="mx-3"> 
            <tablefilter v-bind="{name: 'pageitem'}" > </tablefilter>
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
import Vue from 'vue'
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'

import mixing from '@/assets/js/mixing.js'
import TableFilter from '@/components/TableFilter.vue'
import Export from '@/assets/js/export.js'

Vue.component('topmenu', TopMenu)
Vue.component('Footer', Footer)
Vue.component('tablefilter', TableFilter)

export default {
	data () {
    return {
      connection: this.$connection(),
      data: [],
      fields: [],
    }
  },

  head() {
    return {
      title: 'Danh sách chỉ tiêu báo cáo tài chính'
    }
  },
    
    created() {
        this.fields.push(mixing.createField('id', 'Id', 'number', false, true))
        this.fields.push(mixing.createField('company_type', 'Loại DN', 'string', false, true))
        this.fields.push(mixing.createField('report_name', 'Tên báo cáo', 'string', false, true))
        this.fields.push(mixing.createField('item', 'Chỉ tiêu', 'string', false, true))
        this.fields.push(mixing.createField('value', 'Giá trị', 'string', false, true))
        this.fields.push(mixing.createField('formula', 'Công thức', 'string', false, true))          
        this.fields.push(mixing.createField('level', 'Cấp độ', 'string', false, true))
        this.fields.push(mixing.createField('index', 'Thứ tự', 'number', false, true))
        this.fields.push(mixing.createField('parent', 'Cấp trên', 'number', false, true))
        this.fields.push(mixing.createField('readonly', 'Trường mô tả', 'number', false, true))
        this.fields.push(mixing.createField('text', 'Trường dạng text', 'number', false, true))
        this.fields.push(mixing.createField('enable', 'Hiệu lực', 'number', false, true))
        this.fields.push(mixing.createField('action', '', 'string', false, true, '6%', 'select'))
        this.pageitem = {data: [], fields: this.fields, filter: [], record: undefined, action: undefined, enableDelete: true,
        api: {} , origin_api: {}, reload: 0}

        let found= this.connection.requirelist.find(v=>v.name==='reportitem')  
        this.connection.getApi([found])
    },

    watch: {
     'connection.getdataReady' : function(newVal) {
        if(newVal==='success') {
          let data = this.connection.getbatchData[0].data
          this.$store.commit('updateState', {name: 'pageitem', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
          this.$store.commit('updateState', {name: 'pageitem', key: 'data', data: data})
          if(Object.keys(this.pageitem.origin_api).length===0) {
            this.$store.commit('updateState', {name: 'pageitem', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
          }
        }
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
    },
    
    methods: {
      exportData() {
        var _export = new Export()
        let  dataTypes = {
            id: 'String', 
            company_type : 'String',
            report_name: 'String',
            item: 'String',
            value: 'String',
            value1: 'String',
            formula: 'String',
            level: 'String',
            index: 'String',
            parent: 'String',
            readonly: 'String',
            text: 'String'
        }

        let fields = ['id', 'company_type', 'report_name', 'item', 'value', 'value1', 'formula', 'level', 'index', 'parent', 'readonly', 'text']
        _export.set(this.pageitem.filter, 'report-item', dataTypes, fields)
        _export.exportfile()
      }
    }
}
</script>