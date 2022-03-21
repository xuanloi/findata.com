<!-- eslint-disable -->
<template>
<div>
  <TopMenu v-bind="{type: 'tophead', tophead: news? news.title : ''}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
<div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-gapless is-centered is-marginless is-paddingless">
<div class="column is-11 is-marginless is-paddingless">
    <div v-if="news" class="px-3 has-text-dark">
        <nav class="breadcrumb mt10 mb-3" aria-label="breadcrumbs">
  <ul>
    <li><nuxt-link to="/news/page">Tin tức</nuxt-link></li>
    <li v-if="news.category_parent">
      <nuxt-link :to="{path: '/news/category', query: {id: news.category_parent.id}}">
      {{news.category_parent.value}}
      </nuxt-link>
    </li>
    <li><nuxt-link :to="{path: '/news/category', query: {id: news.category}}">{{news.category__value}}</nuxt-link></li>
     <li class="is-active"> <a> Chi tiết </a></li>
  </ul>
</nav>

  <div class="tile is-ancestor is-marginless is-paddingless">
  <div class="tile is-8 is-parent">
    <div :class="ismobile? '' : 'mr-6'">
      <div class="fs24 has-text-dark fb500">  {{news.title}} 
         <span class="ml-2 fs14 has-text-grey has-text-weight-normal" v-if="ismobile">{{displayTime(news)}}</span>
      </div>
        <Like class="mt-3" v-if="news"
    v-bind="{name: 'news', keyval: 'comment', api: 'newscomment', likeApi: 'newslike', topic: news, showtime: true}">
  </Like>
    <p class="mt20 has-text-dark fs17 content" v-html="news.content"> </p>
    </div>
  </div>
  <div class="tile is-4 is-vertical">
      <p class="panel-heading has-text-dark mt10 pt10 pb10 mb40 fs28">
    Các tin tức khác
  </p>
        <div class="columns"  v-for="(v,i) in right" :key="i">
        <div class="column is-4">  
      <nuxt-link :to="{path: '/news/open', query: {id: v.id}}">
      <img v-lazy="connection.path + 'static/images/' + v.image">
    </nuxt-link>
        </div>
        <div class="column is-8">
      <nuxt-link class="fb500 has-text-dark" :to="{path: '/news/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link> 
        </div>
    </div>
  </div>
  </div>

  <Comment class="mt-5" v-if="news" ref="commentbox"
    v-bind="{name: 'news', keyval: 'comment', api: 'newscomment', likeApi: 'newslike', topic: news}">
  </Comment>
   </div>

<div class="px-3">
<nav class="level is-mobile mt-6 mb40 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);" v-if="news && below.length>0">
  <div class="level-left">
    <div class="level-item">
     <p class="title"> {{news.category__value}} </p>
    </div>
  </div>

  <div class="level-right">
    <p class="level-item">
      <nuxt-link class="fs16" :to="{path: '/news/category', query: {id: news.category}}"> Xem thêm 
        <span class="icon"> <i class="mdi mdi-chevron-double-right"/> </span> 
      </nuxt-link>
    </p>
  </div>
</nav>

  <div class="tile is-ancestor" v-if="below.length>0">
    <div class="tile is-parent">
    <article class="tile is-child" v-for="(v,i) in below" :key="i">
      <div class="ml10 mr10" v-if="!v.dummy">
      <nuxt-link class="image" :to="{path: '/news/open', query: {id: v.id}}">
      <img v-lazy="connection.path + 'static/images/' + v.image">
      </nuxt-link>
    <p class="mt15 mb20"> 
      <nuxt-link class="fb500 has-text-dark" :to="{path: '/news/open', query: {id: v.id}}"> {{v.name}}
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
      news: undefined,
      newslist: [],
      right: [],
      below: [],
      values: 'id,creator,title,content,image,category,category__value,category__level,category__parent,create_time'
    }
  },

  head() {
    return {
      title: 'Xem nội dung thông báo'
    }
  },
    
  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') {
        let data = this.connection.getbatchData.find(v=>v.name==='news').data
        if(data.length===0) return

        this.news = data[0]
        if(this.news.category__level===1) {
          let found = this.category.find(v=>v.item===this.news.category__parent)
          if(found) this.news.category_parent = found  
        }

        let found =  {name: 'related', url: 'data/News', params: {values: this.values, filter: {category: this.news.category}, page: 1}}
        this.connection1.getApi([found])
      }
    },

    'connection1.getdataReady': function(newVal) {
      if (newVal==='success') {
        this.newslist = this.connection1.getbatchData[0].data
        let filter = this.newslist.filter(v=>v.id!==this.news.id)
        this.right = filter.slice(0,5)
        this.below = filter.slice(5,10)
        if(this.below.length>0) this.below = mixing.dummyData(this.below)
        this.below = this.below.slice(0,5)
      }
    },

    path: function(newVal) {
      this.news = undefined
      let row = this.newslist.find(v=>v.id===parseInt(newVal.id))
      let filter = this.newslist.filter(v=>v.id!==row.id)
      this.right = filter.slice(0,5)
      this.below = filter.slice(5,10)
      if(this.below.length>0) this.below = mixing.dummyData(this.below)
      this.below = this.below.slice(0,5)
      let self = this
      
      mixing.delay(function() {
        self.news = row
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }, 20)
    },

    action: function(newVal) {
      if(!newVal) return
      if(newVal.name==='goto-comment') this.$refs.commentbox.$el.scrollIntoView()
    }
  },

  created() {
    let connlist = [{name: 'news', url: 'data/News', params: {values: this.values, filter: {id: this.$route.query.id}}}]
    if(!this.category) connlist.push(this.connection.requirelist.find(v=>v.name==='category'))
    this.connection.getApi(connlist)
  },

  computed: {
    path() {
      return this.$route.query
    },

    category: {
      get: function() {return this.$store.state.category},
      set: function(val) {this.$store.commit('updateCategory', {category: val})}
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
