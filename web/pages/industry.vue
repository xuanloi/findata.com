<!-- eslint-disable -->
<template>
<div>
    <TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}"></TopMenu>
    <div class="pt60"/>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body pt5 pb15 pl0 pr0">
        <div class="mx-3"> 
            <TableFilter v-bind="{name: 'pagecompany'}" > </TableFilter>
        </div>
        </div>
    </section>
  <Footer></Footer>
</div>
</template>

<script>
/* eslint-disable */

import mixing from "@/assets/js/mixing.js";
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'
import TableFilter from '@/components/TableFilter.vue'
import Export from '@/assets/js/export.js'

export default {
    components: {
        TopMenu,
        Footer,
        TableFilter
    },

    data() {
        return {
            tophead: 'Danh sách mã ngành',
            connection: this.$connection()
        }
    },

    head() {
      return {
        title: this.tophead
      }
    },

    created() {
        let fields = []
        fields.push(fields.push(mixing.createField('id', 'Id', 'number', false, true)))
        fields.push(fields.push(mixing.createField('level1_name', 'level1_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField("level1_code", 'level1_code', 'string', false, true)))
        fields.push(fields.push(mixing.createField('level2_name', 'level2_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField('level2_code', 'level2_code', 'string', false, true)))
        fields.push(fields.push(mixing.createField('level3_name', 'level3_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField('level3_code', 'level3_code', 'string', false, true)))
        this.pagecompany = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: false,
        api: {name: 'industry', full_data: true} , origin_api: {name: 'industry', full_data: true}, reload: 0}
        
        //connect data
        let array = this.connection.checkDataReady(['industry'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) this.connection.getApi(list)
        else this.fillData()
    },

    watch: {
       'connection.getdataReady' : function(newVal) {
          if(newVal==='success') this.fillData()
        },

        menuaction : function(newVal) {
            if(newVal? newVal.action==='download': false) this.exportData()
        }
    },

    computed: {
        api: {
            get: function() {return this.$store.state.api},
            set: function(val) {this.$store.commit('updateApi', {api: val})}
        },

        pagecompany: {
          get: function() {return this.$store.state.pagecompany},
          set: function(val) {this.$store.commit('updatePageCompany', {pagecompany: val})}
        },
        
        companylist: {
            get: function() {return this.$store.state.companylist},
            set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
        },

        menuaction: {
            get: function() {return this.$store.state.menuaction},
            set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
        },

        industry: {
            get: function() {return this.$store.state.industry},
            set: function(val) {this.$store.commit('updateIndustry', {industry: val})}
        },
    },

    methods: {
        fillData() {
            let data = this.$copy(this.industry)
            this.$store.commit('updateState', {name: 'pagecompany', key: 'data', data: data})
        },

        exportData() {
            var _export = new Export()
            let  dataTypes = {
                id: 'String', 
                level1_name : 'String',
                level1_code: 'String',
                level2_name: 'String',
                level2_code: 'String',
                level3_name: 'String',
                level3_code: 'String'
            }
            let fields = ['id', 'level1_name', 'level1_code', 'level2_name', 'level2_code', 'level3_name', 'level3_code']
            _export.set(this.pagecompany.filter===undefined? this.pagecompany.data : this.pagecompany.filter, 'industry-list', dataTypes, fields)
            _export.exportfile()
        }
    }
}
</script>