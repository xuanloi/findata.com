<template>
  <div>
  <div class="columns is-centered mb-0">
    <div class="column is-6 pt-2 pb-0">
   <div class="field" v-if="editable">
      <b-upload v-model="file">
        <a class="button is-dark fs13" :class="isloading? 'is-loading' : ''">
          <b-icon icon="mdi mdi-plus mr5 fs30"></b-icon>
          <span> Tải lên </span>
        </a>
      </b-upload>
      <p class="fs13 mt-2"> {{title}} </p>
    </div>

    <template v-if="file">
    <div class="field mt-5">
      <label class="label">Tiêu đề chính <strong class="has-text-danger">*</strong></label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="title">
      </p>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
    </div>

    <div class="field is-horizontal mt-5">
      <div class="field-body">
      <div class="field">
      <label class="label">Loại tài liệu <strong class="has-text-danger">*</strong></label>
      <div class="control">
          <b-autocomplete
            :open-on-focus="true"
              v-model="docname"
              :data="doctype"
              placeholder="Chọn..."
              icon="magnify"
              clearable
              file="value"
              @select="option => option? selected = option : false">
          </b-autocomplete>
      </div>
    </div>

    <div class="field">
    <label class="label">Ngày phát hành <strong class="has-text-danger">*</strong></label>
      <p class="control is-expanded">
        <b-datepicker
        icon-right="calendar-month-outline"
        v-model="issue_date"
        placeholder=""
        :max-date="maxDate"
        locale="en-GB">
      </b-datepicker>
      </p>
    </div>
    </div>
    </div>

    <div class="field mt-5" v-if="selected.code==='annual-report'">
    <label class="label">Năm tài chính <strong class="has-text-danger">*</strong></label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="year">
      </p>
    </div>

    <template v-else-if="selected.code==='analysis-report'">
      <div class="field is-horizontal mt-5">
      <div class="field-body">
          <div class="field">
      <label class="label">Nguồn phát hành <strong class="has-text-danger">*</strong></label>
      <div class="control is-expanded">
        <CompanySearch :company="source" @doChange="changeCompany" /> 
      </div>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
    </div>
        <div class="field">
    <label class="label">Chuyên gia <strong class="has-text-danger">*</strong></label>
      <p class="control is-expanded">
          <ExpertSearch @selectexpert="changeExpert" /> 
      </p>
      <p class="fs12 has-text-dark mt-2"> Chưa có trong danh sách chuyên gia? 
        <a class="fs16 fb600 ml-5" @click="newExpert=true">Tạo mới</a></p>
    </div>
  </div>
      </div>
     
    <div class="field is-grouped is-grouped-multiline mt-5" v-if="expertlist.length>0">
  <div class="control" v-for="(v,i) in expertlist" :key="v.id">
    <div class="tags has-addons">
      <a class="tag is-dark">{{v.email}}</a>
      <a class="tag is-delete" @click="removeExpert(i)"></a>
    </div>
  </div>
    </div>
  
    <div class="mt-5 px-5 py-5" v-if="newExpert" style="border: solid 1px #b1a7a6">
      <div class="field is-horizontal">
      <div class="field-body">
      <div class="field">
        <label class="label">Email <strong class="has-text-danger">*</strong></label>
        <p class="control is-expanded">
          <input class="input" type="text" placeholder="" v-model="email">
        </p>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
      </div>

      <div class="field">
        <label class="label">Tên chuyên gia <strong class="has-text-danger">*</strong></label>
        <p class="control is-expanded">
          <input class="input" type="text" placeholder="" v-model="name">
        </p>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
      </div>
      </div>
      </div>
      <div class="field is-horizontal">
      <div class="field-body">
      <div class="field">
        <label class="label">Điện thoại</label>
        <p class="control is-expanded">
          <input class="input" type="text" placeholder="" v-model="phone">
        </p>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
      </div>

      <div class="field">
        <label class="label">Công ty <strong class="has-text-danger">*</strong></label>
        <div class="control is-expanded">
          <CompanySearch :company="company" @doChange="changeCompany" /> 
        </div>
          <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
      </div>
      </div>
      </div>
       <div class="field mt-5">
      <a class="button is-primary" @click="createExpert()">Tạo mới</a>
      <a class="button is-dark ml-5" @click="newExpert=false">Đóng lại</a>
    </div>
    </div>
     
    <div class="field">
    <label class="label">Số trang<strong class="has-text-danger">*</strong></label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="number_page">
      </p>
     </div>
        </template>

        <div class="field mt-5">
    <label class="label">Ghi chú (nếu có)</label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="note">
      </p>
    </div>

    <div class="field mt-6">
      <a class="button is-primary" @click="upload()">Lưu lại</a>
    </div>
    </template>
  </div>
  </div>
  <TableFilter v-if="pagetask" class="mx-4" v-bind="{name: 'pagetask'}" />
  </div>
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import CompanySearch from '@/components/CompanySearch.vue'
import ExpertSearch from '@/components/ExpertSearch.vue'
export default {
  components: {
    CompanySearch,
    ExpertSearch
  },
  props: ['type', 'editable'],
  data() {
    return {
      errors: [],
      title: undefined,
      issue_date: undefined,
      file: undefined,
      isloading: false,
      year: undefined,
      newExpert: false,
      name: undefined,
      email: undefined,
      phone: undefined,
      source: undefined,
      numberPage: undefined,
      expertlist: [],
      doctype: [],
      docname: undefined,
      selected: {},
      maxDate: new Date(),
      note: undefined,
      number_page: undefined,
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(),
      connection3: this.$connection(this.$buefy),
      connection4: this.$connection(this.$buefy),
      company: undefined,
      values: 'id,company,company__name,company__stock_code,title,note,type,type__code,type__value,issue_date,file,file__file,file__user__name,source__stock_code,source__name,task,year'
    }
  },
  created() {
    this.doctype = this.api.filter2var('document', 'type')
    this.pagetask = {data: [], fields: [], filter: [], record: undefined, action: undefined, 
    enableDelete: true, enableApprove: false, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
    this.loadData()
  },

  watch: {
    file: function(newVal) {
      if(!newVal) return
      this.title = newVal.name
    },

    type: function(newVal) {
      newVal? this.loadData() : false
    },

    'connection.getdataReady': function(newVal) {
      if(newVal==='success') {
        let record = this.connection.getbatchData[0].data[0]
        let data = {company: this.$route.query.company, title: this.title, note: this.note, type: this.selected.id, file: record.id, source: undefined, 
        task: this.$route.query.task, year: this.year, number_page: this.number_page}
        data.issue_date = this.$dayjs(this.issue_date).format("YYYY-MM-DD")
        if(this.selected.code==='analysis-report' && this.source) data.source = this.source.id
        this.connection1.insert('document', data, this.values)
        this.isloading = false
      } else if(newVal==='error') this.isloading = false
    },
    'connection1.getupdateRecord': function(newVal) {
      if(newVal) {
        let data = this.$copy(this.pagetask.data)
        data.splice(0, 0, newVal)
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        this.resetValue()
        if(this.selected.code!=='analysis-report') return 
        data = []
        this.expertlist.map(v=>{
          data.push({document: newVal.id, expert: v.id})
        })
        this.connection4.insert('author', data)
      }
    },
    'connection2.getdataReady': function(newVal) {
      if(newVal==='success') {
        let data = this.connection2.getbatchData[0].data
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
      }
    },
    'pagetask.record': function(newVal) {
      if(newVal) {
        mixing.download(this.connection.path + 'static/files/' + newVal.file__file)
      }
    }
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    },
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
    }  
  },

  methods: {
    resetValue() {
      this.title = undefined
      this.issue_date = undefined
      this.year = undefined
      this.docname = undefined
      this.note = undefined
      this.company = undefined
      this.source = undefined
      this.number_page = undefined
      this.file = undefined
    },

    loadData() {
      let fields = [this.$createField('id', 'Id', 'number', true, true),
        this.$createField('company__stock_code', 'Công ty', 'string', true, true),
        this.$createField('type__value', 'Loại file', 'string', true, true)
      ]
      let field = this.$createField('title', 'Tiêu đề', 'string', true, true)
      field.style = {list: [{value: this.$route.query.stock_code, class: 'button is-small is-primary is-outlined has-text-dark'}],
        condition: 'company__stock_code', click: true}
      fields.push(field)

      fields.push(this.$createField('issue_date', 'Ngày phát hành', 'string', true, true))
      fields.push(this.$createField('year', 'Năm tài chính', 'string', true, true))
      fields.push(this.$createField('file__user__name', 'Người tải lên', 'string', true, true))
      fields.push(this.$createField('note', 'Ghi chú', 'string', true, true))
      fields.push(this.$createField('action', '', 'string', true, true, '7%', 'select,edit,open'))
      this.$store.commit('updateState', {name: 'pagetask', key: 'fields', data: fields})
      this.connection2.getApi([{name: 'document', params: {sort: '-create_time', values: this.values, filter: {company: this.$route.query.company}}}])
    },

    upload() {
      var file = this.$upload(this.file, 'file', this.login.id)
      if(file.error) {
        let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: file.text}
        this.$buefy.notification.open(info)
        return
      }
      let found = {name: 'uploadfile', url: 'upload/', path: 'path', method: 'post', data: file.form, params: {}} 
      this.connection.getApi([found])
      this.isloading = true
    },

    changeCompany(option) {
      this.source = option
      this.company = option
    },

    createExpert() {
      let data = {name: this.name, email: this.email, phone: this.phone, company: this.source.id}
      this.connection3.insert('expert', data)
      this.newExpert = undefined
    },

    changeExpert(option) {
      this.expertlist.find(v=>v.id===option.id)? false : this.expertlist.push(option)
    },

    removeExpert(i) {
      this.$delete(this.expertlist, i)
    }
  }
}
</script>