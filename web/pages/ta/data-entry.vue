<!-- eslint-disable -->
<template>
<div v-if="dataready===true">
<TopMenu v-bind="{type: 'tophead', tophead: this.tophead}"></TopMenu>
<section class="hero mt60">
  <div class="hero-body is-marginless pl0 pr0 pt7 pb40">
    <div class="columns is-multiline is-mobile">
<div class="column is-10">
<div class="steps">
  <div class="step-item" :class="result.find(v=>v.name==='assign') !==undefined? result.find(v=>v.name==='assign').value : ''">
    <div class="step-marker">1</div>
    <div class="step-details">
      <p class="step-title is-size-5"><span class="font-smaller"> Giao việc </span></p>
    <p class="is-size-7 pt5 has-text-grey"> {{task.assignDate}} </p>
    </div>
  </div>
  <div class="step-item" :class="result.find(v=>v.name==='entered') !==undefined? result.find(v=>v.name==='entered').value : ''">
    <div class="step-marker">2</div>
    <div class="step-details">
      <p class="step-title is-size-5"> <span class="font-smaller"> Đang nhập </span></p>
    <p class="is-size-7 pt5 has-text-grey"> {{task.entry_time===null? undefined : showTime(task.entry_time)}} </p>
    </div>
  </div>
<div class="step-item" :class="result.find(v=>v.name==='waiting-approve') !==undefined? result.find(v=>v.name==='waiting-approve').value : ''">
    <div class="step-marker">3</div>
    <div class="step-details">
      <p class="step-title is-size-5"> <span class="font-smaller"> Chờ duyệt 1</span></p>
       <p class="is-size-7 pt5 has-text-grey">{{task.waiting1_time===null? undefined : showTime(task.waiting1_time)}} </p>    
    </div>
  </div>

  <div class="step-item" :class="result.find(v=>v.name==='waiting-approve-2') !==undefined? result.find(v=>v.name==='waiting-approve-2').value : ''">
    <div class="step-marker">4</div>
    <div class="step-details">
    <p class="step-title is-size-5"><span class="font-smaller"> Chờ duyệt 2</span></p>
        <p class="is-size-7 pt5 has-text-grey">{{task.waiting2_time===null? undefined : showTime(task.waiting2_time)}} </p>    
    </div>
  </div>

    <div class="step-item" :class="result.find(v=>v.name==='approved') !==undefined? result.find(v=>v.name==='approved').value : ''">
    <div class="step-marker">5</div>
    <div class="step-details">
    <p class="step-title is-size-5"><span class="font-smaller"> Đồng ý</span></p>
    <p class="is-size-7 pt5 has-text-grey">{{task.approve_time===null? undefined : showTime(task.approve_time)}} </p>    
    </div>
  </div>
</div>
 </div>
 <div class="column is-2">
    <span class="button is-primary is-outlined pl5 pr5 pt0 pb0" @click="closeWindow()">
        <i class="mdi mdi-close is-size-4"></i>
    </span>
 </div>

<div class="column is-8 has-text-dark pt5">
<nav class="level is-mobile">
    <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Mã</p>
      <p class="font-smaller mt5">{{task.id}}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Ngày dữ liệu</p>
      <p class="font-smaller mt5">{{task.stock_date}}</p>
    </div>
  </div>
    <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Tên báo cáo</p>
      <p class="font-smaller mt5">{{task.report_name__value}}</p>
    </div>
  </div>
    <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Người giao</p>
      <p class="font-smaller mt5">{{task.assigner__name}}</p>
    </div>
  </div>
      <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Người nhận</p>
      <p class="font-smaller mt5">{{task.recipient__name}}</p>
    </div>
  </div>
