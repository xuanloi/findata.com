<template>
<div>
<TopMenu v-bind="{type: 'tophead', tophead: this.tophead}"></TopMenu>
<div class="pt60"/>

<section class="hero is-white">
<div class="columns pt50 pb50">
<div class = "column is-8 is-offset-1"> 
<article class="message is-primary">
  <div class="message-header">
    <p class="is-size-4">Lưu ý</p>
      </div>
      <div class="message-body has-background-white has-text-dark fs18">
      {{api.getvalue(api.find3var('information','export-data','desc'))}}
  </div>
</article>
 
  <div class="columns">
<div class="column is-4 pb0">
  <div class="field pt5 pl0">
  <b-checkbox v-model="rangeDate" class="has-text-primary fs18" type='is-primary'>Trong khoảng thời gian</b-checkbox> 
  </div>
</div>

<div class="column is-4 pb0">
  <div class="field" v-if="rangeDate===true">
<div class="control">
<b-datepicker
ref="datepicker"
placeholder="Chọn ngày"
v-model="fdate"
>
</b-datepicker>
</div> 
  <p class="help is-danger" v-if="msgList.find(v=>v.name==='fdate') !==undefined">{{msgList.find(v=>v.name==='fdate').message}}</p>
</div>  
</div>

<div class="column is-4 pb0">
<div class="field" v-if="rangeDate===true">
<div class="control">
<b-datepicker
ref="datepicker"
placeholder="Chọn ngày"
v-model="tdate"
>
</b-datepicker>
</div> 
  <p class="help is-danger" v-if="msgList.find(v=>v.name==='tdate') !==undefined">{{msgList.find(v=>v.name==='tdate').message}}</p>
</div>  
</div>
</div>

<p class="mt40 is-size-5" v-if="message!==undefined" :class="message.type"> {{message.message}} </p>

</div>
  <div class = "column is-3"> 
<div v-if="loading === true">
 <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>
</div>
<div class="field pt50">
   <a v-if="loading === false" class="button is-medium is-rounded is-primary is-outlined" @click="exportdata()" >
     <i class="mdi mdi-database-export-outline"  style="font-size:35px;"> </i></a>
   <span v-if="result===true" class="pl20"> </span>
<a v-if="result===true" class="button is-medium is-rounded is-primary is-outlined" @click="download()" >
  <i class="mdi mdi-cloud-download-outline"  style="font-size:35px;"> </i></a>
  </div>
</div>
</div>
</section>
<Footer> </Footer>
</div>
</template>

<script>
import mixing from "@/assets/js/mixing.js";
export default {
  data() {
    return {
      tophead: 'Xuất dữ liệu ra file định dạng MS Access',
      loading: false,
      result: undefined,
      rangeDate: undefined,
      fdate: undefined,
      tdate: undefined,
      msgList: [],
      message: undefined,
      connection: this.$connection()
    }
  },

  head() {
    return {
      title: this.tophead
    }
  },

  watch: {
    'connection.getdataReady': function(newVal) {
      if(newVal==='success') {
        this.result = true
        this.loading = false
        this.message = {message: 'Xuất dữ liệu thành công', type: 'has-text-success'}
      }
      else if (newVal==='error') {
        this.result = false
        this.loading = false
        this.message = {message: 'Có lỗi xẩy ra. Xuất dữ liệu thất bại', type: 'has-text-danger'}
      }
    },
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
  },

  methods: {
    verify() {
      this.msgList = []
      if(this.rangeDate!==true) return true
      if(this.$empty(this.fdate)===true) this.msgList.push({name: 'fdate', message: 'Từ ngày không được bỏ trống'})
      if(this.$empty(this.tdate)===true) this.msgList.push({name: 'tdate', message: 'Đến ngày không được bỏ trống'})

      if(this.msgList.length===0) {
      if(mixing.compare(new Date(this.fdate), new Date(this.tdate))===1)
      this.msgList.push({name: 'tdate', message: 'Từ ngày phải <= đến ngày'})
      }

      if(this.msgList.length>0) return false
      else return true
    },

    exportdata() {
      if(this.verify()===false) return
      this.result = undefined
      this.exportAgain = this.exportAgain === null? false : true
      this.message = undefined
      this.loading = true
      var url = this.connection.path + 'export-data/'
      var obj = {nane: 'exportdata', url: 'export-data', params: !this.rangeDate? {} :
      {filter: {create_time__gte: mixing.yyyymmdd(this.fdate),create_time__lte: mixing.yyyymmdd(this.tdate)}}}
      this.connection.getApi([obj])
    },

    download() {
      mixing.download(this.connection.path + 'download-file/' + 'DataEntry.mdb/')
    },
  }
}
</script>