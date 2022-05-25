<template>
  <div>
    <b-autocomplete ref="searchbox" expanded @focus="focus=true" @blur="focus=false"
      :value="expert? expert.email : null"
      :data="data"
      keep-first
      clearable
      placeholder="Nhập email"
      icon-right="magnify"
      field="email"
      @typing="searchExpert"
      @select="option => option? this.$emit('selectexpert', option) : false">
        <template slot-scope="props">
        <div class="media">
        <div class="media-left has-text-danger">
        {{ props.option.id}}
        </div>
        <div class="media-content">
        {{ props.option.name}}
        <span class="tag is-primary is-rounded ml-3"> {{ props.option.company__stock_code}} </span>
        </div>
        </div>
        </template>
        <template slot="empty">Không có giá trị thỏa mãn</template>
        </b-autocomplete>
  </div>
</template>

<script>
export default {
  props: ['expert'],
  data() {
    return {
      data: [],
      timer: undefined,
      search: undefined,
      connection: this.$connection(),
      focus: false
    }
  },
  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        this.data = this.connection.getbatchData.find(v=>v.name==='expert').data
      }
    }
  },
  methods: {
    searchExpert(val) {
      this.search = val
      let self = this
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        let conn = {name: 'expert', url: 'data/Expert', params: {page: 1, onpage: 30, 
        values: 'id,name,email,phone,company,company__stock_code', filter_or: {email__icontains: val, name__icontains: val, phone__icontains: val}}}    
        self.connection.getApi([conn])
      }, 200)
    }
  }
}
</script>