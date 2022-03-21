<!-- eslint-disable -->
<template>
<div>
  <TopMenu/>
<div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
<div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-gapless is-centered is-marginless is-paddingless">
<div class="column is-11 is-marginless is-paddingless">
  <div class="px-3 has-text-dark">
  <nav class="breadcrumb mt10" style="margin-bottom: 15px !important" aria-label="breadcrumbs">
  <ul>
    <li><nuxt-link to="/help/page">Trợ giúp</nuxt-link></li>
     <li>  
      <nuxt-link :to="{path: '/help/category', query: {id: mainTopic.id}}">
      {{mainTopic.value}}
      </nuxt-link>
     </li>
  </ul>
</nav>

<div class="pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
  <p class="tags">
  <nuxt-link class="tag is-medium is-rounded"
  :to="{path: '/help/category', query: {id: v.id}}"
  :class="v.id===openTopic.id? 'is-primary' : ''" v-for="(v,i) in subTopic" :key="i">
    {{v.value}}
  </nuxt-link>
  </p>
</div>

  <div class="fs20 fb500 has-text-primary has-text-centered mt30"
    v-if="helplist? (helplist.length===0? 1>0: 1<0) : 1<0">
   Chưa có tin tức trong mục này
 </div>

<div class="tile is-ancestor mt10" v-else-if="openTopic.level===1 && helplist">
  <div class="tile is-9 is-vertical">
    <div class="tile is-parent mt10" v-for="(v,i) in helplist" :key="i" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
      <article class="tile is-child is-9">
        <div class="ml10 mr10">
        <p class="fs19 fb500 pb10 has-text-dark"> 
         <nuxt-link class="has-text-dark" :to="{path: '/help/open', query: {id: v.id}}"> {{v.title}} 
         </nuxt-link>  
         </p>
        <p class="fb15 pb10"> {{v.subtitle}} </p>
        </div>
      </article>
      <article class="tile is-child">
         <div class="ml10 mr10">
          <nuxt-link class="image" :to="{path: '/help/open', query: {id: v.id}}">
          <img v-lazy="connection.path + 'static/images/' + v.image">
        </nuxt-link>
         </div>
      </article>
      
    </div>
  </div>
  </div>
  <Category v-else-if="openTopic.level===0 && helplist" v-bind="{showlist: helplist, subTopic: subTopic, keyword: '/help'}" class="mt15"/>
  </div>
  </div>
  </div>
</div>
  </div>
  <Footer class="mt60" />
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '~/components/TopMenu.vue'

import Category from  '~/components/Category.vue'
import Footer from '~/components/Footer.vue'

export default {
  components: {
    TopMenu,
    Category,
    Footer
  },

  data() {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      helplist: undefined,
      change: false,
      mainTopic: {},
      subTopic: [],
      openTopic: {}
    }
  },

  head() {
    return {
      title: 'Mở chuyên mục trong trang trợ giúp'
    }
  },  

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') this.getData()
    },

    'connection1.getdataReady': function(newVal) {
      if (newVal==='success') {
        this.helplist = this.connection1.getbatchData[0].data
        if(this.change) {
          window.scrollTo({ top: 0, behavior: 'smooth' })
          this.change = false
        }
      }
    },

    path: function(newVal) {
      this.change = true
      this.helplist = undefined
      this.getData()
    }
  },

  created() {
    if(!this.category) this.connection.getApi([this.connection.requirelist.find(v=>v.name==='helpcategory')])
    else this.getData()
  },

  computed: {
    path() {
      return this.$route.query
    },

    category: {
      get: function() {return this.$store.state.helpcategory},
      set: function(val) {this.$store.commit('updateHelpCategory', {helpcategory: val})}
    },
  },

  methods: {
    getData() {
      let values = 'id,title,subtitle,content,image,category,category__value,category__level,category__parent'
      this.openTopic = this.category.find(v=>v.id===parseInt(this.$route.query.id))
      this.mainTopic = this.openTopic.level===0? this.openTopic : this.category.find(v=>v.item===this.openTopic.parent)
      this.subTopic = this.category.filter(v=>v.parent===this.mainTopic.item)
      let list = this.subTopic.map(v=>v.id)
      list.push(this.mainTopic.id)
      let filter = this.openTopic.level===1? {category: this.openTopic.id} : {category__in: list}
      let val = {name: 'helplist', url: 'data/Help', params: {values: values, filter: filter}, page:1} 
      this.connection1.getApi([val])
    }
  }
}

</script>
