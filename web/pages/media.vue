<template>
  <div>
 <TopMenu v-bind="{title: 'Quản lý hình ảnh'}" v-if="!modal" />
<section class="hero is-fullheight-with-navbar">
  <div class="hero-body px-0 py-5" style="align-items: flex-start">
    <div class="container is-fluid">
  <div class="tile is-ancestor mb-4 px-3 mx-0" v-if="image">
    <div class="tile is-1"/>
  <div class="tile is-7">
    <cropper
    ref="cropper"
    :src="image"
    @change="onChange"
	  :stencil-props="getRatio" />
  </div>
  <div class="tile is-1"> </div>
  <div class="tile"><div>
    <p class="title fs26"> Cắt hình ảnh </p>
    <p class="mt-2 fs16">Chọn tỷ lệ hoặc nhập vào chiều rộng và cao</p>
      <div class="tags are-medium mt-2">
  <a :class="curRatio.k===v.k? 'tag is-primary' : 'tag'" v-for="(v,i) in ratios" :key="i" @click="curRatio=v">{{v.k}}</a>
</div>

      <div class="block mt-5">
        <b-radio v-model="radio"
          native-value="replace">
          Ghi đè
        </b-radio>
        <b-radio v-model="radio" class="ml-3"
          native-value="new">
          Tạo file mới
        </b-radio>
      </div>

    <p class="mt-4">
      <a class="button is-primary mr-4 mb-2" :class="isLoading? 'is-loading' : ''" @click="updateImage()"> Lưu lại </a> 
      <a class="button is-success is-light" @click="image=undefined"> Đóng lại </a>
    </p>

    <p class="mt-2" v-if="coordinates">
      Hình ảnh cắt, {{'W: ' + coordinates.width +  ', H: ' + coordinates.height + ', W/H: ' + coordinates.ratio}}
    </p>
    </div>
  </div>
  </div>

    <div class="field is-horizontal">
    <div class="field-body">
    <div class="field" v-if="modal">
      <p class="control">
        <label class="label">Chọn {{title}} từ kho lưu trữ  hoặc tải lên.</label>
      </p>
      </div>  
    <div class="field is-narrow">
      <p class="control">
       <b-upload v-model="file">
        <a class="button is-primary" :class="isLoading? 'is-loading' : ''">
          <b-icon icon="mdi mdi-plus mr5 fs30"></b-icon>
          <span>Tải lên</span>
        </a>
      </b-upload>
      <a class="button is-dark" v-if="modal" @click="$emit('closemedia')">Đóng lại</a>
      </p>
    </div>
  </div>
</div>

<div class="tile is-ancestor mx-0 px-0 my-3">
  <div class="tile is-vertical">
      <div class="tile is-parent" v-for="(v,i) in group" :key="i">
        <article class="tile is-child" v-for="(k,j) in getData(i)" :key="j" @mouseover="focus=k">
        <div class="image px-2 pb-2" v-if="k.file && type==='image'">
       <nuxt-img :src="connection.path + 'static/images/' + k.file" :id="'commentImage' + k.id"></nuxt-img>
          <div class="text-image" v-if="focus===k">
            <a class="button is-primary" @click="selectMedia(k)"> <span class="icon fs22"> <i class="mdi mdi-checkbox-marked-outline"/> </span> </a>
            <a class="button is-primary ml-2" @click="editImage(k)"> <span class="icon fs22"> <i class="mdi mdi-crop"/> </span> </a>
            <a class="button is-primary ml-2" @click="copyMedia(k, 'image')"> <span class="icon fs22"> <i class="mdi mdi-content-copy"/> </span> </a>
             <a class="button is-danger ml-2" @click="deleteMedia(k, 'image')"> <span class="icon fs22"> <i class="mdi mdi-trash-can-outline"/> </span> </a>
          </div>
      </div>

      <div class="ml-2 mr-2" v-else-if="k.file && type==='video'">
        <vue-plyr>
        <video :src="connection.path + 'static/videos/' + k.file">
          <source :src="connection.path + 'static/videos/' + k.file" type="video/mp4" size="720">
        </video>
        <div class="mt-2" v-if="focus===k">
            <a class="button is-primary" @click="selectMedia(k)"> <span class="icon fs24"> <i class="mdi mdi-checkbox-marked-outline"/> </span> </a>
          </div>
      </vue-plyr>
      </div>
      <div class="ml-2 mr-2" v-else-if="k.file && type==='file'">
        {{k.file}}
        <div class="mt-2" v-if="focus===k">
            <a class="button is-primary" @click="selectMedia(k)"> <span class="icon fs24"> <i class="mdi mdi-checkbox-marked-outline"/> </span> </a>
          </div>
        </div>  
    </article>
    </div>
  </div>
 </div>
    </div>
  </div>
</section>
  </div>
</template>

