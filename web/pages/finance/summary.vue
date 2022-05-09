<template>
  <div>
    <TopMenu v-bind="{type: 'tophead', tophead: title}"></TopMenu>
    <div class="columns mt-6 ml-2 mb-0">
    <div class="column is-4">
      <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
  <label class="label fs14">Từ ngày<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
  <b-datepicker
   size="is-small"
    locale="en-GB"
    placeholder=""
    v-model="start"
    @input="changeDate"
    >
  </b-datepicker>
  </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='code')">{{errors.find(v=>v.name==='code').text}}</p>
</div>
        <div class="field">
  <label class="label fs14">Đến ngày<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <b-datepicker
       size="is-small"
        locale="en-GB"
        placeholder=""
        v-model="end"
        @input="changeDate"
      >
      </b-datepicker>
      </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='name')">{{errors.find(v=>v.name==='name').text}}</p>
      </div>
      </div>
     </div>
    </div>
    </div>
    <DataTable class="mx-3" v-bind="{pagename: 'pagedata'}" @opendetail="openDetail" />
  </div>
</template>

<script>
export default {
  head() {
    return {title: this.title}
  },
  data() {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      start: undefined,
      end: undefined,
      errors: [],
      defaultFields: [],
      title: 'Báo cáo tổng kết công việc',
      connlist: []
    }
  },

  created() {
    this.pagedata = {data: [], fields: [], action: undefined, enableDelete: true, api: {full_data: true} , origin_api: {full_data: true}, showFilter: true}
    let ele = this.connection.find('usersetting')
    ele.params.filter = {name: 'task-summary'}
    this.connection.getApi([ele])    
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if(newVal==='success') {
        let row = this.connection.getbatchData.find(v=>v.name==='usersetting').data[0]
        let json = JSON.parse(row.detail)
        this.defaultFields = json.fields
        this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: this.$copy(json.fields)})
        this.currentsetting = this.$copy(row)
        if(json.tablesetting) this.tablesetting = json.tablesetting
        const now = this.$dayjs()
        if(!this.$empty(this.$route.query.startdate)) {
          this.start = new Date(this.$route.query.startdate)
          this.end = new Date(this.$route.query.enddate)
          this.changeDate()
        } else {
          let arr = this.$daysInMonth(now.year(), now.month())
          this.start = new Date(arr[0].format('YYYY-MM-DD'))
          this.end = new Date(arr[arr.length-1].format('YYYY-MM-DD'))
          this.loadData(arr)
        }
      }
    },

    'connection1.getdataReady': function(newVal) {
      if(newVal==='success') {
        let rows = this.$copy(this.connlist)
        this.connection1.getbatchData.map(k=>{
          let data = k.data
          let row = rows.find(v=>v.name===k.name)
          this.pagedata.fields.filter(v=>v.date).map(v=>{
            let fdate = this.$dayjs(v.date).format('YYYYMMDD')
            let date = this.$dayjs(v.date).format('YYYY-MM-DD')
            let found = data.find(x=>x[row.tag]===date && x.status===row.id)
            row['f' + fdate] = found? found.count : undefined // this.$numtoString(found.count)
          })
        })
        this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: rows})
      } else if (newVal==='error') console.log('fail')
    }
  },

  computed: {
    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit('updatePageData', {pagedata: val})}
    },
    currentsetting: {
      get: function() {return this.$store.state.currentsetting},
      set: function(val) {this.$store.commit("updateCurrentSetting", {currentsetting: val})}
    },
    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    },
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    }
  },

  methods: {
    loadData(arr) {
      let template = `<div v-if="row[field.name]">
      <a class="has-text-dark" @click="$emit('clickevent', {name: 'opendetail'})">
      <p>{{row[field.name]}}</p>
      </a>
      </div>`
      let fields = this.$copy(this.defaultFields)
      let arr1 = arr.map(v=> {
        let date = v.format('YYYY-MM-DD')
        let label = '<div><p style="border-bottom: 2px solid white">' + Number(date.substring(8,10)) + '</p><p>' + Number(date.substring(5,7)) + '</p></div>'
        let field = this.$createField('f' + v.format('YYYYMMDD'), label, 'string', true)
        field.date = date
        field.template = template
        field.minwidth = "45"
        return field
      })
      fields = fields.concat(arr1)
      this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: fields})

      this.connlist = [{id: 158, name: "not-yet-entered", tag: 'create_time__date', value: 'Chưa nhập'}, {id: 242, name: "entered", tag: 'entry_time__date', value: 'Đang nhập'}, 
        {id: 171,name: "waiting-approve", tag: 'waiting1_time__date', value: 'Chờ duyệt 1'}, {id: 677,name: "waiting-approve-2", tag: 'waiting2_time__date', value: 'Chờ duyệt 2'}, 
        {id: 241, name: "retype", tag: 'update_time__date', value: 'Sửa lại'}, {id: 157, name: "approved", tag: 'approve_time__date', value: 'Đồng ý'}]
      let conns = []
      this.connlist.map(y=>{
        let conn = this.$copy(this.connection.find('tasklist'))
        conn.name = y.name
        let filter = {status__code: y.name}
        filter[y.tag + '__gte'] = this.$dayjs(this.start).format('YYYY-MM-DD')
        filter[y.tag + '__lte'] = this.$dayjs(this.end).format('YYYY-MM-DD')
        conn.params = {values: 'status,status__value,' + y.tag,
        distinct_values: {count: {type: 'Count', field: 'id', condition: {id__gt:0}}}, summary: 'annotate', filter: filter}
        conns.push(conn)
      })
      this.connection1.getApi(conns)
    },

    changeDate() {
      let arr = this.$fromToDate(this.start, this.end)
      this.$router.push({path: '/finance/summary', query: {startdate: this.$dayjs(this.start).format('YYYY-MM-DD'), enddate: this.$dayjs(this.end).format('YYYY-MM-DD')}})
      this.loadData(arr)
    },

    openDetail(row, field, data) {
      let query = {status: row.id}
      query[row.tag] = this.$dayjs(field.date).format('YYYY-MM-DD')
      let routeData = this.$router.resolve({path: '/finance/view-detail', query: query})
      window.open(routeData.href, '_blank')
    }
  }
}
</script>