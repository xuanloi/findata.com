<!-- eslint-disable -->

<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: 'Danh mục thông báo'}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
<div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-centered  mt10 mb20"  v-if="pagenews.action==='insert' || pagenews.action==='edit'">
  <div class="column is-12">
  <a class="close-button" @click="close()"><i class="mdi mdi-close-circle-outline is-size-3 has-text-dark has-background-white" > </i>   </a>
  <div class="ml10 mr10 mb10 mt10">
  <div class="pt20 pb20 pl20 pr20" style="border: solid 1px hsl(0, 0%, 86%)">
    <CreateNews/>
  </div>
  </div>
  </div>
  </div>
  <TableFilter v-bind="{name: 'pagenews'}" />
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
import CreateNews from '~/components/CreateNews.vue'

export default {
  components: {
    TopMenu,
    TableFilter,
    CreateNews
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
      title: 'Danh sách tin tức'
    }
  },

  head() {
    return {
      title: 'Danh sách thông báo'
    }
  },
    
  computed: {
    pagenews: {
      get: function() {return this.$store.state.pagenews},
      set: function(val) {this.$store.commit('updatePageNews', {pagenews: val})}
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
    this.pagenews = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true,
    api: {} , origin_api: {}, reload: 0}

    var val = {name: 'news', url: 'data/News', params: {
      values:'id,creator,title,category,category__value,creator__name,approve_status,approve_status__value,approver,approver__name,subtitle,content,image'}}
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
      let data = this.$copy(this.connection.getbatchData.find(v=>v.name==='news').data)  
      this.$store.commit('updateState', {name: 'pagenews', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
      this.$store.commit('updateState', {name: 'pagenews', key: 'data', data: data})
      if(Object.keys(this.pagenews.origin_api).length===0) {
        this.$store.commit('updateState', {name: 'pagenews', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
      }   
    },

    close() {
      this.$store.commit('updateState', {name: 'pagenews', key: 'record',  data: undefined})
      this.$store.commit('updateState', {name: 'pagenews', key: 'action',  data: undefined})        
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