<!-- eslint-disable -->
<template>
<div>
    <div class="columns is-centered mt15">
    <div class="column is-10">
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

 <div class="field is-horizontal mt30">
  <div class="field-body">
<div class="field">
<label class="label">Chuyên mục</label>
  <div class="control">
          <b-autocomplete
                icon-right="magnify"
                v-model="topic"
                placeholder=""
                :keep-first=true
                :open-on-focus=true
                :data="filteredTopic"
                field="value"
                @select="option => selectTopic = option">
            </b-autocomplete>
  </div>
    <p class="help is-danger" v-if="errors.find(v=>v.name==='topic')">{{errors.find(v=>v.name==='topic').text}}</p>
</div>
<div class="field">
    <label class="label">Tiểu mục (nếu có)</label>
  <div class="control">
         <b-autocomplete
                icon-right="magnify"
                v-model="subTopic"
                placeholder=""
                :keep-first=true
                :open-on-focus=true
                :data="filteredSubTopic"
                field="value"
                @select="option => selectSubTopic = option">
            </b-autocomplete>
  </div>
</div>
      </div>
  </div>

  <div class="field is-horizontal mt20" v-if="choose">
  <div class="field-body">
  <div class="field" v-if="choose==='delay' || choose==='range'">
  <label class="label">{{choose==='delay'? 'Ngày hiển thị' : 'Từ ngày'}}</label>
    <div class="control">
           <b-datetimepicker
              v-model="valid_from"
                rounded
                placeholder=""
                icon="calendar"
                :timepicker="{ hourFormat: '24' }"
                horizontal-time-picker>
            </b-datetimepicker>
    </div>
      <p class="help is-danger" v-if="errors.find(v=>v.name==='valid_from')">{{errors.find(v=>v.name==='valid_from').text}}</p>
  </div>
  <div class="field" v-if="choose==='range'">
      <label class="label">Đến ngày</label>
    <div class="control">
               <b-datetimepicker
               v-model="valid_to"
                rounded
                placeholder=""
                icon="calendar"
                :timepicker="{ hourFormat: '24' }"
                horizontal-time-picker>
            </b-datetimepicker>
      </div>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='valid_to')">{{errors.find(v=>v.name==='valid_to').text}}</p>
    </div>
          </div>
      </div>

  <article class="message is-primary mt40 mb20">
 <div class="message-body has-background-daytot has-text-dark pt15 pb15">
    <p class="title fs26"> Dành cho quản trị viên </p>
  </div>
</article>

 <div class="field is-horizontal mt30">
      <div class="field-body">
          <div class="field">
                <label class="label">Hiệu lực</label>
              <div class="control">
   <div class="block mt15 has-text-left">
            <b-radio v-model="radio"
                :native-value=true>
                Có
            </b-radio>
            <b-radio v-model="radio" class="ml20"
                :native-value=false>
                Không
            </b-radio>
 </div>
              </div>
          </div>
              <div class="field">
                    <label class="label">Người tạo</label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" readonly v-model="creator">
      </p>
    </div>
