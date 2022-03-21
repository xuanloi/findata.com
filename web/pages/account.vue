<!-- eslint-disable -->
<template>
<div>
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}"></topmenu>
    <div class="pt60"/>

    <section class="hero is-paddingless is-marginless">
    <div class="hero-body pt10 pb15 pl0 pr0">
        <div class="mx-3 pl0 pr0"> 
            <tablefilter v-bind="{name: 'pageaccount'}" > </tablefilter>
        </div>
        </div>
    </section>
    <Footer></Footer>
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
            tophead: 'Danh sách tài khoản người dùng',
            data: [],
            fields: [],
            connection: this.$connection()
        }
    },

    head() {
      return {
        title: 'Danh sách người sử dụng'
      }
    },

    created() {
        let fields = []
        fields.push(mixing.createField('id', 'Id', 'number', false, true))
        fields.push(mixing.createField('name', 'Họ và tên', 'string', false, true))
        fields.push(mixing.createField('dob', 'Ngày sinh', 'string', false, true))
        fields.push(mixing.createField('identity', 'CMT/Hộ chiếu', 'string', false, true))
        fields.push(mixing.createField('sex', 'Giới tính', 'string', false, true))
        fields.push(mixing.createField('phone', 'Điện thoại', 'string', false, true))
        fields.push(mixing.createField('email', 'Email', 'string', false, true))
        fields.push(mixing.createField("position", 'Vị trí', 'string', false, true))
        fields.push(mixing.createField('team_name', 'Nhóm', 'string', false, true))                
        field = mixing.createField('status_name', 'Trạng thái', 'string', false, true)
        field.style = {list: [{value: 'no', class: 'tag is-small is-danger is-outlined'},
                      {value: 'yes', class: 'tag is-small is-primary is-outlined'},
                      {value: 'wait', class: 'tag is-small is-link is-outlined'},
                      {value: 'amend', class: 'tag is-small is-warning is-outlined'}], condition: 'status_code', click: false}
        fields.push(field)
        fields.push(mixing.createField('last_login', 'Last login', 'string', false, true))
        fields.push(mixing.createField('enable', 'Hoạt động', 'string', false, true))
        let field = mixing.createField('action', '', 'string', false, true, '6%', 'open')
        let type = this.login.type
        if(type.code==='admin' || type.code==='manager')
            field = mixing.createField('action', '', 'string', false, true, '6%', 'open,insert')
        fields.push(field)
        
        this.fields = fields
        this.pageaccount = {data: [], fields: this.fields, filter: [], record: undefined, action: undefined, enableDelete: false,
        api: {name: 'account', full_data: true} , origin_api: {name: 'account', full_data: true}, reload: 0}
        this.connectData()
    },

    watch: {
        'connection.getdataReady' : function(newVal) {
          if(newVal==='success') this.fillData()
        },

        'pageaccount.record' : function(newVal) {
            if(newVal===undefined) return
            if(this.pageaccount.action==='insert') this.$router.push({ path: '/account-register'})
            else this.$router.push({ path: '/profile', query: {id: newVal.id}})
            this.$store.commit('updateState', {name: 'pageaccount', key: 'record', data: undefined})
        },

        menuaction : function(newVal) {
            if(newVal? newVal.action==='download': false) this.exportData()
        },

        accountlist: function(oldVal, newVal) {
            if(oldVal===undefined) return
            this.fillData()
        }
    },

    computed: {
        api: {
            get: function() {return this.$store.state.api},
            set: function(val) {this.$store.commit('updateApi', {api: val})}
        },

        pageaccount: {
            get: function() {return this.$store.state.pageaccount},
            set: function(val) {this.$store.commit('updatePageAccount', {pageaccount: val})}
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
            let array = this.connection.checkDataReady(['accountlist'])
            let list = array.filter(v=>v.ready===false)
            if(list.length>0) this.connection.getApi(list)
            else this.fillData()
        },

        fillData() {
            this.data = JSON.parse(JSON.stringify(this.accountlist))
            if(this.login.type.code==='teamlead') {
                this.data = this.data.filter(v=>v.team===this.login.team.id)
            }

            this.data.sort(function(a,b){return new Date(b.create_time) - new Date(a.create_time)})
            this.data.forEach(element => {
                element.position = this.$empty(element.type)===false? this.api.getbyid(element.type).value : undefined
                element.team_name = this.$empty(element.team)===false? this.api.getbyid(element.team).value : undefined
                element.status_code = this.$empty(element.approve)===false? this.api.getbyid(element.approve).code : undefined
                element.status_name =  this.$empty(element.approve)===false? this.api.getbyid(element.approve).value : undefined
                element.last_login = this.$empty(element.last_login)===false? element.last_login.substring(0,16).replace('T', ' ') : undefined
            })
            this.$store.commit('updateState', {name: 'pageaccount', key: 'data', data: this.data})
            this.$store.commit('updateState', {name: 'pageaccount', key: 'filter', data: this.data})
        },

        exportData() {
            var _export = new Export()
            let dataTypes = {}
            let fields = []

            this.fields.forEach(element => {
                dataTypes[element.name] = 'String'
                fields.push(element.name)
            })
            dataTypes['address'] = 'String'
            fields.push('address')

            _export.set(this.pageaccount.filter, 'account-list', dataTypes, fields)
            _export.exportfile()
        }        
    }
}
</script>