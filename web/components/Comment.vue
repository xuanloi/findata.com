<!-- eslint-disable -->
<template>
<div>
  <nav class="level is-mobile mt40 mb30 pb10" style=" border-bottom: 1px solid hsl(0, 0%, 86%);">
    <!-- Left side -->
    <div class="level-left">
        <div class="level-item">
        <p class="title fs30"> Bình luận</p>
        </div>
    </div>

    <!-- Right side -->
    <div class="level-right">
        <p class="level-item">
        <a @click="sortaz = !sortaz">
        <span class="icon fs24"> <i :class="sortaz? 'mdi mdi-sort-alphabetical-ascending' : 'mdi mdi-sort-alphabetical-descending'"> </i>
        </span>
        </a>
        </p>
    </div>
    </nav>

  <div class="tile is-ancestor px-0 mx-0 py-0 my-0">
  <div class="tile is-vertical px-0 mx-0 py-0 my-0">
    <div class="tile is-parent px-0 mx-0 py-0 my-0" v-for="(v,i) in comments.filter(v=>v.parent===null)" :key="i">
    <div class="tile is-child is-8 px-0 mx-0 py-0 my-0">
    <article class="media my-2">
  <figure class="media-left" v-if="!ismobile">
    <b-tooltip :label="v.creator__name" type="is-dark" position="is-bottom" v-if="!v.creator__avatar">
 <div class="number-circle" style="width:40px; height:40px; padding:4px">
      <div class="is-vertical-center">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + v.creator__name.substring(0,1).toLowerCase() + ' fs30'"></i>
      </span>
      </div>
      </div>
      </b-tooltip>

     <figure class="image" style="width:40px; height:40px" v-else>
       <b-tooltip :label="v.creator__name" type="is-dark" position="is-bottom">
      <img class="is-rounded" :src="connection.path + 'static/images/' + v.creator__avatar"/>
       </b-tooltip> 
    </figure>
  </figure>
  <div class="media-content">
  <nav class="level is-mobile mb-2" v-if="ismobile">
  <div class="level-left">
    <div class="level-item">
      <b-tooltip :label="v.creator__name" type="is-dark" position="is-right" v-if="!v.creator__avatar">
         <div class="number-circle" style="width:40px; height:40px; padding:4px">
      <div class="is-vertical-center">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + v.creator__name.substring(0,1).toLowerCase() + ' fs30'"></i>
      </span>
      </div>
      </div>
      </b-tooltip>
     <figure class="image" style="width:40px; height:40px" v-else>
       <b-tooltip :label="v.creator__name" type="is-dark" position="is-right">
      <img class="is-rounded" :src="connection.path + 'static/images/' + v.creator__avatar"/>
       </b-tooltip>
    </figure>
    </div>
    <div class="level-item fb500"> 
      {{v.creator__name}}
      <span class="ml-2 fs14 has-text-grey has-text-weight-normal">{{displayTime(v)}}</span>
    </div>
    </div>
    </nav>
    
    <div class="content" @mouseover="focus=v">
    <span v-html="v[keyval]" class="has-text-grey-darker" v-if="v[keyval].indexOf('$$')<0"> </span>
     <vue-mathjax :formula="v[keyval]" :safe="false" class="has-text-grey-darker" v-else></vue-mathjax>
    </div> 
  
  <div class="field is-grouped is-grouped-multiline mb-1" @mouseover="focus=v">
  <div class="control">
          <div class="dropdown is-hoverable is-up">
        <div class="dropdown-trigger">
          <a :class="commentlike.find(x=>x.id===v.id)? (commentlike.find(x=>x.id===v.id).you? 'has-text-primary fs15' : 'has-text-grey-darker fs15') : 'has-text-grey-darker fs15'"
            aria-haspopup="true" aria-controls="dropdown-menu4">
            <span class="icon fs20" :class="commentlike.find(x=>x.id===v.id)? (commentlike.find(x=>x.id===v.id).you? 'has-text-primary fs15' : 'has-text-grey-darker fs15') : 'has-text-grey-darker fs15'"
            ><i class="mdi mdi-thumb-up-outline"></i></span> thích
          </a>
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content" style="width:264px">
            <div class="dropdown-item">
              <a class="fs22" v-for="(x,j) in emoji" :key="j" @click="likeComment(x, v)">
                {{x.value}}
              </a>
            </div>
          </div>
        </div>
      </div>
  </div>
  <div class="control ml10">
      <a @click="openReply(v)" class="has-text-grey-darker fs15"> 
          <span class="icon fs20"><i class="mdi mdi-comment-outline"></i></span> trả lời
      </a>
      </div>
        <div class="control" v-if="commentlike.find(x=>x.id===v.id)? commentlike.find(x=>x.id===v.id).total>0 : 1<0"> 
        <div class="ml10" v-for="(k,s) in commentlike.filter(x=>x.id===v.id)" :key="s">
        <span class="fs17" :class="j>0? 'ml3' : ''" v-for="(x,j) in k.type" :key="j">
        {{x.type__value}}
        </span>
      
      <template v-if="k.total>0">
        <span class="ml3"> </span>
        <b-dropdown aria-role="list">
          <p
            class="tag has-background-white tagborder is-rounded"
            slot="trigger"
            role="button"
          >
          <span class="fs17 has-text-black"> {{k.total}} </span>
          </p>
          <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-for="(x,j) in k.list" :key="j" 
          style="border-bottom: 1px solid hsl(0, 0%, 86%)">{{x.user__name}} <span class="ml10"> {{x.type__value}} </span>
          </b-dropdown-item>
          <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-if="k.total>k.list.length">
            và {{k.total - k.list.length}} người khác 
          </b-dropdown-item>
      </b-dropdown>
      </template>
    </div>
    </div>
    <div class="control ml10 fs14 has-text-grey" v-if="!ismobile">
        {{displayTime(v)}}
      </div>
    <div class="control ml10" v-if="focus===v">
    <a @click="violate=true"> <span class="icon fs20" style="color:	red"> <i class="mdi mdi-alert"> </i> </span> </a>
    <a @click="editComment(v)" v-if="login? login.id===v.creator : 1<0"> 
      <span class="icon fs20 ml20" style="color:	red"> <i class="mdi mdi-square-edit-outline"> </i> </span>
    </a>
    </div>
  </div>

  <div class="tile is-ancestor px-0 mx-0 py-0 my-0" v-if="comments.filter(h=>h.parent===v.id).length>0">
  <div class="tile is-vertical px-0 mx-0 py-0 my-0">
    <div class="tile is-parent px-0 mx-0 py-0 my-0" v-for="(ele,h) in comments.filter(h=>h.parent===v.id)" :key="h">
    <div class="tile is-child px-0 mx-0 py-0 my-0" :class="ele.image? 'is-10' : 'is-12'" >
    <article class="media my-2">
  <figure class="media-left">
    <b-tooltip :label="ele.creator__name" type="is-dark" :position="ismobile? 'is-right' : 'is-bottom'" v-if="!ele.creator__avatar">
 <div class="number-circle" style="width:40px; height:40px; padding:4px">
      <div class="is-vertical-center">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + ele.creator__name.substring(0,1).toLowerCase() + ' fs30'"></i>
      </span>
      </div>
      </div>
      </b-tooltip>

       <figure class="image" style="width:40px; height:40px" v-else>
          <b-tooltip :label="ele.creator__name" type="is-dark" :position="ismobile? 'is-right' : 'is-bottom'">
      <img class="is-rounded" :src="connection.path + 'static/images/' + ele.creator__avatar"/>
          </b-tooltip>
    </figure>

  </figure>
  <div class="media-content" @mouseover="focus=ele">
    <div class="content">
    <span v-html="ele[keyval]" class="has-text-grey-darker" v-if="ele[keyval].indexOf('$$')<0"> </span>
    <vue-mathjax :formula="ele[keyval]" :safe="false" class="has-text-grey-darker" v-else></vue-mathjax>
    </div>

  <div class="field is-grouped is-grouped-multiline mb-1">
  <div class="control">
          <div class="dropdown is-hoverable is-up">
        <div class="dropdown-trigger">
          <a :class="commentlike.find(x=>x.id===ele.id)? (commentlike.find(x=>x.id===ele.id).you? 'has-text-primary fs15' : 'has-text-grey-darker fs15') : 'has-text-grey-darker fs15'"
            aria-haspopup="true" aria-controls="dropdown-menu4">
            <span class="icon fs20" :class="commentlike.find(x=>x.id===ele.id)? (commentlike.find(x=>x.id===ele.id).you? 'has-text-primary fs15' : 'has-text-grey-darker fs15') : 'has-text-grey-darker fs15'"
            ><i class="mdi mdi-thumb-up-outline"></i></span> thích
          </a>
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content" style="width:264px">
            <div class="dropdown-item">
              <a class="fs22" v-for="(x,j) in emoji" :key="j" @click="likeComment(x, ele)">
                {{x.value}}
              </a>
            </div>
          </div>
        </div>
      </div>
  </div>
    <div class="control" v-if="commentlike.find(x=>x.id===ele.id)? commentlike.find(x=>x.id===ele.id).total>0 : 1<0">
       <div class="ml10" v-for="(k,s) in commentlike.filter(x=>x.id===ele.id)" :key="s"> 
          <span class="fs17" :class="j>0? 'ml3' : ''" v-for="(x,j) in k.type" :key="j">
          {{x.type__value}}
        </span>

          <template v-if="k.total>0">
          <span class="ml5"> </span>
          <b-dropdown aria-role="list">
            <p
              class="tag has-background-white tagborder is-rounded"
              slot="trigger"
              role="button"
            >
            <span class="fs17 has-text-black"> {{k.total}} </span>
            </p>
            <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-for="(x,j) in k.list" :key="j" 
            style="border-bottom: 1px solid hsl(0, 0%, 86%)">{{x.user__name}} <span class="ml10"> {{x.type__value}} </span>
            </b-dropdown-item>
            <b-dropdown-item class="has-background-grey-darker has-text-white" aria-role="listitem" v-if="k.total>k.list.length">
              và {{k.total - k.list.length}} người khác 
            </b-dropdown-item>
        </b-dropdown>
        </template>
  </div>
  </div>
      <div class="control ml10 fs14 has-text-grey" v-if="!ismobile">
        {{displayTime(ele)}}
      </div>
    <div class="control ml10" v-if="focus===ele">
    <a @click="violate=true"> <span class="icon fs20" style="color:	red"> <i class="mdi mdi-alert"> </i> </span> </a>
    <a @click="editReplyComment(ele)" v-if="login? login.id===ele.creator : 1<0"> 
      <span class="icon fs20 ml20" style="color:	red"> <i class="mdi mdi-square-edit-outline"> </i> </span>
    </a>
      </div>
  </div>
  </div>
    </article>
    </div>

    <div class="tile is-child is-2" v-if="ele.image">
      <a class="image ml10 mr10" v-if="ele.image" @click="gallery=ele.image">
       <img v-lazy="connection.path + 'static/images/' + ele.image">
      </a>
    </div>
    </div>
  </div>
      </div>

    <div class="tile is-ancestor px-0 mx-0 py-0 my-0" v-if="reply? reply.id===v.id : 1<0" :id="'replybox' + v.id">
    <div class="tile is-parent px-0 mx-0 py-0 my-0">
      <article class="tile is-child" :class="(replyImage || !login) ? 'is-10' : ''">
        <textarea class="textarea" rows="2" :placeholder="placeholder" v-model="replyContent"></textarea>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='reply')">{{errors.find(v=>v.name==='reply').text}}</p>

   <nav class="level is-mobile mt15" v-if="login">
  <div class="level-left">
    <div class="level-item">
      <a class="button is-primary" @click="replyComment()"> Trả lời </a>
    </div>
    <div class="level-item">
      <a class="button is-dark is-light"
      @click="closeReply()"> Hủy </a>
    </div>
  </div>
    <div class="level-right">
    <div class="level-item"> 
        <div>
          <a class="button is-success is-light" @click="media = {component: componentid, name: 'reply-image', open: true}"> Hình ảnh (nếu có) </a>
        </div>
    </div>
    </div>
   </nav>
      </article>
      
    <article class="tile is-child is-2" v-if="replyImage || !login">
      <template class="tile is-child" v-if="login">
      <div v-if="replyImage" class="ml10 mr10">
      <a class="image" @click="gallery=replyImage">
        <img v-lazy="connection.path + 'static/images/' + replyImage">
      </a>
      <p class="has-text-centered">
        <a @click="replyImage=undefined"> <span class="icon"> 
          <i class="mdi mdi-close-circle-outline has-text-danger fs22"/> </span> 
        </a>
      </p>
      </div>    
      </template>
      <p v-else>
       <a @click="getLink()" class="button is-primary is-outlined ml-4 mt-3"> Đăng nhập </a>
     </p>
      </article>
    </div>
  </div>
  </div>
  </article>
  </div>

    <div class="tile is-2 is-child">
      <a class="image ml10 mr10" v-if="v.image" @click="gallery=v.image">
       <img v-lazy="connection.path + 'static/images/' + v.image">
      </a>
    </div>
    </div>
  </div>
