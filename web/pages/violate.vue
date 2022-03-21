<!-- eslint-disable -->

<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: title}"/>
  <div class="mt60 mx-3">
  <div class="columns is-centered  mt10 mb20"  v-if="pageparam.action==='insert' || pageparam.action==='edit'">
  <div class="column is-9" >
  <a class="close-button" @click="close()"><i class="mdi mdi-close-circle-outline is-size-3 has-text-dark has-background-white" > </i>   </a>
  <div class="ml10 mr10 mb10 mt10">
  <div class="pt20 pb20 pl20 pr20" style="border: solid 1px hsl(0, 0%, 86%)">
 <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
  <label class="label">Người báo cáo</label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.reporter__name" readonly>
  </div>
</div>
<div class="field">
  <label class="label">Loại vi phạm</label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.type__value" readonly>
  </div>
</div>
<div class="field">
  <label class="label">Người viết</label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.poster__name" readonly>
  </div>
</div>
      </div>
  </div>

  <div class="field is-horizontal mt20">
      <div class="field-body">
        <div class="field">
  <label class="label">Nội dung bài viết</label>
  <div class="control">
    <textarea class="textarea" placeholder="" rows="4" :value="violate.content" readonly></textarea>
  </div>
</div>
</div>
 </div>

  <div class="field is-horizontal mt20">
      <div class="field-body">
        <div class="field">
  <label class="label">Xử lý vi phạm</label>
  <div class="control">
    <div class="select is-fullwidth">
    <select v-model="record.handle_method">
    <option selected disabled value="">Chọn... </option>
    <option v-for="(v,i) in api.filter2var('list','violate-handle')" :key="i" :value="v.id">{{v.value}}</option>
    </select>
    </div>
  </div>
</div>
<div class="field">
  <label class="label">Người xử lý</label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.handler__name" readonly>
  </div>
</div>
      </div>
  </div>

<div class="field is-horizontal mt30">
  <div class="field-label">
    <!-- Left empty for spacing -->
  </div>
  <div class="field-body">
    <div class="field">
      <div class="control">
        <button class="button is-primary" @click="update()">
          Cập nhật
        </button>
      </div>
    </div>
  </div>
</div>
  </div>
  </div>
  </div>
  </div>
  <TableFilter class="mt10" v-bind="{name: 'pageparam'}" />
  </div>
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '~/components/TopMenu.vue'
import TableFilter from '~/components/TableFilter.vue'

import mixing from "@/assets/js/mixing.js";

export default {
  components: {
    TopMenu,
    TableFilter
  },

  data () {
    return {
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(),
      connection2: this.$connection(),
      connection3: this.$connection(),
      title: 'Danh sách báo cáo nội dung vi phạm',
      record: {},
      violate: {},
      values: 'id,refid,link,reporter,reporter__name,type,type__value,content,handler,handler__name,poster,poster__name,handle_method,handle_method__value,create_time'
    }
  },

  created() {
    let connlist = [{name: 'violate', url: 'data/Violate', params: {values: this.values}}]
    this.connection.getApi(connlist)
    const fields = []
    fields.push(mixing.createField('id', 'Id', 'number', false, true))
    fields.push(mixing.createField('reporter__name', 'Người báo cáo', 'string', false, true))
    fields.push(mixing.createField('type__value', 'Loại', 'string', false, true))
    fields.push(mixing.createField('poster__name', 'Người viết bài', 'string', false, true))
    fields.push(mixing.createField('content', 'Nội dung', 'string', false, true))
    fields.push(mixing.createField('refid', 'Comment ID', 'string', false, true))
    fields.push(mixing.createField('link', 'Link', 'string', false, true))
    fields.push(mixing.createField('handler__name', 'Người xử lý', 'string', false, true))
    fields.push(mixing.createField('handle_method__value', 'Xử lý', 'string', false, true))
    fields.push(mixing.createField('createtime', 'Ngày tạo', 'string', false, true))
    fields.push(mixing.createField('action', '', 'string', false, true, '8%', 'select,edit'))
    this.pageparam = {data: [], fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true,
    api: {} , origin_api: {}, reload: 0}
  },
  
  watch: {
    'connection.getdataReady': function(newVal) {
      if(newVal==='success') {
        let data = this.connection.getbatchStatus.find(v=>v.name==='violate')
        this.$store.commit('updateState', {name: 'pageparam', key: 'api', data: data})
        this.$store.commit('updateState', {name: 'pageparam', key: 'origin_api', data: data})
        this.fillData()
      }
      else if (newVal==='error') this.$router.push({path: '/error'})
    },

    'connection1.getupdateStatus': function(newVal) {
      if(newVal) {
        let found = this.api.getbyid(parseInt(this.record.handle_method))
        this.violate.deleted = found.code==='not-show'? true : false
        let ishelp = this.record.link.indexOf('/help/')>=0? true : false
        this.connection3.update(ishelp? 'helpcomment' : 'newscomment', this.violate)
      } else if(newVal===false) this.message(false)
    },

    'connection2.getdataReady': function(newVal) {
      if(newVal==='success') {
        this.violate = this.$copy(this.connection2.getbatchData[0].data[0])
        this.violate.content = mixing.stripHtml(this.violate.comment)
      }
    },

    'connection3.getupdateStatus': function(newVal) {
      if(newVal) {
        this.violate = this.connection3.getupdateRecord
        this.violate.content = mixing.stripHtml(this.violate.comment)
        this.message(true)
      } else if(newVal===false) this.message(false)
    },

    'pageparam.record': function(newVal) {
      if(newVal) {
        this.record = this.$copy(newVal)
        let ishelp = newVal.link.indexOf('/help/')>=0? true : false
        let found = {name: ishelp? 'helpcomment' : 'newscomment' , url: ishelp? 'data/Help_Comment' : 'data/News_Comment', params: {filter: {id: newVal.refid}}}
        this.connection2.getApi([found])
      }
    }
  },

  computed: {
    pageparam: {
      get: function() {return this.$store.state.pageparam},
      set: function(val) {this.$store.commit('updatePageParam', {pageparam: val})}
    },

    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    },
  },

  methods: {
    fillData() {
      let data = this.$copy(this.connection.getbatchData.find(v=>v.name==='violate').data)          
      data.map(v=>v.createtime = mixing.yyyymmddhhmm(new Date(v.create_time)))
      this.$store.commit('updateState', {name: 'pageparam', key: 'data', data: data})
    },

    close() {
      this.$store.commit('updateState', {name: 'pageparam', key: 'record', data: undefined})
      this.$store.commit('updateState', {name: 'pageparam', key: 'action', data: undefined})
    },

    update() {
      if(this.record.handle_method === this.pageparam.record.handle_method) return
      this.record.handler = this.login.id
      this.connection1.update('violate', this.record, this.values)
    },

    message(success) {
      let text = success? 'Cập nhật dữ liệu thành công' : 'Lỗi. Cập nhật dữ liệu không thành công.'
      let info = {duration: 4000, type: success? 'is-success' : 'is-danger', hasIcon: false, message: text}
      this.$buefy.notification.open(info)
    }
  }
}
</script>