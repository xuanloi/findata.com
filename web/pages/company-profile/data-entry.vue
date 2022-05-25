<template>
  <div>
    <TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}" @approve="changeApprove" @edit="changeMode" />
    <div class="tabs is-boxed mt-6 pt-5 mb-4">
      <ul>
        <li :class="activeTab===v.code? 'is-active fb900' : null" @click="activeTab=v.code"
        v-for="v in menulist" :key="v.code">
          <a :class="activeTab===v.code? 'has-text-primary' : null">
            <span class="icon is-small fs25"><i :class="v.icon" aria-hidden="true"></i></span>
          <span>{{v.name}}</span>
        </a>
      </li>
    </ul>
  </div>
    <Upload v-if="activeTab==='document'" v-bind="{editable: editable}" />
    <ShareHolder v-bind="{editable: editable}" v-else-if="activeTab==='shareholder'" />
    <Management v-bind="{editable: editable}" v-else-if="activeTab==='management'" @updatetask="updateTask" />
    <Subsidiary v-bind="{editable: editable}" v-else-if="activeTab==='subsidiary'" @updatetask="updateTask" />
    <div class="columns is-centered" v-else-if="activeTab==='general' && company">
      <div class="column is-6">
        <EditCompany v-bind="{company: company, embedded: true, editable: editable}" />
      </div>
    </div>
    <News v-bind="{editable: editable}" v-else-if="activeTab==='news'" />
    <Approve :task="task" v-if="open" @close="open=false" @changetask="changeTask" />
  </div>
</template>

<script>
import Upload from '@/components/profile/Upload'
import ShareHolder from '@/components/profile/ShareHolder'
import Management from '@/components/profile/Management'
import Subsidiary from '@/components/profile/Subsidiary'
export default {
  components: {
    Upload,
    ShareHolder,
    Management,
    Subsidiary,
    EditCompany: () => import("@/components/profile/EditCompany"),
    News: () => import("@/components/profile/News"),
    Approve: () => import("@/components/profile/Approve")
},
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      tophead: 'Nhập hồ sơ công ty ' + this.$route.query.stock_code,
      menulist: [{code: 'general', name: 'Thông tin chung', icon: 'mdi mdi-information'}, {code: 'management', name: 'Ban lãnh đạo', icon: 'mdi mdi-account-group'}, 
      {code: 'shareholder', name: 'Cơ cấu cổ đông', icon: 'mdi mdi-chart-pie'}, {code: 'subsidiary', name: 'Công ty con & liên kết', icon: 'mdi mdi-sitemap'}, 
      {code: 'document', name: 'Tài liệu công bố', icon: 'mdi mdi-file'}, {code: 'news', name: 'Tin tức', icon: 'mdi mdi-newspaper-variant'}],
      activeTab: 'general',
      errors: [],
      issue_date: undefined,
      minDate: new Date('1990-01-01'),
      maxDate: new Date(),
      isLoading: false,
      company: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      task: {},
      open: false,
      editable: true,
      values: undefined
    }
  },
  created() {
    this.values = 'id,company,company__name,company__stock_code,company__type__code,report_period,report_period__code,report_period__value,year,report_name,report_name__code,'
    this.values += 'assigner,assigner__name,recipient,recipient__name,assign_date,due_date,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time,detail'
    let found = {name: 'company', url: 'data/Company', params: {filter: {id:this.$route.query.company}}}
    let conn = this.connection.find('taskprofile')
    conn.params = {filter: {id: this.$route.query.task}, values: this.values}
    this.connection.getApi([found, conn])
  },
  watch: {
    "connection.getdataReady": function(newVal) {
      if (newVal==="success") {
        this.company = this.connection.getbatchData.find(v=>v.name==='company').data[0]
        this.task = this.connection.getbatchData.find(v=>v.name==='taskprofile').data[0]
        if(this.task.status__code==='approved') this.editable = false
        this.getHeader()
      }
    },
    'connection1.getupdateRecord': function(newVal) {
      if(newVal) {
        this.task = this.connection1.getupdateRecord
        this.getHeader()
      }
    }
  },
  methods: {
    changeApprove() {
      this.open = true
      this.getHeader()
    },
    changeMode() {
      if(this.editable) return this.$buefy.snackbar.open('Chế độ sửa đổi đang được mở')
      let arr = ['manager', 'admin']
      if(arr.findIndex(v=>v===this.login.type.code)<0) {
        return this.$buefy.snackbar.open('Bạn không có quyền sửa dữ liệu')
      }
      this.editable = true
      this.$buefy.snackbar.open('Chế độ sửa đổi dữ liệu đã được mở')
      this.getHeader()
    },
    getHeader() {
      this.tophead = `<div>Nhập hồ sơ công ty: <b>${this.$route.query.stock_code}</b><span class="ml-6">Trạng thái công việc:
      <a class="${this.task.status__code==='retype'? 'has-text-danger' : 'has-text-primary'}" @click="$emit('clickevent', 'approve')">
      <b>${this.task.status__value}</b></a></span><span class="ml-6">Chế độ sửa đổi:
      <a class="${this.editable? 'has-text-primary' : 'has-text-danger'}" @click="$emit('clickevent', 'edit')"><b>${this.editable? 'Mở' : 'Đóng'}</b></a></span></div>`
    },
    changeTask(event) {
      this.task = event
      this.getHeader()
    },
    updateTask() {
      if(this.task.status__code==='not-yet-entered') {
        let copy = this.$copy(this.task)
        copy.status = 242
        copy.entry_time = new Date()
        copy.update = new Date()
        this.connection1.update('taskprofile', copy, this.values)
      }
    }
  },
  computed: {
    title() {
      let found = this.menulist.find(v=>v.code===this.activeTab)
      return `${this.$route.query.stock_code} - ${found.name}`
    },
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    }
  }
}
</script>