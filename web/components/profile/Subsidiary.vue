<template>
<div>
  <div class="buttons mx-6 mb-0 mt-0" v-if="editable">
    <a class="button is-dark is-rounded fs13" @click="openModal()">Thêm công ty</a>
    <a class="button is-dark is-rounded fs13" @click="open=true; menu='excel'">Nhập từ Excel</a>
  </div>
  <TableFilter class="mx-4" v-bind="{name: 'pagetask'}" />
  <div class="modal is-active" v-if="open && menu==='manual'">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:48%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="close()"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <p class="title">Thêm công ty con, liên kết với <strong class="has-text-danger ml-2">{{$route.query.stock_code}}</strong></p>
      <div class="field">
        <label class="label">Chọn công ty <strong class="has-text-danger">*</strong></label>
        <div class="control">
          <CompanySearch :company="company" @doChange="selectCompany" />
        </div>
        <p class="fs12 mt-2">Không tìm thấy trong danh sách?
          <a class="fs16 fb600 ml-3" @click="resetValue(); addNew=true">Tạo mới</a>
          <a class="fs16 fb600 has-text-warning-dark ml-3" @click="addNew=true" v-if="company">Sửa đổi</a>
          <a class="fs16 fb600 has-text-danger ml-3" @click="checkDelete()" v-if="company">Xóa công ty</a>
        </p>
      </div>
            
      <div class="my-5 px-5 py-5" v-if="addNew" style="border: solid 1px #b1a7a6">
        <EditCompany :company="company" @newcompany="company=$event; addNew=false" @closeform="addNew=false"/>
      </div>

      <p class="has-text-right">
        <b-tooltip position="is-left" label="Xóa thông tin công ty con">
          <a class="mr-4" @click="deleteSubsidiay()">
            <span class="icon fs28  has-text-danger">
              <i class="mdi mdi-minus-thick" />
            </span>
          </a>
        </b-tooltip>
      </p>
      <div class="mb-5 px-5 pb-5" style="border: solid 1px #b1a7a6">
       <div class="field is-horizontal mt-5">
        <div class="field-body">
          <div class="field">
          <label class="label">Vốn góp <strong class="has-text-danger">*</strong></label>
          <div class="control">
            <input class="input" type="text" placeholder="" v-model="capital">
          </div>
        </div>
        <div class="field">
          <label class="label">Tỷ lệ biểu quyết (%)</label>
          <div class="control">
            <input class="input" type="text" placeholder="" v-model="voting_rate">
          </div>
        </div>
        </div>
        </div>
        <div class="field is-horizontal mt-5">
        <div class="field-body">
        <div class="field">
          <label class="label">Tỷ lệ lợi ích (%) <strong class="has-text-danger">*</strong></label>
          <div class="control">
            <input class="input" type="text" placeholder="" v-model="percentage">
          </div>
        </div>
        <div class="field">
          <label class="label">Loại công ty con <strong class="has-text-danger">*</strong></label>
          <div class="control">
            <b-autocomplete
            :v-model="subsidiary"
            :value="subsidiary? subsidiary.value : null"
            :data="subsidiaries"
            keep-first
            clearable
            icon-right="magnify"
            field="value"
            :open-on-focus="true"
            @select="option => option? subsidiary = option : false">
          </b-autocomplete>
          </div>
          <p class="mt-3 fs14 has-text-warning-dark" v-if="company">Sàn giao dịch: {{company.listed_on}}</p>
        </div>
        </div>
      </div>
      </div>
    <div class="my-5">
      <a class="button is-primary" @click="update()"> Cập nhật </a>
    </div>
    </section>
    </div>
  </div>

  <div class="modal is-active" v-if="open && menu==='excel'">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:75%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="close()"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <ImportSub @reload="loadData()" />
    </section>
    </div>
  </div>
</div>
</template>

