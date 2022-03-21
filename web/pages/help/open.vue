<!-- eslint-disable -->
<template>
  <div>
  <TopMenu v-bind="{type: 'tophead', tophead: help? help.title : ''}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
  <div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-gapless is-centered is-marginless is-paddingless">
  <div class="column is-11 is-marginless is-paddingless">
    <div v-if="help" class="px-3 has-text-dark">
        <nav class="breadcrumb mt10 mb-3" aria-label="breadcrumbs">
  <ul>
    <li><nuxt-link to="/help/page">Trợ giúp</nuxt-link></li>
    <li v-if="help.category_parent">
      <nuxt-link :to="{path: '/help/category', query: {id: help.category_parent.id}}">
      {{help.category_parent.value}}
      </nuxt-link>
    </li>
    <li><nuxt-link :to="{path: '/help/category', query: {id: help.category}}">{{help.category__value}}</nuxt-link></li>
     <li class="is-active"> <a> Chi tiết </a></li>
  </ul>
</nav>

  <div class="tile is-ancestor is-marginless is-paddingless">
  <div class="tile is-8 is-parent">
    <div :class="ismobile? '' : 'mr-6'">
      <div class="fs24 has-text-dark fb500">  {{help.title}}
        <span class="ml-2 fs14 has-text-grey has-text-weight-normal" v-if="ismobile">{{displayTime(help)}}</span>
      </div>
        <Like class="mt-3" v-if="help"
    v-bind="{name: 'help', keyval: 'comment', api: 'helpcomment', likeApi: 'helplike', topic: help, showtime: true}">
  </Like>

    <p class="mt30 has-text-grey-darker fs17 content" v-html="help.content"> </p>
    </div>
  </div>
  <div class="tile is-4 is-vertical">
      <p class="panel-heading has-text-dark mt10 pt10 pb10 mb40 fs28">
    Các trợ giúp khác
  </p>
    <div class="columns" v-for="(v,i) in right" :key="i">
        <div class="column is-4">
        <nuxt-link :to="{path: '/help/open', query: {id: v.id}}">
      <img v-lazy="connection.path + 'static/images/' + v.image">
    </nuxt-link>
        </div>
        <div class="column is-8">
      <nuxt-link class="fb500 has-text-dark" :to="{path: '/help/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link> 
        </div>
    </div>
  </div>
  </div>
  
  <Comment class="mt-5" v-if="help" ref="commentbox"
    v-bind="{name: 'help', keyval: 'comment', api: 'helpcomment', likeApi: 'helplike', topic: help}">
  </Comment>
    </div>

  <div class="px-3">
  <nav class="level is-mobile mt-6 mb40 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);" v-if="help && below.length>0">
    <div class="level-left">
      <div class="level-item">
      <p class="title"> {{help.category__value}} </p>
      </div>
    </div>

    <div class="level-right">
      <p class="level-item">
        <nuxt-link class="fs16" :to="{path: '/help/category', query: {id: help.category}}"> Xem thêm 
          <span class="icon"> <i class="mdi mdi-chevron-double-right"/> </span> 
        </nuxt-link>
      </p>
    </div>
  </nav>

  <div class="tile is-ancestor" v-if="below.length>0">
    <div class="tile is-parent">
    <article class="tile is-child" v-for="(v,i) in below" :key="i">
      <div class="ml10 mr10" v-if="!v.dummy">
      <nuxt-link class="image" :to="{path: '/help/open', query: {id: v.id}}">
      <img v-lazy="connection.path + 'static/images/' + v.image">
      </nuxt-link>
    <p class="mt15 mb20"> 
      <nuxt-link class="fb500 has-text-dark" :to="{path: '/help/open', query: {id: v.id}}"> {{v.name}}
        {{v.title}} 
      </nuxt-link>  
       </p>
      </div>
    </article>
    </div>
  </div>
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

import Footer from '~/components/Footer.vue'
import mixing from '@/assets/js/mixing.js'
import Comment from '~/components/Comment.vue'
import Like from '~/components/Like.vue'

export default {
  components: {
    TopMenu,
    Footer,
    Comment,
    Like
  },

  data() {
    return {
      connection: this.$connection(),
      connection1: this.$connection(),
      help: undefined,
      newslist: [],
      right: [],
      below: [],
      values: 'id,creator,title,content,image,category,category__value,category__level,category__parent,create_time'
    }
  },

  head() {
    return {
      title: 'Mở nội dung trợ giúp'
    }
  },  

  created() {
    let connlist = [{name: 'help', url: 'data/Help', params: {values: this.values, filter: {id: this.$route.query.id}}}]
    if(!this.category) connlist.push(this.connection.requirelist.find(v=>v.name==='helpcategory'))
    this.connection.getApi(connlist)
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') {
        let data = this.connection.getbatchData.find(v=>v.name==='help').data
        if(data.length===0) return

        this.help = data[0]
        if(this.help.category__level===1) {
          if(!this.category) this.category = this.connection.getbatchData.find(v=>v.name==='category').data
          let found = this.category.find(v=>v.item===this.help.category__parent)
          if(found) this.help.category_parent = found  
        }

        let found =  {name: 'related', url: 'data/Help', params: {values: this.values, filter: {category: this.help.category}, page: 1}}
        this.connection1.getApi([found])
      }
    },

    'connection1.getdataReady': function(newVal) {
      if (newVal==='success') {
        this.newslist = this.connection1.getbatchData[0].data
        let filter = this.newslist.filter(v=>v.id!==this.help.id)
        this.right = filter.slice(0,5)
        this.below = filter.slice(5,10)
        if(this.below.length>0) this.below = mixing.dummyData(this.below)
        this.below = this.below.slice(0,5)
      }
    },

    path: function(newVal) {
      this.help = undefined
      let row = this.newslist.find(v=>v.id===parseInt(newVal.id))
      if(!row) {
        let connlist = [{name: 'help', url: 'data/Help', params: {values: this.values, filter: {id: this.$route.query.id}}}]
        if(!this.category) connlist.push(this.connection.requirelist.find(v=>v.name==='helpcategory'))
        this.connection.getApi(connlist)
        return
      }

      let filter = this.newslist.filter(v=>v.id!==row.id)
      this.right = filter.slice(0,5)
      this.below = filter.slice(5,10)
      if(this.below.length>0) this.below = mixing.dummyData(this.below)
      this.below = this.below.slice(0,5)
      let self = this
      mixing.delay(function() {
        self.help = row
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }, 20)
    },

    action: function(newVal) {
      if(!newVal) return
      if(newVal.name==='goto-comment') this.$refs.commentbox.$el.scrollIntoView()
    }
  },

  computed: {
    path() {
      return this.$route.query
    },

    category: {
      get: function() {return this.$store.state.helpcategory},
      set: function(val) {this.$store.commit('updateHelpCategory', {helpcategory: val})}
    },

    action: {
      get: function() {return this.$store.state.action},
      set: function(val) {this.$store.commit('updateAction', {action: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit('updateIsMobile', {ismobile: val})}
    }
  },

  methods: {
    displayTime(v) {
      if(!v.create_time) return
      let result = mixing.dateDiffCalc(new Date(v.create_time), new Date())
      return result.display
    }
  }
}

</script>
