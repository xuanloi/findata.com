<template>
  <div>
    <b-autocomplete ref="searchbox" expanded @focus="focus=true" @blur="focus=false"
      :value="company? company.stock_code : null"
      :data="data"
      keep-first
      clearable
      placeholder="Nhập mã"
      icon-right="magnify"
      field="stock_code"
      @typing="searchCompany"
      @select="option => option? this.$emit('doChange', option) : false">
        <template slot-scope="props">
        <div class="media">
        <div class="media-left has-text-danger">
        {{ props.option.stock_code}}
        </div>
        <div class="media-content">
        {{ props.option.name}}
        <span class="tag is-primary is-rounded ml-3"> {{ props.option.listed_on}} </span>
        </div>
        </div>
        </template>
        <template slot="empty">Không có giá trị thỏa mãn</template>
        </b-autocomplete>
  </div>
</template>

<script>
export default {
  props: ['company', 'setfocus', 'type'],

  data() {
    return {
      data: [],
      timer: undefined,
      search: undefined,
      connection: this.$connection(),
      focus: false
    }
  },

  mounted() {
    if(this.setfocus && this.$refs.searchbox) this.$refs.searchbox.focus()
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') {
        let companies = this.connection.getbatchData.find(v=>v.name==='company').data
        if(this.type) companies = companies.filter(v=>v.type===this.type)
        this.data = this.$companyFilter(companies, this.search)
      }
    }
  },

  methods: {
    searchCompany(val) {
      this.search = val
      let self = this
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        let conn = {name: 'company', url: 'data/Company', params: {page: 1, onpage: 30, 
        values: 'id,stock_code,name,type,type__code,listed_on', filter_or: {stock_code__icontains: val, name__icontains: val}}}    
        self.connection.getApi([conn])
      }, 200)
    }
  }
}
</script>