<template>
<div>
      <div class="field">
      <label class="label">Người sở hữu cổ phiếu {{$route.query.stock_code}} <strong class="has-text-danger">*</strong></label>
      <div class="control">
        <PeopleSearch :people="people" @doChange="selectPeople" />
      </div>
       <p class="fs12 mt-2">Không tìm thấy trong danh sách?
          <a class="fs16 fb600 ml-3" @click="selectPeople(undefined); addNew=true">Tạo mới</a> 
          <a class="fs16 fb600 has-text-warning-dark ml-3" @click="addNew=true" v-if="people">Sửa đổi</a>
          <a class="fs16 fb600 has-text-danger ml-3" @click="confirmDelete()" v-if="people">Xóa người</a>
        </p>
    </div>
    <div class="my-5 px-5 py-5" v-if="addNew" style="border: solid 1px #b1a7a6">
      <EditPeople :people="people" @newpeople="selectPeople" @closeform="addNew=false" />
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
      <a class="button is-primary" @click="update()">Cập nhật</a>
    </div>
</div>
</template>

<script>
import PeopleSearch from '@/components/profile/PeopleSearch'
import EditPeople from '@/components/profile/EditPeople'
export default {
  components: {
    PeopleSearch,
    EditPeople
  },
  props: ['showPeople'],
  data() {
    return {
      numberOfShare: undefined,
      percentage: undefined,
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(this.$buefy),
      connection9: this.$connection(this.$buefy),
      people: undefined,
      addNew: false,
      currentRow: undefined
    }
  },
  created() {
    if(this.showPeople) this.selectPeople(this.showPeople)
  },

  watch: {
   "connection.getdataReady": function(newVal) {
      if (newVal==="success") {
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

    'connection9.getupdateStatus': function(newVal) {
      if(newVal) {
        let data = this.connection9.getupdateRecord
        if(data[0].deleted) {
          let copy = this.$copy(this.pagetask.data)
          let idx = copy.findIndex(v=>v.people===data[0].id)
          this.$delete(copy, idx)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
          this.selectPeople(undefined, true)
        } else {
          let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: 'Lỗi. Xoá dữ liệu thất bại.'}
          this.$buefy.notification.open(info)
        }
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
      this.people = undefined
    },

    selectPeople(event) {
      this.people=event
      this.numberOfShare = undefined
      this.percentage = undefined
      this.addNew=false
      if(!event) return
      let conn = {name: 'privateholder', params: {filter: {company: this.$route.query.company, people: event.id}}}
      this.connection.getApi([conn])
    },

    update() {
      if(!this.people) return
      if(this.$empty(this.numberOfShare)) {
        if(this.currentRow) this.connection1.delete('privateholder', this.currentRow.id)
      } else {
        let data = {id: this.currentRow? this.currentRow.id : undefined, people: this.people.id, company: this.$route.query.company, 
        number_share: this.$formatNumber(this.numberOfShare), percentage: this.$empty(this.percentage)? null : this.percentage }
        data.id? this.connection1.update('privateholder', data) : this.connection1.insert('privateholder', data)
      }
      let self = this
      setTimeout(function() {self.$emit('reload')}, 100)
    },

    deleteHolder() {
      if(this.currentRow) {
        this.connection2.delete('privateholder', this.$copy(this.currentRow.id))
        let copy = this.$copy(this.pagetask.data)
        let idx =copy.findIndex(v=>v.people===this.currentRow.people)
        this.$delete(copy, idx)
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      }
      else this.resetData()
    },

    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Xóa ' + this.people.name,
        message: 'Bạn có chắc chắn muốn xóa <b>' + this.people.name + '</b>? Toàn bộ thông tin về cá nhân, chức vụ, sở hữu, quan hệ sẽ bị xóa.',
        confirmText: 'Xác nhận',
        cancelText: 'Hủy bỏ',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.connection9.delete('people', [{id: this.people.id}])
      })
    },
  }
}
</script>