<script>
import Connection from '@/assets/js/connection.js'
import CompanySearch from '@/components/CompanySearch'
import EditCompany from '@/components/profile/EditCompany'
export default {
  components: {
    CompanySearch,
    EditCompany,
    ImportSub: () => import('@/components/profile/ImportSub')
  },
  props: ['editable'],
  data() {
    return {
      connection: new Connection(this.$store, this.$buefy),
      connection1: new Connection(this.$store, this.$buefy),
      connection2: new Connection(this.$store, this.$buefy),
      connection3: new Connection(this.$store),
      connection4: new Connection(this.$store, this.$buefy),
      connection5: new Connection(this.$store),
      connection6: new Connection(this.$store),
      connection7: new Connection(this.$store),
      connection8: new Connection(this.$store, this.$buefy),
      open: false,
      addNew: false,
      company: undefined,
      capital: undefined,
      percentage: undefined,
      subsidiaries: [],
      subsidiary: undefined,
      currentRow: undefined,
      voting_rate: undefined,
      menu: 'manual'
    }
  },

  created() {
     window.addEventListener('keydown', (e) => {
      if (e.key == 'Escape' && this.open) this.open = false
    })
    this.subsidiaries = this.$copy(this.api.filter2var('list', 'subsidiary'))
    this.loadData()
  },

  watch: {
    "connection.getdataReady": function(newVal) {
      if (newVal === "success") {
        let data = this.$copy(this.connection.getbatchData[0].data)
        data.map(v=>{
          v.capital = v.capital? this.$numtoString(v.capital.toFixed(2)) : undefined
          v.percentage = v.percentage? this.$numtoString(v.percentage.toFixed(2)) : undefined
          v.voting_rate = v.voting_rate? this.$numtoString(v.voting_rate.toFixed(2)) : undefined
        })
        this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        if(Object.keys(this.pagetask.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection.getbatchStatus[0])})
        }
      }
    },
    
    'connection1.getupdateStatus': function(newVal) {
      if(newVal) this.$emit('updatetask')
    },

    "connection2.getdataReady": function(newVal) {
      if (newVal === "success") {
        let data = this.connection2.getbatchData[0].data
        let found = data.length>0? data[0] : undefined
        if(found) {
          this.capital = found.capital
          this.percentage = found.percentage
          this.voting_rate = found.voting_rate
          this.subsidiary = this.subsidiaries.find(v=>parseInt(v.id)===found.type)
          this.currentRow = found
        }
      }
    },

    "connection3.getdataReady": function(newVal) {
      if (newVal === "success") {
        this.selectCompany(this.connection3.getbatchData[0].data[0])
        this.open = true
        this.menu = 'manual'
      }
    },

    'connection4.getupdateStatus': function(newVal) {
      if(newVal) this.close(true)
    },

    "connection5.getdataReady": function(newVal) {
      if(newVal== "success") {
        let found = false
        let filter = this.connection5.getbatchData.filter(v=>['tasklist', 'stockprice', 'taskprofile'].findIndex(x=>x===v.name)>=0)
        filter.map(v=>{if(v.data.length>0) found = true})
        if(found) {
          let info = {duration: 4000, type: 'is-danger', hasIcon: false,
          message: 'Dữ liệu / tài chính / giao dịch / hồ sơ / gắn với công ty này đã có. Không thể xóa công ty này.'}
          this.$buefy.notification.open(info)
        }
        else {
           this.$buefy.dialog.confirm({
            title: 'Xóa công ty: ' + this.company.stock_code,
            message: 'Bạn có chắc chắn muốn xóa <b>' + this.company.name + '</b>? Toàn bộ thông tin về công ty, sở hữu, công ty con sẽ bị xóa.',
            confirmText: 'Xác nhận',
            cancelText: 'Hủy bỏ',
            type: 'is-danger',
            hasIcon: true,
            onConfirm: () => {
              let holder = this.connection5.getbatchData.find(v=>v.name==='orgholder').data
              let subsidiary = this.connection5.getbatchData.find(v=>v.name==='subsidiary').data
              if(holder.length>0) this.connection6.delete('orgholder', holder)
              else if(subsidiary.length>0) this.connection7.delete('subsidiary', subsidiary)
              else this.connection8.delete('companylist', this.company.id)
            }
          })
        }
      }
    },

    'connection6.getupdateStatus': function(newVal) {
      if(newVal) {
        let subsidiary = this.connection5.getbatchData.find(v=>v.name==='subsidiary').data
        if(subsidiary.length>0) this.connection6.delete('subsidiary', subsidiary)
        else this.connection7.delete('companylist', this.company.id)
      }
    },

    'connection7.getupdateStatus': function(newVal) {
      if(newVal) this.connection8.delete('companylist', this.company.id)
    },

    'connection8.getupdateStatus': function(newVal) {
      if(newVal) {
        if(this.currentRow) {
          let copy = this.$copy(this.pagetask.data)
          let idx =copy.findIndex(v=>v.id===this.currentRow.id)
          this.$delete(copy, idx)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
        }
        this.close(true)
      }
    },

    menuaction: function(newVal) {
      if(newVal? newVal.action==='download': false) {
        let types = {} 
        this.pagetask.fields.map(v=>types[v.name] = 'String')
        this.$exportExcel(this.pagetask.data, 'subsidiary-list', this.pagetask.fields.map(v=>v.name), types)
      }
    },

    'pagetask.record': function(newVal) {
      if(newVal) {
        if(this.pagetask.action==='show') {
          let conn = {name: 'company', url: 'data/Company', params: {filter: {id: newVal.subsidiary}}}    
          this.connection3.getApi([conn])
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
    resetValue() {
      this.company = undefined
      this.percentage = undefined
      this.capital = undefined
      this.voting_rate = undefined
      this.subsidiary = undefined
    },

    selectCompany(event) {
      this.company = event
      let conn = {name: 'subsidiary', params: {filter: {company: this.$route.query.company, subsidiary: event.id}}}
      this.connection2.getApi([conn])
      if(this.addNew) this.addNew = false
      this.percentage = undefined
      this.capital = undefined
      this.voting_rate = undefined
      this.subsidiary = undefined
    },

    openModal() {
      this.company=undefined
      this.addNew=false
      this.open=true
      this.menu = 'manual'
    },

    loadData() {
      let fields = []
      fields.push(this.$createField('subsidiary__stock_code', 'Mã định danh', 'string', true, true))
      let field = this.$createField('subsidiary__name', 'Tên công ty', 'number', true, true)
      field.style = {list: [{value: parseInt(this.$route.query.company), class: 'button is-small is-primary is-outlined has-text-dark'}],
        condition: 'company', click: true}
      fields.push(field)
      fields.push(this.$createField('subsidiary__listed_on', 'Sàn GD', 'string', true, true))
      fields.push(this.$createField('capital', 'Vốn góp', 'string', true, true))
      fields.push(this.$createField('percentage', 'Tỷ lệ lợi ích (%)', 'string', true, true))
      fields.push(this.$createField('voting_rate', 'Tỷ lệ biểu quyết (%)', 'string', true, true))
      fields.push(this.$createField('type__value', 'Loại cty con', 'string', true, true))
      fields.push(this.$createField('action', '', 'string', false, true, '7%', 'delete'))
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
      enableDelete: true, enableApprove: true, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
      let values = 'id,company,subsidiary,subsidiary__stock_code,subsidiary__name,capital,percentage,voting_rate,type,type__value,subsidiary__listed_on'
      this.connection.getApi([{name: 'subsidiary', params: {values: values, filter: {company: this.$route.query.company}}}])
    },

    update() {
      if(!this.company || !this.subsidiary) return
      if(this.$empty(this.percentage)) {
        if(this.currentRow) {
          let conn = new Connection(this.$store)
          conn.delete('subsidiary', this.currentRow.id)
        }
      } else {
        let data = {id: this.currentRow? this.currentRow.id : undefined, 
        voting_rate: this.$empty(this.voting_rate)? null : this.$formatNumber(this.voting_rate),
        company: this.$route.query.company, subsidiary: this.company.id, 
        capital: this.$empty(this.capital)? null : this.$formatNumber(this.capital),
        percentage: this.$empty(this.percentage)? null : this.$formatNumber(this.percentage), type: this.subsidiary.id}
        data.id? this.connection1.update('subsidiary',  data) : this.connection1.insert('subsidiary',  data)
      }
      let self = this
      setTimeout(function() {
        self.loadData()
        self.close(true)
      }, 100)
    },

    close(keepForm) {
      this.capital = undefined
      this.voting_rate = undefined
      this.percentage = undefined
      this.subsidiary = undefined
      this.company = undefined
      this.currentRow = undefined
      if(!keepForm) this.open = false
    },

    deleteSubsidiay() {
      if(this.currentRow) {
        this.connection4.delete('subsidiary', this.$copy(this.currentRow.id))
        let copy = this.$copy(this.pagetask.data)
        let idx =copy.findIndex(v=>v.subsidiary===this.currentRow.subsidiary)
        this.$delete(copy, idx)
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      }
      else this.close(true)
    },

    checkDelete() {
      let conn1 = this.connection5.find('tasklist')
      conn1.params = {values: 'id', filter: {company: this.company.id}}
      let conn2 = this.connection5.find('stockprice')
      conn2.params = {values: 'id', filter: {company: this.company.id}}
      let conn3 = this.connection5.find('taskprofile')
      conn3.params = {values: 'id', filter: {company: this.company.id}}
      let conn4 = this.connection5.find('orgholder')
      conn4.params.filter = {organization: this.company.id}
      let conn5 = this.connection5.find('subsidiary')
      conn5.params.filter = {subsidiary: this.company.id}
      this.connection5.getApi([conn1, conn2, conn3, conn4, conn5])
    }
  }
}
</script>