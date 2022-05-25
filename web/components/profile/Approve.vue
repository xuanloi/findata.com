<template>
<div class="modal is-active">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="$store.state.ismobile? '' : 'width:35%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close"
      @click="close()"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
    <template v-if="task.status__code==='entered' || task.status__code==='not-yet-entered'">
      <article class="message">
      <div class="message-header">
        <p>Gửi báo cáo</p>
      </div>
      <div class="message-body">
        Gửi báo cáo đi sẽ không thay đổi được dữ liệu đã nhập nếu không có yêu cầu sửa lại. Bạn có muốn tiếp tục không?
      </div>
    </article>
      <p><a class="button is-primary" @click="send()">Gửi đi</a></p>
    </template>
    <template v-else-if="rightApprove">
      <article class="message is-light">
          <div class="message-body pt5 pb5 has-text-left">
            <label class="label is-medium pb5">{{this.api.getvalue(this.api.find3var('information','approved','label'))}}</label>
            <div class="field has-addons">
              <div class="control is-expanded">
                <div class="select is-fullwidth">
                <select name="country" v-model="selected">
                  <option v-for="(item,key) in approvelist" :key="key" :value="item">{{api.getvalue(item)}}</option>
                </select>
                </div>
              </div>
              <div class="control">
                  <button type="submit" class="button is-primary" @click="approveTask()">{{this.api.getvalue(this.api.find3var('information','choose','label'))}}</button>
              </div>
              </div>
          </div>
      </article>
      <div class="field" v-if="selected? selected.code==='retype' : false">
        <div class="control">
          <textarea class="textarea is-primary" v-model="retypeReason" rows="4" :placeholder="api.getvalue(api.find3var('information','reason','label'))"></textarea>
        </div>
      </div>
      </template>
      <template v-else-if="task.status__code==='approved'">
      <article class="message is-primary">
      <div class="message-header">
        <p>Thông tin</p>
      </div>
      <div class="message-body">
        {{message}}
      </div>
    </article>
    </template>
    <template v-else-if="task.status__code==='retype'">
      <article class="message is-danger">
      <div class="message-header">
        <p>Sửa báo cáo</p>
      </div>
      <div class="message-body">
        {{message}}
      </div>
    </article>
    <p><a class="button is-primary" @click="send()">Gửi lại báo cáo</a></p>
    </template>
    </section>
  </div>
  </div>
</template>

<script>
export default {
  props: ['task'],
  data() {
    return {
      selected: undefined,
      connection: this.$connection(this.$buefy),
      approvelist: [],
      rightApprove: false,
      retypeReason: undefined,
      message: undefined
    }
  },
  created() {
    window.addEventListener('keydown', (e) => {if(e.key == 'Escape') this.close()})
    this.checkRights()
    this.selected = this.api.find3var('list','task-status', this.task.status__code)
    this.retypeReason = this.task.detail
  },
  watch: {
    'connection.getupdateRecord': function(newVal) {
      if(newVal) {
        this.$emit('changetask', this.connection.getupdateRecord)
        this.close()
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
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    send() {
      this.selected = this.api.find3var('list','task-status', 'waiting-approve') 
      this.approveTask()
    },
    checkRights() {
      let status = this.api.getbyid(this.task.status)
      let type = this.login.type
      if(status.code==='retype') {
        this.message = 'Báo cáo được yêu cầu sửa lại với lý do: ' +  this.task.detail
      }

      if(type.code==='staff' || type.code==='ctv') {
        if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {
          this.message = 'Báo cáo đang ở trạng thái chờ duyệt. Bạn không thể thay đổi được thông tin.'
        }
      } else {
        if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {
          this.rightApprove = true
          this.approvelist = []
          this.approvelist.push(this.api.find3var('list','task-status','waiting-approve'))
          this.approvelist.push(this.api.find3var('list','task-status','waiting-approve-2'))
          this.approvelist.push(this.api.find3var('list','task-status','retype'))
          if(type.code==='admin' || type.code==='manager') {
            this.approvelist.push(this.api.find3var('list','task-status','approved'))
          }
        } else if(status.code==='approved') {
          this.message = 'Báo cáo đã được duyệt. Bạn không thể thay đổi được thông tin.'
        }
      }
    },
    approveTask() {
      let copy = this.$copy(this.task)
      copy.detail = this.retypeReason
      if(this.selected.code==='waiting-approve' && this.$empty(copy.waiting1_time)) copy.waiting1_time = new Date()
      if(this.selected.code==='waiting-approve-2' && this.$empty(copy.waiting2_time)) copy.waiting2_time = new Date()
      if(this.selected.code==='approved' && this.$empty(copy.approve_time)) copy.approve_time = new Date()
      copy.update_time = new Date()
      let values = 'id,company,company__name,company__stock_code,company__type__code,report_period,report_period__code,report_period__value,year,report_name,report_name__code,'
      values += 'assigner,assigner__name,recipient,recipient__name,assign_date,due_date,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time,detail'
      copy.status = this.selected.id
      this.connection.update('taskprofile', copy, values)
    }
  }
}
</script>