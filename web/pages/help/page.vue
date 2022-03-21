<!-- eslint-disable -->
<template>
  <div>
  <TopMenu v-bind="{type: 'tophead', tophead: this.title}" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
  <div class="column is-11 is-marginless is-paddingless">
  <div class="columns is-gapless is-centered is-marginless is-paddingless">
  <div class="column is-11 is-marginless is-paddingless">

  <div class="px-3 mt-4">
  <div class="tile is-ancestor is-marginless is-paddingless" v-if="headline.length>0">
  <div class="tile is-vertical is-9">
    <div class="tile">
    <div class="tile is-parent is-7">
      <article class="tile is-child">
        <p v-for="(v,i) in headline.slice(0,1)" :key="i">
          <nuxt-link  :to="{path: '/help/open', query: {id: v.id}}">
          <img v-lazy="connection.path + 'static/images/' + v.image">
          </nuxt-link>
        </p>
      </article>
      </div>

      <div class="tile is-parent">
        <article class="tile is-child">
        <div class="ml15 mr15">
      <nuxt-link class="fs24 fb500 has-text-dark" :to="{path: '/help/open', query: {id: headline[0].id}}">
        {{headline[0].title}} 
      </nuxt-link>
      <p class="mt10 fs16 has-text-dark content" v-for="(v,i) in headline.slice(0,1)" :key="i"> 
          {{v.subtitle}}
          <nuxt-link class="tag has-background-white tagborder is-rounded"
          :to="{path: '/help/category', query: {id: v.category}}"> {{v.category__value}} </nuxt-link>
       </p>
        </div>
        </article>
      </div>
    </div>

    <div class="tile is-parent">
      <article class="tile is-child" v-for="(v,i) in headline.slice(2,5)" :key="i">
        <div class="ml10 mr10" v-if="!v.dummy">
      <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: '/help/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link>
        <p class="mt10 fs16 has-text-dark mb20 content">  {{v.subtitle}} 
          <nuxt-link class="tag has-background-white tagborder is-rounded"
          :to="{path: '/help/category', query: {id: v.category}}"> {{v.category__value}} 
          </nuxt-link> 
        </p>
        </div>
      </article>
    </div>
  </div>
  <div class="tile is-parent">
    <article class="tile is-child">
      <div class="content" v-for="(v,i) in headline.slice(1,2)" :key="i">
        <template v-if="!v.dummy">
        <nuxt-link :to="{path: '/help/open', query: {id: v.id}}">
      <img v-lazy="connection.path + 'static/images/' + v.image">
    </nuxt-link>
        <p class="mt10">
          <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: '/help/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link>
        </p>
          <p class="mt10 fs16 has-text-dark content">  {{v.subtitle}} 
            <nuxt-link class="tag has-background-white tagborder is-rounded"
            :to="{path: '/help/category', query: {id: v.category}}"> {{v.category__value}} 
            </nuxt-link> </p>
        </template>
      </div>
    </article>
  </div>