</nav>
</div>

    <div class="column is-4 pt5">
    <div class="tabs">
    <ul>
      <li :class="activeTab==='action'? 'is-active' : ''"><a @click="activeTab='action'">Hoạt động</a></li>
      <li :class="activeTab==='history'? 'is-active' : ''"><a @click="activeTab='history'">{{'Chỉnh sửa' + (history.length>0? '(' + history.length + ')' : '')}}</a></li>
      <li :class="activeTab==='file'? 'is-active' : ''"><a @click="activeTab='file'">{{file? 'File(1)' : 'File'}}</a></li>
      <li :class="activeTab==='image'? 'is-active' : ''"><a @click="activeTab='image'">{{images.length===0? 'Hình ảnh' : ('Hình ảnh(' + images.length + ')')}}</a></li>
    </ul>
    </div>

    <div v-if="activeTab==='action'">
    <div class="notification pt10 pb10 mb10 is-dark" v-if="msgLocked.length>0">
    <button class="delete" @click="msgLocked=[]"></button>
    <article class="media pt3 pb3 is-marginless" v-for="(ele,key) in msgLocked" :key="key">
    <figure class="media-left">
            <i :class="ele.type==='success'? 'icon-check2 font-color-blue' : ele.type==='error'? 'icon-cross2 has-text-danger' : 'icon-warning has-text-warning'"> </i>
    </figure>
    <div class="media-content">
        <div class="content">
        <p class="font-smaller" :class="ele.type==='success'? 'font-color-blue' : ele.type==='error'? 'has-text-danger' : 'has-text-warning'">  {{ele.message}} </p>
        </div>
    </div>
    </article>
    </div>

    <div class="pb5" v-if="rightApprove===true">
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

      <div class="field" v-if="selected? selected.code==='retype' : 1<0">
        <div class="control">
          <textarea class="textarea is-primary" v-model="retypeReason" rows="4" :placeholder="api.getvalue(api.find3var('information','reason','label'))"></textarea>
        </div>
      </div>
    </div>

    <div class="notification pt10 pb10 mb10 is-white" v-if="msgInfo.length>0">
    <button class="delete" @click="msgInfo=[]"></button>
    <article class="media pt3 pb3 is-marginless" v-for="(ele,key) in msgInfo" :key="key">
    <figure class="media-left">
            <i :class="ele.type==='success'? 'icon-check2 font-color-blue' : ele.type==='error'? 'icon-cross2 has-text-danger' : 'icon-warning has-text-warning'"> </i>
    </figure>
    <div class="media-content">
        <div class="content">
        <p class="font-smaller" :class="ele.type==='success'? 'font-color-blue' : ele.type==='error'? 'has-text-danger' : 'has-text-link'">  {{ele.message}} </p>
        </div>
    </div>
    </article>
    </div>

    <div class="buttons mt20 is-centered">
      <button class="button is-primary font-smaller" @click="loginForm=true" v-if="retype===false">Sửa báo cáo</button>
      <button class="button is-primary font-smaller" v-if="api.getbyid(task.status).code==='entered' || api.getbyid(task.status).code==='retype'" @click="sendReport()">Gửi báo cáo</button>
      <button class="button is-primary is-outlined font-smaller" @click="saveData()" v-if="editable===true">Lưu lại</button>
    </div>
    </div>

    <div v-else-if="activeTab==='history'">
        <article class="message is-warning"  v-for="(v,i) in history" :key="i">
        <div class="message-body pt10 pb10 has-background-white">
          <p class="font-smaller has-text-dark has-text-left">   {{'Báo cáo được yêu cầu sửa lại với lý do : ' +  v.message}} </p>
           <nav class="level is-mobile mt5">
      <div class="level-left">
        <a class="level-item" style="text-decoration: none">
          <span class="icon is-small"><i class="icon-clock2"></i></span>
          <span class="font-small ml10"> {{v.time}} </span>
        </a>
      </div>
    </nav>
    </div>
    </article>
    </div>

    <div v-else-if="activeTab==='file'">
       <div class="mb-5" v-if="task.data_file"> File dữ liệu đã tải lên:
       <p class="mt-2"> <a @click="downloadDataFile()"> {{task.data_file}} </a> </p>
      </div>
      <article class="message is-primary">
      <div class="message-body has-background-white py-3 has-text-dark">
        Nếu bạn có dữ liệu đính kèm, hãy gắn nó vào đây.
      </div>
    </article>
     
      <p v-if="file"><a @click="download()"> {{file.file}} </a> 
      <a class="ml-3" @click="file=undefined" v-if="editable">
        <span class="icon fs24 has-text-danger"> <i class="mdi mdi-close"> </i> </span> </a> </p>
      <a v-if="editable && !file" class="button is-primary is-light"
      @click="media = {component: componentid, name: 'file', type: 'file', open: true}"> Chọn file </a>
    </div>

  <div v-else-if="activeTab==='image'">
    <article class="message is-primary">
  <div class="message-body has-background-white py-3 has-text-dark">
    Hình ảnh minh họa, thuyết minh, chú thích, những điểm cần lưu ý sẽ rất hữu ích cho các nhà đầu tư trong việc lựa chọn cổ phiếu tốt. Hãy đính kèm nếu bạn có các thông tin đó.
  </div>
  </article>
  <div class="columns is-multiline is-mobile" v-if="images.length>0">
  <div class="column is-one-quarter" v-for="(v,i) in images" :key="i">
    <figure class="image">
    <a @click="gallery=v.file"> <img :src="connection.path + 'static/images/' + v.file"> </a>
     <p> <a @click="removeImage(v,i)" v-if="editable"> <span class="icon fs24 has-text-danger"> <i class="mdi mdi-close"> </i> </span> </a></p>
    </figure>
  </div>
  </div>
  <a class="button is-primary is-light mt-3" v-if="editable"
  @click="media = {component: componentid, name: 'image', type: 'image', open: true}"> Hình ảnh (nếu có) </a>
  </div>
    </div>

  <div class="column is-12 pt0" v-if="editable">
    <Import ref="import" v-bind="{task: task}"> </Import>
  </div>
    <div class="column is-12 pt0">
    <div class="mx-5">
    <nav class="level is-mobile mt40 mb40 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
    <div class="level-left">
        <div class="level-item">
        <p class="title fs30"> Dữ liệu đã nhập trong hệ thống </p>
        </div>
    </div>
    </nav>
    <TableFilter v-bind="{name: 'pageitem'}" v-if="pageitem"> </TableFilter>
    </div>
    </div>
    </div>
