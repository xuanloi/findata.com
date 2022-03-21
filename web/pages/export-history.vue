<!-- eslint-disable -->
<template>
<div>
<topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body mt30 pb15">
        <div class="columns">
        <div class="column is-8 is-offset-1">
            <div class="mx-3"> 
                <tablefilter v-bind="{name: 'pagetask'}" > </tablefilter>
            </div>
        </div>
        <div class="column is-3">
             <button class="button is-primary is-outlined mt30" @click="download()">Tải dữ liệu mới nhất</button>
        </div>
        </div>
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
            errList: [],
            tophead: 'Lịch sử xuất dữ liệu',
        }
    },

    head() {
      return {
        title: 'Lịch sử xuất dữ liệu'
      }
    },
    
    created() {
        let fields = []
        fields.push(mixing.createField('id', 'Id', 'number', false, true))
        let field = mixing.createField('type', 'Loại', 'string', false, true)
        fields.push(field)

        fields.push(mixing.createField('etl_date', 'Ngày xuất', 'string', false, true))
        fields.push(mixing.createField('start_time', 'Bắt đầu', 'string', false, true))
        fields.push(mixing.createField('end_time', 'Kết thúc', 'string', false, true))

        field = mixing.createField('status_name', 'Trạng thái', 'string', false, true)
        field.style = {list: [{value: true, class: 'tag is-small is-primary'},
                      {value: false, class: 'tag is-small is-danger'}], condition: 'status', click: false}
        fields.push(field)

        this.fields = fields
        this.pagetask = {data: [], fields: this.fields, filter: [], record: undefined, action: undefined, enableDelete: true,
        api: {} , origin_api: {}, reload: 0}
        let found = {name: 'history', url: 'data/Etl_Log/', params: {sort:'-id'}}
        this.connection.getApi([found])
    },

    watch: {
       'connection.getdataReady' : function(newVal) {
          if(newVal==='success') this.fillData()
          else if(newVal==='error') this.$router.push({ name: 'error'})
        },

        menuaction : function(newVal) {
            if(newVal? newVal.action==='download': false) this.exportData()
        },

       'pagetask.reload': function(newVal, oldVal) {
            if(oldVal===undefined) return
            let found = newVal===0? this.$copy(this.pagetask.origin_api) : this.$copy(this.pagetask.api)
            if(Object.keys(found).length>0) this.connection.getApi([found])
        },
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

        menuaction: {
            get: function() {return this.$store.state.menuaction},
            set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
        },
    },
    
    methods: {
        fillData() {
            this.data = this.connection.getbatchData[0].data
            this.data.forEach(v => {
                v.status_name = v.status===true? 'Thành công' : 'Thất bại'
                v.start_time = v.start_time? mixing.yyyymmddhhmm(new Date(v.start_time)) : undefined
                v.end_time = v.end_time? mixing.yyyymmddhhmm(new Date(v.end_time)) : undefined
            })
            this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
            this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: this.data})
            if(Object.keys(this.pagetask.origin_api).length===0) {
                this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
            }
        },

        download() {
            mixing.download(this.connection.path + 'download-file/' + 'DataEntry.mdb/')
        },

        exportData() {
            var _export = new Export()

            let  dataTypes = {
                id: 'String', 
                type: 'String',
                etl_date : 'String',
                start_time: 'String',
                end_time: 'String',
                status: 'String',
            }

            let fields = ['id', 'type', 'etl_date', 'start_time', 'end_time', 'status']
            _export.set(this.pagetask.filter, 'export-history', dataTypes, fields)
            _export.exportfile()
        }
    }
}
</script>