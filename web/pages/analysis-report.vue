<template>
  <div>
    <TopMenu v-bind="{type: 'tophead', tophead: 'Danh sách báo cáo phân tích từ CTCK'}" />
   <DataTable v-if="tablesetting" class="mt-6 pt-4 mx-2" v-bind="{pagename: 'pagedata'}" @delete="deleteRecord" />
    <div class="modal is-active" v-if="pagedata.action? (pagedata.action.event==='edit' || pagedata.action.event==='insert') : false">
      <div class="modal-background" style="opacity:0.7 !important;"></div>
      <div class="modal-card" :style="$store.state.ismobile? '' : 'width:60%'">
      <p class="has-text-right">
        <button class="delete is-large has-background-black" aria-label="close" 
        @click="close()"></button>
      </p>
      <section class="modal-card-body" style="min-height:300px">
        <AnalysisReport @browsemedia="browseMedia" @close="close()" />
      </section>
      </div>
    </div>
         <section>
    <b-sidebar
      type="is-light"
      :fullheight="true"
      :fullwidth="true"
      :overlay="true"
      :right="true"
      v-model="open"
      style="z-index:1000"
    >
    <media v-bind="{mediatype: 'file', modal: true}" @selectmedia="selectMedia" @closemedia="selectMedia" />
    </b-sidebar>
     </section>
     </div>
</template>

<script>
import AnalysisReport from '@/components/AnalysisReport'
import media from '@/pages/media'
export default {
  components: {AnalysisReport, media},
  data() {
    return {
      connection: this.$connection(this.$buefy),
      data: [],
      currentDelete: undefined,
      open: false,
      currentAction: undefined,
    }
  },

  created() {
    window.addEventListener('keydown', (e) => {if (e.key == 'Escape') this.close()})
    this.pagedata = {data: [], fields: [], action: undefined, enableDelete: true, api: {full_data: true} , origin_api: {full_data: true}, showFilter: true}
    let ele = this.connection.find('usersetting')
    ele.params.filter = {name: 'analysis-report'}
    let connlist = [ele]
    if(!this.companylist) {
      let found = this.connection.find('companylist')
      connlist.push(found)
    }
    let conn = this.connection.find('analysisreport')
    connlist.push(conn)
    this.connection.getApi(connlist)
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if(newVal==='success') {
        let row = this.connection.getbatchData.find(v=>v.name==='usersetting').data[0]
        let json = JSON.parse(row.detail)
        this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: this.$copy(json.fields)})
        this.currentsetting = this.$copy(row)
        if(json.tablesetting) this.tablesetting = json.tablesetting
        let data = this.connection.getbatchData.find(v=>v.name==='analysisreport').data
        this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: this.$copy(data)})
      }
      else if (newVal==='error') console.log('fail')
    },

    'connection.getupdateStatus' : function(newVal) {
      if(newVal) {
        let copy = this.$copy(this.pagedata)
        let index = copy.data.findIndex(v=>v.id===this.currentDelete.id)
        this.$delete(copy.data, index)
        this.pagedata = copy
      }
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
    companylist: {
      get: function() {return this.$store.state.companylist},
      set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
    }
  },

  methods: {
    close() {
      this.$store.commit('updateState', {name: 'pagedata', key: 'action', data: undefined})  
    },

    deleteRecord(row) {
      this.currentDelete = row
      this.$buefy.dialog.confirm({
      message: 'Bạn muốn xóa bản ghi: ' + row.id,
      onConfirm: () => this.connection.delete('analysisreport', row.id)})
    },

    browseMedia(record) {
      this.currentAction = this.$copy(this.pagedata.action)
      this.currentAction.row = this.$copy(record)
      this.$store.commit('updateState', {name: 'pagedata', key: 'action', data: undefined})
      this.open = true
    },

    selectMedia(v) {
      this.open = false
      this.currentAction.event = 'edit'
      if(v) this.currentAction.row.file = this.connection.path + 'static/file/' + v.file
      this.$store.commit('updateState', {name: 'pagedata', key: 'action', data: this.currentAction})  
    }
  }
}
</script>