<!-- eslint-disable -->
<template>
    <nav class="level is-mobile" v-if="topiclike">
      <div class="level-left">
      <div class="level-item has-text-grey-darker">
      <div class="dropdown is-hoverable is-up">
        <div class="dropdown-trigger">
          <a :class="topiclike.you? 'has-text-primary fs15' : 'has-text-grey-darker fs15'"
            aria-haspopup="true" aria-controls="dropdown-menu4">
            <span class="icon fs20" :class="topiclike.you? 'has-text-primary fs15' : 'has-text-grey-darker fs15'"
            ><i class="mdi mdi-thumb-up-outline"></i></span> thích
          </a>
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content" style="width:264px">
            <div class="dropdown-item">
              <a class="fs22" v-for="(x,j) in emoji" :key="j" @click="likeTopic(x, topiclike)">
                {{x.value}}
              </a>
            </div>
          </div>
        </div>
      </div>
      </div>
        <div class="level-item ml10">
         <a @click="gotoComment()" class="has-text-grey-darker fs15"> 
           <span class="icon fs20"><i class="mdi mdi-comment-outline"></i></span> bình luận
         </a>
        </div>
          <div class="level-item has-text-grey-darker ml10" v-if="topiclike.type.length>0"> 
          <span class="fs18" :class="j>0? 'ml3' : ''" v-for="(x,j) in topiclike.type" :key="j">
          {{x.type__value}}
        </span>

          <template v-if="topiclike.total>0">
          <span class="ml5"> </span>
          <b-dropdown aria-role="list">
            <p
              class="tag has-background-white tagborder is-rounded"
              slot="trigger"
              role="button"
            >
            <span class="fs17 has-text-black"> {{topiclike.total}} </span>
            </p>
            <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-for="(x,j) in topiclike.list" :key="j" 
            style="border-bottom: 1px solid hsl(0, 0%, 86%)">{{x.user__name}} <span class="ml10"> {{x.type__value}} </span>
            </b-dropdown-item>
            <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-if="topiclike.total>topiclike.list.length">
              và {{topiclike.total - topiclike.list.length}} người khác 
            </b-dropdown-item>
        </b-dropdown>
        </template>
    </div>
    <div class="level-item ml10 fs14 has-text-grey" v-if="showtime && !ismobile">
      {{displayTime(topic)}}
    </div>
    </div>
    </nav>
</template>

<script>
/* eslint-disable */

import mixing from '@/assets/js/mixing.js'
import socket from '~/plugins/socket.io.js'

export default {
  props: ['name', 'keyval', 'api', 'likeApi', 'topic', 'showtime'],

  data() {
    return {
      topiclike: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      emoji: []
    }
  },

  created() {
    this.emoji = this.sysapi.filter2var('list', 'emoji')
    let id = this.topic.id
    let values = 'id,user,user__name,type,type__value,' + this.name + ',' + this.keyval 
    let found = this.connection.requirelist.find(v=>v.name===this.likeApi)
    let filter = this.keyval==='comment'? {comment__isnull: 1} : {}
    filter[this.name] = id 
    var connlist = [{name: 'liketopic', url: found.url, params: {values: values, page: 1, filter: filter}}]

    filter = {comment__isnull: 1}
    if(this.login) {
      filter.user = this.login.id
      filter[this.name] = id
      var val1 = {name: 'youlike', url: found.url, params: {values: values, filter: filter}}
      connlist.push(val1)        
    }
    this.connection.getApi(connlist)
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') {        
        let data1 = this.login? this.connection.getbatchData.find(v=>v.name==='youlike').data : []
        let data2 = this.connection.getbatchData.find(v=>v.name==='liketopic').data
  
        let found = data1.find(v=>!v.comment)
        this.topiclike = {you: found? true : false, id: found? found.id : undefined}
        this.topiclike.list = found? (data2.find(v=>v.id===found.id)? data2 : data2.concat(data1)) : data2
        this.topiclike.type = mixing.unique(this.topiclike.list, ['type'])
        let status = this.connection.getbatchStatus.find(v=>v.name==='liketopic')
        this.topiclike.total = status.total_rows
      }
    },

    'connection1.getupdateStatus': function(newVal) {
      if(newVal===true) { 
        let data = this.$copy(this.connection1.getupdateRecord)
        data.user__name = this.login.name
        data.type__value = this.emoji.find(v=>parseInt(v.id)===data.type).value
        if(!this.topiclike.you) {
          this.topiclike.id = data.id
          this.topiclike.you = true
          this.topiclike.list.push(data)
          this.topiclike.type = mixing.unique(this.topiclike.list, ['type'])
          this.topiclike.total = this.topiclike.total + 1
          if(data.user!==this.topic.creator) {
            let found = this.sysapi.find3var('list', 'notification', 'emotion')
            let link = {path: this.$route.path, query: this.$route.query}
            let obj = {receiver: this.topic.creator, sender: this.login.id, link: JSON.stringify(link), type: found.id, seen: false, refid: this.topic.id}
            let values ='id,sender,sender__name,sender__avatar,receiver,type,type__value,seen,refid,link,create_time'
            this.connection2.insert('notification', obj, values)
          }
        } else {
          let index = this.topiclike.list.findIndex(v=>v.id===this.topiclike.id)
          if(index>=0) this.topiclike.list[index] = data
          this.topiclike.type = mixing.unique(this.topiclike.list, ['type'])
        }
        this.topiclike = this.$copy(this.topiclike)
      }
    },

    'connection2.getupdateStatus': function(newVal) {
      if(newVal===true) {
        let data = this.connection2.getupdateRecord
        socket.emit('send-message', {name: 'notification', data: [data]})
      }
    }
  },

  computed: {
    sysapi: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit('updateLogin', {login: val})}
    },

    notification: {
      get: function() {return this.$store.state.notification},
      set: function(val) {this.$store.commit('updateNotification', {notification: val})}
    },

    action: {
      get: function() {return this.$store.state.action},
      set: function(val) {this.$store.commit('updateAction', {action: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", {ismobile: val})}
    },
  },

  methods: {
    likeTopic(type, v) {
      if(!this.login) {
         this.$buefy.snackbar.open('Bạn cần đăng nhập để thể hiện cảm xúc')
         this.$router.push( {path: '/signin', query: {to: this.$route.path, params: JSON.stringify(this.$route.query)}})
         return
      }

      let data = {user: this.login.id, type: type.id, id: v.id}
      data[this.name] = this.topic.id
      data[this.keyval] = null
      if(data.id) this.connection1.update(this.likeApi, data)
      else this.connection1.insert(this.likeApi, data)
    },

    gotoComment() {
      this.action = {name: 'goto-comment', time: new Date()}
    },

    displayTime(v) {
      if(!v.create_time) return
      let result = mixing.dateDiffCalc(new Date(v.create_time), new Date())
      return result.display
    }
  }
}
</script>