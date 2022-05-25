<template>
<div>
  <div class="field">
    <b-upload v-model="file" ref="upload">
      <a class="button is-dark" :class="isloading? 'is-loading' : ''">
        <b-icon icon="mdi mdi-plus mr5 fs30"></b-icon>
        <span> Tải lên file Excel </span>
      </a>
    </b-upload>
    <a class="button is-primary" @click="download()"> Tải xuống template </a>
  </div>
  
  <div class="columns" v-if="msgInfo.length>0">
  <div class="column is-7">
   <div class="notification is-white">
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
  <div class="column has-text-centered" v-if="ready">
    <a class="button is-dark" @click="update()">Cập nhật</a>
  </div>
  </div>  

  <TableFilter class="mx-4" v-bind="{name: 'pageimport'}" v-if="datafile"/>
</div>
</template>

<script>
export default {
  data() {
    return {
      isloading: false,
      file: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(this.$buefy),
      msgInfo: [],
      datafile: undefined,
      ready: false,
      requireFields: ['name', 'stock_code', 'capital', 'percentage', 'voting_rate', 'type'],
      classinfo: [{type: 'success', icon_class: 'mdi mdi-check', text_class: 'has-text-primary'},
        {type: 'error', icon_class: 'mdi mdi-close has-text-danger', text_class: 'has-text-danger'},
        {type: 'warning', icon_class: 'mdi mdi-alert has-text-warning', text_class: 'has-text-warning'},
        {type: 'waiting', icon_class: 'mdi mdi-timer-sand has-text-primary', text_class: 'has-text-primary'}
      ]
    }
  },

  watch: {
    file: function(newVal) {
      if(newVal) this.upload()
      if(this.$refs.upload? this.$refs.upload.$refs : false) this.$refs.upload.$refs.input.value = ''
    },

    "connection1.getdataReady": function(newVal) {
      if (newVal==="success") {
        let filter = this.connection1.getbatchData.filter(v=>v.data.length===0)
        let copy = this.$copy(this.pageimport)
        if(filter.length>0) {
          filter.map(x=>{
            let found = copy.data.find(y=>parseInt(y.index)===parseInt(x.name))
            found.error = 'Công ty chưa có trong hệ thống'
          })
          this.msgInfo.push({message: 'Dữ liệu có lỗi. Hãy kiểm tra lại', type: 'error'})
          let field = this.$createField('error', 'error', 'string', false, true)
          copy.fields.push(field)
        } else {
          this.connection1.getbatchData.map(x=>{
            let found = copy.data.find(y=>parseInt(y.index)===parseInt(x.name))
            found.subsidiary = x.data[0].id
            found.company = this.$route.query.company
            found.capital = this.$empty(found.capital)? null : found.capital
            found.percentage = this.$empty(found.percentage)? null : found.percentage
            found.voting_rate = this.$empty(found.voting_rate)? null : found.voting_rate
            let obj = this.pagetask.data.find(y=>y.subsidiary===found.subsidiary)
            if(obj) found.id = obj.id
          })
          this.msgInfo.push({message: 'Dữ liệu hợp lệ, click [Cập nhật] để tải vào hệ thống', type: 'success'})
          this.ready = true
        }
        this.pageimport = copy
      }
    },

    'connection2.getupdateRecord': function(newVal) {
      if(newVal) this.$emit('reload')
    }
  },

  created() {
    this.pageimport = {data: [], fields: [], filter: [], record: undefined, action: undefined, 
    enableDelete: true, enableApprove: true, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
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
    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
    }
  },

  methods: {
    download() {
      window.open(this.connection.path + 'download-file/subsidiary_template.xlsx', '_blank')
    },

    upload() {
      this.ready = false
      this.msgInfo = []
      var thefile = this.$upload(this.file, 'file', undefined)
      if (!(thefile.name.search('.xls') > 0 || thefile.name.search('.xlsx') > 0)) {
          this.msgInfo.push({message: this.api.find3var('inform', 'import', 'file-type-invalid').value, type: 'error'} )
          return
      }

      this.$axios.post(this.connection.path + 'upload-file/', thefile.form)
      .then(response => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-ok').value, type: 'success'})
          this.getfile(thefile.name)
        }
      )
      .catch(error => {
        this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-fail').value, type: 'error'})
      })
    },

    getfile(filename) {
      this.$axios.get(this.connection.path + 'getfile/' + filename)
      .then(response => {
        this.datafile = JSON.parse(response.data)
        this.fillData()
      })
      .catch(error => {
        this.msgInfo.push({message: 'Lỗi. ' + error.toString(), type: 'error'})
      })
    },

    fillData() {
      let fields = []
      this.datafile.schema.fields.forEach(ele => {
        let field = this.$createField(ele.name, ele.name, 'string', false, true)
        if(field.name!=='index') fields.push(field)
      })
      let copy = this.$copy(this.pageimport)
      copy.data = this.datafile.data
      copy.fields = fields
      this.pageimport = copy
      
      let misslist = []
      this.requireFields.map(v=>{
        let found = fields.find(x=>x.name===v)
        if(!found) misslist.push(found)
      })
      if(misslist.length>0) {
        this.msgInfo.push({message: (this.api.find3var('inform','import','field-list-fail').value + ': ' + misslist.join(', ')), type: 'error'})
      } else {
        this.msgInfo.push({message: this.api.find3var('inform','import','field-list-ok').value, type: 'success'})
        this.validateFontend()
      }
    },

    validateFontend() {
      let err = false
      let copy = this.$copy(this.pageimport)
      copy.data.map(v=>{
        if(this.$empty(v.name) || this.$empty(v.percentage)) {
          v.error = 'Trường [name, percentage] không được bỏ trống'
          err = true
        }
      })
     
      if(err) {
        this.msgInfo.push({message: 'Dữ liệu có lỗi. Hãy kiểm tra lại', type: 'error'})
        let field = this.$createField('error', 'error', 'string', true, true)
        copy.fields.push(field)
      } else {
        let connlist = []
        copy.data.map(v=>{
          let filter = this.$empty(v.stock_code)? {name: v.name} : {name: v.name, stock_code: v.stock_code}
          connlist.push({name: v.index.toString(), url: 'data/Company', params: {filter_or: filter}})
        })
        this.connection1.getApi(connlist)
      }
      this.pageimport = copy
    },

    update() {
      this.connection2.insert('subsidiary', this.pageimport.data)
    }
  }
}
</script>