</div>

 <b-pagination v-if="total>perPage" class="mt10"
            :total="total"
            :current.sync="current"
            range-before="2"
            range-after="2"
            :rounded=true
            :per-page="perPage"
            icon-prev="chevron-left"
            icon-next="chevron-right"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">
        </b-pagination>

    <div class="tile is-ancestor mt-3" ref="editorbox">
  <div class="tile is-parent">
    <div class="tile is-child is-9">
      <article class="media">
    <div class="media-content">
      <div class="field">
        <div class="control">
        <editor
        :placeholder="placeholder"
        v-model="content"
       api-key="0a3xn20t37fgzj36azuoo8e1fscw2q0xg0k2t12k7ztg5f0m"
       :init="{
         height: 280,
         menubar: true,
        statusbar: true,
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help'
       }"
     />
        </div>
      <p class="help is-danger" v-if="errors.find(v=>v.name==='comment')">{{errors.find(v=>v.name==='comment').text}}</p>
      </div>
      <nav class="level is-mobile mt20 mb-2" v-if="login">
        <div class="level-left">
          <div class="level-item">
            <a class="button is-primary" @click="createComment()">{{ismobile? 'Gửi đi' :  'Gửi bình luận' }} </a>
          </div>
        </div>
         <div class="level-item" v-if="ismobile">
            <a class="button is-success is-light ml-2" @click="media = {component: componentid, name: 'comment-image', open: true}">Hình ảnh (nếu có)</a>
         </div>
      </nav>
    </div>
  </article>

  </div>
  <div class="tile">
    <article class="tile is-child" v-if="login">
      <div v-if="image" class="ml10 mr10">
    <a class="image" @click="gallery=image">
      <img v-lazy="connection.path + 'static/images/' + image">
    </a>
      <p class="has-text-centered">
        <a @click="image=undefined"> <span class="icon"> 
          <i class="mdi mdi-close-circle-outline has-text-danger fs22"/> </span> 
        </a>
      </p>
      </div>
        <div v-else-if="!ismobile">
          <a class="button is-success is-light ml20" @click="media = {component: componentid, name: 'comment-image', open: true}"> Hình ảnh (nếu có) </a>
        </div>
    </article>
   <article class="tile is-child" v-else>
     <p>
       <a @click="getLink()" class="button is-primary is-outlined ml-4 mt-4"> Đăng nhập </a>
     </p>
   </article>
  </div>  
  </div>
  </div>

  <div class="modal is-active" v-if="openMedia===componentid">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content" style="position: absolute; top: 0px">
        <media v-bind="{mediatype: 'image', modal: true}" />
     </div>
    <button @click="media=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
  </div>

  <div class="modal is-active" v-else-if="violate">
  <div class="modal-background"></div>
  <div class="modal-card">
    <section class="modal-card-body">
      <p class="has-text-right">
       <button @click="violate=false" class="delete is-large has-background-grey-darker" aria-label="close"></button>
      </p>
        <Violate v-bind="{comment: focus, name: this.name}" class="ml10 mr10" />
    </section>
  </div>
