<!-- eslint-disable -->

<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: this.title}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt70">
  <div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-centered mb20" v-if="pagehelp.action==='insert' || pagehelp.action==='edit'">
  <div class="column is-12">
  <a class="close-button" @click="close()"><i class="mdi mdi-close-circle-outline is-size-3 has-text-dark has-background-white"> </i> </a>
  <div class="ml10 mr10 mb10 mt10">
  <div class="pb20 pl20 pr20" style="border: solid 1px hsl(0, 0%, 86%)">
   <CreateHelp/>
  </div>
  </div>
  </div>
  </div>
  <TableFilter v-bind="{name: 'pagehelp'}" />
  </div>
  </div>
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '~/components/TopMenu.vue'
import TableFilter from '~/components/TableFilter.vue'
import Connection from "@/assets/js/connection.js"
import mixing from "@/assets/js/mixing.js"
import CreateHelp from '~/components/CreateHelp.vue'

export default {
  components: {
    TopMenu,
    TableFilter,
    CreateHelp
  },

  data () {
    return {
        connection: this.$connection(this.$buefy),
        connection1: this.$connection(),
        connection2: this.$connection(),
        code: undefined,
        name: undefined,
        tags: [],
        filteredTags: [],
        subjects: [],
        classSubject: [],
        title: 'Danh sách bài viết trang trợ giúp'
      }
    },

    head() {
      return {
        title: this.title
      }
    },
    
    computed: {
      pagehelp: {
        get: function() {return this.$store.state.pagehelp},
        set: function(val) {this.$store.commit('updatePageHelp', {pagehelp: val})}
      }
    },

    created() {
        const fields = []
        fields.push(mixing.createField('id', 'Id', 'number', false, true))
        fields.push(mixing.createField('title', 'Tiêu đề', 'string', false, true))
        fields.push(mixing.createField('category__value', 'Chuyên mục', 'string', false, true))
        fields.push(mixing.createField('creator__name', 'Người tạo', 'string', false, true))
        fields.push(mixing.createField('approve_status__value', 'Phê duyệt', 'string', false, true))
        fields.push(mixing.createField('approver__name', 'Người duyệt', 'string', false, true))
        fields.push(mixing.createField('action', '', 'string', false, true, '8%', 'insert,edit,select'))
        this.pagehelp = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true,
        api: {} , origin_api: {}, reload: 0}

        var val = {name: 'help', url: 'data/Help', params: {
          values:'id,title,category,category__value,creator,creator__name,approve_status,approve_status__value,approver,approver__name,subtitle,content,image'}}
        this.connection.getApi([val])
    },
  
  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
      else if (newVal==='error') this.$router.push({path: '/error'})
    }
  },

  methods: {
      fillData() {
        let data = this.$copy(this.connection.getbatchData.find(v=>v.name==='help').data)  
        this.$store.commit('updateState', {name: 'pagehelp', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagehelp', key: 'data', data: data})
        if(Object.keys(this.pagehelp.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagehelp', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
        }   
      },

      close() {
        this.$store.commit('updateState', {name: 'pagehelp', key: 'record',  data: undefined})
        this.$store.commit('updateState', {name: 'pagehelp', key: 'action',  data: undefined})        
      },

      getFilteredTags(text) {
        this.filteredTags = this.subjects.filter((option) => {
            return option.name
                .toString()
                .toLowerCase()
                .indexOf(text.toLowerCase()) >= 0
        })
      }
  }
}
</script>