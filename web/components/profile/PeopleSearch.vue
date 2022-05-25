<!-- eslint-disable -->
<template>
  <div>
    <b-autocomplete ref="searchbox" expanded @focus="focus=true" @blur="focus=false"
      :value="people? (people.uid + ' | ' + people.name) : null"
      :data="data"
      keep-first
      clearable
      placeholder="Nhập mã định danh, họ tên để tìm"
      icon-right="magnify"
      field="stock_code"
      @typing="searchPeople"
      @select="option => option? this.$emit('doChange', option) : false">
        <template slot-scope="props">
        <div class="media">
        <div class="media-left has-text-danger">
        {{ props.option.uid}}
        </div>
        <div class="media-content">
        {{ props.option.name}}
        <span class="tag is-light is-rounded ml-3" v-if="props.option.management__position__value"> {{props.option.management__position__value}} </span>
        <span class="tag is-primary is-rounded ml-3" v-if="props.option.management__company__stock_code"> {{props.option.management__company__stock_code}} </span>
        <span class="tag is-light is-rounded ml-3" v-if="props.option.dob"> {{props.option.dob}} </span>
        </div>
        </div>
        </template>
        <template slot="empty">Không có giá trị thỏa mãn</template>
        </b-autocomplete>
  </div>
</template>

<script>
import Connection from "@/assets/js/connection.js"
export default {
  props: ['people'],

  data() {
    return {
      data: [],
      timer: undefined,
      search: undefined,
      connection: new Connection(this.$store),
      focus: false
    }
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        this.data = []
        this.connection.getbatchData.find(v=>v.name==='people').data.map(v=>{
          let found = this.data.find(x=>x.id===v.id)
          if(!found) this.data.push(v)
        })
      }
    }
  },

  methods: {
    searchPeople(val) {
      this.search = val
      let self = this
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        let conn = {name: 'people', url: 'data/People', path: 'path', params: {page: 1, onpage: 30,
        sort: 'management__position__index',
        values: 'id,uid,name,legal_id,avatar,address,phone,email,dob,domicile,management__position,management__position__code,management__position__value,management__company,management__company__stock_code', filter_or: {uid__icontains: val, name__icontains: val}}}    
        self.connection.getApi([conn])
      }, 200)
    }
  }
}
</script>