<template>
<div>
  <div class="field is-horizontal">
    <div class="field-body">
      <div class="field">
      <label class="label">Tên công ty <strong class="has-text-danger">*</strong></label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="record.name">
      </div>
    </div>

    <div class="field" v-if="company">
        <label class="label">Mã chứng khoán <strong class="has-text-danger">*</strong></label>
        <p class="control">
          <input class="input" type="text" placeholder="" v-model="record.stock_code">
        </p>
      </div>
    </div>
  </div>

  <div class="field is-horizontal mt-5" v-if="!company">
    <div class="field-body">
      <div class="field">
        <label class="label">Mã chứng khoán <strong class="has-text-danger">*</strong></label>
        <p class="control">
          <input class="input" type="text" placeholder="" v-model="record.stock_code">
        </p>
      </div>
      <div class="field is-narrow">
        <p class="control mt-5 pt-4">
          <b-field>
            <b-checkbox v-model="nonStockCode" :disabled="company? true : false">Không có mã CK</b-checkbox>
          </b-field>
        </p>
      </div>
    </div>
  </div>

    <div class="field is-horizontal mt-5">
    <div class="field-body">
    <div class="field">
      <label class="label">Đã niêm yết?</label>
      <div class="control">
        <b-radio v-model="radio" v-for="v in choices" :key="v.code"
          :native-value="v">
          {{v.name}}
        </b-radio>
      </div>
    </div>

    <div class="field">
      <label class="label">Sàn chứng khoán</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.listed_on">
      </div>
    </div>
    </div>
    </div>

    <div class="field mt-5">
      <label class="label">Loại hình công ty <strong class="has-text-danger">*</strong></label>
      <div class="control">
        <b-autocomplete
        :v-model="type"
        :value="type? type.value : null"
        :data="types"
        keep-first
        clearable
        icon-right="magnify"
        field="value"
        :open-on-focus="true"
        @select="option => option? type = option : false">
      </b-autocomplete>
      </div>
    </div>

    <div class="field mt-5">
      <label class="label">Ngành nghề kinh doanh</label>
      <div class="control">
         <b-autocomplete
          :v-model="selectIndustry"
          :value="selectIndustry? selectIndustry.level3_name : null"
          :data="filterIndustry"
          keep-first
          clearable
          icon-right="magnify"
          field="level3_name"
          :open-on-focus="true"
          @typing="searchIndustry"
          @select="option => option? selectIndustry = option : false">
        <template slot-scope="props">
        <div class="media">
        <div class="media-left has-text-danger">
        {{ props.option.id}}
        </div>
        <div class="media-content">
        {{props.option.level1_name}} | {{props.option.level2_name}} | {{props.option.level3_name}}
        </div>
        </div>
        </template>
        <template slot="empty">Không có giá trị thỏa mãn</template>
        </b-autocomplete>
      </div>
    </div>

    <div class="field is-horizontal mt-5">
    <div class="field-body">
    <div class="field">
      <label class="label">Mã số thuế</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.tax_code">
      </div>
    </div>

      <div class="field">
      <label class="label">Logo</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.logo">
      </div>
    </div>
    </div>
    </div>

    <div class="field is-horizontal mt-5">
    <div class="field-body">
    <div class="field">
      <label class="label">Địa chỉ</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.address">
      </div>
    </div>

    <div class="field">
      <label class="label">Điện thoại</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.phone">
      </div>
    </div>
    </div>
    </div>

    <div class="field is-horizontal mt-5">
    <div class="field-body">
    <div class="field">
      <label class="label">Email</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.email">
      </div>
    </div>

    <div class="field">
      <label class="label">Website</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.website">
      </div>
    </div>
    </div>
    </div>

    <div class="field mt-5">
          <label class="label">Lịch sử hình thành</label>
      <div class="control">
        <editor
          v-model="record.detail"
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
    </div>

    <div class="mt-5" v-if="!editable===false">
      <a class="button is-primary" @click="updateCompany()"> {{company? 'Cập nhật' : 'Tạo mới'}} </a>
      <a class="button is-dark ml-3" @click="$emit('closeform', true)" v-if="!embedded"> Đóng lại </a>
    </div>
</div>
</template>

<script>
import Connection from '@/assets/js/connection.js'
import Editor from '@tinymce/tinymce-vue'
export default {
  components: {
    Editor
  },
  props: ['company', 'embedded', 'editable'],
  data() {
    return {
      record: {},
      nonStockCode: false,
      connection: new Connection(this.$store, this.$buefy),
      choices: [{code: 'no', name: 'Không'}, {code: 'yes', name: 'Có'}],
      radio: {code: 'no', name: 'Không'},
      types: [],
      type: undefined,
      selectIndustry: undefined,
      filterIndustry: []
    }
  },

  created() {
    if(!this.industry) this.connection.getApi([{name: 'industry'}])
    else this.filterIndustry = this.industry
    this.types = this.api.filter2var('list', 'company-type')
    this.type = this.api.find3var('list', 'company-type', 'SX')

    if(!this.company) return
    this.record = this.$copy(this.company)
    this.type = this.types.find(v=>parseInt(v.id)===this.record.type)
    this.radio = this.choices.find(v=>v.code===(this.record.listed? 'yes' : 'no'))
    if(this.record.industry && this.industry) this.selectIndustry = this.industry.find(v=>v.id===this.record.industry)
  },

  watch: {
     "connection.getdataReady": function(newVal) {
      if (newVal === "success") {
        if(this.record.industry) this.selectIndustry = this.industry.find(v=>v.id===this.record.industry)
        this.filterIndustry = this.industry
      }
    },

    'connection.getupdateRecord': function(newVal) {
      if(newVal) {
        if(!this.company) this.record = {}
        this.$emit('newcompany', newVal)
      }
    },
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },
    
    industry: {
      get: function() {return this.$store.state.industry},
      set: function(val) {this.$store.commit('updateIndustry', {industry: val})}
    },
  },

  methods: {
    searchIndustry(val) {
      if(val === undefined || val === null || val === '' || val==="") this.filterIndustry = this.industry
      else {
        let text = val.toLowerCase()
        this.filterIndustry = this.industry.filter(v=>
          v.id.toString().indexOf(text)>=0 ||
          v.level1_name.toLowerCase().indexOf(text)>=0 ||
          v.level2_name.toLowerCase().indexOf(text)>=0 ||
          v.level3_name.toLowerCase().indexOf(text)>=0 
        )
      }
    },

    updateCompany() {
      let data = this.$resetNull(this.$copy(this.record))
      data.type = this.type.id
      if(this.selectIndustry) data.industry = this.selectIndustry.id
      data.listed = this.radio.code==='yes'? true : false
      if(data.id) this.connection.update('companylist', data)
      else {
        this.nonStockCode? data.stock_code = this.$dayjs().format('YYYYMMDDHHmmss') : false
        this.connection.insert('companylist', data)
      }
    }
  }
}
</script>