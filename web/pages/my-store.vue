<template>
  <div>
    <topmenu v-bind="{type: 'tophead', tophead: 'Danh sách thiết lập'}"></topmenu>
    <div class="title fs26 mx-5 pt-5 mt-2"> My Store </div>
    <div class="mx-5">
  <div class="columns">
    <div class="column is-3">
    <aside class="menu">
    <ul class="menu-list">
      <li>
        <a class="is-active">Danh mục thiết lập</a>
        <ul>
          <li v-for="v in settingclass" :key="v.id">
            <a :class="active===v.code? 'fb800 has-text-danger' : ''" @click="changeTab(v)">{{v.name}}</a></li>
        </ul>
      </li>
    </ul>
  </aside>
  </div>
    <div class="column">
      <DataTable v-bind="{pagename: 'pagedata'}" @opensetting="openSetting" @editsetting="getSetting($event.id)"
      @deletesetting="deleteSetting" @dotest="doTest($event)"> </DataTable>
    </div>
  </div>
  </div>

    <div class="modal is-active" v-if="change">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
  <div class="modal-card" :style="ismobile? '' : 'width:55%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" @click="change=false"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
        <div class="field is-horizontal mt-3">
  <div class="field-body">
    <div class="field">
       <label class="label">Tên thiết lập <span class="has-text-danger"> * </span> </label>
      <p class="control">
        <input class="input" type="text" placeholder="" v-model="record.name">
      </p>
        <p class="help has-text-danger" v-if="errors.find(v=>v.name==='name')"> {{errors.find(v=>v.name==='name').message}} </p>
    </div>
    <div class="field">
      <label class="label"> Loại thiết lập <span class="has-text-danger"> * </span> </label>
       <b-autocomplete
        icon-right="magnify"
        :value="selectType? selectType.name : ''"
        placeholder=""
        :keep-first=true
        :open-on-focus=true
        :data="settingtype"
        field="name"
        @select="option => selectType = option">
      </b-autocomplete>
    </div>

    <div class="field" v-if="login.type===2">
      <label class="label"> Phân loại <span class="has-text-danger"> * </span> </label>
       <b-autocomplete
        icon-right="magnify"
        :value="selectClass? selectClass.name : ''"
        placeholder=""
        :keep-first=true
        :open-on-focus=true
        :data="settingclass"
        field="name"
        @select="option => selectClass = option">
      </b-autocomplete>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt-5">
  <div class="field-body">
        <div class="field">
      <label class="label"> Mặc định<span class="has-text-danger"> * </span> </label>
      <p class="control is-expanded">
           <b-radio v-model="record.default"
                :native-value="true">
                Có
            </b-radio>
            <b-radio v-model="record.default"
                :native-value="false">
                Không
            </b-radio>
      </p>
      </div>
        <div class="field" v-if="choices.findIndex(x=>x.code===record.classify__code)>=0
        && (record.type__code==='public' || record.type__code==='system')">
      <label class="label">{{'Hiển thị trên menu ' + choices.find(x=>x.code===record.classify__code).name + '?'}}</label>
      <p class="control is-expanded">
           <b-radio v-model="record.on_menu"
                :native-value="true">
                Có
            </b-radio>
            <b-radio v-model="record.on_menu"
                :native-value="false">
                Không
            </b-radio>
      </p>
      </div>
        <div class="field">
      <label class="label">Hiển thị trên menu của Tôi?</label>
      <p class="control is-expanded">
           <b-radio v-model="record.my_menu"
                :native-value="true">
                Có
            </b-radio>
            <b-radio v-model="record.my_menu"
                :native-value="false">
                Không
            </b-radio>
      </p>
      </div>
    </div>
  </div>
  <div class="field mt-5">
    <label class="label">Ghi chú</label>
    <div class="control">
       <editor
      v-model="text"
       api-key="0a3xn20t37fgzj36azuoo8e1fscw2q0xg0k2t12k7ztg5f0m"
       :init="{
            setup (editor) {
      editor.on('change', function () {
        const headings = editor.getBody().querySelectorAll('h1, h2, h3, h4, h5, h6');
        for (let i = 0; i < headings.length; i++) {
          if (!headings[i].id) {
            headings[i].id = Math.random().toString(32).substr(2, 5);
          }
        }
      })
    }   ,
         height: depth,
         menubar: true,
        statusbar: true,
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | preview | code | help'
       }"
     />
    </div>
  </div>
  <div class="mt-5">
    <a class="tag is-medium is-primary is-rounded mr-4" @click="updateSetting()"> Cập nhật </a>
    <a class="tag is-medium is-dark is-rounded" @click="change=false"> Đóng lại </a>
  </div>
    </section>
  </div>
  </div>
  </div>
