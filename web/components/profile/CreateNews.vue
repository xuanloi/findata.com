<template>
<div>
      <article class="media">
  <div class="media-content">
    <div class="content">
      <div class="field is-horizontal">
  <div class="field-body">
    <div class="field">
        <label class="label">Tiêu đề chính</label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="title">
      </p>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='title')">{{errors.find(v=>v.name==='title').text}}</p>
    </div>
  </div>
  </div>

  <div class="field is-horizontal mt20">
  <div class="field-body">
    <div class="field">
          <label class="label">Tiêu đề phụ</label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="subtitle">
      </p>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='subtitle')">{{errors.find(v=>v.name==='subtitle').text}}</p>
    </div>
  </div>
</div>
    
  </div>
  </div>
  <div class="media-right">
    <div v-if="image" class="ml10 mr10">
    <a class="image is-128x128" @click="gallery=image">
      <img v-lazy="connection.path + 'static/images/'  + image">
    </a>
      <p class="has-text-centered">
        <a @click="image=undefined"> <span class="icon"> 
          <i class="mdi mdi-close-circle-outline has-text-danger fs22"/> </span> 
        </a>
      </p>
      </div>
        <div class="mt30" v-else>
        <a class="button is-primary is-light" @click="media = {name: 'news-image', open: true}"> Hình ảnh (nếu có) </a>
        </div>
  </div>
</article>

<div class="field is-horizontal mt20">
  <div class="field-body">
    <div class="field">
          <label class="label">Bài viết</label>
      <div class="control">
        <editor
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
        <p class="help is-danger" v-if="errors.find(v=>v.name==='content')">{{errors.find(v=>v.name==='content').text}}</p>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt20">
  <div class="field-body">
    <div class="field">
          <label class="label">Ghi chú (nếu có) </label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" v-model="note">
      </p>
    </div>
  </div>
</div>

<div class="field is-horizontal mt30">
  <div class="field-label">
    <!-- Left empty for spacing -->
  </div>
  <div class="field-body">
    <div class="field">
      <div class="control">
        <button class="button is-primary" @click="createNews()">
           {{(pagenews.record? pagenews.record.id : false)? 'Cập nhật bài viết' : 'Tạo bài viết'}}
        </button>
      </div>
    </div>

    </div>
  </div>
  <div class="modal is-active" v-if="openMedia">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content" style="position: absolute; top: 0px">
        <media v-bind="{mediatype: 'image', modal: true}" />
     </div>
    <button @click="media=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
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
import mixing from '@/assets/js/mixing.js'
import media from '@/pages/media.vue'
export default {
  components: {
    media
  },
  data () {
    return {
      headline: 'Tạo tin mới',
      title: undefined,
      subtitle: undefined,
      radio: true,
      connection: this.$connection(),
      connection1: this.$connection(this.$buefy),
      content: undefined,
      choose: undefined,
      image: undefined,
      gallery: false,
      note: undefined,
      creator: undefined,
      errors: []
    }
  },
  created() {
    this.fillData() 
  },
  watch: {
    media: function(newVal) {
      if(newVal? !newVal.select : 1>0) return
      if(newVal.name==='news-image') this.image = newVal.select.file
    },
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
      else if (newVal==='error') this.$router.push({path: '/error'})
    },
    'connection1.getupdateStatus': function(newVal) {
      if(newVal) {
        let row = this.connection1.getupdateRecord
        let copy = mixing.copy(this.pagenews.data)
        let index = copy.findIndex(v=>v.id===row.id)
        if(index>=0) copy[index] = row
        else copy.push(row)
        this.$store.commit('updateState', {name: 'pagenews', key: 'data',  data: copy})
        this.$store.commit('updateState', {name: 'pagenews', key: 'record',  data: row})
        this.fillData()      
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },
    category: {
      get: function() {return this.$store.state.category},
      set: function(val) {this.$store.commit('updateCategory', {category: val})}
    },
    media: {
      get: function() {return this.$store.state.media},
      set: function(val) {this.$store.commit("updateMedia", {media: val})}
    },
    pagenews: {
      get: function() {return this.$store.state.pagenews},
      set: function(val) {this.$store.commit("updatePageNews", {pagenews: val})}
    },
    openMedia() {
      return this.media? this.media.open : false
    } 
  },

  methods: {
    fillData() {
      let news = this.pagenews.record? this.pagenews.record : {}
      this.title = news.title
      this.subtitle = news.subtitle
      this.content = news.content
      this.creator = news.creator__name
      this.image = news.image   
      this.note = news.note
    },

    checkError() {
      this.errors = []
      if(mixing.isEmpty(this.title)) this.errors.push({name: 'title', text: 'Tiêu đề  chính không được bỏ trống'})
      if(mixing.isEmpty(this.subtitle)) this.errors.push({name: 'subtitle', text: 'Tiêu đề phụ không được bỏ trống'})
      if(mixing.isEmpty(this.content)) this.errors.push({name: 'content', text: 'Nội dung không được bỏ trống'})
      return this.errors.length>0? true : false
    },

    createNews() {
      if(this.checkError()) return
      let id = this.pagenews? (this.pagenews.record? this.pagenews.record.id : undefined) : undefined
      let data = {id: id, company: this.$route.query.company, title: this.title, subtitle: this.subtitle, content: this.content, note: this.note, 
      update_time: new Date(),
      creator: id? this.pagenews.record.creator : this.login.id, image: this.image? this.image : undefined}
      let values = 'id,company,company__stock_code,title,subtitle,content,image,note'
      if(!data.id) this.connection1.insert('companynews', data, values)
      else this.connection1.update('companynews', data, values)
    }
  }
}

</script>