</div>
      </div>
 <div class="field is-horizontal mt30">
    <div class="field-body">
    <div class="field">
      <label class="label">Phê duyệt</label>
    <div class="control">
      <b-autocomplete
        icon-right="magnify"
        v-model="approve"
        placeholder=""
        :keep-first=true
        :open-on-focus=true
        :data="approvestatus"
        field="value"
        @select="option => selectApprove = option"
        :disabled="!(login.type.code==='admin' || login.type.code==='manager')">
        </b-autocomplete>
    </div>
      <p class="help is-danger" v-if="errors.find(v=>v.name==='approve')">{{errors.find(v=>v.name==='approve').text}}</p>
    </div>
    <div class="field">
      <label class="label">Người phê duyệt</label>
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="" readonly v-model="approver">
      </p>
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
import Editor from '@tinymce/tinymce-vue'
import TopMenu from '~/components/TopMenu.vue'
import media from '@/pages/media.vue'
export default {
  components: {
    Editor,
    TopMenu,
    media
  },
  data () {
    return {
      topic: undefined,
      topics: [],
      subTopic: undefined,
      subTopics: [],
      selectTopic: undefined,
      headline: 'Tạo tin tức mới',
      title: undefined,
      subtitle: undefined,
      radio: true,
      connection: this.$connection(),
      connection1: this.$connection(this.$buefy),
      subTopic: undefined,
      selectTopic: undefined,
      selectSubTopic: undefined,
      content: undefined,
      choose: undefined,
      image: undefined,
      gallery: false,
      approve: undefined,
      selectApprove: undefined,
      note: undefined,
      creator: undefined,
      valid_from: undefined,
      valid_to: undefined,
      errors: [],
      approvestatus: [],
      approver: undefined
    }
  },

  created() {
    this.approvestatus = this.api.filter2var('list', 'approve')
    var connlist = this.connection.checkDataReady(['category', 'approvestatus'])
    if(connlist.find(v=>v.name==='category').ready) { this.topics = this.category.filter(v=>v.level===0)}
    let filter = connlist.filter(v=>!v.ready)
    if(filter.length>0) this.connection.getApi(filter)
    else if(this.pagenews) this.fillData() 
  },

  watch: {
    category: function(newVal) {
      if(!newVal) return
      this.topics = this.category.filter(v=>v.level===0)
    },

    selectTopic: function(newVal) {
      if(this.$empty(this.selectTopic)) return
      this.subTopics = this.category.filter(v=>v.parent===this.selectTopic.item)
    },

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
        let copy = this.$copy(this.pagenews.data)
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
    },

    filteredTopic() {
      if(!this.topic) return this.topics

      return this.topics.filter((option) => {
        return option.value
        .toString()
        .toLowerCase()
        .indexOf(this.topic.toLowerCase()) >= 0
      })
    },

    filteredSubTopic() {
      if(!this.subTopic) return this.subTopics

      return this.subTopics.filter((option) => {
        return option.value
        .toString()
        .toLowerCase()
        .indexOf(this.subTopic.toLowerCase()) >= 0
      })
    }
  },

  methods: {
    fillData() {
      if(this.pagenews.record? !this.pagenews.record.id : false) {
        this.selectApprove = this.approvestatus.find(v=>v.category==='list' && v.classify==='approve' && v.code==='wait')
        this.approve = this.selectApprove.value
        this.creator = this.login.name
        return
      }

      let news = this.pagenews.record
      this.title = news.title
      this.subtitle = news.subtitle
      this.content = news.content
      let category = this.category.find(v=>v.id===news.category)
      if(category.level===1) {
        let found = this.category.find(v=>v.item===category.parent)
        this.selectTopic = found
        this.topic = this.selectTopic.value
        this.selectSubTopic = category
        this.subTopic = category.value
      }
      else {
        this.selectTopic = category
        this.topic = category.value
      }

      this.creator = news.creator__name
      this.image = news.image
      this.valid_from = news.valid_from? new Date(news.valid_from) : undefined
      this.valid_to = news.valid_to? new Date(news.valid_to) : undefined
      
      this.selectApprove = this.approvestatus.find(v=>parseInt(v.id)===news.approve_status)
      this.approve = this.selectApprove.value
      this.note = news.note
      this.approver = news.approver__name
    },

    checkError() {
      this.errors = []
      if(this.$empty(this.title)) this.errors.push({name: 'title', text: 'Tiêu đề  chính không được bỏ trống'})
      if(this.$empty(this.subtitle)) this.errors.push({name: 'subtitle', text: 'Tiêu đề phụ không được bỏ trống'})
      if(this.$empty(this.content)) this.errors.push({name: 'content', text: 'Nội dung không được bỏ trống'})
      if(this.$empty(this.selectTopic)) this.errors.push({name: 'topic', text: 'Chuyên mục không được bỏ trống'})
      //if(this.$empty(this.selectSubTopic)) this.errors.push({name: 'subtopic', text: 'Tiểu mục không được bỏ trống'})
      if(this.$empty(this.selectApprove)) this.errors.push({name: 'approve', text: 'Trạng thái phê duyệt chưa được chọn'})

      return this.errors.length>0? true : false
    },

    createNews() {
      if(this.checkError()) return
      let id = this.pagenews? (this.pagenews.record? this.pagenews.record.id : undefined) : undefined
      let data = {id: id, title: this.title, subtitle: this.subtitle, content: this.content,
      category: this.selectSubTopic? this.selectSubTopic.id : 
      (this.selectTopic? this.selectTopic.id : undefined), note: this.note, update_time: new Date(),
      creator: id? this.pagenews.record.creator : this.login.id, image: this.image? this.image : 'no-image.jpg', approve_status: this.selectApprove.id, 
      valid_from: this.valid_from? new Date(this.valid_from) : undefined,
      valid_to: this.valid_to? new Date(this.valid_to) : undefined,
      approver: this.pagenews.record.approver? this.pagenews.record.approver : (this.selectApprove.code==='yes'? this.login.id : undefined)}

      if(!data.id) this.connection1.insert('news', data, this.pagenews.api.params.values)
      else this.connection1.update('news', data, this.pagenews.api.params.values)
    }
  }
}

</script>
