<!-- eslint-disable -->
<template>
<div>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body pt20 pb20">
    <div class="columns is-multiline is-mobile pt0 pb0 mb0">
        <div class="column is-2">
            <div class="ml30" v-if="dataready===true">
            <nav class="level" v-if="readylist.filter(v=>v.record_type==='new').length>0">
            <div class="level-left">
            <div class="level-item">
            <p class="ml20">
              <span class="tag is-primary is-size-6 mr20"> {{readylist.filter(v=>v.record_type==='new').length}} </span> 
              <span class="has-text-primary"> Mới </span>
            </p>
            </div>
            </div>
            </nav>
            <nav class="level" v-if="readylist.filter(v=>v.record_type==='existed').length>0">
            <div class="level-left">
            <div class="level-item">
            <p class="ml20">
                <span class="tag is-dark is-size-6 mr20"> {{readylist.filter(v=>v.record_type==='existed').length}} </span> 
                <span> Đã tồn tại </span>
            </p>
            </div>
            </div>
            </nav>
            </div>

            <nav class="level" v-else-if="data.filter(v=>v.error===true).length>0">
            <div class="level-left">
            <div class="level-item">
            <p class="ml20">
              <span class="tag is-danger  is-size-6 mr20">  {{data.filter(v=>v.error===true).length}} </span> 
              <span class="has-text-danger"> Có lỗi </span>
            </p>
            </div>
            </div>
            </nav>
        </div>
        <div class="column is-1">
          <b-upload v-model="file" ref="upload">
            <a class="is-primary" :class="isLoading? 'is-loading' : ''">
              <span class="icon"> <i class="mdi mdi-cloud-upload-outline is-size-2 has-text-primary" /> </span>
            </a>
          </b-upload>

          <p class="mt-5"> 
            <b-tooltip label="Tải file template" position="is-bottom" type="is-dark">
              <a @click="downloadTemplate()"><span class="icon is-size-2 has-text-primary"> <i class="mdi mdi-arrow-collapse-down" /> </span></a>
          </b-tooltip>
          </p>
        </div>

        <div class="column is-6 is-paddingless">
            <div class="notification pt10 pb10 mb10 is-white" v-if="msgInfo.length>0">
            <button class="delete" @click="msgInfo=[]"></button>
            <article class="media pt3 pb3 is-marginless" v-for="(ele,key) in msgInfo" :key="key">
            <figure class="media-left">
                <i :class="classinfo.find(v=>v.type===ele.type).icon_class"> </i>
            </figure>
            <div class="media-content">
                <div class="content">
                <p :class="classinfo.find(v=>v.type==ele.type).text_class"> {{ele.message}} </p>
                </div>
            </div>
            </article>
            </div>
        </div>

        <div class="column is-3 pt0  is-centered" v-if="dataready===true">
            <div class="block mt10 mb20">
                <b-checkbox v-model="optionNew" class="has-text-primary" type='is-primary' v-if="optionNew!==undefined">
                    Thêm mới
                </b-checkbox>
                <b-checkbox v-model="optionUpdate" class="ml20 has-text-primary" type='is-primary' v-if="optionUpdate!==undefined">
                    Cập nhật
                </b-checkbox>
            </div>
            <p>
            <a class="tag is-medium is-primary" @click="importData()" v-if="!(optionNew===undefined && optionUpdate===undefined)"> Thực hiện </a>
            </p>
        </div>
        </div>
        <div class="mx-3 pt5" v-if="data.length>0"> 
          <tablefilter v-bind="{name: 'pageimport'}"> </tablefilter>
        </div>
    </div>
    </section>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'

import mixing from '@/assets/js/mixing.js'
import TableFilter from '@/components/TableFilter.vue'
import axios from 'axios'

Vue.component('tablefilter', TableFilter)