</template>

<script>
import Editor from '@tinymce/tinymce-vue'
export default {
  components: {
    Editor
  },
  
  head() {
    return {
      title: 'Danh sách thiết lập'
    }
  },

  props: ['modal'],
  data() {
    return {
      connection: this.$connection(),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(),
      connection3: this.$connection(this.$buefy),
      connection4: this.$connection(),
      connection5: this.$connection(),
      connection6: this.$connection(),
      radio: 'your',
      change: false,
      errors: [],
      selectType: undefined,
      record: undefined,
      selectClass: undefined,
      open: false,
      setting: undefined,
      active: undefined,
      choices: [{code: 'screener', name: 'Bộ lọc'}, {code: 'priceboard', name: 'Bảng giá'}, {code: 'industry-ratio', name: 'Ngành'},
      {code: 'industry-structure', name: 'Ngành'}]
    }
  },

  created() {
    if(!this.login) this.radio = 'system'
    this.pagedata = {data: [], fields: [], filter: [], action: undefined, showFilter: true, filterby: undefined, api: {} , origin_api: {}}
    this.loadData()
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Escape' && this.change) this.change = false
    })
  },

  watch: {
    "connection.getdataReady": function(newVal) {
      if (newVal==="success") {
        let row =  this.connection.getbatchData.find(v=>v.name==='settingfields').data[0]
        let json = JSON.parse(row.detail)
        this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: this.$copy(json.fields)})
        this.currentsetting = this.$copy(row)
        if(json.tablesetting) this.tablesetting = json.tablesetting
        let data = this.connection.getbatchData.find(v=>v.name==='usersetting').data
        data.map(v=>{
          var res = this.$timeFormat(new Date(v.create_time), new Date())
          v.show_time = res.display
        })
        let api = this.connection.getbatchStatus[0]
        this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: this.$copy(data)})
        this.$store.commit('updateState', {name: 'pagedata', key: 'api', data: this.$copy(api)})
        this.$store.commit('updateState', {name: 'pagedata', key: 'origin_api', data: this.$copy(api)})
      }
    },

    'connection1.getupdateStatus': function(newVal) {
      if(newVal) {
        let row = this.connection1.getupdateRecord
        this.record = this.$copy(row)
        this.selectType = this.settingtype.find(v=>v.id===this.record.type)
        this.selectClass = this.settingclass.find(v=>v.id===this.record.classify)

        var res = this.$timeFormat(new Date(row.create_time), new Date())
        row.show_time = res.display
        let copy = this.$copy(this.pagedata.data)
        let index = copy.findIndex(v=>v.id===row.id)
        copy[index] = row       
        this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: copy})
        if(this.pagedata.filters.length>0) {
          let self = this
          setTimeout(function(){
          self.$store.commit('updateState', {name: 'pagedata', key: 'filterby', data: self.$copy(self.pagedata.filters)})
          }, 50)
        }
      }  
    },

    "connection4.getdataReady": function(newVal) {
      if (newVal==="success") {
        this.record = this.$copy(this.connection4.getbatchData[0].data[0])
        this.selectType = this.settingtype.find(v=>v.id===this.record.type)
        this.selectClass = this.settingclass.find(v=>v.id===this.record.classify)
        this.change = true
      }
    },

    "connection5.getdataReady": function(newVal) {
      if (newVal==="success") {
        this.setting = this.connection5.getbatchData[0].data[0]
        this.open = true
      }
    },

    'connection6.getupdateStatus': function(newVal) {
      if(newVal) {
        let copy = this.$copy(this.pagedata.data)
        this.$delete(copy, copy.findIndex(v=>v.id===this.connection6.getupdateRecord.id))
        this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: copy})
      }
    },

    radio: function(newVal) {
      this.record = undefined
      this.change = false
      this.loadData()
    }
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },

    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit("updatePageData", {pagedata: val})}
    },

    settingtype: {
      get: function() {return this.$store.state.settingtype},
      set: function(val) {this.$store.commit("updateSettingType", {settingtype: val})}
    },

    systemsetting: {
      get: function() {return this.$store.state.systemsetting},
      set: function(val) {this.$store.commit("updateSystemSetting", {systemsetting: val})}
    },

    settingclass: {
      get: function() {return this.$store.state.settingclass},
      set: function(val) {this.$store.commit("updateSettingClass", {settingclass: val})}
    },

    currentsetting: {
      get: function() {return this.$store.state.currentsetting},
      set: function(val) {this.$store.commit("updateCurrentSetting", {currentsetting: val})}
    },

    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", { ismobile: val })}
    }
  },

  methods: {
    openSetting(row) {
      this.$router.push(this.$linkSetting(row))
    },

    deleteSetting(row) {
      this.$buefy.dialog.confirm({
        message: 'Bạn muốn xóa thiết lập: ' + row.name,
        onConfirm: () => {
          this.connection6.delete('usersetting', row.id)
        }
      })
    },

    doTest(row) {
      this.getSetting(row.id, true)
    },

    getSetting(id, isTest) {
      let found = this.connection4.requirelist.find(v=>v.name==='usersetting')
      found.commit = undefined
      found.params.filter = {id: id}
      isTest? this.connection5.getApi([found]) : this.connection4.getApi([found])
    },

    loadData() {
      let values = 'id,name,user,user__name,type,type__code,type__name,note,default,create_time,update_time,classify,classify__code,classify__name'
      let found = this.connection.requirelist.find(v=>v.name==='usersetting')
      let filter = this.radio==='your'? {user: this.login.id} : {type__code: this.radio}
      found.params = {values: values, sort: '-create_time', filter: filter}
      let name = this.radio==='your'? 'your-setting-fields' : (this.radio==='system'? 'system-setting-fields' : 'share-setting-fields')
      let conn = {name: 'settingfields', url: 'data/User_Setting', params: {filter: {name: name}}}
      this.connection.getApi([found, conn])
    },

    updateSetting() {
      let found = this.connection1.requirelist.find(v=>v.name==='usersetting')
      this.record.type = this.selectType.id
      this.record.classify = this.selectClass.id
      let msg = {success: 'Lưu thiết lập thành công.', error: 'Lỗi. Hãy thử lại một lần nữa.'}
      this.connection1.update('usersetting', this.record, found.params.values, undefined, undefined, msg)
    },

    updateChange() {
      let row = this.connection1.getupdateRecord
      var res = this.$timeFormat(new Date(row.create_time), new Date())
      row.show_time = res.display
      let copy = this.$copy(this.pagedata.data)
      let index = copy.findIndex(v=>v.id===row.id)
      if(index>=0) copy[index] = row
      this.$store.commit('updateState', {name: 'pagedata', key: 'data', data: copy})
    },

    changeTab(v) {
      let filter = {format: 'string', label: 'Phân loại', name: 'classify__name', select: [v.name]}
      this.$store.commit('updateState', {name: 'pagedata', key: 'filterby', data: [filter]})
    }
  }
}
</script>