</div>
</section>

 <div class="modal" :class="loginForm!==undefined? 'is-active' : ''" v-if="loginForm!==undefined">
  <div class="modal-background has-background-white"></div>
  <div class="modal-content my-0 py-0">
   <loginform v-bind="{modal: true}"> </loginform>
  </div>
  <button class="modal-close is-large has-background-dark" aria-label="close" @click="loginForm=undefined"></button>
</div>
    
  <div class="modal is-active" v-if="openMedia===componentid">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content" style="position: absolute; top: 0px">
        <media v-bind="{mediatype: media.type, modal: true}" />
     </div>
    <button @click="media=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
  </div>

  <div class="modal is-active" v-else-if="gallery">
  <div class="modal-background"></div>
  <div class="modal-content">
   <div class="tile is-ancestor ml10 mr10 mt10 mb10">
  <div class="tile is-2"></div>
  <div class="tile is-8">
    <img v-lazy="connection.path + 'static/images/' + gallery" class="mt0 mb0 pt0 pb0">
    </div>
  </div>
</div>  
<button @click="gallery=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
</div>
 <Footer></Footer>
</div>
</template>

<script>
import Vue from 'vue'
import Export from '@/assets/js/export.js'
import mixing from '@/assets/js/mixing.js'
import axios from 'axios'
import login from '@/pages/login.vue'
import media from '@/pages/media.vue'
import Import from '@/components/Import'
import "bulma-extensions/bulma-steps/dist/css/bulma-steps.min.css"
import socket from '~/plugins/socket.io.js'
Vue.component('loginform', login)
Vue.component('media', media)
Vue.component('Import', Import)

