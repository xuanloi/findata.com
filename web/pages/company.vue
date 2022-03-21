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
            tophead: 'Danh sách công ty',
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
        fields.push(fields.push(mixing.createField('stock_code', 'Mã CK', 'string', false, true)))
        fields.push(fields.push(mixing.createField("type__code", 'Loại DN', 'string', false, true)))
        fields.push(fields.push(mixing.createField('name', 'Tên', 'string', false, true)))
        fields.push(fields.push(mixing.createField('short_name', 'Tên viết tắt', 'string', false, true)))
        fields.push(fields.push(mixing.createField('address', 'Địa chỉ', 'string', false, true)))
        fields.push(fields.push(mixing.createField('tax_code', 'MST', 'string', false, true)))
        fields.push(fields.push(mixing.createField('listed', 'Niêm yết', 'string', false, true)))
        fields.push(fields.push(mixing.createField('listed_on', 'Sàn CK', 'string', false, true)))
        fields.push(fields.push(mixing.createField('factor', 'Hệ số', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level1_name', 'level1_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level1_code', 'level1_code', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level2_name', 'level2_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level2_code', 'level2_code', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level3_name', 'level3_name', 'string', false, true)))
        fields.push(fields.push(mixing.createField('industry__level3_code', 'level3_code', 'string', false, true)))    
        this.pagecompany = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: false,
        api: {name: 'company', full_data: true} , origin_api: {name: 'company', full_data: true}, reload: 0}
        this.connectData()
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
    },

    methods: {
        connectData() {
            let array = this.connection.checkDataReady(['companylist'])
            let list = array.filter(v=>v.ready===false)
            if(list.length>0) this.connection.getApi(list)
            else this.fillData()
        },

        fillData() {
            let data = JSON.parse(JSON.stringify(this.companylist))
            this.$store.commit('updateState', {name: 'pagecompany', key: 'data', data: data})
        },

        exportData() {
            var _export = new Export()

            let  dataTypes = {
                id: 'String', 
                stock_code : 'String',
                type: 'String',
                name: 'String',
                short_name: 'String',
                address: 'String',
                tax_code: 'String',
                listed: 'String',
                listed_on: 'String',
                factor: 'String',
                level1_name: 'String',
                level1_code: 'String',
                level2_name: 'String',
                level2_code: 'String',
                level3_name: 'String',
                level3_code: 'String',
            }
            let fields = ['id', 'stock_code', 'type__code', 'name', 'short_name', 'address', 'tax_code', 'listed', 'listed_on', 'factor', 'industry__level1_name', 'industry__level1_code','industry__level2_name', 'industry__level2_code', 'industry__level3_name', 'industry__level3_code']
            _export.set(this.pagecompany.filter===undefined? this.pagecompany.data : this.pagecompany.filter, 'company-list', dataTypes, fields)
            _export.exportfile()
        }
    }
}
</script>