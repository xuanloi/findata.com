<!-- eslint-disable -->
<template>
    <div class="columns pt10 pb10 is-multiline is-mobile"  v-if="recordEdit">
        <div class="column is-4 pt0">
            <div class="field">
                  <label class="label has-text-left">Id</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.id" disabled>
                </div> 
            </div>   
        </div>
        <div class="column is-4 pt0">
            <div class="field">
                  <label class="label has-text-left">Phân loại</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.category">
                </div> 
            </div>   
        </div>
        <div class="column is-4 pt0">
            <div class="field">
                  <label class="label has-text-left">Phân lớp</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.classify">
                </div> 
            </div>   
        </div>

        <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Mã</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.code">
                </div> 
            </div>   
        </div>
        <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Biểu tượng</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.icon">
                </div> 
            </div>   
        </div>
        <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Hình ảnh</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.image">
                </div> 
            </div>   
        </div>

            <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Liên kết</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.link">
                </div> 
            </div>   
                    </div>

                <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Hiệu lực</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.enable">
                </div> 
            </div>
        </div>
        
                <div class="column is-4 pt5">
            <div class="field">
                  <label class="label has-text-left">Thứ tự</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.index">
                </div> 
            </div>   
        </div>

          <div class="column is-12 pt5">
            <div class="field">
                  <label class="label has-text-left">VN (tiếng Việt)</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.value">
                </div> 
            </div>   
                    </div>
          
          <div class="column is-12 pt5">
            <div class="field">
                  <label class="label has-text-left">EN (tiếng Anh) </label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.value1">
                </div> 
            </div>   
                    </div>

            <div class="column is-12 pt5">
            <div class="field">
                  <label class="label has-text-left">Chi tiết</label>
            <div class="control">
                <input  class="input font-smaller" type="text" v-model="recordEdit.detail">
                </div> 
            </div>   
        </div>
      <div class="column is-12 pt5">
        <a class="button is-primary" @click="updateData()"> Lưu lại </a>
      </div>
    </div>
</template>

<script>
import mixing from '@/assets/js/mixing.js'
export default {
  data() {
    return {
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(),
      recordEdit: undefined,
      action: undefined
    }
  },
  
  created() {
    this.action = this.pageparam.action
    if(this.action==='edit') {this.recordEdit = JSON.parse(JSON.stringify(this.pageparam.record))}
    else if(this.action==='insert') {
        this.recordEdit = {id: undefined, category: undefined, classify: undefined, code: undefined, value: undefined, value1: undefined,
        icon: undefined, image: undefined, link: undefined, enable: true, create_time: null}
    }
  },

  watch: {
    'connection.getupdateStatus': function(newVal) {
      if(newVal) {
        this.$store.commit('updateState', {name: 'api', key: 'data', data: this.syspara})
        this.$store.commit('updateState', {name: 'pageparam', key: 'data', data: this.$copy(this.syspara)})
        if(this.pageparam.currentFilter? this.pageparam.currentFilter.length>0 : false) {
          this.$store.commit('updateState', {name: 'pageparam', key: 'filterby', data: this.$copy(this.pageparam.currentFilter)})
        }
        let connlist = [{name: 'rights', url: 'data/Classification',
        params: {sort: 'index', filter: {function__account_type: this.login.type.id, function__enable: 1, enable: 1}}}]
        this.connection1.getApi(connlist)
      }
    },
    "connection1.getdataReady": function(newVal) {
      if (newVal==="success") {
        let data = this.connection1.getbatchData.find(v=>v.name==='rights').data
        data.filter(v=>v.category==='function').map(v=>{
          let found = this.api.find3var('functions','admin', v.classify)
          if(found? (found.enable? !data.find(x=>x.id===found.id): false) : false) data.push(found)
        })
        mixing.multiSort(data, {index: 'asc'})
        this.rights = data
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit("updateApi", {api: val})}
    },
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },
    syspara: {
      get: function() {return this.$store.state.syspara},
      set: function(val) {this.$store.commit("updateSystemParameter", {syspara: val})}
    },
    pageparam: {
      get: function() {return this.$store.state.pageparam},
      set: function(val) {this.$store.commit('updatePageParam', {pageparam: val})}
    },
    rights: {
      get: function() {return this.$store.state.rights},
      set: function(val) {this.$store.commit('updateRights', {rights: val})}
    },
  },

  methods: {
    updateData() {
      if(this.recordEdit.create_time===null) this.recordEdit.create_time = new Date()
      this.recordEdit.detail = this.recordEdit.detail===null? '' :  this.recordEdit.detail
      this.recordEdit.image = this.recordEdit.image===null? '' :  this.recordEdit.image
      this.recordEdit.link = this.recordEdit.link===null? '' :  this.recordEdit.link
      this.recordEdit.icon = this.recordEdit.icon===null? '' :  this.recordEdit.icon
      this.recordEdit = this.$resetNull(this.recordEdit)
      if(this.recordEdit.id) this.connection.update('syspara', this.recordEdit)
      else this.connection.insert('syspara', this.recordEdit)
    }
  }
}
</script>