</div>

  <div v-for="(v,i) in topic" :key="i">
    <!-- Main container -->
    <nav class="level mt40 mb40 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
    <!-- Left side -->
    <div class="level-left">
        <div class="level-item">
        <p class="title"> 
          <nuxt-link class="has-text-dark" :to="{path: '/help/category', query: {id: v.id}}"> {{v.value}} </nuxt-link>
          </p>
        </div>
          <div class="level-item">
              <p class="tags">
        <nuxt-link class="tag is-medium is-rounded"  :to="{path: '/help/category', query: {id: x.id}}"
        v-for="(x,j) in category.filter(y=>y.parent===v.item)" :key="j">
          {{x.value}}
        </nuxt-link>
      </p>
        </div>
    </div>
        <!-- Right side -->
    <div class="level-right" v-if="v.data.length>0">
        <p class="level-item">
        <nuxt-link class="fs16" :to="{path: '/help/category', query: {id: v.id}}"> Xem thêm 
            <span class="icon"> <i class="mdi mdi-chevron-double-right"/> </span> 
        </nuxt-link>
        </p>
    </div>
    </nav>

    <div class="fs20 fb500 has-text-primary has-text-centered mt30" v-if="v.data.length===0">
      Chưa có tin trong mục này
    </div>

    <div class="tile is-ancestor" v-else>
        <div class="tile is-5 is-vertical">
          <div class="tile is-parent" v-for="(x,j) in v.data.slice(0,3)" :key="j">
              <article class="tile is-child is-4">
      <nuxt-link  :to="{path: '/help/open', query: {id: x.id}}" v-if="!x.dummy">
      <img v-lazy="connection.path + 'static/images/' + x.image">
      </nuxt-link>
              </article>
              
              <article class="tile is-child">
                <p class="ml20 fs18 fb500" v-if="!x.dummy"> 
                 <nuxt-link class="has-text-dark" :to="{path: '/help/open', query: {id: x.id}}"> {{x.title}} </nuxt-link>
                 </p>
              </article>
          </div>
        </div>
            <div class="tile is-parent">
      <article class="tile is-child is-7">
        <div class="ml20 mr20 mb20" v-for="(x,j) in v.data.slice(3,5)" :key="j">
      <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: '/help/open', query: {id: x.id}}" v-if="!x.dummy">
        {{x.title}} 
      </nuxt-link>
        <p class="mt10 fs16 has-text-dark content" v-if="!x.dummy">  {{x.subtitle}} 
          <nuxt-link class="tag has-background-white tagborder is-rounded"
          :to="{path: '/help/category', query: {id: x.category}}"> {{x.category__value}} 
          </nuxt-link> 
        </p>
        </div>
      </article>
        <article class="tile is-child" v-for="(x,j) in v.data.slice(5,6)" :key="j">
            <div class="ml10 mr10" v-if="!x.dummy">
        <nuxt-link class="image" :to="{path: '/help/open', query: {id: x.id}}">
        <img v-lazy="connection.path + 'static/images/' + x.image">
        </nuxt-link>

        <div class="mt10"> 
          <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: '/help/open', query: {id: x.id}}"> {{x.name}}
              {{x.title}} 
          </nuxt-link>
          <p class="mt10 fs16 has-text-dark content">  {{x.subtitle}} 
           <nuxt-link class="tag has-background-white tagborder is-rounded"
           :to="{path: '/help/category', query: {id: x.category}}"> {{x.category__value}} </nuxt-link> 
          </p>
        </div>
            </div>
        </article>
        </div>
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

import Category from  '~/components/Category.vue'
import Footer from '~/components/Footer.vue'
import mixing from '@/assets/js/mixing.js'

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
      headline: [],
      topic: [],
      title: ''
    }
  },

  head() {
    return {
      title: 'Trang trợ giúp sử dụng'
    }
  },
    

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') this.getData()
    },

    'connection1.getdataReady': function(newVal) {
      if (newVal==='success') {
        this.helplist = this.connection1.getbatchData
        this.fillData()
      }
    }
  },

  created() {
    this.title = 'Chào mừng ' + (this.login? this.login.name : 'bạn') + ' đến với trang trợ giúp'
    let list = this.connection.checkDataReady(['helpcategory'])
    if(list.filter(v=>!v.ready).length>0) this.connection.getApi(list)
    else this.getData()
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    },

    category: {
      get: function() {return this.$store.state.helpcategory},
      set: function(val) {this.$store.commit('updateHelpCategory', {helpcategory: val})}
    },

    helplist: {
      get: function() {return this.$store.state.helplist},
      set: function(val) {this.$store.commit('updateHelpList', {helplist: val})}
    },
  },

  methods: {
    getData() {
      if(this.helplist) {
        this.fillData()
        return
      }

      let connlist = []
      let values = 'id,title,subtitle,content,image,category,category__value,category__level,category__parent'
      this.category.map(v=>{
        let val = {name: v.id, url: 'data/Help', params: {values: values, page: 1, perpage: 20, filter: {category: v.id}}}
        connlist.push(val)
      })
      this.connection1.getApi(connlist)
    },

    fillData() {
      for (let index = 0; index < 10; index++) {
        if(this.headline.length<10) {
          this.helplist.map(v=>{
            if(v.data.length>index) this.headline.push(v.data[index])
          })
        }
      }
      if(this.headline.length>0) this.headline = mixing.dummyData(this.headline)

      this.topic = this.$copy(this.category.filter(v=>v.level===0))
      this.topic.map(v=>{
        v.data = []
        let list = this.category.filter(x=>x.parent===v.item || x.id===v.id)
        for (let index = 0; index < 10; index++) {
          if(v.data.length<10) {
            list.map(x=>{
              let found = this.helplist.find(y=>y.name===x.id)
              if(found.data.length>index) v.data.push(found.data[index])
            })
          }
        }
        if(v.data.length>0) v.data = mixing.dummyData(v.data)
      })
    }
  }
}

</script>
