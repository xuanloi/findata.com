<template>
  <div class="columns is-centered mb-0 pb-0">
  <div class="column is-10 py-0">
    <div class="buttons mx-6 my-2" v-if="editable">
      <a class="button is-dark is-rounded fs13" @click="openModal()">Tạo tin mới</a>
    </div>
    <TableFilter class="mx-4" v-bind="{name: 'pagenews'}" />
    <div class="modal is-active" v-if="open">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:55%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="open=false; menu=undefined"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <p class="title"> Thêm tin liên quan đến <strong class="has-text-danger ml-2">{{$route.query.stock_code}}</strong></p>
      <CreateNews />
    </section>
      </div>
      </div>
  </div>
  </div>
</template>

<script>
export default {
  components: {
    CreateNews: () => import('@/components/profile/CreateNews')
  },
  props: ['editable'],
  data() {
    return {
      open: false,
      connection: this.$connection()
    }
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Escape' && this.open) this.open = false
    })
    let fields = [this.$createField('id', 'Id', 'number', true, true),
      this.$createField('company__stock_code', 'Công ty', 'string', true, true),
      this.$createField('title', 'Tiêu đề', 'string', true, true),
      this.$createField('subtitle', 'Tiều đề phụ', 'string', true, true),
    ]
    fields.push(this.$createField('image', 'Hình ảnh', 'string', true, true))
    fields.push(this.$createField('action', '', 'string', true, true, '7%', 'select,edit,open'))
    
    this.pagenews = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
    enableDelete: true, enableApprove: false, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
    this.connection.getApi([{name: 'companynews', params: {values: 'id,company,title,subtitle,image,company__stock_code', filter: {company: this.$route.query.company}}}])
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
      else if (newVal==='error') this.$router.push({path: '/error'})
    }
  },
  computed: {
    pagenews: {
      get: function() {return this.$store.state.pagenews},
      set: function(val) {this.$store.commit("updatePageNews", {pagenews: val})}
    }
  },
  methods: {
    openModal() {
      this.open = true
    },

    fillData() {
      let data = this.connection.getbatchData[0].data
      this.$store.commit('updateState', {name: 'pagenews', key: 'api', data: this.connection.getbatchStatus[0]})
      this.$store.commit('updateState', {name: 'pagenews', key: 'data', data: data})
      if(Object.keys(this.pagenews.origin_api).length===0) {
        this.$store.commit('updateState', {name: 'pagenews', key: 'origin_api', data: this.connection.getbatchStatus[0]})
      }
    }
  }
}
</script>