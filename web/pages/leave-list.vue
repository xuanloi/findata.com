<!-- eslint-disable -->
<template>
<div>
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <div class="pt60"/>

    <section class="hero is-paddingless is-marginless">
    <div class="hero-body pt-3">
        <div class="mx-3"> 
            <tablefilter v-bind="{name: 'pageleave'}" > </tablefilter>
        </div>
        </div>
    </section>

    <Footer> </Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'

import mixing from "@/assets/js/mixing.js";
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'
import TableFilter from '@/components/TableFilter.vue'
import Export from '@/assets/js/export.js'

Vue.component('topmenu', TopMenu)
Vue.component('Footer', Footer)
Vue.component('tablefilter', TableFilter)

export default {
    data() {
        return {
            tophead: 'Danh sách nghỉ phép',
            connection: this.$connection(),
            fields: []
        }
    },

    head() {
      return {
        title: 'Danh sách nghỉ phép'
      }
    },

    created() {
        let fields = []
        fields.push(mixing.createField('id', 'Id', 'number', false, true))
        fields.push(mixing.createField('name', 'Tên', 'string', false, true))
        fields.push(mixing.createField('start_date', 'Từ ngày', 'string', false, true))
        fields.push(mixing.createField('end_date', 'Đến ngày', 'string', false, true))
        fields.push(mixing.createField('type', 'Loại nghỉ phép', 'string', false, true))
        fields.push(mixing.createField('reason', 'Lý do', 'string', false, true))
        fields.push(mixing.createField('detail', 'Chi tiết', 'string', false, true))          
        fields.push(mixing.createField('status', 'Trạng thái', 'string', false, true))
        fields.push(mixing.createField('action', '', 'string', false, true, '8%', 'select,edit'))
        this.fields = fields
        this.pageleave = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true,
        api: {name: 'leave', full_data: true} , origin_api: {name: 'leave', full_data: true}, reload: 0}

        let array = this.connection.checkDataReady(['leavelist', 'accountlist'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) this.connection.getApi(list)
        else this.fillData()
    },

    watch: {
        'connection.getdataReady' : function(newVal) {
          if(newVal==='success') this.fillData()
          else if (newVal==='error') this.$router.push({path: '/error'})
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

        leavelist: {
            get: function() {return this.$store.state.leavelist},
            set: function(val) {this.$store.commit("updateLeaveList", { leavelist: val })}
        },

        login: {
            get: function() {return this.$store.state.login},
            set: function(val) {this.$store.commit('updateLogin', {login: val})}
        },

        pageleave: {
            get: function() {return this.$store.state.pageleave},
            set: function(val) {this.$store.commit('updatePageLeave', {pageleave: val})}
        },

        accountlist: {
            get: function() {return this.$store.state.accountlist},
            set: function(val) {this.$store.commit('updateAccountList', {accountlist: val})}
        },

        menuaction: {
          get: function() {return this.$store.state.menuaction},
          set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
        },
    },

    methods: {
        fillData() {
          let data = this.$copy(this.leavelist)
          let code = this.login.type.code

          if(code==='ctv' || code==='staff') data = data.filter(v=>v.account===this.login.id)
          data.forEach(element => {
              element.name = this.accountlist.find(v=>v.id===element.account).name
              element.type = this.api.getbyid(element.type).value
              element.status = this.api.getbyid(element.status).value
          })
          this.$store.commit('updateState', {name: 'pageleave', key: 'data', data: data})  
        },

        exportData() {
          var _export = new Export()
          let dataTypes = {}
          let fields = []

          this.fields.forEach(element => {
              dataTypes[element.name] = 'String'
              fields.push(element.name)
          })

          _export.set(this.pageleave.filter===undefined? this.pageleave.data : this.pageleave.filter, 'salary-list', dataTypes, fields)
          _export.exportfile()
        }
    }
}
</script>