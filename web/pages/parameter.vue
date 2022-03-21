<!-- eslint-disable -->

<template>
  <div>
 <TopMenu v-bind="{type: 'tophead', tophead: 'Danh sách tham số', enableDownload: true}" />
 <div class="mx-3">
  <div class="columns is-centered  mt60 mb20"  v-if="pageparam.action==='insert' || pageparam.action==='edit'">
  <div class="column is-9" >
  <a class="close-button" @click="close()"><i class="mdi mdi-close-circle-outline is-size-3 has-text-dark has-background-white" > </i>   </a>
  <div class="ml10 mr10 mb10 mt10">
  <div class="pt20 pb20 pl20 pr20" style="border: solid 1px hsl(0, 0%, 86%)">
    <ParameterEdit/>
  </div>
  </div>
  </div>
  </div>
  <TableFilter class="mt60" v-bind="{name: 'pageparam'}" />
  </div>
  </div>
</template>

<script>
import ParameterEdit from '~/components/ParameterEdit.vue'
import mixing from "@/assets/js/mixing.js";
import Export from '@/assets/js/export.js';

export default {
  components: {
    ParameterEdit
  },

  created() {
    let data = this.$route.query.category? this.$copy(this.api.filter1var(this.$route.query.category)) : this.$copy(this.api.data)
    data.map(v=>v.create_time = mixing.yyyymmddhhmm(new Date(v.create_time)))
    const fields = [
      mixing.createField('id', 'Id', 'number', false, true),
      mixing.createField('category', 'Phân loại', 'string', false, true),
      mixing.createField('classify', 'Phân lớp', 'string', false, true),
      mixing.createField('code', 'Mã', 'string', false, true),
      mixing.createField('value', 'Giá trị (VN)', 'string', false, true),
      mixing.createField('value1', 'Giá trị (EN)', 'string', false, true),
      mixing.createField('icon', 'Biểu tượng', 'string', false, true),
      mixing.createField('image', 'Hình ảnh', 'string', false, true),
      mixing.createField('link', 'Đường dẫn', 'string', false, true),
      mixing.createField('index', 'Thứ tự', 'string', false, true),
      mixing.createField('action', '', 'string', false, true, '8%', 'insert,edit,select')
    ]
    this.pageparam = {data: data, fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true, filterby: undefined,
    api: {name: 'syspara', full_data: true} , origin_api: {name: 'syspara', full_data: true}, reload: 0}
  },

  head() {
    return {
      title: 'Quản lý tham số hệ thống'
    }
  },
    
  watch: {
    menuaction: function(newVal) {
      if(newVal? newVal.action==='download': false) this.exportData()
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit("updateApi", {api: val})}
    },
    pageparam: {
      get: function() {return this.$store.state.pageparam},
      set: function(val) {this.$store.commit('updatePageParam', {pageparam: val})}
    },
    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    }
  },

  methods: {
    close() {
      this.$store.commit('updateState', {name: 'pageparam', key: 'action', data: undefined})  
      this.$store.commit('updateState', {name: 'pageparam', key: 'record', data: undefined})  
    },

    exportData() {
      var _export = new Export()
      let  dataTypes = {
          id: 'String', 
          category : 'String',
          classify: 'String',
          code: 'String',
          value: 'String',
          value1: 'String',
          icon: 'String',
          image: 'String',
          link: 'String',
          detail: 'String',
          index: 'String',
          enable: 'String'
      }

      let fields = ['id', 'category', 'classify', 'code', 'value', 'value1', 'icon', 'image', 'link', 'detail', 'index', 'enable']
      _export.set(this.pageparam.filter, 'parameters', dataTypes, fields)
      _export.exportfile()
    }
  }
}
</script>