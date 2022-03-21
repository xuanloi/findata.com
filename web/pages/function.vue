<!-- eslint-disable -->
<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: this.title}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
    <div class="column is-11 is-marginless is-paddingless">
      <div class="columns is-centered  mt10 mb20"  v-if="pagefunction.action==='insert' || pagefunction.action==='edit'">
        <div class="column is-9" >
          <a class="close-button" @click="close()"><i class="mdi mdi-close-circle-outline is-size-3 has-text-dark has-background-white" > </i>   </a>
        <div class="ml10 mr10 mb10 mt10">
        <Function class="pt20 pb20 pl20 pr20" style="border: solid 1px hsl(0, 0%, 86%)" />
  </div>
  </div>
  </div>
    <TableFilter class="mt10" v-bind="{name: 'pagefunction'}" />
  </div>
  </div>
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '~/components/TopMenu.vue'
import TableFilter from '~/components/TableFilter.vue'

import mixing from "@/assets/js/mixing.js";
import Function from '~/components/Function.vue'

export default {
  components: {
    TopMenu,
    TableFilter,
    Function
  }, 

  data () {
    return {
      type: this.$route.query.type,
      connection: this.$connection(),
      title: 'Quản lý chuyên mục'
    }
  },

  head() {
    return {
      title: this.title
    }
  },
    
    created() {
      const fields = []
      fields.push(mixing.createField('id', 'Id', 'number', false, true))
      fields.push(mixing.createField('item', 'Mã', 'string', false, true))
      fields.push(mixing.createField('value', 'Tên chức năng', 'string', false, true))
      fields.push(mixing.createField('level', 'Cấp bậc', 'string', false, true))
      fields.push(mixing.createField('parent', 'Cấp trên', 'string', false, true))
      fields.push(mixing.createField('index', 'Chỉ mục', 'number', false, true))
      fields.push(mixing.createField('icon', 'Biểu tượng', 'string', false, true))
      fields.push(mixing.createField('image', 'Hình ảnh', 'string', false, true))
      fields.push(mixing.createField('link', 'Đường dẫn', 'string', false, true))
      fields.push(mixing.createField('action', '', 'string', false, true, '8%', 'insert,edit,select'))
      this.pagefunction = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true,
      api: {name: this.type, full_date: true} , origin_api: {name: this.type, full_date: true}, reload: 0}

      let connlist = this.connection.checkDataReady([this.type])
      let filter = connlist.filter(v=>!v.ready)
      if(filter.length>0) this.connection.getApi(filter)
      else this.fillData()
    },
  
  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
      else if (newVal==='error') this.$route.push({path: '/error'})
    }
  },

  computed: {
    pagefunction: {
      get: function() {return this.$store.state.pagefunction},
      set: function(val) {this.$store.commit('updatePageFunction', {pagefunction: val})}
    }
  },

  methods: {
    fillData() {
      let data = this.$copy(this.$store.state[this.type])
      this.$store.commit('updateState', {name: 'pagefunction', key: 'data', data: data})
      if(this.connection.getbatchStatus.length===0) return
      this.$store.commit('updateState', {name: 'pagefunction', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
      if(Object.keys(this.pagefunction.origin_api).length===0) {
        this.$store.commit('updateState', {name: 'pagefunction', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
      }
    },

    close() {
      this.$store.commit('updateState', {name: 'pagefunction', key: 'record', data: undefined})
      this.$store.commit('updateState', {name: 'pagefunction', key: 'action', data: undefined})
    }
  }
}
</script>