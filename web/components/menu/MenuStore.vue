<template>
  <div>
         <div class="field mb-2">
        <div :class="loading? 'control is-loading' : 'control'">
          <input class="input is-rounded is-primary fs13" type="text" 
          placeholder="Gõ tên thiết lập muốn tìm" v-model="search" ref="searchbox">
        </div>
          <p class="is-help mt-2"> Danh sách thiết lập có sẵn trong <strong class="has-text-danger"> My Store </strong> </p>
      </div>

           <p class="panel-tabs mb-1">
            <a v-for="(v,i) in settingchoice.filter(v=>login? true : ['public', 'system'].find(x=>x===v.code))" :key="i"
            :class="selectType? (selectType.id===v.id? 'is-active' : '') : ''"
            @click="selectType = v"
            >
              {{v.name}}
            </a>
          </p>

          <a class="panel-block is-active" v-for="(row,key) in filterData" 
          :key="key" @click="doSelect(row)">
          {{row.name }} <span class="ml-4 has-text-grey"> {{showTime(row.create_time)}} </span>
            <span class="icon has-text-primary" v-if="currentsetting? currentsetting.id===row.id : false"> <i class="mdi mdi-check"/> </span>
          </a>

           <b-pagination class="mt-2" v-if="data.length>10"
            :total="data.length"
            v-model="current"
            :range-before="1"
            :range-after="1"
            :size="'is-small'"
            :rounded="true"
            :simple="true"
            :per-page="10"
            :icon-prev="'chevron-left'"
            :icon-next="'chevron-right'"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">
        </b-pagination>
</div>
</template>

<script>


export default {
  props: ['classify', 'focus'],

  data() {
    return {
      search: '',
      selectType: undefined,
      connection: this.$connection(),
      data: [],
      loading: false,
      filterData: [],
      originData: [],
      current: 1
    }
  },

  created() {
    this.selectType = this.settingchoice.find(v=>this.login? v.code==='your' : v.code==='system')
  },

  watch: {
    selectType: function(newVal) {
      if(!newVal) return
      let found = this.connection.requirelist.find(v=>v.name==='usersetting')
      found.commit = undefined
      if(newVal.code==='public' || newVal.code==='share') {
        found.params.filter = newVal.code==='public'?  {type__code: 'public', classify: this.classify? this.classify : undefined}
        : {classify: this.classify? this.classify : undefined}
      } 
      else if(newVal.code==='your') found.params.filter = {classify: this.classify, user: this.login.id}
      else if(newVal.code==='system') found.params.filter = {classify: this.classify, type__code: 'system'}
      this.connection.getApi([found])
    },

    "connection.getdataReady": function(newVal) {
      if(newVal === "success") this.getData(this.connection.getbatchData[0].data)
    },

    search: function(newVal) {
      newVal? this.doSearch() : false
    },

    current: function(newVal) {
      this.filterData = this.data.filter((ele,index) => (index>=(newVal-1)*10 && index<newVal*10))
    },

    focus: function(newVal) {
      if(this.$refs.searchbox) this.$refs.searchbox.focus()
      if(this.$empty(this.search)) return
      this.search = undefined
      this.doSearch()
    }
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },

    settingchoice: {
      get: function() {return this.$store.state.settingchoice},
      set: function(val) {this.$store.commit("updateSettingChoice", {settingchoice: val})}
    },

    systemsetting: {
      get: function() {return this.$store.state.systemsetting},
      set: function(val) {this.$store.commit("updateSystemSetting", {systemsetting: val})}
    },

    usersetting: {
      get: function() {return this.$store.state.usersetting},
      set: function(val) {this.$store.commit("updateUserSetting", {usersetting: val})}
    },

    currentsetting: {
      get: function() {return this.$store.state.currentsetting},
      set: function(val) {this.$store.commit("updateCurrentSetting", {currentsetting: val})}
    }
  },

  methods: {
    getData(rows) {
      rows = this.$copy(rows)
      rows = this.$multiSort(rows, {id: 'desc'})
      this.originData =  rows
      this.data = rows
      this.filterData = this.data.slice(0,10)
      this.current = 1
    },

    doSelect(row) {
      this.$emit('opensetting', row)
    },
   
    showTime(date) {
      let res= this.$timeFormat(new Date(date), new Date())
      return res.display
    },

    doSearch() {
      this.current = 1
      this.data = this.$empty(this.search)
        ? this.$copy(this.originData)
        : this.$copy(
            this.originData.filter(
              (v) =>
                v.name.toLowerCase().indexOf(this.search.toLowerCase()) >= 0
            )
          );
      this.filterData = this.data.slice(0, 10);
    },
  }
}
</script>