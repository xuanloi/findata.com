<!-- eslint-disable -->
<template>
<div>
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <div class="pt60"/>
<section class="hero is-white pt20 pb20">
    <div class="columns ">
        <div class="column is-1"> </div>
         <div class="column is-2"> <a class="button is-primary is-size-6" @click="createlink()">Tạo link </a> </div>
        <div class="column is-6 has-text-left">
        <div v-if="link !== ''">  
<a :href="link" class="is-size-6" style="text-decoration: underline;" v-html="link"></a>
    <div class="pt30 pb10">
        <h4 class="title is-size-4">Gửi link qua email</h4>
        <div class="field is-horizontal">

        <div class="field-body">
            <div class="field">
                
            <p class="control is-expanded">
              <label class="label"  v-html="api.getvalue(api.find3var('information','email','label'))"></label>
                <input class="input is-boder-gray font-df" type="text" placeholder="" v-model="email" @input="change()">
            </p>
            </div>

        <div class="field">        
            <p class="control is-expanded">
                <label class="label"  v-html="api.getvalue(api.find3var('information','subject','label'))"></label>
              <input class="input is-boder-gray font-df" type="text" placeholder="" v-model="subject" @input="change()">
            </p>
            </div>
        </div>
        </div>

        <div class="field is-horizontal">
        <div class="field-body">
            <div class="field">
            <div class="control">
                    <label class="label"  v-html="api.getvalue(api.find3var('information','content','label'))"></label>
                <textarea class="textarea is-boder-gray font-smaller" placeholder="" v-model="content" @input="change()"></textarea>
            </div>
            </div>
        </div>
        </div>

        <div class="field is-horizontal mt40">
        <div class="field-body">
            <div class="field">
            <div class="control">
              <a class="button is-primary is-size-6" @click="sendemail()">Gửi email </a>
              <span v-if="message" class=" pl30 pt10"
              :class="message.success? 'has-text-primary' : 'has-text-danger'"> {{message.text}} </span>
            </div>
            </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div v-if="link !== ''" class="column is-2"> 
            <a class="button is-primary is-size-6" @click="copylink()">Copy link</a> 
        </div>

    </div>
</section>
    <div class="mt20"/>
    <Footer> </Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'

import mixing from "@/assets/js/mixing.js";
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'

Vue.component('topmenu', TopMenu)
Vue.component('Footer', Footer)

export default {
  data() {
    return {
      tophead: 'Tạo liên kết mở tài khoản',
      link: '',
      email: '',
      subject: undefined,
      content: '',
      message: undefined,
      connection: this.$connection(),
      connection1: this.$connection()
    }
  },

  head() {
    return {
      title: 'Mở tài khoản người sử dụng'
    }
  },

  created() {
    this.subject =  this.api.getvalue(this.api.find3var('subtitle','account','link'))
  },

  watch: {
    'connection.getupdateStatus': function(newVal) {
      if(newVal===false) this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','message','msg3'))}
    },

   'connection1.getdataReady': function(newVal) {
      if(newVal) {
        this.message = {success: true, text: this.api.getvalue(this.api.find3var('inform','account','email-sent'))}
      }
      if(newVal==='error') {
        this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','message','msg3'))}
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
  },

  methods: {
    sendemail() {
      this.message = undefined
      if(this.email === '') {
          this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','account','email-empty'))}
      } else {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(re.test(String(this.email).toLowerCase()) === false) {
          this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','account','email-invalid'))}
        }
      }

      if(this.$empty(this.subject)) {
        this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','account','subject-empty'))}
      }
      else if(this.$empty(this.content)) {
        this.message = {success: false, text: this.api.getvalue(this.api.find3var('inform','account','content-empty'))}
      }
      if(this.message) return
      
      //send email
      let data = {'subject': this.subject, 'content': this.content, 'to': this.email}
      let found = {name: 'sendemail', url: 'send-email/', method: 'post', data: data, params: {}}
      this.connection1.getApi([found])
    },

    change() {
      this.message = undefined
    },

    createlink() {
      var key =  this.api.guid()
      let routeData = this.$router.resolve({name: 'account-register', query: {token: key}});
      var href = window.location.href 
      href = href.substring(0, href.indexOf(this.$route.path)) + routeData.href
      this.link = href
      this.content =  this.api.getvalue(this.api.find3var('information','email','content'))
      this.content += '\n'
      this.content += href
      this.content += '\n\n'
      this.content += this.api.getvalue(this.api.find3var('footer','company','name'))
      this.message = undefined
      this.email = ''
      
      var data =  {
          'guid' : key,
          'route_name': 'account-register',
          'query': 'token: ' + key,
          'link': this.link,
          'valid_from':  new Date(),
          'valid_to':  new Date(Date.now() + 2 * 24*60*60*1000),
          'action_result': this.api.getval(this.api.find3var('list','action-result','initialize'), 'id'),
          'detail': 'Account register link'
      }
      this.connection.insert('link', data)
    },

    copylink() {
      const el = document.createElement('textarea');
      el.value = this.link;
      el.setAttribute('readonly', '');
      el.style.position = 'absolute';
      el.style.left = '-9999px';
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
    }
  }
}
</script>