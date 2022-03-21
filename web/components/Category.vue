<!-- eslint-disable -->
<template>
<div v-if="showlist.length>0">
  <div class="tile is-ancestor mt-3" v-if="headline.length>0">
  <div class="tile is-vertical is-9">
    <div class="tile">
    <div class="tile is-parent is-7">
      <article class="tile is-child">
        <p v-for="(v,i) in headline.slice(0,1)" :key="i">
          <nuxt-link  :to="{path: keyword + '/open', query: {id: v.id}}" v-if="v.image">
          <img v-lazy="connection.path + 'static/images/' + v.image">
          </nuxt-link>
        </p>
      </article>
      </div>

      <div class="tile is-parent">
        <article class="tile is-child">
        <div class="ml15 mr15">
      <nuxt-link class="fs24 fb500 has-text-dark" :to="{path: keyword + '/open', query: {id: headline[0].id}}">
        {{headline[0].title}} 
      </nuxt-link>
      <p class="mt10 fs16 has-text-dark" v-for="(v,i) in headline.slice(0,1)" :key="i"> 
           {{v.subtitle}} 
          <nuxt-link class="tag has-background-white tagborder is-rounded"
          :to="{path: keyword + '/category', query: {id: v.category}}"> {{v.category__value}} </nuxt-link>
       </p>
        </div>
        </article>
      </div>
    </div>

    <div class="tile is-parent">
      <article class="tile is-child" v-for="(v,i) in headline.slice(2,5)" :key="i">
        <div class="ml10 mr10" v-if="!v.dummy">
      <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: keyword + '/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link>
        <p class="mt10 fs16 has-text-dark mb20">  {{v.subtitle}} 
          <nuxt-link class="tag has-background-white tagborder is-rounded"
          :to="{path: keyword + '/category', query: {id: v.category}}"> {{v.category__value}} 
          </nuxt-link> 
        </p>
        </div>
      </article>
    </div>
  </div>
  <div class="tile is-parent" v-if="!headline[1].dummy">
    <article class="tile is-child">
      <div class="content" v-for="(v,i) in headline.slice(1,2)" :key="i">
        <nuxt-link :to="{path: keyword + '/open', query: {id: v.id}}" v-if="v.image">
      <img v-lazy="connection.path + 'static/images/' + v.image">
    </nuxt-link>
        <p class="mt10">
          <nuxt-link class="fs18 fb500 has-text-dark" :to="{path: keyword + '/open', query: {id: v.id}}">
        {{v.title}} 
      </nuxt-link>
        </p>
          <p class="mt10 fs16 has-text-dark">  {{v.subtitle}} 
            <nuxt-link class="tag has-background-white tagborder is-rounded"
            :to="{path: keyword + '/category', query: {id: v.category}}"> {{v.category__value}} 
            </nuxt-link> </p>
      </div>
    </article>
  </div>
</div>

    <div v-for="(topic,i) in topics" :key="i">
    <!-- Main container -->
    <nav class="level is-mobile mt40 mb40 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
    <!-- Left side -->
    <div class="level-left">
        <div class="level-item">
        <p class="title fs30"> {{topic.value}} </p>
        </div>
    </div>

    <!-- Right side -->
    <div class="level-right" v-if="topic.data.length>0">
        <p class="level-item">
        <nuxt-link class="fs16" :to="{path: keyword + '/category', query: {id: topic.id}}"> Xem thêm 
            <span class="icon"> <i class="mdi mdi-chevron-double-right"/> </span> 
        </nuxt-link>
        </p>
    </div>
    </nav>

    <div class="fs20 fb500 has-text-primary has-text-centered mt30" v-if="topic.data.length===0">
      Chưa có tin trong mục này
    </div>

    <div class="tile is-ancestor" v-else>
            <div class="tile is-parent">
        <article class="tile is-child" v-for="(v,i) in topic.data" :key="i">
            <div class="ml10 mr10">
        <nuxt-link class="image" :to="{path: keyword + '/open', query: {id: v.id}}" v-if="v.image">
        <img v-lazy="connection.path + 'static/images/' + v.image">
        </nuxt-link>
        <p class="mt10"> 
        <nuxt-link class="has-text-dark fs18 fb500" :to="{path: keyword + '/open', query: {id: v.id}}"> {{v.name}}
            {{v.title}} 
        </nuxt-link>  
        </p>
        </div>
        </article>
        </div>
    </div>
    </div>
</div>
</template>

<script>
/* eslint-disable */
import mixing from '@/assets/js/mixing.js'


export default {
  props: ['showlist', 'subTopic', 'keyword'],

  data() {
    return {
      headline: [],
      topics: [],
      connection: this.$connection(),
    }
  },

  created() {
    this.headline = this.showlist.slice(0,6)
    this.headline = mixing.dummyData(this.headline)
    this.topics = this.$copy(this.subTopic)
    this.topics.map(v=>{
      let filter = this.showlist.filter(x=>x.category===v.id)
      if(filter.length>0) filter = mixing.dummyData(filter)
      v.data = filter.slice(0,5)
    })
  }
}
</script>