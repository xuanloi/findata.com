<!-- eslint-disable -->
<template>
<div>
   <TopMenu v-bind="{type: 'tophead', tophead: 'Thay đổi hình đại diện'}" v-if="!modal" />
  <div class="columns is-gapless is-centered is-marginless is-paddingless mt60">
<div class="column is-11 is-marginless is-paddingless">
  <div class="tile is-ancestor mt20 mb30 px-3 mx-0" v-if="image">
  <div class="tile is-7">      
    <cropper ref="cropper" :src="image" @change="onChange" :stencil-component="$options.components.CircleStencil" />
  </div>
  <div class="tile is-1"> </div>

  <div class="tile">
  <div>
        <div class="notification is-success is-light fs18">
  Hãy chọn khung hình tốt nhất bằng cách di chuyển, co giãn hình vuông trên ảnh.  
</div>

      <div class="block mt40">
        <b-radio v-model="radio"
          native-value="replace">
          Ghi đè
        </b-radio>
        <b-radio v-model="radio" class="ml20"
          native-value="new">
          Tạo file mới
        </b-radio>
      </div>

    <p class="mt30">
      <a class="button is-primary mr-4 mb-2" :class="isloading? 'is-loading' : ''" @click="updateImage()"> Đặt hình đại điện </a> 
      <a class="button is-success is-light" @click="image=undefined"> Đóng lại </a>
    </p>

    <p class="mt-2" v-if="coordinates">
      Hình ảnh cắt, {{'rộng: ' + coordinates.width +  ' cao: ' + coordinates.height}}
    </p>
    </div>
  </div>
  </div>

    <div class="field is-horizontal px-3 mt-3">
    <div class="field-body">
    <div class="field">
      <p class="control">
        <label class="label">Chọn {{title}} từ kho lưu trữ  hoặc tải lên.
        </label>
      </p>
      </div>  
    <div class="field is-narrow">
      <p class="control">
       <b-upload v-model="file">
        <a class="button is-primary" :class="isloading? 'is-loading' : ''">
          <b-icon icon="mdi mdi-plus mr5 fs30"></b-icon>
          <span> Tải lên {{title}} </span>
        </a>
      </b-upload>
      </p>
    </div>
  </div>
</div>

<div class="tile is-ancestor mx-0 px-0 my-3">
  <div class="tile is-vertical">
      <div class="tile is-parent" v-for="(v,i) in group" :key="i">
        <article class="tile is-child" v-for="(k,j) in getData(i)" :key="j" @mouseover="focus=k">
        <div class="image px-2 pb-2" v-if="k.file && type==='image'">
       <img v-lazy="connection.path + 'static/images/' + k.file" :id="'commentImage' + k.id">
          <div class="text-image" v-if="focus===k">
            <a class="button is-primary ml20" @click="editImage(k)"> <span class="icon fs30"> <i class="mdi mdi-checkbox-marked-outline"/> </span> </a>
          </div>
      </div>
    </article>
    </div>
  </div>
 </div>
</div>
  </div>
  <Footer class="mt60" v-if="!modal" />
</div>
</template>

<script>
/* eslint-disable */
import TopMenu from '~/components/TopMenu.vue'
import Footer from '~/components/Footer.vue'
import Vue from 'vue'

import mixing from "@/assets/js/mixing.js";
import { CircleStencil, Cropper } from 'vue-advanced-cropper'
import axios from 'axios'

export default {
  props: ['modal'],

  components: {
    TopMenu,
    Footer,
    Cropper,
    CircleStencil
  },

  data() {
    return {
      data: [],
      group: [],
      dataImage: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      connection3: this.$connection(),
      focus: undefined,
      title: 'Thay đổi hình đại diện',
      type: 'image',
      image: undefined,
      selected: undefined,
      radio: 'replace',
      rectangle: true,
      fileName: undefined,
      file: undefined,
      isloading: false,
      coordinates: undefined
    }
  },

  head() {
    return {
      title: this.title
    }
  },

  created() {
    let found = this.connection.requirelist.find(v=>v.name===this.type)
    found.params = {filter: {user: this.login.id}}
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
        mixing.delay(function() {
          self.isloading = false
          self.data.splice(0, 0, record)
        }, 1000)
      }
    },

    'connection2.getdataReady': function(newVal) {
      if(newVal==='success') {
         if(this.radio==='new') {
          let self = this
          let record = this.connection2.getbatchData[0].data[0]
          mixing.delay(function() {self.data.splice(0, 0, record)}, 1000)
        } else {
          this.data = this.$copy(this.data)
        }
        let copy = this.$copy(this.login)
        copy.avatar = this.fileName
        copy.update_time = new Date()
        copy.approve = copy.approve? copy.approve.id : copy.approve
        copy.bank = copy.bank? copy.bank.id : copy.bank
        copy.city = copy.city? copy.city.id : copy.city
        copy.team = copy.team? copy.team.id : copy.team
        copy.type = copy.type? copy.type.id : copy.type
        this.connection3.update('accountlist', copy)
      }
    },

    'connection3.getupdateStatus': function(newVal) {
      if (newVal===true) {
        let self = this
        this.isloading = false
        mixing.delay(function() {
            let copy = this.$copy(self.login)
            copy.avatar = self.fileName
            self.login = copy
        }, 1000)
      }
    },

    file: function(newVal) {
      if(!newVal) return
      var file = mixing.upload(newVal, this.type, this.login.id)
      if(file.error) {
        let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: file.text}
        this.$buefy.notification.open(info)
        return
      }
      this.dataImage = file
      let found = {name: 'uploadfile', url: 'upload/', method: 'post', data: file.form, params: {}} 
      this.connection1.getApi([found])
      this.isloading = true
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
  },
    
  methods: {
    getData(i) {
      if(this.type==='video') {
        var list = this.data.slice(i*4, i*4+4)
        for (let index = 0; index < 4; index++) {
          if(list.length<index+1) list.push({file: undefined})
        }
      } else {
        list = this.data.slice(i*5, i*5+5)
        for (let index = 0; index < 5; index++) {
          if(list.length<index+1) list.push({file: undefined})
        }
      }
      return list
    },

    editImage(v) {
      this.isloading = true
      this.selected = v
      let self = this
      let params = {name:  v.file, type: 'image'  }
      axios.get(this.connection.path + 'download/',  {params: params, responseType:"blob" })
      .then(function (response) {
        var reader = new window.FileReader()
        reader.onload = (e) => {self.image = e.target.result}
        reader.readAsDataURL(response.data)
        self.isloading = false
      })
    },

    updateImage() {
      const { canvas } = this.$refs.cropper.getResult()
			if (canvas) canvas.toBlob(blod=>this.saveAs(blod))
    },
    
    saveAs(blod) {
      this.isloading = true
      var form = new FormData();
      let name = this.selected.file.indexOf('-')>0? this.selected.file.substring(15, this.selected.file.length) : this.selected.file
      this.fileName = mixing.yyyymmddhhmmss(new Date()) + '-' + name
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
    }
  }
}
</script>