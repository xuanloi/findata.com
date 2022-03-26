<template>
  <Nuxt v-if="ready" />
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import Api from '@/assets/js/api.js'
export default {
  data() {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      ready: false
    }
  },

  mounted() {
    let connlist = this.connection.checkDataReady(['syspara', 'moneyunit', 'datatype', 'filterchoice', 'colorchoice', 'textalign', 'placement', 'textcolor',
    'colorscheme', 'filtertype', 'sorttype', 'tablesetting', 'settingchoice', 'sharechoice', 'menuchoice', 'settingtype', 'settingclass'])
    let filter = connlist.filter(v=>!v.ready)
    if(filter.length>0) this.connection.getApi(filter)
    else this.ready = true
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='error') {
        this.ready = true
        this.$router.push({path: '/error'})
      }
    },

    'connection1.getdataReady' : function(newVal) {
      if (newVal==='success') {
        this.ready = true
        let data = this.connection1.getbatchData[0].data
        let found = data.length>0? data[0] : undefined
        if(found? !found.enable : true) {
          alert('Liên kết không hợp lệ. Hệ thống sẽ tự động chuyển đến trang chủ')
          this.$router.push({ path: '/'})
        }
        else {
          let val1 = mixing.compare(new Date(), new Date(found.valid_from))
          let val2 = mixing.compare(new Date(), new Date(found.valid_to))
          if(!(val1>=0 && val2<=0)) {
            alert('Liên kết hết hạn. Hệ thống sẽ tự động chuyển đến trang chủ')
            this.$router.push({ path: '/'})
          } 
        }
      }
    },

    syspara: function(newVal) {
      if(newVal) {
        if(!this.api) {
          let _api = new Api()
          _api.set(this.syspara)
          this.api = _api
        }
        let checklist = ['account-register', 'get-password']
        if(checklist.find(v=>v===this.$route.name) && this.$route.query.token) {
          let conn = {name: 'link', url: 'data/Link', params: {filter: {guid: this.$route.query.token}}}
          this.connection1.getApi([conn])
        }
        else if(!(this.login || this.$route.name==='login' || this.$route.name==='error')) {
          let query = {to: this.$route.path}
          query.params = JSON.stringify(this.$route.query)
          this.$router.push({path: '/login', query: query})
          this.ready = true
        }
        else this.ready = true
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit("updateApi", {api: val})}
    },

    syspara: {
      get: function() {return this.$store.state.syspara},
      set: function(val) {this.$store.commit("updateSystemParameter", {syspara: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    }
  }
}
</script>
<!--
<style>
html {
  font-family:
    'Source Sans Pro',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
</style>-->