<script>
import { CircleStencil, Cropper } from 'vue-advanced-cropper'
import axios from 'axios'
import 'vue-advanced-cropper/dist/style.css'
export default {
  components: {
    Cropper,
    CircleStencil
  },
  props: ['mediatype', 'modal'],
  data() {
    return {
      data: [],
      group: [],
      dataImage: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      connection3: this.$connection(this.$buefy),
      focus: undefined,
      title: 'hình ảnh',
      type: undefined,
      image: undefined,
      selected: undefined,
      radio: 'replace',
      rectangle: true,
      fileName: undefined,
      file: undefined,
      isLoading: false,
      coordinates: undefined,
      current: undefined,
      curRatio: {k: '1/1'},
      ratios: [{k: '1/1'}, {k: '5/4'}, {k:'4/3'}, {k: '3/2'}, {k: '5/3'}, {k:'16/9'}, {k: '2/1'}, {k: '3/1'}, {k: '4/5'}, {k: '3/4'}, {k: '2/3'}, {k: '3/5'}, {k: '9/16'}, {k: '1/2'}, {k: '1/3'}]
    }
  },

  created() {
    if(!this.$empty(this.$route.query.mediatype)) this.type = this.$route.query.mediatype
    else this.type = this.mediatype
    this.title = this.type!=='image'? this.type : this.title 
    let found = this.connection.requirelist.find(v=>v.name===this.type)
    found.params = {filter: {user: this.login.id}, sort: '-create_time'}
    this.connection.getApi([found])
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if(newVal==='success') this.data = this.connection.getbatchData[0].data
    },

    'connection1.getdataReady': function(newVal) {
      if(newVal==='success') {
        let record = this.connection1.getbatchData[0].data[0]
        let self = this
        setTimeout(function() {
          self.isLoading = false
          self.data.splice(0, 0, record)
        }, 1000)
      }
    },

    'connection2.getdataReady': function(newVal) {
      if(newVal==='success') {
        let self = this
        if(this.radio==='replace') { 
          let index = this.data.findIndex(v=>v.id===this.selected.id)
          if(index>=0) this.$delete(this.data, index)
        }
        let record = this.connection2.getbatchData[0].data[0]
        setTimeout(function() {
          self.isLoading = false
          self.data.splice(0, 0, record)
        }, 1000)
        this.image = undefined
      }
    },

    'connection3.getupdateStatus': function(newVal) {
      if(newVal) {
        let idx = this.data.findIndex(v=>v.id===this.current.id)
        this.$delete(this.data, idx)
      }
    },

    file: function(newVal) {
      if(!newVal) return
      var file = this.$upload(newVal, this.type, this.login.id)
      if(file.error) {
        let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: file.text}
        this.$buefy.notification.open(info)
        return
      }
      this.dataImage = file
      let found = {name: 'uploadfile', url: 'upload/', method: 'post', data: file.form, params: {}} 
      this.connection1.getApi([found])
      this.isLoading = true
    },

    data: function() {
      this.group = []
      for (let index = 0; index < this.data.length/ (this.type==='video'? 4 : 5) ; index++) {
        this.group.push(index)
      }
    }
  },

  computed: {
    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },
    media: {
      get: function() {return this.$store.state.media},
      set: function(val) {this.$store.commit("updateMedia", {media: val})}
    },
    getRatio() {
      return {aspectRatio: this.$calc(this.curRatio.k)}
    }
  },
    
  methods: {
    getData(i) {
      if(this.type==='video') {
        var list = this.data.slice(i*5, i*5+5)
        for (let index = 0; index < 5; index++) {
          if(list.length<index+1) list.push({file: undefined})
        }
      } else {
        list = this.data.slice(i*6, i*6+6)
        for (let index = 0; index < 6; index++) {
          if(list.length<index+1) list.push({file: undefined})
        }
      }
      return list
    },
    
    selectMedia(v) {
      let copy = this.media? this.$copy(this.media) : {}
      copy.type = 'image'
      copy.open = false
      copy.select = v
      this.media = copy
      this.$emit('selectmedia', v)
    },

    editImage(v) {
      this.isLoading = true
      this.selected = v
      let self = this
      let params = {name:  v.file, type: 'image'  }
      axios.get(this.connection.path + 'download/',  {params: params, responseType:"blob" })
      .then(function (response) {
        var reader = new window.FileReader()
        reader.onload = (e) => {self.image = e.target.result}
        reader.readAsDataURL(response.data)
        self.isLoading = false
      })
    },

    copyMedia(v) {
      this.$copyToClipboard(this.connection.path + 'static/images/' + v.file)
    },

    updateImage() {
      const { canvas } = this.$refs.cropper.getResult()
			if (canvas) canvas.toBlob(blod=>this.saveAs(blod))
    },
    
    saveAs(blod) {
      this.isLoading = true
      var form = new FormData();
      let name = this.selected.file.indexOf('-')>0? this.selected.file.substring(15, this.selected.file.length) : this.selected.file
      this.fileName = this.$dayjs(new Date()).format("YYYYMMDDhhmmss") + '-' + name
      if(this.radio==='replace') this.fileName = this.selected.file

      form.append('name', this.fileName)
      form.append('file', blod)
      form.append('type', 'image')
      form.append('size', this.selected.size)
      form.append('user', this.login.id)

      let found = {name: 'uploadfile', url: 'upload/', method: 'post', data: form, params: {}} 
      this.connection2.getApi([found])
    },

    onChange({ coordinates, canvas}) {
      this.coordinates = coordinates
      this.coordinates.ratio = (this.coordinates.width*1.00 / this.coordinates.height).toFixed(2)
    },

    deleteMedia(v, name) {
      this.current = this.$copy(v)
      this.$buefy.dialog.confirm({
        message: 'Bạn muốn xóa file: ' + v.file,
        onConfirm: () => this.connection3.delete(name, v.id)})
    }
  }
}
</script>