export default {
   data() {
      return {
        data: [],
        fields: [],
        company: undefined,
        stock_code: undefined,
        dataready: false,
        connection: this.$connection(),
        connection1: this.$connection(),
        connection2: this.$connection(),
        connection3: this.$connection(),
        connection4: this.$connection(),
        connection5: this.$connection(),
        connection6: this.$connection(),
        connection7: this.$connection(),
        result: [],
        models: [],
        datafile: undefined,
        msgInfo: [],
        report: undefined,
        task: undefined,
        sending: false,
        msgLocked: [],
        editable: true,
        dldata: true,
        rightApprove: false,
        selected: undefined,
        changeStatus: undefined,
        retype: undefined,
        retypeReason: '',
        mdlactive: undefined,
        editItem: undefined,
        loginForm: undefined,
        history: [],
        message: [],
        activeTab: 'action',
        tophead: '',
        approve_time: undefined,
        accountlist: [],
        componentid: mixing.id(),
        file: undefined,
        images: [],
        gallery: undefined,
        values: undefined
      }
    },

    head() {
      return {
        title: 'Nhập báo cáo giao dịch chứng khoán'
      }
    },

    created() {
      if(!this.login) {
        let query = {to: this.$route.path}
        query.params = JSON.stringify(this.$route.query)
        return this.$router.push({path: '/login', query: query})
      }
      this.pageitem = undefined
      if(!this.connName) return
      let found = {name: 'reportitem', params: {filter: {company_type: 'PTKT', report_name: this.$route.query.report}}}
      this.connection7.getApi([found])
    },

    watch: {
      "connection.getdataReady": function(newVal) {
        if(newVal==='success') {
          let datalist = this.connection.getbatchData
          let list = datalist.find(v=>v.name==='task').data
          this.task = list.length>0? list[0] : undefined
          if(this.task===undefined) {
              this.$buefy.snackbar.open({
                duration: 5000,
                message: 'Công việc không tồn tại. Hệ thống chuyển hướng đến trang chủ sau 5s',
                position: 'is-bottom',
              })
              let self = this
              mixing.delay(function(){self.$router.push({path: '/'})}, 5000)
              return
          } else if(this.task.file) this.file = {id: this.task.file, file: this.task.file__file}

          this.images = datalist.find(v=>v.name==='taskimage').data
          this.images.map(v=>{
            v.file = v.image__file
            v.imageID = v.image
          })
          this.showData(datalist.find(v=>v.name===this.connName.name).data, this.connection.getbatchStatus.find(v=>v.name===this.connName.name))
          this.getTaskInfo()
          this.taskStatus()
          this.checkRights()
          this.dataready = true
        }
        else if(newVal==='error') this.$router.push({ name: 'error'})
      },

      "connection1.getdataReady": function(newVal) {
        if(newVal==='success') {
          let data = this.connection1.getbatchData[0].data
          if(data.length===0) this.msgInfo.push({message: 'Bạn chưa nhập dữ liệu ngày ' + this.task.stock_date, type: 'error'})
          else this.updateTask()
        }
      },

      'connection2.getupdateStatus': function(newVal, oldVal) {
        if(newVal===true) {
          let message = this.sending===false? 'Cập nhật dữ liệu thành công' : 'Gửi báo cáo đi thành công'
          if(this.changeStatus!==undefined) message = this.changeStatus.msgSuccess
          this.msgInfo.push({message: message, type: 'success'} )
          this.task = this.$copy(this.connection2.updateRecord)
          socket.emit('send-message', {name: 'task-stock-update', data: this.task})
          
          let data = []
          this.images.map(v=>{data.push({id: v.id, task: this.task.id, image: v.imageID})})
          this.connection5.insert('taskimage', data)
          this.getTaskHistory()
        }
        else if(newVal==false)  {
          let message = this.sending===false? 'Cập nhật dữ liệu thất bại' : 'Gửi báo cáo đi thất bại'
          if(this.changeStatus!==undefined) message = this.changeStatus.msgError
          this.msgInfo.push({message: message, type: 'error'} )
        }
        if(this.sending===true) this.sending = false
        if(this.changeStatus!==undefined) this.changeStatus = undefined
      },

      'connection3.getupdateStatus': function(newVal) {
        if(newVal==false) this.msgInfo.push({message: 'Cập nhật điều chỉnh cho chỉ tiêu thất bại', type: 'error'} )
      },

      "connection7.getdataReady": function(newVal) {
        if(newVal==='success') this.getData()
      },

      'task.status': function(newVal) {
        this.taskStatus()
        this.checkRights()
      },

      menuaction: function(newVal) {
        if(newVal===undefined) return
        else if(newVal.action==='download') this.getReport()
        else if(newVal.action==='close-login') {
          this.loginForm = undefined
          this.retype = true
          this.editable = true
          this.msgLocked = []
        }
      },

      media: function(newVal) {
        if(newVal? !newVal.select : 1>0) return
        if(this.componentid!==newVal.component) return
        if(newVal.name==='image') {
          if(!this.images.find(v=>v.imageID===newVal.select.id)) this.images.push({imageID: newVal.select.id, file: newVal.select.file})
        }
        else if(newVal.name==='file') {
          this.file = newVal.select
          this.$store.commit('updateState', {name: 'media', key: 'file', data: this.file})
        }
        this.media = undefined
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.state.api},
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },

      pagetask: {
        get: function() {return this.$store.state.pagetask},
        set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
      },

      pageitem: {
        get: function() {return this.$store.state.pageitem},
        set: function(val) {this.$store.commit('updatePageItem', {pageitem: val})}
      },

      login: {
        get: function() {return this.$store.state.login},
        set: function(val) {this.$store.commit("updateLogin", {login: val})}
      },
      
      menuaction: {
        get: function() {return this.$store.state.menuaction},
        set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
      },

      media: {
        get: function() {return this.$store.state.media},
        set: function(val) {this.$store.commit("updateMedia", {media: val})}
      },

      openMedia() {
        return this.media? this.media.component : false
      },

      connName() {
        var val = undefined
        if(this.$route.query.report==='TKGIA') val = this.connection.requirelist.find(v=>v.name==='stockprice')
        else if(this.$route.query.report==='TKLENH') val = this.connection.requirelist.find(v=>v.name==='stockorder')
        else if(this.$route.query.report==='DTNNLENH') val = this.connection.requirelist.find(v=>v.name==='foreignorder')
        else if(this.$route.query.report==='DTNNTT') val = this.connection.requirelist.find(v=>v.name==='foreigndeal')
        else if(this.$route.query.report==='GIA') val = this.connection.requirelist.find(v=>v.name==='pricelive')
        else if(this.$route.query.report==='CSPTKT') val = this.connection.requirelist.find(v=>v.name==='taindex')
        return val
      }
    },

    methods: {
      closeWindow() {
        window.close()
      },

      getData() {
        let rows = this.connection7.getbatchData[0].data
        let fields = 'id,stock_date,company,company__stock_code,create_time,' + rows.map(v=>'f' + v.item).join()
        let list = [{name: this.connName.name, url: this.connName.url, params: {values: fields, filter:{task: this.$route.query.task}}}]
        this.values = 'id,stock_date,report_name,report_name__code,report_name__value,assigner,assigner__name,recipient,recipient__name,assign_date,due_date,priority,status,status__value,status__code,entry_time,waiting1_time,waiting2_time,approve_time,update_time,file,file__file,data_file'
        let found = {name: 'task', url: 'data/Task_Taindex', params: {values: this.values, filter: {id: this.$route.query.task}}}
        list.push(found)
        found = {name: 'taskimage', url: 'data/Task_Image', params: {values: 'id,task,image,image__file', filter_or: {task: this.$route.query.task}}}
        list.push(found)
        this.connection.getApi(list)
      },

      getTaskInfo() {
        this.task.assignDate = mixing.yyyymmddhhmm(new Date(this.task.assign_date))
        this.task.dueDate = mixing.yyyymmddhhmm(new Date(this.task.due_date))
        this.tophead =  this.task.report_name__value + ' / Ngày '  + this.task.stock_date
        this.getTaskHistory()
      },

      getTaskHistory() {
        if(this.$empty(this.task.history)===true) return
        this.history = JSON.parse(this.task.history)
        this.history.sort((a,b) => (new Date(b.time) - new Date(a.time)))
        this.history.map(v=>v.time=mixing.yyyymmddhhmm(new Date(v.time)))
      },

      uploadFile(file) {
        let data = new FormData();
        data.append('name', file.files[0].name);
        data.append('file', file.files[0]);

        let fileName = file.files[0].name
        //check file name is valid
        if (!(fileName.search('.xls') > 0 || fileName.search('.xlsx') > 0)) {
          this.msgInfo.push({message: this.api.find3var('inform', 'import', 'file-type-invalid').value, type: 'error'} )
          return
        }

        axios.post(this.connection.path + 'upload-file/', data=data)
        .then(response => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-ok').value, type: 'success'})
          this.getfile(file.files[0].name)
          file.value = ''
          }
        )
        .catch(error => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-fail'), type: 'error'})
          file.value = ''
        })
      },

      getfile(filename) {
        const url = this.connection.path + 'getfile/' + filename
        axios.get(url)
        .then(response => {
          this.datafile = JSON.parse(response.data)
          this.fillData()
        })
        .catch(error => {
          this.msgInfo.push({message: 'Có lỗi khi đọc cấu trúc file', type: 'error'})
        })
      },

      getfileTemplate() {
        var _export = new Export()
        let task = this.task
        var filename  = this.task.company__stock_code + '-' + this.task.company__type__code + '-' + task.year + '-Q' + this.task.report_period__code + '-' + this.task.report_type__code + '-' + this.task.report_name__code

        let dataTypes = {
            "item": "String",
            "value": "String",
            "auto_calc": "String",
            "input": "String",
        }
        let fields = []

        _export.set(this.data, filename, dataTypes, fields)
        _export.exportItem()
      },

      getReport() {
        var _export = new Export()
        let task = this.task
        var filename  = this.task.company__stock_code  + '-' + this.task.company__type__code + '-' + task.year + '-Q' + this.task.report_period__code  + '-' + task.report_type__code + '-' + this.task.report_name__code

        let dataTypes = {
            "item": "String",
            "name": "String",
            "value": "String",
        }
        let fields = []
        let array = JSON.parse(JSON.stringify(this.data))
        array.map(v=>v.input = mixing.numbertoString(v.item_value))
        _export.set(array, filename, dataTypes, fields)
        _export.exportReport()
      },

      saveData() {
        let found = {name: 'report', url: this.connName.url, params: {page: 1, 
        filter:{task: this.$route.query.task, stock_date: mixing.yyyymmdd(new Date(this.task.stock_date))}}}
        console.log(found)

        this.connection1.getApi([found])       
      },

      updateTask() {
        let data = JSON.parse(JSON.stringify(this.task))
        if(data.status__code==='not-yet-entered') {
            data.status = this.api.find3var('list', 'task-status', 'entered').id
            data.entry_time = new Date()
        }
        else if(this.sending===true) {
            data.status = this.api.find3var('list', 'task-status', 'waiting-approve').id
            data.waiting1_time = new Date()
        }
        else if(this.changeStatus!==undefined) {
          data.status = this.changeStatus.id
          if(this.selected.code==='retype') {
            this.msgLocked = [{message: 'Báo cáo được yêu cầu sửa lại với lý do : ' + this.retypeReason, type: 'warning'}]
            let list = data.history===null? [] : JSON.parse(data.history)
            list.push({sender: this.login.id, message: this.retypeReason, time: new Date().toString()})
            data.history = JSON.stringify(list)
            this.selected = undefined
          }
          else if(this.selected.code==='waiting-approve-2') {
              data.waiting2_time = new Date()
          }
          else if(this.selected.code==='approved') {
            this.approve_time = new Date()
            data.approve_time = this.approve_time
          }
        }
      
      data.update_time = new Date()
      data.file = this.file? this.file.id : null
      let fileName = this.$refs.import.getFile()
      if(!this.$empty(fileName)) data.data_file = fileName 
      if(this.$empty(this.retypeReason)===false) data.detail = this.retypeReason
      this.connection2.update('tasktaindex', data, this.values)
    },

    taskStatus() {
      this.rightApprove = false
      this.result = []
      let list = [{name: 'success', value: 'is-active is-success'},
                  {name: 'error', value: 'is-active is-danger'},
                  {name: 'normal', value: 'is-active is-warning'}]
      let status = this.api.getbyid(this.task.status)
      this.result.push({name: 'assign', value: list.find(v=>v.name==='success').value})
      
      if(status.code==='not-yet-entered' || status.code==='entered')
          this.result.push({name: 'entered', value: list.find(v=>v.name==='normal').value})

      else if(status.code==='waiting-approve') {
          this.rightApprove = true
          this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='normal').value})
      }

      else if(status.code==='waiting-approve-2') {
          this.rightApprove = true
          this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'waiting-approve-2', value: list.find(v=>v.name==='normal').value})
      }

      else if(status.code==='approved') {
          this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'waiting-approve-2', value: list.find(v=>v.name==='success').value})
          this.result.push({name: 'approved', value: list.find(v=>v.name==='success').value})
          let message = 'Báo cáo đã được duyệt. Bạn không thể thay đổi được thông tin.'
          this.msgLocked = [{message: message, type: 'warning'}]
          this.editable = false
          if(this.login.type.code==='admin' || this.login.type.code==='manager') this.retype = false
        }
      else if(status.code==='retype') {
          this.msgLocked = [{message: 'Báo cáo được yêu cầu sửa lại với lý do : ' +  this.task.detail, type: 'warning'}]
          this.retypeReason = this.task.detail
      }
      this.selected = this.api.getbyid(this.task.status)
    },

    sendReport() {
      this.$buefy.dialog.confirm({
        message: 'Gửi báo cáo đi có thể không thay đổi được dữ liệu đã nhập nếu không có yêu cầu sửa lại. Bạn có muốn tiếp tục không?',
        type: 'is-warning',
        onConfirm: () => {
          this.sending = true
          this.saveData()
        }
      })
    },

    checkRights() {
      let status = this.api.getbyid(this.task.status)
      let type = this.login.type

      if(type.code==='staff' || type.code==='ctv') {
        this.dldata = false
        if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {   
          this.editable = false
          this.rightApprove = false
          let message = 'Báo cáo đang chờ duyệt. Bạn không thể thay đổi được thông tin.'
          this.msgLocked = [{message: message, type: 'warning'}]
        }
      } 
      else {
        if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {
          this.rightApprove = true
          this.approvelist = []
          this.approvelist.push(this.api.find3var('list','task-status','waiting-approve'))
          this.approvelist.push(this.api.find3var('list','task-status','waiting-approve-2'))
          this.approvelist.push(this.api.find3var('list','task-status','retype'))

          if(type.code==='admin' || type.code==='manager') {
            this.approvelist.push(this.api.find3var('list','task-status','approved'))
          }
        }
      }
    },

    approveTask() {
      if(this.selected.code==='retype' && this.$empty(this.retypeReason)===true) {
        this.msgLocked = [{message: 'Lý do sửa lại không được để trống', type: 'warning'}]
        return
      }
      this.changeStatus = {id: this.selected.id, msgSuccess: 'Duyệt công việc thành công.', msgError: 'Duyệt công việc thất bại'}
      this.saveData()
    },

    removeImage(v, i) {
      this.$delete(this.images, i)
      if(v.id) this.connection6.delete('taskimage', v.id)
    },

    showTime(v) {
      if(!v) return
      return mixing.yyyymmddhhmm(new Date(v))
    },

    downloadDataFile() {
      mixing.download( this.connection.path + 'get-datafile/' + this.task.data_file + '/')
    },

    download() {
      mixing.download(this.connection.path + 'static/files/' + this.file.file)
    },

    showData(data, api) {
      let fields = [mixing.createField('id', 'Id', 'number', false, true),
        mixing.createField('stock_date', 'Ngày GD', 'string', false, true),
        mixing.createField('company__stock_code', 'Mã', 'string', false, true)
      ]
      let rows = this.connection7.getbatchData[0].data
      rows.map(v=>{
        let field = mixing.createField('f' + v.item, v.value, 'number', false, true)
        fields.push(field)
      })
      fields.push(mixing.createField('action', '', 'string', false, true, '6%', 'select'))
      this.pageitem = {data: data, fields: fields, filter: [], record: undefined, action: undefined, enableDelete: true
      , api: this.$copy(api) , origin_api: this.$copy(api), reload: 0}
    }
  }
}
</script>

  <style scoped
    src="bulma-extensions/bulma-tooltip/dist/css/bulma-tooltip.min.css">
  </style>