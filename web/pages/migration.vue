<template>
<div>
<!--<SubMenu v-bind="{title: 'Tích hợp dữ liệu'}" />-->
<section class="hero is-fullheight-with-navbar">
  <div class="hero-body px-3 py-5" style="align-items: flex-start">
    <div class="container is-fluid mt-2">
      <div class="field is-horizontal">
          <div class="field-body">
      <div class="field" style="width:60%">
        <label class="label">Nhập danh sách bảng cần tích hợp</label>
  <div class="control">
    <textarea class="textarea" rows="2" placeholder="" v-model="text"></textarea>
  </div>
</div>
   <div class="field">
          <label class="label">Dữ liệu nguồn</label>
          <div class="control">
            <input class="input" type="text" placeholder="Đường dẫn kết nối tới nguồn" v-model="link">
            <p class="buttons are-small">
             <a class="button is-primary mt-3" @click="checkSoureTable()">Kiểm tra</a>
            </p>
          </div>
        </div>
        <div class="field is-narrow">
          <label class="label">Dữ liệu đích</label>
          <div class="control">
            <p class="buttons are-small">
            <a class="button is-primary" @click="checkDestTable()">Kiểm tra</a>
            <a class="button is-danger" @click="checkDestTable('delete')">Xóa dữ liệu</a>
            <a class="button is-warning" @click="checkSoureTable('migrate')">Tích hợp</a>
            </p>
          </div>
        </div>
        
    </div>
      </div>
    <p class="title fs20" v-if="current">Kiểm tra dữ liệu <span class="has-text-danger ml-3">
      {{current==='source'? 'NGUỒN' : 'ĐÍCH'}}</span></p>
  <!--  <DataTable v-bind="{pagename: 'pagedata'}" v-if="tables? tables.length>0 : false"> </DataTable>-->
  </div>
  </div>
</section>
</div>
</template>

<script>
export default {
  head() {
    return {
      title: 'Tích hợp dữ liệu'
    }
  },

  data() {
    return {
      srcConn: this.$connection(),
      destConn: this.$connection(),
      connection: this.$connection(),
      tables: [],
      text: undefined,
      link: undefined,
      current: undefined,
      action: undefined
    }
  },

  created() {
    let fields = [this.$createField('id', 'Stt', 'number', true),
    this.$createField('name', 'Tên bảng', 'string', true), this.$createField('count', 'SL bản ghi', 'number', true)]
    this.pagedata = {data: [], fields: fields, action: undefined, enableDelete: false, api: {}, origin_api: {},
    filterby: undefined, showFilter: true}

    const args = ['moneyunit', 'datatype', 'filterchoice', 'colorchoice', 'textalign', 'placement',
    'colorscheme', 'filtertype', 'sorttype', 'tablesetting', 'settingchoice', 'sharechoice', 'menuchoice', 'settingtype', 'settingclass']
    this.connection.dataPath = 'https://api.akifarm.vn/'
    let connlist = this.connection.checkDataReady(args)
    connlist.map(v=>v.path = 'dataPath')
    //this.connection.getApi(connlist)

    let found = this.connection.find('usersetting')
    //this.connection.dataPath = 'https://api.akifarm.vn/'
    found.path = 'dataPath'
    found.params.filter = {name__in: ['your-setting-fields', 'system-setting-fields', 'share-setting-fields']}
    connlist.push(found)
    //this.connection.getApi([found])
    this.connection.getApi(connlist)
  },

  watch: {
     'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        console.log(this.connection.getbatchData[0].data.length)
        this.data = this.connection.getbatchData[0].data
        this.connection.getbatchData.map(v=>{
          let conn = this.$connection()
          conn.path = 'http://localhost:8000/'
          if(v.name==='usersetting') {
            let copy = this.$copy(v.data)
            copy.map(x=>{
              x.user = 1
              x.classify = 1
              x.type = 1
              }
              )
            conn.insert(v.name, copy)

            console.log(copy)
          }
          else conn.insert(v.name, v.data)
        })
      }
      else if (newVal==='error') console.log('fail')
    },

    "srcConn.getdataReady": function(newVal) {
      if (newVal==="success") {
        let copy = this.$copy(this.pagedata.data)
        this.srcConn.getbatchData.map(v=>{
          let found = copy.find(x=>x.name===v.name)
          let status = this.srcConn.getbatchStatus.find(x=>x.name===v.name)
          found.count = status.total_rows
          this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: copy})
          if(this.action==='migrate') {
            this.action = undefined
            this.migrateData()
          }
        })
      } else if(newVal==='error') {
         this.$buefy.toast.open({
          duration: 4000,
          message: `Đã có lỗi xẩy ra.`,
          type: 'is-link',
          pauseOnHover: true
        })
      }
    },

    "destConn.getdataReady": function(newVal) {
      if (newVal==="success") {
        let copy = this.$copy(this.pagedata.data)
        this.destConn.getbatchData.map(v=>{
          let found = copy.find(x=>x.name===v.name)
          let status = this.destConn.getbatchStatus.find(x=>x.name===v.name)
          found.count = status.total_rows
          this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: copy})
          if(this.action==='delete') {
            this.action = undefined
            this.deleteData()
          }
        })
      } else if(newVal==='error') {
         this.$buefy.toast.open({
          duration: 4000,
          message: `Đã có lỗi xẩy ra`,
          type: 'is-link',
          pauseOnHover: true
        })
      }
    }
  },

  computed: {
    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit('updatePageData', {pagedata: val})}
    }
  },

  methods: {
    extractTable() {
      this.tables = []
      if(this.$empty(this.text) || this.$empty(this.link)) return false
      this.text.split(',').map((v,i)=>{
        this.tables.push({id: i+1, name: v.trim()})
      })
      this.srcConn.path = this.link
      this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: this.$copy(this.tables)})
      return this.tables.length>0? true : false
    },

    checkSoureTable(action) {
      if(!this.extractTable()) return
      this.current = 'source'
      this.action = action
      let args = this.srcConn.checkDataReady(this.tables.map(v=>v.name))
      this.srcConn.getApi(args)
    },

    checkDestTable(action) {
      if(!this.extractTable()) return
      this.current = 'dest'
      this.action = action
      let args = this.destConn.checkDataReady(this.tables.map(v=>v.name))
      this.destConn.getApi(args)
    },

    deleteData() {
      this.destConn.getbatchData.map(v=>{
        let conn = this.$connection()
        conn.delete(v.name, v.data)
        this.tables = []
      })
    },

    migrateData() {
       this.srcConn.getbatchData.map(v=>{
          let conn = this.$connection()
          if(v.name==='usersetting') {
            let data = v.data.filter(v=>v.classify===4)
            data.map(v=>{
              v.classify=21
              v.type = 7
              v.user = 4
            })
            conn.insert(v.name, data)
          }
          else conn.insert(v.name, v.data)
        })
    }
  }
}
</script>