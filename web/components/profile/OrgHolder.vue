<template>
  <div>
      <div class="field">
      <label class="label">Tổ chức sở hữu cổ phiếu {{$route.query.stock_code}} <strong class="has-text-danger">*</strong></label>
      <div class="control">
        <CompanySearch :company="company" @doChange="selectCompany" />
      </div>
       <p class="fs12 mt-2">Không tìm thấy trong danh sách?
          <a class="fs16 fb600 ml-3" @click="selectCompany(undefined); addNew=true">Tạo mới</a>
          <a class="fs16 fb600 has-text-warning-dark ml-3" @click="addNew=true" v-if="company">Sửa đổi</a>
          <a class="fs16 fb600 has-text-danger ml-3" @click="checkDelete()" v-if="company">Xóa công ty</a>
        </p>
    </div>

    <div class="my-5 px-5 py-5" v-if="addNew" style="border: solid 1px #b1a7a6">
      <EditCompany :company="company" @newcompany="selectCompany" @closeform="addNew=false"/>
    </div>
    
    <div class="field is-horizontal mt-5">
    <div class="field-body">
    <div class="field">
      <label class="label">Số lượng cổ phần <strong class="has-text-danger">*</strong></label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="numberOfShare">
      </div>
    </div>

    <div class="field">
      <label class="label">Tỷ lệ %</label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="percentage">
      </div>
    </div>
    <div class="field">
        <div class="control">
        <b-tooltip label="Xóa thông tin cổ đông">
          <a class="ml-2" @click="deleteHolder()">
            <span class="icon fs28  has-text-danger">
              <i class="mdi mdi-minus-thick" />
            </span>
          </a>
        </b-tooltip>
      </div>
      </div>
    </div>
    </div>
    <div class="mt-5">
      <a class="button is-primary" @click="update()"> Cập nhật </a>
    </div>
    </div>
</template>

<script>
import CompanySearch from '@/components/CompanySearch'
import EditCompany from '@/components/profile/EditCompany'
export default {
  components: {
    CompanySearch,
    EditCompany
  },
  props: ['showCompany'],
  data() {
    return {
      numberOfShare: undefined,
      percentage: undefined,
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(this.$buefy),
      connection3: this.$connection(this.$buefy),
      connection4: this.$connection(),
      connection5: this.$connection(),
      connection6: this.$connection(this.$buefy),
      company: undefined,
      currentRow: undefined,
      addNew: false
    }
  },
  created() {
    if(this.showCompany) this.selectCompany(this.showCompany)
  },
  watch: {
   "connection.getdataReady": function(newVal) {
      if (newVal === "success") {
        let data = this.connection.getbatchData[0].data
        let found = data.length>0? data[0] : undefined
        if(found) {
          this.numberOfShare = found.number_share
          this.percentage = found.percentage
          this.currentRow = found
        }
      }
    },

    'connection1.getupdateRecord': function(newVal) {
      if(newVal) this.resetData()
    },

    'connection2.getupdateStatus': function(newVal) {
      if(newVal) this.resetData()
    },

    "connection3.getdataReady": function(newVal) {
      if(newVal== "success") {
        let found = false
        let filter = this.connection3.getbatchData.filter(v=>['tasklist', 'stockprice', 'taskprofile'].findIndex(x=>x===v.name)>=0)
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
              let holder = this.connection3.getbatchData.find(v=>v.name==='orgholder').data
              let subsidiary = this.connection3.getbatchData.find(v=>v.name==='subsidiary').data
              if(holder.length>0) this.connection4.delete('orgholder', holder)
              else if(subsidiary.length>0) this.connection5.delete('subsidiary', subsidiary)
              else this.connection6.delete('companylist', this.company.id)
            }
          })
        }
      }
    },

    'connection4.getupdateStatus': function(newVal) {
      if(newVal) {
        let subsidiary = this.connection3.getbatchData.find(v=>v.name==='subsidiary').data
        if(subsidiary.length>0) this.connection5.delete('subsidiary', subsidiary)
        else this.connection6.delete('companylist', this.company.id)
      }
    },

    'connection5.getupdateStatus': function(newVal) {
      if(newVal) this.connection6.delete('companylist', this.company.id)
    },

    'connection6.getupdateStatus': function(newVal) {
      if(newVal) {
        if(this.currentRow) {
          let copy = this.$copy(this.pagetask.data)
          let idx =copy.findIndex(v=>v.id===this.currentRow.id)
          this.$delete(copy, idx)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
        }
        this.selectCompany()
      }
    },
  },

  computed: {
    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
    }
  },

  methods: {
    resetData() {
      this.currentRow = undefined
      this.numberOfShare = undefined
      this.percentage = undefined
      this.company = undefined
    },

    selectCompany(event) {
      this.company = event
      this.addNew = false
      this.numberOfShare = undefined
      this.percentage = undefined
      if(!event) return
      let conn = {name: 'orgholder', params: {filter: {organization: event.id, company: this.$route.query.company}}}
      this.connection.getApi([conn])
    },

    update() {
      if(!this.company) return
      if(this.$empty(this.numberOfShare)) {
        if(this.currentRow) this.connection1.delete('orgholder', this.currentRow.id)
      } else {
        let data = {id: this.currentRow? this.currentRow.id : undefined, organization: this.company.id, company: this.$route.query.company, 
        number_share: this.$formatNumber(this.numberOfShare), percentage: this.$empty(this.percentage)? null : this.percentage }
        data.id?  this.connection1.update('orgholder', data) : this.connection1.insert('orgholder', data)
      }
      let self = this
      setTimeout(function() {self.$emit('reload')}, 100)
    },

    deleteHolder() {
      if(this.currentRow) {
        this.connection2.delete('orgholder', this.$copy(this.currentRow.id))
        let copy = this.$copy(this.pagetask.data)
        let idx =copy.findIndex(v=>v.id===this.currentRow.id)
        this.$delete(copy, idx)
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      }
      else this.resetData()
    },

    checkDelete() {
      let conn1 = this.connection3.find('tasklist')
      conn1.params = {values: 'id', filter: {company: this.company.id}}
      let conn2 = this.connection3.find('stockprice')
      conn2.params = {values: 'id', filter: {company: this.company.id}}
      let conn3 = this.connection3.find('taskprofile')
      conn3.params = {values: 'id', filter: {company: this.company.id}}
      let conn4 = this.connection3.find('orgholder')
      conn4.params.filter = {organization: this.company.id}
      let conn5 = this.connection3.find('subsidiary')
      conn5.params.filter = {subsidiary: this.company.id}
      this.connection3.getApi([conn1, conn2, conn3, conn4, conn5])
    }
  }
}
</script>
