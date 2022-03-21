<template>
  <div>
  <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
  <label class="label">Tên báo cáo<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.name">
  </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='name')">{{errors.find(v=>v.name==='name').text}}</p>
</div>
        <div class="field">
  <label class="label">Công ty phát hành<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <CompanySearch v-bind="{company: record.selectCompany, setfocus: undefined, type: 155}" @doChange="selectCompany" />
  </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='company')">{{errors.find(v=>v.name==='company').text}}</p>
</div>
  </div>
</div>

  <div class="field is-horizontal">
      <div class="field-body">
        <div class="field is-narrow">
  <label class="label">Ngày phát hành<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
        <b-datepicker
                   locale="en-GB"
            placeholder=""
            v-model="record.date">
        </b-datepicker>
  </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='date')">{{errors.find(v=>v.name==='date').text}}</p>
</div>
        <div class="field">
  <label class="label">Chứng khoán liên quan<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <b-taginput
                v-model="ticker"
                :data="filteredTags"
                autocomplete
                field="stock_code"
                icon="label"
                placeholder="Mã CK"
                @typing="getFilteredTags">
                <template v-slot="props">
                <strong>{{props.option.stock_code}}</strong>: {{props.option.name}}
                </template>
                <template #empty>
                  Không có giá trị thỏa mãn
                </template>
            </b-taginput>
  </div>
     <p class="help is-danger" v-if="errors.find(v=>v.name==='ticker')">{{errors.find(v=>v.name==='ticker').text}}</p>
</div>
      </div>
     </div>

                <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
  <label class="label">Chuyên gia<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <b-taginput
                v-model="expert"
                ellipsis
                icon="label"
                placeholder="Tên chuyên gia"
                aria-close-label="">
            </b-taginput>
  </div>
   <p class="help is-danger" v-if="errors.find(v=>v.name==='expert')">{{errors.find(v=>v.name==='expert').text}}</p>
</div>
      </div>
     </div>
     
           <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
  <label class="label">File đính kèm<span class="has-text-danger ml-1">*</span></label>
  <div class="control">
    <input class="input" type="text" placeholder="" v-model="record.file">
  </div>
   <p class="help is-danger" v-if="errors.find(v=>v.name==='file')">{{errors.find(v=>v.name==='file').text}}</p>
</div>
       <div class="field is-narrow">
           <label class="label">Duyệt</label>
         <a @click="browseMedia()"><i class="mdi mdi-file fs30"></i></a>
       </div>
      </div>
     </div>

<div class="field is-horizontal">
  <div class="field-body">
    <div class="field">
          <label class="label">Nội dung tóm tắt<span class="has-text-danger ml-1">*</span></label>
      <div class="control">
         <editor
      v-model="record.content"
      api-key="0a3xn20t37fgzj36azuoo8e1fscw2q0xg0k2t12k7ztg5f0m"
      :init="{
      setup (editor) {
      editor.on('change', function () {
        const headings = editor.getBody().querySelectorAll('h1, h2, h3, h4, h5, h6');
        for (let i = 0; i < headings.length; i++) {
          if (!headings[i].id) {
            headings[i].id = Math.random().toString(32).substr(2, 5);
          }
        }
      })
    }   ,
         menubar: false,
        statusbar: true,
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | preview | code | help'
       }"
     />
      </div>
        <p class="help is-danger" v-if="errors.find(v=>v.name==='content')">{{errors.find(v=>v.name==='content').text}}</p>
    </div>
  </div>
</div>

<div class="field is-horizontal mt-4">
  <div class="field-label">
    <!-- Left empty for spacing -->
  </div>
  <div class="field-body">
    <div class="field">
      <div class="control">
        <button class="button is-primary" @click="update()">
          Cập nhật
        </button>
      </div>
    </div>
  </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      errors: [],
      record: {},
      expert: [],
      connection: this.$connection(this.$buefy),
      filteredTags: [],
      ticker: []
    }
  },

  created() {
    if(this.pagedata.action? this.pagedata.action.event==='edit' : false) {
      this.record = this.$copy(this.pagedata.action.row)
      if(this.record.issue_date) this.record.date = new Date(this.record.issue_date)
      if(this.record.ticker) this.ticker = this.$copy(this.record.ticker)
      if(this.record.expert) this.expert = this.$copy(this.record.expert)
      if(this.record.company) this.record.selectCompany = this.companylist.find(v=>v.id===this.record.company)
    }
    this.filteredTags = this.companylist
  },

  watch: {
    'connection.getupdateStatus' : function(newVal) {
      if(newVal) {
        let record = this.connection.getupdateRecord
        let copy = this.$copy(this.pagedata)
        let index = copy.data.findIndex(v=>v.id===record.id)
        index>=0? copy.data[index] = record : copy.data.push(record)
        this.pagedata = copy
        if(this.pagedata.filters? this.pagedata.filters.length>0 : false) {
          this.$store.commit('updateState', {name: 'pagedata', key: 'filterby', data: this.$copy(this.pagedata.filters)})
        }
        this.$emit('close')
      }
    }
  },

  computed: {
    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit('updatePageData', {pagedata: val})}
    },
    companylist: {
      get: function() {return this.$store.state.companylist},
      set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
    }
  },

  methods: {
    getFilteredTags(text) {
      if(this.$empty(text)) this.filteredTags = this.companylist
      let value = text.toLowerCase()
      this.filteredTags = this.companylist.filter(v=>v.stock_code.toLowerCase().indexOf(value)>=0 || v.name.toLowerCase().indexOf(value)>=0)
    },

    selectCompany(v) {
      this.record.company = v.id
      this.record.selectCompany = this.$copy(v)
    },

    update() {
      this.errors = []
      if(this.$empty(this.record.file)) this.errors.push({name: 'file', text: 'Chưa chọn file báo cáo'})
      if(this.$empty(this.record.name)) this.errors.push({name: 'name', text: 'Chưa nhập tên báo cáo'})
      if(this.$empty(this.record.company)) this.errors.push({name: 'company', text: 'Chưa nhập công ty phát hành'})
      if(this.$empty(this.record.date)) this.errors.push({name: 'date', text: 'Chưa nhập ngày phát hành'})
      if(this.ticker.length===0) this.errors.push({name: 'ticker', text: 'Chưa nhập chứng khoán liên quan'})
      if(this.expert.length===0) this.errors.push({name: 'expert', text: 'Chưa nhập chuyên gia'})
      if(this.$empty(this.record.content)) this.errors.push({name: 'content', text: 'Chưa nhập nội dung tóm tắt'})
      if(this.errors.length>0) return
      this.record.issue_date = this.$dayjs(this.record.date).format('YYYY-MM-DD')
      this.record.ticker = this.ticker.map(v=>{return {id: v.id, stock_code: v.stock_code, name: v.name}})
      this.record.expert = this.$copy(this.expert)
      let conn = this.connection.find('analysisreport')
      if(this.record.id) this.connection.update('analysisreport', this.record, conn.params.values)
      else this.connection.insert('analysisreport', this.record, conn.params.values)
    },

    browseMedia() {
      this.record.issue_date = this.$dayjs(this.record.date).format('YYYY-MM-DD')
      if(this.ticker.length>0) this.record.ticker = this.ticker.map(v=>{return {id: v.id, stock_code: v.stock_code, name: v.name}})
      if(this.expert.length>0) this.record.expert = this.$copy(this.expert)
      this.$emit('browsemedia', this.record)
    }
  }
}
</script>