export default {
  props: ['task'],
  data () {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      data: [],
      fields: [],
      msgList: [],
      msgInfo: [],
      datafile: undefined,
      filename: undefined,
      dataready: undefined,
      importlist: [],
      readylist: [],
      optionNew: false,
      optionUpdate: false,
      action: '',
      path: '',
      file: undefined,
      isLoading: false,
      classinfo: [{type: 'success', icon_class: 'mdi mdi-check', text_class: 'has-text-dark'},
          {type: 'error', icon_class: 'mdi mdi-close has-text-danger', text_class: 'has-text-danger'},
          {type: 'warning', icon_class: 'mdi mdi-alert has-text-warning', text_class: 'has-text-warning'},
          {type: 'waiting', icon_class: 'mdi mdi-timer-sand has-text-primary', text_class: 'has-text-primary'},
        ]
      }
    },
    
    created() {
      this.getHeader()
      this.connectData()
      this.pageimport = {data: [], fields: [], filter: [], record: undefined, action: undefined, enableDelete: false,
        api: {full_data: true} , origin_api: {full_data: true}, reload: 0}
    },

    watch: {
      'connection1.getupdateStatus': function(newVal) {
        if(newVal) {  
          this.checkResult(this.connection1.getupdateRecord)
        } else if(newVal==false) {
          this.msgInfo.push({message: 'Đã có lỗi xảy ra. Import dữ liệu không thành công', type: 'error'})
        }
      },

      file: function(newVal) {
        if(newVal) this.uploadFile(newVal)
        if(this.$refs.upload? this.$refs.upload.$refs : false) this.$refs.upload.$refs.input.value = ''
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.state.api },
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },
      
      pageimport: {
        get: function() {return this.$store.state.pageimport},
        set: function(val) {this.$store.commit('updatePageImport', {pageimport: val})}
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
    },
    
    methods: {
      connectData() {
        let array = this.connection.checkDataReady(['companylist', 'accountlist'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) this.connection.getApi(list)
      },

      importData() {
        if(!(this.optionNew===true || this.optionUpdate===true)) {
          this.msgInfo.push({message: 'Vui lòng lựa chọn loại import ', type: 'warning'})
          return
        }
        
        if(this.importlist.length>0? this.importlist.find(v=>v.stock_date !== this.task.stock_date): false) {
          this.msgInfo.push({message: 'Ngày dữ liệu không khớp với ngày cần nhập.', type: 'error'})
          return
        }

        this.msgInfo.push({message: 'Đang import dữ liệu...Vui lòng chờ trong giây lát', type: 'waiting'})
        let data = []
        if(this.optionNew===true && this.optionUpdate===true) {
          data = this.importlist
          this.optionNew = undefined
          this.optionUpdate = undefined
        }
        else if(this.optionNew===true) {
          data = this.importlist.filter(v=>v.record_type==='new')
          this.optionNew = undefined
        }
        else if(this.optionUpdate===true) {
          data = this.importlist.filter(v=>v.record_type==='existed')
          this.optionUpdate = undefined
        }
        this.connection1.insert(this.connection1.requirelist.find(v=>v.url==='data/' + this.path).name, data)
      },

      checkResult(data) {
        data.forEach(element => {
          let found = this.data.find(v=>v.index===element.index)
          if(element.error===true) {
            found.error = true
            found.note = element.note.toString()
          }
        })

        let filter = this.data.filter(v=>v.error===true)
        if(filter.length>0) {
          this.msgInfo.push({message: 'Có lỗi xẩy ra. Import dữ liệu không thành công', type: 'error'})
          let field = mixing.createField('error', 'error', 'string', false, true)
          field.tooltip = {position: 'is-left', field: 'note', class: 'tag is-rounded is-danger'}
          this.fields.push(field)   
          this.$store.commit('updateState', {name: 'pageimport', key: 'fields', data: this.$copy(this.fields)})
        } 
        else {
          this.msgInfo.push({message: 'Import dữ liệu thành công', type: 'success'})
        }
      },

      verifyImportGeneral() {
        this.importlist = []
        this.data.map(v=>{
          let row = this.$copy(v)
          row.task = parseInt(this.$route.query.task)
          if(mixing.isDate(row.stock_date))
            row.stock_date = mixing.yyyymmdd(new Date(row.stock_date))
          else {
              v.error = true
              v.note = 'Stock_date phải có định dạng yyyy-mm-dd'
          }
          
          let found = this.companylist.find(x=>x.stock_code===v.company)
          //check error
          if(found) row.company = found.id
          else {
            v.error = true
            v.note = this.api.getvalue(this.api.find3var('inform','task','company-type-invalid'))
          }
          
          this.datafile.schema.fields.forEach(ele => {
            if(!(ele.name==='company' || ele.name==='stock_date' || v.error===true)) {
              if(this.$empty(v[ele.name])) row[ele.name] = null
              else if(!mixing.isNumber(v[ele.name])) {
                v.error = true
                v.note = 'Trường ' + ele.name + ' phải là số.'
              } else row[ele.name] = mixing.formatNumber(v[ele.name])
            }
          })
          this.importlist.push(row)
        })
      },

      verifyImportPriceLive() {
        console.log('this case')
        this.importlist = []
        this.data.map(v=>{
          let row = this.$copy(v)
          row.task = parseInt(this.$route.query.task)
          if(mixing.isDate(row.stock_date))
            row.stock_date = mixing.yyyymmdd(new Date(row.stock_date))
          else {
              v.error = true
              v.note = 'Stock_date phải có định dạng yyyy-mm-dd'
          }
          
          let found = this.companylist.find(x=>x.stock_code===v.company)
          //check error
          if(found) row.company = found.id
          else {
            v.error = true
            v.note = this.api.getvalue(this.api.find3var('inform','task','company-type-invalid'))
          }
          
          this.datafile.schema.fields.forEach(ele => {
            if(!(ele.name==='company' || ele.name==='stock_date' || ele.name==='time' || v.error===true)) {
              if(this.$empty(v[ele.name])) row[ele.name] = null
              else if(!mixing.isNumber(v[ele.name])) {
                v.error = true
                v.note = 'Trường ' + ele.name + ' phải là số.'
              } else row[ele.name] = mixing.formatNumber(v[ele.name])
            }
          })
          this.importlist.push(row)
        })
      },

      getHeader() {
        let found = this.api.find3var('inform','import','file-type')
        this.msgInfo.push({message: found.value, type: 'success'})
        this.action = 'import'
        let name = this.$route.query.report
        if(name==='TKGIA') {
          found = this.api.find3var('inform','import','stock-price-fields')
          this.path = 'Stock_Price/'
        }
        else if(name==='TKLENH') {
          found = this.api.find3var('inform','import','stock-order-fields')
          this.path = 'Stock_Order/'
        }
        else if(name==='DTNNLENH') {
          found = this.api.find3var('inform','import','foreign-order-fields')
          this.path = 'Foreign_Order/'
        }
        else if(name==='DTNNTT') {
          found = this.api.find3var('inform','import','foreign-deal-fields')
          this.path = 'Foreign_Deal/'
        }
        else if(name==='GIA') {
          found = this.api.find3var('inform','import','price-live-fields')
          this.path = 'Price_Live/'
        }
        else if(name==='CSPTKT') {
          found = this.api.find3var('inform','import','taindex-fields')
          this.path = 'Taindex/'
        }
        if(found) this.msgInfo.push({message: found.value, type: 'success'})
      },

      uploadFile(file) {
        this.readylist = []
        this.dataready = false
        this.optionNew = false
        this.optionUpdate = false

        let data = new FormData();
        data.append('name', file.name);
        data.append('file', file);
        //check file name is valid
        if (!(file.name.search('.xls') > 0 || file.name.search('.xlsx') > 0)) {
          this.msgInfo.push({message: this.api.find3var('inform', 'import', 'file-type-invalid').value, type: 'error'} )
          return
        }
        axios.post(this.connection.path + 'upload-file/', data=data)
        .then(response => {
            this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-ok').value, type: 'success'})
            this.filename = file.name
            this.getfile(this.filename)
          }
        )
        .catch(error => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-fail').value, type: 'error'})
        })
      },

      getfile(filename) {
        const url = this.connection.path + 'getfile/' + filename
        axios.get(url)
        .then(response => {
          this.datafile = JSON.parse(response.data)
          this.fillData()
        })
        .catch(error => {
          this.msgInfo.push({message: 'Lỗi. ' + error.toString(), type: 'error'})
        })
      },

      fillData() {
        //Check require fields is ok
        if( this.checkfieldlist() === false) return
        this.data = this.datafile.data
        this.fields = []
        this.datafile.schema.fields.forEach(ele => {
            let field = mixing.createField(ele.name, ele.name, 'string', false, true)
            if(field.name!=='index') this.fields.push(field)
        })
        this.$store.commit('updateState', {name: 'pageimport', key: 'data', data: this.$copy(this.data)})
        this.$store.commit('updateState', {name: 'pageimport', key: 'fields', data: this.$copy(this.fields)})
        this.verifyFromFrontend()
      },

      //check require field
      checkfieldlist() {
          var found = undefined
          let requireFields = []
          if(this.$route.query.report==='TKGIA')
            found = this.api.find3var('inform','import','stock-price-fields')
          else if(this.$route.query.report==='TKLENH')
            found = this.api.find3var('inform','import','stock-order-fields')
          else if(this.$route.query.report==='DTNNLENH')
            found = this.api.find3var('inform','import','foreign-order-fields')
          else if(this.$route.query.report==='DTNNTT')
            found = this.api.find3var('inform','import','foreign-deal-fields')
          else if(this.$route.query.report==='GIA')
            found = this.api.find3var('inform','import','price-live-fields')
          else if(this.$route.query.report==='CSPTKT')
            found = this.api.find3var('inform','import','taindex-fields')

          if(found !== undefined) this.requireFields = found.detail.split(',')
          let misslist = []

          //check field list is ok
          this.requireFields.forEach(element => {
              var field = this.datafile.schema.fields.find(v=>v.name===element)
              if(field===undefined) misslist.push(element)
          })
          if(misslist.length>0) {
              this.msgInfo.push({message: (this.api.find3var('inform','import','field-list-fail').value + ': ' + misslist.join(', ')), type: 'error'})
              return false
          } else {
              this.msgInfo.push({message: this.api.find3var('inform','import','field-list-ok').value, type: 'success'})
              return true
          }
      },

      verifyFromFrontend() {
        let report = ['TKGIA', 'TKLENH', 'DTNNLENH', 'DTNNTT', 'CSPTKT'].find(v=>v===this.$route.query.report)
        report? this.verifyImportGeneral() : report = this.$route.query.report
        if(report==='GIA') this.verifyImportPriceLive()

        let filter = this.data.filter(v=>v.error===true)
        if(filter.length>0) {
          this.msgInfo.push({message: 'Dữ liệu có lỗi', type: 'error'})
          let field = mixing.createField('error', 'error', 'string', false, true)
          field.tooltip = {position: 'is-left', field: 'note', class: 'tag is-rounded is-danger'}
          this.fields.push(field)
          this.$store.commit('updateState', {name: 'pageimport', key: 'data', data: this.$copy(this.data)})
          this.$store.commit('updateState', {name: 'pageimport', key: 'fields', data: this.$copy(this.fields)})
          return  
        }

        this.msgInfo.push({message: 'Đang kiểm tra tính hợp lệ của dữ liệu...Vui lòng chờ trong giây lát', type: 'waiting'})
        const url = this.connection.path + 'validate-import/' + this.path
        let params = {type: 'serializer', filter: {}, action: this.action}
        axios.post(url, this.importlist, {params: params})
        .then(response => {
            this.verifyFromBackend(response.data)
        })
        .catch(error => {
            this.msgInfo.push({message: 'Đã có lỗi xẩy ra', type: 'error'})
        })
      },

      verifyFromBackend(data) {
        data.forEach(element => {
          let found = this.data.find(v=>v.index===element.index)
          found.record_type = element.record_type
          if(element.error===true) {
            found.error = true
            found.note = JSON.stringify(element.note)
          }
        })

        let filter = this.data.filter(v=>v.error===true)
        if(filter.length>0) {
          this.msgInfo.push({message: 'Dữ liệu có lỗi', type: 'error'})
          let field = mixing.createField('error', 'error', 'string', false, true)
          field.tooltip = {position: 'is-left', field: 'note', class: 'tag is-rounded is-danger'}
          this.fields.push(field)
          this.$store.commit('updateState', {name: 'pageimport', key: 'fields', data: this.fields})
          this.$store.commit('updateState', {name: 'pageimport', key: 'data', data: this.$copy(this.data)})
        }
        else {
          let field = mixing.createField('record_type', 'record_type', 'string', false, true)
              field.style = {list: [{value: 'new', class: 'button is-small is-primary is-outlined'},
                {value: 'existed', class: 'button is-small is-dark is-outlined'},
              ], condition: 'record_type', click: false}

          this.fields.push(field)
          filter = data.filter(v=>v.record_type==='new')
          filter.map(v=>v.status = this.api.find3var('list', 'task-status', 'not-yet-entered').id)
          this.importlist = data
          this.readylist = data

          this.$store.commit('updateState', {name: 'pageimport', key: 'data', data: this.$copy(this.data)})
          this.$store.commit('updateState', {name: 'pageimport', key: 'fields', data: this.$copy(this.fields)})
          this.dataready = true
          this.msgInfo.push({message: 'Kiểm tra dữ liệu hoàn thành. Hãy chọn kiểu import dữ liệu', type: 'success'})
        }
      },

      downloadTemplate() {
        if(this.$route.query.report==='TKGIA')
          mixing.download(this.connection.path + 'download-file/price_template.xlsx')
        else if(this.$route.query.report==='TKLENH')
          mixing.download(this.connection.path + 'download-file/order_template.xlsx')
        else if(this.$route.query.report==='DTNNLENH')
          mixing.download(this.connection.path + 'download-file/foreign_order_template.xlsx')
        else if(this.$route.query.report==='DTNNTT')
          mixing.download(this.connection.path + 'download-file/foreign_deal_template.xlsx')
        else if(this.$route.query.report==='GIA')
          mixing.download(this.connection.path + 'download-file/price_live_template.xlsx')
        else if(this.$route.query.report==='CSPTKT')
          mixing.download(this.connection.path + 'download-file/taindex_template.xlsx')
      },

      getFile() {
        return this.filename
      }
  }
}
</script>