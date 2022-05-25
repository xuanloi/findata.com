<template>
<div>
  <div class="columns mb-0">
  <div class="column is-4">
    <p class="ml-6">
    <strong class="mr-3"> Hiển thị cổ đông theo: </strong>
    <b-radio v-model="radio" v-for="v in choices" :key="v.code"
      :native-value="v">
      {{v.name}}
    </b-radio>
    </p>
  </div>
  <div class="column is-5" v-if="editable">
    <a class="button is-dark is-rounded fs13" @click="openModal()"> Thêm cổ đông</a>
    </div>
  </div>
  <TableFilter class="mx-4" v-bind="{name: 'pagetask'}" />

  <div class="modal is-active" v-if="open">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:48%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="open=false"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <p class="title mb-5">Thêm cổ đông <strong class="has-text-danger ml-3">{{$route.query.stock_code}}</strong></p>
      <b-radio v-model="type" v-for="(v,i) in types" :key="i"
        :native-value="v.code">
        {{v.name}}
      </b-radio>
      <PrivateHolder class="mt-5 pt-3" v-bind="{showPeople: showPeople}" @reload="reload(radio)" v-if="type==='private'" />
      <OrgHolder class="mt-5 pt-3" v-bind="{showCompany: showCompany}" @reload="reload(radio)" v-else-if="type==='org'" />
    </section>
    </div>
  </div>
</div>
</template>

<script>
import PrivateHolder from '@/components/profile/PrivateHolder.vue'
import OrgHolder from '@/components/profile/OrgHolder.vue'
import Export from '@/assets/js/export.js'
export default {
  components: {
    PrivateHolder,
    OrgHolder
  },
  props: ['editable'],
  data() {
    return {
      choices: [{code: 'private', name: 'Cá nhân'}, {code: 'org', name: 'Tổ chức'}],
      radio: {code: 'private', name: 'Cá nhân'},
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(),
      open: false,
      type: 'private',
      types: [{code: 'private', name: 'Cổ đông cá nhân'}, {code: 'org', name: 'Cổ đông tổ chức'}],
      showPeople: undefined,
      showCompany: undefined
    }
  },

  created() {
    window.addEventListener('keydown', (e) => {
      if(e.key == 'Escape' && this.open) this.open = false
    })
    this.getPrivateHolder()
  },

  watch: {
    "connection.getdataReady": function(newVal) {
      if(newVal==="success") this.fillData()
    },

    "connection1.getdataReady": function(newVal) {
      if (newVal==="success") {
        if(this.type==='private') this.showPeople = this.connection1.getbatchData[0].data[0]
        else this.showCompany = this.connection1.getbatchData[0].data[0]
        this.open = true
      }
    },

    radio: function(newVal) {
      this.reload(newVal)
      if(newVal) this.type = newVal.code
    },

    menuaction: function(newVal) {
      if(newVal? newVal.action==='download': false) {
        let types = {} 
        this.pagetask.fields.map(v=>types[v.name] = 'String')
        this.$exportExcel(this.pagetask.data, 'shareholder', this.pagetask.fields.map(v=>v.name), types)
      }
    },

    'pagetask.record': function(newVal) {
      if(newVal) {
        if(this.pagetask.action==='show') {
          let conn = {name: 'people', url: 'data/People', params: {filter: {id: newVal.people},
          values: 'id,uid,name,legal_id,avatar,address,phone,email,dob,domicile,management__position,management__position__code,management__position__value,management__company,management__company__stock_code'}}
          if(this.type==='org') conn = {name: 'company', url: 'data/Company', params: {filter: {id: newVal.organization}}}    
          this.connection1.getApi([conn])
        }
        this.$store.commit('updateState', {name: 'pagetask', key: 'record', data: undefined})
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile },
      set: function(val) {this.$store.commit('updateIsMobile', {ismobile: val})}
    },
    
    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    },
  },

  methods: {
    openModal() {
      this.open = true
      this.showPeople = undefined
      this.showCompany = undefined
    },

    reload(newVal) {
       newVal.code==='private'? this.getPrivateHolder() : this.getOrgHolder()
    },

    getPrivateHolder() {
      let fields = []
      fields.push(this.$createField('id', 'Id', 'number', true, true))
      fields.push(this.$createField('company__stock_code', 'Cổ phiếu', 'string', true, true))
      let field = this.$createField('people__name', 'Họ tên', 'string', true, true)
      field.style = {list: [{value: this.$route.query.stock_code, class: 'button is-small is-primary is-outlined has-text-dark'}],
        condition: 'company__stock_code', click: true}
      fields.push(field)
      fields.push(this.$createField('number_share', 'Số lượng CP', 'number', true, true))
      fields.push(this.$createField('percentage', 'Tỷ lệ', 'string', true, true))
      fields.push(this.$createField('people__uid', 'Mã định danh', 'string', true, true))
      fields.push(this.$createField('action', '', 'string', true, true, '7%', 'delete'))
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
      enableDelete: true, enableApprove: true, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
      let values = 'id,people,people__name,number_share,percentage,company,company__stock_code,people__uid'
      this.connection.getApi([{name: 'privateholder', params: {values: values, filter: {company: this.$route.query.company}}}])
    },

    getOrgHolder() {
      let fields = []
      fields.push(this.$createField('id', 'Id', 'number', true, true))
      fields.push(this.$createField('company__stock_code', 'Cổ phiếu', 'string', true, true))
      let field = this.$createField('organization__name', 'Tên tổ chức', 'string', true, true)
      field.style = {list: [{value: this.$route.query.stock_code, class: 'button is-small is-primary is-outlined has-text-dark'}],
        condition: 'company__stock_code', click: true}
      fields.push(field)

      fields.push(this.$createField('number_share', 'Số lượng CP', 'number', true, true))
      fields.push(this.$createField('percentage', 'Tỷ lệ', 'string', true, true))
      fields.push(this.$createField('organization__stock_code', 'Mã định danh', 'string', true, true))
      fields.push(this.$createField('action', '', 'string', true, true, '7%', 'delete'))
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
      enableDelete: true, enableApprove: true, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
      let values = 'id,organization,organization__name,organization__stock_code,number_share,percentage,company,company__stock_code'
      this.connection.getApi([{name: 'orgholder', params: {values: values, filter: {company: this.$route.query.company}}}])
    },

    fillData() {
      let data = this.$copy(this.connection.getbatchData[0].data)
      data.map(v=>{
        v.number_share = v.number_share? this.$numtoString(v.number_share.toFixed(2)) : null
        v.percentage = v.percentage? this.$numtoString(v.percentage.toFixed(2)) : null
     })
      this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
      this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
      if(Object.keys(this.pagetask.origin_api).length===0) {
        this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
      }
    },

    exportData() {
      var _export = new Export()
      let dataTypes = {}
      this.pagetask.fields.forEach(v => {dataTypes[v.name] = 'String'})
      _export.set(this.pagetask.filter, 'subsidiary-list', dataTypes, this.pagetask.fields.map(v=>v.name))
      _export.exportfile()
    }        
  }
}
</script>
