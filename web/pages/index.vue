<template>
  <div v-if="rights">
    <TopMenu/>
    <section class="hero is-fullheight-with-navbar">
  <div class="hero-body mt-5" style="align-items: flex-start">
  <div class="container">
        <div class="columns is-multiline">
          <div class="column is-3 has-text-centered" v-for="(v,i) in data" :key="i" :class="i>3? 'pt-1' : ''">
           <nuxt-link class="box-icon" :to="v.link" v-if="v.link">
            <span class="vertical-center">
          <i :class="v.icon? v.icon : 'mdi mdi-menu'"/>
            </span>
            </nuxt-link>
            <a class="box-icon" @mousemove="openMenu(v)" v-else>
               <span class="vertical-center">
               <i :class="v.icon? v.icon : 'mdi mdi-menu'"/>
               </span>
            </a>
            <p class="fs20 fb600 has-text-grey-darker mt-1"> {{v.value}}</p>

    <div class="box px-1 py-2 mr-2" style="background-color:white" v-if="rights.find(x=>x.classify===v.code) && showlist.find(x=>x.id===v.id)">
        <p class="content has-text-left py-0 my-0" style="max-height:132px; overflow-y: auto;">
          <ul class="mb-1 mt-1">
            <li class="pb-1 border-bottom fs15" v-for="(ele,key) in rights.filter(x=>x.classify===v.code)" :key="key">
              <nuxt-link class="has-text-black-ter" style="text-decoration: none" v-if="ele.link" :to="ele.link"> {{ele.value}} </nuxt-link>
              <a class="has-text-grey-lighter" style="text-decoration: none" v-else> {{ele.value}} </a>
            </li>
          </ul>
        </p>
      </div>
      </div>
    </div>
  </div>
  </div>
</section>
  <Footer class="mt50"/>
  </div>
</template>

<script>
import mixing from "@/assets/js/mixing.js"
export default {
  data () {
    return {
      connection: this.$connection(),
      data: [],
      showlist: [],
      openState: false,
    }
  },

  head() {
    return {
      title: 'Hệ thống nhập dữ liệu báo cáo tài chính'
    }
  },

  created() {
    if(!this.login) return
    this.data = this.rights.filter(v=>v.category==='functions')
    this.toggleMenu()
  },
 
  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },
    rights: {
      get: function() {return this.$store.state.rights},
      set: function(val) {this.$store.commit('updateRights', {rights: val})}
    },
    hasnews: {
      get: function() {return this.$store.state.hasnews},
      set: function(val) {this.$store.commit('updateHasNews', {hasnews: val})}
    }
  },

  methods: {
    toggleMenu() {
      this.openState = ! this.openState
      this.showlist = []
      if(this.openState) {
        this.data.map(x=>this.showlist.push(x))
      }
    },

    openMenu(ele) {
      let found = this.showlist.find(v=>v===ele.id)
      if(!found) this.showlist.push(ele)
    },

    getlink(link) {
      try {
        var val = link.indexOf('{')>=0? JSON.parse(link) : link
      } catch (error) {
        console.log(error)  
      }
      finally {
        if(link.indexOf('{')>=0) console.log(val)
        return val? val : ""
      }
    },

    getList(k) {
      let filter = this.$copy(this.data.slice(4*k,4*(k+1)))
      return mixing.dummyData(filter, 4)
    }
  }
}
</script>