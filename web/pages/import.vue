<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: this.tophead}"></TopMenu>
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body mt30 pb40">
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
        <div class="column is-1 is-paddingless has-text-centered">
            <div class="control tooltip is-tooltip-left mt10" data-tooltip="Tải lên file excel">
            <div class="file has-name is-right" ref='file'>
            <label class="file-label">
                <input class="file-input" type="file" id="fileUpload" v-on:change="uploadFile()">
                <a class="button is-white">
                  <i class="mdi mdi-cloud-upload-outline is-size-2 has-text-primary"></i>
                </a>
            </label>
            </div>
            </div>
            <p class="mt-5"> 
              <b-tooltip label="Tải file template" position="is-bottom" type="is-dark" class="ml-6">
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
          <TableFilter v-bind="{name: 'pageimport'}" > </TableFilter>
        </div>
    </div>
    </section>
    <Footer></Footer>
</div>
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import axios from 'axios'
import "bulma-extensions/bulma-steps/dist/css/bulma-steps.min.css"

export default {
  data () {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      data: [],
      fields: [],
      msgList: [],
      tophead: '',
      isLoading: false,
      msgInfo: [],
      datafile: undefined,
      filename: '',
      dataready: undefined,
      importlist: [],
      readylist: [],
      optionNew: false,
      optionUpdate: false,
      action: '',
      path: '',
      classinfo: [{type: 'success', icon_class: 'mdi mdi-check', text_class: 'has-text-dark'},
          {type: 'error', icon_class: 'mdi mdi-close has-text-danger', text_class: 'has-text-danger'},
          {type: 'warning', icon_class: 'mdi mdi-alert has-text-warning', text_class: 'has-text-warning'},
          {type: 'waiting', icon_class: 'mdi mdi-timer-sand has-text-primary', text_class: 'has-text-primary'},
        ]
      }
    },

    head() {
      return {
        title: 'Nhập dữ liệu vào hệ thống'
      }
    },
    
    created() {
      this.getHeader()
      this.connectData()
      this.pageimport = {data: [], fields: [], filter: [], record: undefined, action: undefined, enableDelete: false,
        api: {full_data: true} , origin_api: {full_data: true}, reload: 0}},

    watch: {
      'connection.getdataReady' : function(newVal) {
        if(newVal==='success') this.isLoading = false
        else if(newVal==='error') this.$router.push({ name: 'error'})
      },

      'connection1.getupdateStatus': function(newVal) {
        if(newVal) {  
          this.checkResult(this.connection1.getupdateRecord)
        } else if(newVal==false) {
          this.msgInfo.push({message: 'Đã có lỗi xảy ra. Import dữ liệu không thành công', type: 'error'})
        }
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
      industry: {
        get: function() {return this.$store.state.industry},
        set: function(val) {this.$store.commit('updateIndustry', {industry: val})}
      }
    },
    
    methods: {
      connectData() {
        let array = this.connection.checkDataReady(['companylist', 'accountlist', 'industry'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) {
          this.isLoading = true
          this.connection.getApi(list)
        }
      },

      importData() {
        if(!(this.optionNew===true || this.optionUpdate===true)) {
          this.msgInfo.push({message: 'vui lòng lựa chọn loại import ', type: 'warning'})
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
        if(this.$route.query.type==='delete-task') {
          this.connection1.delete(this.connection1.requirelist.find(v=>v.url==='data/' + this.path).name, data)
        } else {
          this.connection1.insert(this.connection1.requirelist.find(v=>v.url==='data/' + this.path).name, data)
        }
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

      verifyImportCompany() {
        this.importlist = []
        this.data.forEach(ele => {
          let obj = this.$copy(ele)
          var type = this.api.find3var('list','company-type', ele.type)
          //check error
          if(type === undefined) {
              ele.error = true
              ele.note = this.api.getvalue(this.api.find3var('inform','task','company-type-invalid'))
          } else obj.type = type.id

          if(mixing.isNumber(ele.factor)===false) {
              ele.error = true
              ele.note = this.api.getvalue(this.api.find3var('inform','task','factor-invalid'))
          } else if(!this.$empty(ele.level3_code)) {
            let found = this.industry.find(v=>v.level3_code===ele.level3_code)
            if(!found) {
              ele.error = true
              ele.note = this.api.getvalue(this.api.find3var('inform','task','industry-invalid'))
            } else obj.industry = found.id
          }
          this.importlist.push(obj)
        })
      },

      verifyBatchApprove() {
        this.importlist = []
        this.data.forEach(ele => {
          //check approve is valid
          let obj = {index: ele.index, id: ele.id}
          if (!(ele.approve === 'yes' || ele.approve === '1' || ele.approve.toLowerCase() === 'true')) {
            ele.error = true
            ele.note = this.api.getvalue(this.api.find3var('inform','task','readonly-invalid'))
          } 
          else {
            obj.status = this.$route.query.status==='waiting-approve'? this.api.find3var('list', 'task-status', 'waiting-approve-2').id : this.api.find3var('list', 'task-status', 'approved').id
          }
          this.importlist.push(obj)
        })
        this.optionNew = undefined
      },

      verifyImportTask() {
        this.importlist = []
        this.data.forEach(ele => {
            let obj = this.$copy(ele)
            let found = this.companylist.find(v=>v.stock_code===ele.company)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Mã chứng khoán không tồn tại'
            } else obj.company = found.id

            found = this.api.find3var('list', 'report-period', ele.report_period)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Kỳ báo cáo không hợp lệ'
            } else obj.report_period = found.id

            if(this.$empty(ele.year)===true || mixing.isNumber(ele.year)===false) {
                ele.error = true
                ele.note = 'Năm không hợp lệ'
            }

            found = this.api.find3var('list','report-type', ele.report_type)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Loại báo cáo không hợp lệ'
            } else obj.report_type = found.id

            found = this.api.find3var('list', 'report-name', ele.report_name)
              if(found===undefined) {
                  ele.error = true
                  ele.note = 'Tên báo cáo không hợp lệ'
              } else {
                  obj.report_name = found.id
                  if(obj.company_type!==undefined) {
                      let name = ele.report_name==='LCTT-TT' || ele.report_name==='LCTT-GT'? 'LCTT' : ele.report_name
                      obj.unit_price = this.api.find3var('unit-price', obj.company_type, name).value
                      obj.into_money = obj.company_factor *  obj.unit_price
                  }
              }

            found = this.accountlist.find(v=>v.email===ele.assigner)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Người giao việc không tồn tại'
            } else obj.assigner = found.id

            found = this.accountlist.find(v=>v.email===ele.recipient)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Tên nhận việc không tồn tại'
            } else obj.recipient = found.id

            if(this.$empty(ele.priority)===true || mixing.isNumber(ele.priority)===false) {
              ele.error = true
              ele.note = 'Giá trị ưu tiên không hợp lệ'
            }
            this.importlist.push(obj)
        })
      },

      verifyImportStockData() {
        this.importlist = []
        this.data.forEach(ele => {
            let obj = this.$copy(ele)
            if(mixing.isDate(obj.stock_date))
              obj.stock_date = mixing.yyyymmdd(new Date(obj.stock_date))
            else {
              ele.error = true
              ele.note = 'Stock_date phải có định dạng yyyy-mm-dd'
            }
            let found = this.api.find3var('list', 'stock-report-name', ele.report_name)
            if(found===undefined) {
              ele.error = true
              ele.note = 'Tên báo cáo không hợp lệ'
            } else {
              obj.report_name = found.id
              obj.unit_price = this.api.find3var('unit-price', 'stock', ele.report_name).value
              obj.into_money = obj.unit_price
            }
            
            found = this.accountlist.find(v=>v.email===ele.assigner)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Người giao việc không tồn tại'
            } else obj.assigner = found.id

            found = this.accountlist.find(v=>v.email===ele.recipient)
            if(found===undefined) {
                ele.error = true
                ele.note = 'Tên nhận việc không tồn tại'
            } else obj.recipient = found.id

            if(this.$empty(ele.priority)===true || mixing.isNumber(ele.priority)===false) {
              ele.error = true
              ele.note = 'Giá trị ưu tiên không hợp lệ'
            }
            this.importlist.push(obj)
        })
      },

      verifyDeleteTask() {
        this.optionNew = undefined
        this.importlist = this.data
      },

      verifyImportParameter() {
        this.importlist = this.data
      },

      verifyImportItem() {
        this.importlist = []
        this.data.forEach(ele => {
          let obj = JSON.parse(JSON.stringify(ele))
          var company_type_id = this.api.find3var('list','company-type', ele.company_type)
          var report_name_id = this.api.find3var('list','report-name', ele.report_name)
          if(!report_name_id) report_name_id = this.api.find3var('list','stock-report-name', ele.report_name)

          //check error
          if(company_type_id === undefined) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','company-type-invalid'))
          }

          //check error
          if(report_name_id === undefined) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','report-name-invalid'))
          }

          if(obj.item.length < 5) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','item-length'))
          }

          if(obj.value === '') {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','value-invalid'))
          }

          if(obj.value1 === '') {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','value1-invalid'))
          }

          if(mixing.isNumber(obj.level)===false) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','number-invalid'))
          }
          
          if(mixing.isNumber(obj.index) === false) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','number-invalid'))
          }

          //check readonly is valid
          if (!(obj.readonly === 'yes' || obj.readonly === 'no' || obj.readonly === '1' ||obj.readonly === '0'
          || obj.readonly.toLowerCase() === 'true' || obj.readonly.toLowerCase() === 'false')) {
              obj.error = true
              obj.note = this.api.getvalue(this.api.find3var('inform','task','readonly-invalid'))
          }
          this.importlist.push(obj)
        })
      },

      verifyIndustry() {
        this.importlist = this.data
      },

      getHeader() {
        let found = this.api.find3var('inform','import','file-type')
        this.msgInfo.push({message: found.value, type: 'success'})
        this.action = 'import'

        let name = this.$route.query.type
        if(name==='task') {
            this.tophead = 'Giao việc nhập dữ liệu Báo cáo tài chính'     
            found = this.api.find3var('inform','import','task-fields')
            this.path = 'Task/'
        }
        else if(name==='delete-task') {
            this.tophead = 'Xóa việc đã giao từ file Excel'
            found = this.api.find3var('inform','import','delete-task-fields')
            this.path = 'Task/'
            this.action = 'delete'
        }
        else if(name==='company') {
            this.tophead = 'Nhập danh sách công ty từ file Excel'
            found = this.api.find3var('inform','import','company-fields')
            this.path = 'Company/'
        }
        else if(name==='item') {
            this.tophead = 'Nhập danh sách chỉ tiêu từ file Excel'
            found = this.api.find3var('inform','import','item-fields')
            this.path = 'Report_Item/'
        }
        else if(name==='parameter') {
            this.tophead = 'Nhập danh sách tham số từ file Excel'
            found = this.api.find3var('inform','import','parameter-fields')
            this.path = 'Classification/'
        }
        else if(name==='batch-approve') {
            this.tophead = this.$route.query.status==='waiting-approve'? 'Duyệt theo lô từ file Excel ( trạng thái chờ duyệt 1 -> chờ duyệt 2 )': 'Duyệt theo lô từ file Excel ( trạng thái chờ duyệt 2 -> đồng ý )'
            found = this.api.find3var('inform','import','batch-approve-fields')
            this.path = 'Task/'
            this.action = 'approve'
        }
        else if(name==='stock-data') {
          this.tophead = 'Giao việc nhập dữ liệu Giao dịch chứng khoán'
          found = this.api.find3var('inform','import','stock-data-fields')
          this.path = 'Task_Stock/'
        }
        else if(name==='industry') {
          this.tophead = 'Nhập file danh sách mã ngành'
          found = this.api.find3var('inform','import','industry-fields')
          this.path = 'Industry/'
        }
        else if(name==='taindex') {
          this.tophead = 'Giao việc nhập dữ liệu Chỉ số phân tích kỹ thuật'
          found = this.api.find3var('inform','import','stock-data-fields')
          this.path = 'Task_Taindex/'
        }
        if(this.tophead)  this.msgInfo.push({message: found.value, type: 'success'})
      },

      uploadFile() {
        this.readylist = []
        this.dataready = false
        this.optionNew = false
        this.optionUpdate = false
        var file = document.getElementById("fileUpload");
        if(file.files.length == 0) return
        
        let data = new FormData();
        data.append('name', file.files[0].name);
        data.append('file', file.files[0]);
        this.filename = file.files[0].name

        let fileName = file.files[0].name
        //check file name is valid
        if (!(fileName.search('.xls') > 0 || fileName.search('.xlsx') > 0)) {
          this.msgInfo.push({message: this.api.find3var('inform', 'import', 'file-type-invalid').value, type: 'error'} )
          return
        }

        axios.post(this.connection.path + 'upload-file/', data=data)
        .then(response => {
            this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-ok').value, type: 'success'})
            this.getfile(file.files[0].name)
            file.value = ''
          }
        )
        .catch(error => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-fail').value, type: 'error'})
          file.value = ''
        })
      },

      getfile(filename) {
          const url = this.connection.path + 'getfile/' + filename
          axios.get(url)
          .then(response => {
              //this.datafile = JSON.parse(response.data)
              let obj = JSON.parse(response.data)
              obj.data = obj.data.map(v=>v = this.$resetNull(v))
              this.datafile = obj
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
          let found = this.api.find3var('inform','import','task-fields')
          if(this.$route.query.type==='delete-task')
              found = this.api.find3var('inform','import','delete-task-fields')
          else if(this.$route.query.type=='item')
              found = this.api.find3var('inform','import','item-fields')
          else if(this.$route.query.type==='parameter')
              found = this.api.find3var('inform','import','parameter-fields')
          else if(this.$route.query.type==='company')
              found = this.api.find3var('inform','import','company-fields')
          else if(this.$route.query.type==='batch-approve')
              found = this.api.find3var('inform','import','batch-approve-fields')
          else if(this.$route.query.type==='stock-data')
            found = this.api.find3var('inform','import','stock-data-fields')
          else if(this.$route.query.type==='industry')
            found = this.api.find3var('inform','import','industry-fields')
          else if(this.$route.query.type==='taindex')
            found = this.api.find3var('inform','import','stock-data-fields')

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
      if(this.$route.query.type==='task') this.verifyImportTask()
      else if(this.$route.query.type==='delete-task') this.verifyDeleteTask()
      else if(this.$route.query.type==='company') this.verifyImportCompany()
      else if(this.$route.query.type==='item') this.verifyImportItem()
      else if(this.$route.query.type==='parameter') this.verifyImportParameter()
      else if(this.$route.query.type==='batch-approve') this.verifyBatchApprove()
      else if(this.$route.query.type==='stock-data') this.verifyImportStockData()
      else if(this.$route.query.type==='industry') this.verifyIndustry()
      else if(this.$route.query.type==='taindex') this.verifyImportStockData()
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
        console.log(error)
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
      if(this.$route.query.type==='task')
        mixing.download(this.connection.path + 'download-file/task_template.xlsx')
      else if(this.$route.query.type==='delete-task')
        mixing.download(this.connection.path + 'download-file/delete_template.xlsx')
      else if(this.$route.query.type==='parameter')
        mixing.download(this.connection.path + 'download-file/parameter_template.xlsx')
      else if(this.$route.query.type=='item')
        mixing.download(this.connection.path + 'download-file/item_template.xlsx')
      else if(this.$route.query.type==='company')
        mixing.download(this.connection.path + 'download-file/company_template.xlsx')
      else if(this.$route.query.type==='batch-approve')
        mixing.download(this.connection.path + 'download-file/approve_template.xlsx')
      else if(this.$route.query.type==='stock-data')
        mixing.download(this.connection.path + 'download-file/stock_template.xlsx')
      else if(this.$route.query.type==='industry')
        mixing.download(this.connection.path + 'download-file/industry.xlsx')
      else if(this.$route.query.type==='taindex')
        mixing.download(this.connection.path + 'download-file/taindex_template.xlsx')
    }
  }
}
</script>