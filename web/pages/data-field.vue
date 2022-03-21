<template>
  <div class="mx-5">
    <div class="field is-grouped is-grouped-multiline border-bottom py-1 mt-2">
  <div class="control mr-5">
   <a class="button is-text has-text-black px-1" style="text-decoration:none">
    <figure class="image mr-5" style="width: 50px">
    <nuxt-link to="/"> <img :src="require(`@/assets/images/logo.png`)"/> </nuxt-link>
    </figure>
   </a>
  </div>
  <div class="control">
        <div class="dropdown is-hoverable" @mouseenter="focus=$id()">
  <div class="dropdown-trigger">
    <a class="button is-text has-text-black px-1" @click="doSelect('MenuReport')" style="text-decoration:none">
          My Store
           <i class="mdi mdi-chevron-down fs22 ml-1" />
        </a>
  </div>
  <div class="dropdown-menu" role="menu">
        <div style="min-width:23rem; background-color:#d3d3d3" v-if="!ismobile">
          <MenuStore class="px-2 py-2" v-bind="{classify: 1, focus: focus}" @opensetting="openSetting" />
        </div>
    </div>
    </div>
  </div>
    <div class="control">
        <div class="dropdown is-hoverable" @mouseenter="focus=$id()">
  <div class="dropdown-trigger">
    <a class="button is-text has-text-black px-1" @click="doSelect('MenuReport')" style="text-decoration:none">
          Tạo trường
           <i class="mdi mdi-chevron-down fs22 ml-1" />
        </a>
  </div>
  <div class="dropdown-menu" role="menu">
        <div style="min-width:23rem; background-color:#d3d3d3" v-if="!ismobile">
          <NewField class="px-3 py-2" v-bind="{pagename: 'pagedata', focus: focus}" />
        </div>
    </div>
    </div>
  </div>
             <div class="control">
        <div class="dropdown is-hoverable" @mouseenter="focus=$id()">
  <div class="dropdown-trigger">
    <a class="button is-text has-text-black" @click="doSelect('MenuReport')" style="text-decoration:none">
         <span class="icon fs26"> <i class="mdi mdi-content-save-outline"> </i> </span>
        </a>
  </div>
  <div class="dropdown-menu" role="menu">
      <div style="min-width:21rem; background-color:#d3d3d3" v-if="!ismobile">
          <MenuSave class="px-3 pb-3"  v-bind="{pagename: 'pagedata', classify: 3, focus: focus}" v-if="login" />
        </div>
    </div>
    </div>
  </div>

  <div class="control">
    <div class="dropdown is-hoverable" @mouseenter="focus=$id()">
  <div class="dropdown-trigger">
    <a class="button is-text has-text-black" @click="doSelect('MenuReport')" style="text-decoration:none">
        <span class="icon fs26"> <i class="mdi mdi-cog-outline"> </i> </span>
        </a>
  </div>
  <div class="dropdown-menu" role="menu">
       <div style="min-width:39rem; background-color:#d3d3d3" v-if="!ismobile">
          <TableSetting v-bind="{focus: focus}" class="px-3"/>
        </div>
    </div>
    </div>
  </div>
     </div>
   <div class="has-text-black-bis my-4" v-if="currentsetting">
    Bạn đang mở thiết lập: <b class="ml-2 fs18 has-text-danger">{{currentsetting.name}}</b>
  </div>
    <DataTable class="mt-3" v-bind="{pagename: 'pagedata'}" />
  </div>
</template>

<script>
import NewField from '@/components/menu/NewField'
import MenuStore from '@/components/menu/MenuStore'
import TableSetting from '@/components/datatable/TableSetting'
import MenuSave from '@/components/menu/MenuSave'
export default {
  components: {
    NewField,
    MenuStore,
    TableSetting,
    MenuSave
  },

  head() {
    return {
      title: 'Quản lý trường dữ liệu'
    }
  },

  data() {
    return {
      settingID: this.$route.query.setting,
      connection: this.$connection(),
      open: false,
      menu: undefined,
      focus: undefined
    }
  },

  created() {
    this.currentsetting = undefined
    this.pagedata = {data: [], fields: [], action: undefined, enableDelete: false, showFilter: true,
    api: {name: this.type, full_data: true}, origin_api: {name: this.type, full_data: true}}
    if(this.settingID) {
      let found = this.$copy(this.connection.find('usersetting'))
      found.commit = undefined
      found.params.filter = {id: this.settingID}
      this.connection.getApi([found])
    } 
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        let found = this.connection.getbatchData.find(v=>v.name==='usersetting')
        if(found? found.data.length>0 : false) {
         this.currentsetting = this.$clone(found.data[0])
          let json = JSON.parse(found.data[0].detail)
          this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: json.fields})
          if(json.tablesetting) this.tablesetting = json.tablesetting   
          let copy = this.$copy(this.pagedata.fields)
          let obj = copy.find(v=>v.label==='Menu')
          if(obj) {
            obj.disable = 'search,filter,value'
            this.$store.commit('updateState', {name: 'pagedata', key: 'fields', data: copy})
          }
        }
      }
    }
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },

    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit('updatePageData', {pagedata: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", { ismobile: val })}
    },

    currentsetting: {
      get: function() {return this.$store.state.currentsetting},
      set: function(val) {this.$store.commit("updateCurrentSetting", {currentsetting: val})}
    },

    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    }
  },

  methods: {
    doSelect(v) {
      if(this.ismobile) {
        this.open = true
        this.menu = v
      }
    },

    openSetting(option) {
      let found = this.$copy(this.connection.requirelist.find(v=>v.name==='usersetting'))
      found.commit = undefined
      found.params.filter = {id: option.id}
      this.connection.getApi([found])
    }
  }
}
</script>