</div>

<div class="modal is-active" v-else-if="gallery">
  <div class="modal-background"></div>
  <div class="modal-content">
   <div class="tile is-ancestor ml10 mr10 mt10 mb10">
  <div class="tile is-2"></div>
  <div class="tile is-8">
    <img v-lazy="connection.path + 'static/images/' + gallery" class="mt0 mb0 pt0 pb0">
    </div>
  </div>
</div>  
<button @click="gallery=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
</div>

</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import Editor from '@tinymce/tinymce-vue'
import mixing from '@/assets/js/mixing.js'

import Violate from '~/components/Violate.vue'
import media from '@/pages/media.vue'
import socket from '~/plugins/socket.io.js'

export default {
  props: ['name', 'keyval', 'api', 'likeApi', 'topic'],

  components: {
    Editor,
    Violate,
    media
  },

  data() {
    return {
      content: undefined,
      image: undefined,
      gallery: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(this.$buefy),
      connection4: this.$connection(this.$buefy),
      connection5: this.$connection(),
      connection6: this.$connection(this.$buefy),
      commentlike: [],
      comments: [],
      sortaz: true,
      placeholder: undefined,
      reply: undefined,
      replyImage: undefined,
      replyContent: undefined,
      isReply: false,
      current: 1,
      perPage: 10,
      total: 0,
      focus: undefined,
      violate: false,
      errors: [],
      editRecord: undefined,
      componentid: mixing.id(),
      values: undefined,
      emoji: [],
      currentComment: undefined
    }
  },

  created() {
    this.emoji = this.sysapi.filter2var('list', 'emoji')
    if(!this.login) {
      if(this.keyval==='comment') this.placeholder = 'Hãy đăng nhập để bình luận'
      else this.placeholder = 'Hãy đăng nhập để trả lời'
    } else {
      if(this.keyval==='comment') this.placeholder = 'Viết bình luận của bạn tại đây'
      else this.placeholder = 'Viết câu trả lời của bạn tại đây'
    }
    this.getData()
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if (newVal==='success') {
        let data = this.connection.getbatchData[0].data
        if(data.length===0) return
        let found = this.$copy(this.connection.requirelist.find(v=>v.name===this.api))
        let filter = {parent__in: data.map(v=>v.id)}
        filter[this.name] = this.topic.id
        found.params = {values: this.values, page: 1, filter: filter, sort: this.sortaz? 'create_time' : '-create_time'}
        this.connection6.getApi([found])
      }
    },

    'connection6.getdataReady': function(newVal) {
      if (newVal==='success') {
        let data = this.$copy(this.connection.getbatchData[0].data)
        let data1 = this.$copy(this.connection6.getbatchData[0].data)
        this.comments = data.concat(data1)
        this.total = this.connection.getbatchStatus[0].total_rows
        this.getLike()
      }
    },
    
    'connection1.getdataReady': function(newVal) {
      if (newVal==='success') {
        let data1 = this.login? this.connection1.getbatchData.find(v=>v.name==='youlike').data : []
        let rows = []
        this.comments.map(v =>{
          let data3 = this.connection1.getbatchData.find(x=>x.name==='likecomment' + v.id).data
          let found = data1.find(x=>x.comment===v.id)
          let row = {id: v.id, you: found? true : false, likeid: found? found.id : undefined}
          row.list = found? (data3.find(x=>x.id===found.id)? data3 : data3.concat([found])) : data3
          row.type = mixing.unique(row.list, ['type'])
          let status = this.connection1.getbatchStatus.find(x=>x.name==='likecomment' + v.id)
          row.total = status.total_rows
          rows.push(row)
        })
        this.commentlike = rows
      }
    },

    'connection2.getupdateStatus': function(newVal) {
      if(newVal===true) { 
        let data = this.$copy(this.connection2.getupdateRecord)
        data.user__name = this.login.name
        data.type__value = this.emoji.find(v=>parseInt(v.id)===data.type).value
        if(data.comment) {
          let found = this.commentlike.find(v=>v.id===data.comment)
          if(found? !found.you: false) {
            found.likeid = data.id
            found.you = true
            found.list.push(data)
            found.type = mixing.unique(found.list, ['type'])
            found.total = found.total + 1

            let link = {path: this.$route.path, query: this.$route.query}
            let type = this.sysapi.find3var('list', 'notification', 'emotion')
            let record = {receiver: this.currentComment.creator, sender: this.login.id,
            link: JSON.stringify(link), type: type.id, seen: false, refid: data.id}
            let ele = this.connection5.requirelist.find(v=>v.name==='notification')
            ele.commit = undefined
            let values = this.connection.requirelist.find(v=>v.name==='notification').params.values
            this.connection5.insert('notification', record, values)
          } else {
            let index = found.list.findIndex(x=>x.id===data.id)
            found.list[index] = data
            found.type = mixing.unique(found.list, ['type'])
          }
          this.commentlike = this.$copy(this.commentlike)
        }
      }
    },

    'connection4.getupdateStatus': function(newVal) {
      if(newVal===true) {
        let data = this.$copy(this.connection4.getupdateRecord)
        data.creator__name = this.login.name
        if(this.editRecord) {
          let found = this.comments.find(v=>v.id===this.editRecord.id)
          found[this.keyval] = data[this.keyval]
          found.update_time = data.update_time
          found.image = data.image
          this.editRecord = undefined
          this.comments = this.$copy(this.comments)
        } 
        else {
          this.comments.push(data)
          this.commentlike.push({id: data.id, you: false, list: [], type: [], total: 0})
        }
        
        if(this.isReply) this.closeReply()
        else {
          this.content = ''
          this.image = undefined
        }
        if(this.topic.creator===data.creator) return
        let link = {path: this.$route.path, query: this.$route.query}
        let type = this.sysapi.find3var('list', 'notification', 'comment')
        let record = {receiver: this.topic.creator, sender: data.creator,
        link: JSON.stringify(link), type: type.id, seen: false, refid: data.id}
        let found = this.connection5.requirelist.find(v=>v.name==='notification')
        found.commit = undefined
        let values = this.connection.requirelist.find(v=>v.name==='notification').params.values
        this.connection5.insert('notification', record, values)
      }
    },

    'connection5.getupdateStatus': function(newVal) {
      if(newVal===true) {
        let data = this.connection5.getupdateRecord
        socket.emit('send-message', {name: 'notification', data: [data]})
      }
    },

    sortaz: function(newVal) {
      this.getData()
    },

    current: function(newVal) {
      this.getData()
    },

    action: function(newVal) {
      if(newVal? newVal.name==='close' : 1<0) {
        let index = this.comments.findIndex(v=>v.id===this.focus.id)
        if(index>=0) this.$delete(this.comments, index)
        this.violate = false
      }
    },

    media: function(newVal) {
      if(newVal? !newVal.select : 1>0) return
      if(this.componentid!==newVal.component) return
      if(newVal.name==='comment-image') this.image = newVal.select.file
      if(newVal.name==='reply-image') this.replyImage = newVal.select.file
      this.media = undefined  
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

    media: {
      get: function() {return this.$store.state.media},
      set: function(val) {this.$store.commit("updateMedia", {media: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", {ismobile: val})}
    },

    openMedia() {
      return this.media? this.media.component : false
    },
  },

  methods: {
    getData() {
      this.values = 'id,creator,creator__name,creator__avatar,image,create_time,parent,' + this.name + ',' + this.keyval
      let found = this.$copy(this.connection.requirelist.find(v=>v.name===this.api))
      let filter = {parent__isnull: 1, deleted: 0}
      filter[this.name] = this.topic.id
      found.params = {values: this.values, page: this.current, perpage: this.perPage, filter: filter, 
      sort: this.sortaz? 'create_time' : '-create_time'}
      this.connection.getApi([found])
    },

    getLike() {
      let id = this.topic.id
      let values = 'id,user,user__name,type,type__value,' + this.name + ',' + this.keyval 
      let found = this.connection.requirelist.find(v=>v.name===this.likeApi)
      let filter = {}
      if(this.keyval) filter[this.keyval + '__isnull'] = 1
      filter[this.name] = id 
      var connlist = [{name: 'liketopic', url: found.url, params: {values: values, page: 1, filter: filter}}]
      
      filter = {}
      filter[this.keyval + '__isnull'] = 0
      if(this.login) {
        filter.user = this.login.id
        filter[this.name] = id   
        var val1 = {name: 'youlike', url: found.url, params: {values: values, filter: filter}}
        connlist.push(val1)        
      }

      filter = {}
      filter[this.name] = id
      this.comments.map(v=>{
        filter[this.keyval] = v.id
        let val = {name: 'likecomment' + v.id, url: found.url, params: {values: values, page: 1, filter: this.$copy(filter)}}
        connlist.push(val)
      })
      this.connection1.getApi(connlist)
    },

    createComment() {
      this.errors = []
      if(this.$empty(this.content)) {
        this.errors.push({name: 'comment', text: 'Nội dung không được bỏ trống'})
        return
      }
      if(this.login.type !== 3) {
        let val = mixing.checkExternalLink(this.content)
        if(val.result) {
          this.errors.push({name: 'comment', text: val.text})
          return
        }
      }

      this.isReply = false
      var data = {creator: this.login.id, image: this.image? this.image : null }
      data[this.keyval] = this.content 
      data[this.name] = this.topic.id
      if(this.editRecord) {
        data.id = this.editRecord.id
        data.update_time = new Date()
        this.connection4.update(this.api, data, this.values)
      }
      else this.connection4.insert(this.api, data, this.values)
    },

    likeComment(type, v) {
      if(!this.login) {
         this.$buefy.snackbar.open('Bạn cần đăng nhập để thể hiện cảm xúc')
         this.$router.push( {path: '/signin', query: {to: '/' + this.name + '/open', params: JSON.stringify({id:this.topic.id})}})
         return
      }

      let data = {user: this.login.id, type: type.id}
      data[this.name] = this.topic.id
      data[this.keyval] = v.id
      this.currentComment = v
      let found = this.commentlike.find(y=>parseInt(y.id)===parseInt(v.id))
      if(found? found.you : false) data.id = found.likeid
      if(data.id) this.connection2.update(this.likeApi, data)
      else this.connection2.insert(this.likeApi, data)
    },

    getLink() {
      let query = {to: this.$route.path}
      if(this.$route.query!=={}) query.params = JSON.stringify(this.$route.query)
      this.$router.push({path: '/signin', query: query})
    },

    replyComment() {
      this.errors = []
      if(this.$empty(this.replyContent)) {
        this.errors.push({name: 'reply', text: 'Nội dung không được bỏ trống'})
        return
      }

      if(this.login.type !== 3) {
        let val = mixing.checkExternalLink(this.replyContent)
        if(val.result) {
          this.errors.push({name: 'reply', text: val.text})
          return
        }
      }

      this.isReply = true
      var data = {creator: this.login.id, image: this.replyImage? this.replyImage : null, parent: this.reply.id}
      data[this.keyval] = this.replyContent 
      data[this.name] = this.topic.id
      if(this.editRecord) {
        data.id = this.editRecord.id
        data.update_time = new Date()
        this.connection4.update(this.api, data, this.values)
      }
      this.connection4.insert(this.api, data, this.values)
    },

    openReply(v) {
      this.reply = v
      mixing.delay(function() {
        let docid = document.getElementById('replybox' + v.id)
        if(docid) docid.scrollIntoView()    
      }, 30)
    },

    closeReply() {
      this.reply=undefined
      this.replyContent=undefined
      this.replyImage=undefined
      if(this.editRecord) this.editRecord = undefined
    },

    editComment(v) {
      this.editRecord = v
      this.content = v.comment
      if(v.image) this.image = v.image
      if(this.$refs.editorbox.$el) this.$refs.editorbox.$el.scrollIntoView()
      else this.$refs.editorbox.scrollIntoView()
    },

    editReplyComment(v) {
      this.editRecord = v
      this.replyContent = v.comment
      if(v.image) this.replyImage = v.image
      this.reply = this.comments.find(x=>x.id===v.parent)
    },

    displayTime(v) {
      if(!v.create_time) return
      let result = mixing.dateDiffCalc(new Date(v.create_time), new Date())
      return result.display
    }
  }
}
</script>