<template>
<div>
  <div class="buttons mx-6 mb-0" v-if="editable">
    <a class="button is-dark is-rounded fs13" @click="openModal()"> Thêm lãnh đạo</a>
  </div>
  <TableFilter class="mx-4" v-bind="{name: 'pagetask'}" />
  <div class="modal is-active" v-if="open">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:70%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close"
      @click="close()"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <p class="title"> Thêm lãnh đạo công ty <strong class="has-text-danger ml-2">{{$route.query.stock_code}}</strong></p>
      <div class="field">
        <label class="label">Chọn người <strong class="has-text-danger">*</strong></label>
        <div class="control">
          <PeopleSearch :people="people" @doChange="selectPeople" />
        </div>
        <p class="fs12 mt-2">Không tìm thấy trong danh sách?
          <a class="fs16 fb600 ml-3" @click="selectPeople(undefined, true); addNew=true">Tạo mới</a> 
          <a class="fs16 fb600 has-text-warning-dark ml-3" @click="addNew=true" v-if="people">Sửa đổi</a>
          <a class="fs16 fb600 has-text-danger ml-3" @click="confirmDelete()" v-if="people">Xóa người</a>
        </p>
      </div>
      
      <div class="my-5 px-5 py-5" v-if="addNew" style="border: solid 1px #b1a7a6">
        <EditPeople :people="people" @newpeople="selectPeople($event, true); addNew=false" @closeform="addNew=false" />
      </div>
      
      <div class="field is-horizontal mt-5" v-for="(v,i) in manageData" :key="i">
        <div class="field-body">
          <div class="field">
          <label class="label">Chức vụ <strong class="has-text-danger">*</strong></label>
          <div class="control">
            <b-autocomplete
            :v-model="v.position"
            :value="v.position? v.position.value : null"
            :data="positionData? positionData : positions"
            keep-first
            clearable
            icon-right="magnify"
            field="value"
            :open-on-focus="true"
            @input="filterPosition"
            @focus="positionData=positions"
            @select="option => v.position = option">
             <template slot-scope="props">
              <div class="media">
              <div class="media-left has-text-danger">
              {{ props.option.index}}
              </div>
              <div class="media-content">
              {{ props.option.value}}
              </div>
                </div>
            </template>
          </b-autocomplete>
          </div>
        </div>

          <div class="field">
          <label class="label">Thời gian bổ nhiệm</label>
          <div class="control">
            <input class="input" type="text" placeholder="" v-model="v.date">
          </div>
        </div>

        <div class="field">
        <div class="control">
           <b-tooltip label='Thêm chức vụ'>
          <a @click="addPosition()">
            <span class="icon fs28">
              <i class="mdi mdi-plus-thick" />
            </span>
          </a>
           </b-tooltip>
          <b-tooltip label='Xóa chức vụ'>
            <a class="ml-2" @click="removePosition(v, i)">
            <span class="icon fs28 has-text-danger">
              <i class="mdi mdi-minus-thick" />
            </span>
          </a>
          </b-tooltip>
      </div>
      </div>
        </div>
        </div>

      <div class="field is-horizontal mt-5">
        <div class="field-body">
      <div class="field">
      <label class="label">Số lượng cổ phần <strong class="has-text-danger">*</strong></label>
      <div class="control has-icons-right">
         <input class="input" type="text" placeholder="" v-model="holder.number_share">
             <span class="icon is-small is-right">
      <i class="mdi mdi-information-variant has-text-white"></i>
    </span>
      </div>
    </div>

    <div class="field">
      <label class="label">Tỷ lệ %</label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="holder.percentage">
      </div>
    </div>

      <div class="field">
        <div class="control">
          <a>
            <span class="icon fs28 has-text-white">
              <i class="mdi mdi-plus-thick" />
            </span>
          </a>
           <b-tooltip label='Xóa thông tin cổ đông'>
            <a class="ml-2" @click="deleteHolder()">
            <span class="icon fs28  has-text-danger">
              <i class="mdi mdi-minus-thick" />
            </span>
          </a>
           </b-tooltip>
      </div>
      </div>
    </div>
    </div>

      <div class="mt-5 px-5 py-5" style="border: solid 1px #b1a7a6">
        <p>
          <strong class="mr-5"> Người có liên quan đến lãnh đạo công ty? </strong>
          <b-radio v-model="radio" v-for="v in choices" :key="v.code"
          :native-value="v">
          {{v.name}}
          </b-radio>
        </p>
        
        <template v-if="radio? radio.code==='yes' : false">
        <div class="field is-horizontal mt-4" v-for="(v,i) in relativePeople" :key="i">
        <div class="field-body">
          <div class="field">
          <label class="label">Chọn người <strong class="has-text-danger">*</strong></label>
          <div class="control">
             <PeopleSearch :people="v.other" @doChange="v.other=$event" />
          </div>
           <p class="fs12 mt-2">Không tìm thấy trong danh sách?
            <a class="fs16 fb600 ml-3" @click="addRelation=v">Tạo mới</a> 
          </p>
        </div>

          <div class="field" style="width:20%">
          <label class="label">Quan hệ <strong class="has-text-danger">*</strong></label>
          <div class="control">
           <b-autocomplete
            :v-model="v.type"
            :value="v.type? v.type.value : null"
            :data="relationData? relationData : relations"
            keep-first
            clearable
            icon-right="magnify"
            field="value"
            :open-on-focus="true"
            @focus="relationData=relations"
            @input="filterRelation"
            @select="option => option? v.type = option : false">
             <template slot-scope="props">
              <div class="media">
              <div class="media-left has-text-danger">
              {{ props.option.index}}
              </div>
              <div class="media-content">
              {{ props.option.value}}
              </div>
                </div>
            </template>
          </b-autocomplete>
          </div>
        </div>

      <div class="field" style="width:20%">
      <label class="label">Số lượng cổ phần <strong class="has-text-danger">*</strong></label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="v.number_share">
      </div>
    </div>

    <div class="field" style="width:10%">
      <label class="label">Tỷ lệ %</label>
      <div class="control">
         <input class="input" type="text" placeholder="" v-model="v.percentage">
      </div>
    </div>

      <div class="field">
        <div class="control">
           <b-tooltip label='Thêm quan hệ'>
          <a @click="addPeople()">
            <span class="icon fs28">
              <i class="mdi mdi-account-plus-outline" />
            </span>
          </a>
           </b-tooltip>
            <b-tooltip label='Xóa quan hệ'>
            <a @click="removePeople(v, i)">
            <span class="icon fs28 has-text-danger">
              <i class="mdi mdi-account-remove-outline" />
            </span>
          </a>
        </b-tooltip>
      </div>
      </div>
      </div>
    </div>
    </template>
    </div>
    <div class="my-5">
      <a class="button is-primary" @click="update()"> Cập nhật </a>
    </div>
    </section>
    </div>
  </div>

  <div class="modal is-active" v-if="addRelation">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:70%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close"
      @click="addRelation=undefined"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <EditPeople :people="undefined" @newpeople="createRelation" @closeform="addRelation=undefined" />
    </section>
    </div>
  </div>
</div>
</template>

<script>
import PeopleSearch from '@/components/profile/PeopleSearch'
import EditPeople from '@/components/profile/EditPeople'
export default {
  components: {
    PeopleSearch,
    EditPeople
  },
  props: ['editable'],
  data() {
    return {
      open: false,
      people: undefined,
      addNew: false,
      addRelation: undefined,
      choices: [{code: 'no', name: 'Không'}, {code: 'yes', name: 'Có'}],
      radio: {code: 'no', name: 'Không'},
      positions: [],
      relativePeople: [{other: undefined, type: undefined}],
      relations: [],
      manageData: [{}],
      connection: this.$connection(this.$buefy),
      connection1: this.$connection(this.$buefy),
      connection2: this.$connection(this.$buefy),
      connection3: this.$connection(this.$buefy),
      connection4: this.$connection(this.$buefy),
      connection5: this.$connection(this.$buefy),
      connection6: this.$connection(),
      connection7: this.$connection(),
      connection8: this.$connection(),
      connection9: this.$connection(),
      connection10: this.$connection(),
      errors: [],
      privateHolder: [],
      holder: {},
      positionData: undefined,
      relationData: undefined
    }
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Escape') {
        if(this.addRelation) this.addRelation = undefined
        else if(this.open) this.open = false
      }
    })
    this.relations = this.$copy(this.api.filter2var('family', 'relation'))
    this.positions = this.$copy(this.api.filter2var('list', 'position'))
    this.loadData()
  },
  watch: {
    "connection.getdataReady": function(newVal) {
      if (newVal==="success") {
        let data = this.$copy(this.connection.getbatchData.find(v=>v.name==='management').data)
        data.map(v=>{
          v.position = this.positions.find(x=>parseInt(x.id)===v.position)
        })
        if(data.length>0) this.manageData = data
        let list = this.connection.getbatchData.find(v=>v.name==='privateholder').data
        list.length>0? this.holder = list[0] : false
        let arr = this.connection.getbatchData.find(v=>v.name==='relation').data
        if(arr.length===0) return
        this.radio = this.choices.find(v=>v.code==='yes')
        this.relativePeople = []
        arr.map(v=>{
          this.relativePeople.push({id: v.id, other: {id: v.other, uid: v.other__uid, name: v.other__name}
          , type: this.relations.find(x=>parseInt(x.id)===v.type)})
        })
        let conn = {name: 'privateholder', path: 'path', params: {filter: {company: this.$route.query.company, people__in: arr.map(v=>v.other)}}}
        this.connection6.getApi([conn])   
      }
    },

    'connection1.getupdateRecord': function(newVal) {
      if(newVal) {
        let data = []
        let delList = []
        let updateList = []
        this.relativePeople.filter(x=>x.other && x.type).map(v=>{
          data.push({id: v.id, people: this.people.id, other: v.other.id, type: v.type.id})
          if(this.$empty(v.number_share)) {
            if(v.holderID) delList.push({id: v.holderID})
          } else {
            updateList.push({id: v.holderID, number_share: this.$formatNumber(v.number_share), percentage: v.percentage, people: v.other.id,
            company: this.$route.query.company})
          }
        })
        data.length>0? this.connection2.insert('relation', data) : false
        if(updateList.length>0) this.connection7.insert('privateholder', updateList)
        delList.map(v=>{
          let conn = this.$connection()
          conn.delete('privateholder', v.id)
        })
        this.$emit('updatetask')
      }
    },
    
    "connection4.getdataReady": function(newVal) {
      if (newVal==="success") {
        let data = this.$copy(this.connection4.getbatchData[0].data)
        this.$store.commit('updateState', {name: 'pagetask', key: 'api', data: this.$copy(this.connection4.getbatchStatus[0])})
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: data})
        if(Object.keys(this.pagetask.origin_api).length===0) {
          this.$store.commit('updateState', {name: 'pagetask', key: 'origin_api', data: this.$copy(this.connection4.getbatchStatus[0])})
        }
      }
    },

    "connection6.getdataReady": function(newVal) {
      if (newVal==="success") {
        this.privateHolder = this.connection6.getbatchData[0].data
        this.privateHolder.map(v=>{
          let found = this.relativePeople.find(x=>x.other.id===v.people)
          found.number_share = this.$numtoString(v.number_share)
          found.percentage = v.percentage
          found.holderID = v.id
        })
        this.relativePeople = this.$copy(this.relativePeople)
      }
    },

    "connection8.getdataReady": function(newVal) {
      if (newVal==="success") {
        let row = this.connection8.getbatchData[0].data[0]
        this.open = true
        this.selectPeople(row)
      }
    },

    'connection9.getupdateStatus': function(newVal) {
      if(newVal) {
        let data = this.connection9.getupdateRecord
        if(data[0].deleted) {
          let copy = this.$copy(this.pagetask.data)
          let idx = copy.findIndex(v=>v.people===data[0].id)
          this.$delete(copy, idx)
          this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
          this.selectPeople(undefined, true)
        } else {
          let info = {duration: 4000, type: 'is-danger', hasIcon: false, message: 'Lỗi. Xoá dữ liệu thất bại.'}
          this.$buefy.notification.open(info)
        }
      }
    },

    people: function(newVal) {
      if(!newVal) {
        this.relativePeople = [{other: undefined, type: undefined}]
        this.position = undefined
        this.date = undefined
        this.radio = this.choices.find(v=>v.code==='no')
      }
    },

    menuaction: function(newVal) {
      if(newVal? newVal.action==='download': false) {
        let types = {} 
        this.pagetask.fields.map(v=>types[v.name] = 'String')
        this.$exportExcel(this.pagetask.data, 'management', this.pagetask.fields.map(v=>v.name), types)
      }
    },

    'pagetask.record': function(newVal) {
      if(newVal) {
        if(this.pagetask.action==='show') {
          let conn = {name: 'people', url: 'data/People', path: 'path', params: {filter: {id: newVal.people},
          sort: 'management__position__index',
          values: 'id,uid,name,legal_id,avatar,address,phone,email,dob,domicile,management__position,management__position__code,management__position__value,management__company,management__company__stock_code'}}
          this.connection8.getApi([conn])
        }
        this.$store.commit('updateState', {name: 'pagetask', key: 'record', data: undefined})
      }
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api },
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile },
      set: function(val) {this.$store.commit('updateIsMobile', {ismobile: val})}
    },

    pagetask: {
      get: function() {return this.$store.state.pagetask},
      set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    },
  },
    
  methods: {
    loadData() {
      let fields = []
      fields.push(this.$createField('id', 'Id', 'number', true, true))
      fields.push(this.$createField('company__stock_code', 'Công ty', 'string', true, true))
      let field = this.$createField('people__name', 'Họ tên', 'string', true, true)
      field.style = {list: [{value: this.$route.query.stock_code, class: 'button is-small is-primary is-outlined has-text-dark'}],
        condition: 'company__stock_code', click: true}
      fields.push(field)
      fields.push(this.$createField('position__value', 'Chức vụ', 'number', true, true))
      fields.push(this.$createField('date', 'Ngày bổ nhiệm', 'string', true, true))
      fields.push(this.$createField('people__uid', 'Mã định danh', 'string', true, true))
      fields.push(this.$createField('action', '', 'string', true, true, '7%', 'delete'))
      this.pagetask = {data: [], fields: fields, filter: [], record: undefined, action: undefined, 
      enableDelete: true, enableApprove: true, api: {}, origin_api: {}, reload: 0, highlight: undefined, filterby: undefined}
      let values = 'id,people,people__name,people__uid,company,company__stock_code,company__name,position,position__value,date'
      this.connection4.getApi([{name: 'management', path: 'path', params: {values: values, filter: {company: this.$route.query.company}}}])
    },

    openModal() {
      this.people=undefined
      this.addNew=false
      this.radio = this.choices.find(v=>v.code==='no')
      this.date = undefined
      this.position = undefined
      this.relativePeople = [{other: undefined, type: undefined}]
      this.holder = {}
      this.manageData = [{}]
      this.open=true
      this.positionData = undefined
      this.relationData = undefined
    },

    addPeople(option, v) {
      if(option) {
        v.people = option
        this.relativePeople = this.$copy(this.relativePeople)
      }
      else this.relativePeople.push({other: undefined, type: undefined})
    },

    removePeople(v, i) {
      if(v.id) this.connection3.delete('relation', v.id)
      this.$delete(this.relativePeople, i)
      if(this.relativePeople.length===0) this.relativePeople = [{other: undefined, type: undefined}]
    },

    update() {
      let data = []
      this.manageData.map(v=>{
        if(this.$empty(v.position)) {
          if(v.id) {
            let conn = this.$connection()
            conn.delete('management', v.id)
          }
        } else {
          data.push({id: v.id, people: this.people.id,  position: v.position.id, company: this.$route.query.company, date: v.date})
        }
      })
      this.connection1.insert('management', data)
      let self = this
      setTimeout(function() {self.loadData()}, 100)
      if(this.$empty(this.holder.number_share)) {
        if(this.holder.id) this.connection6.delete('privateholder', this.holder.id)
      } else {
        let copy = this.$copy(this.holder)
        copy.number_share = this.$formatNumber(copy.number_share)
        copy.company = this.$route.query.company
        copy.people = this.people.id
        this.connection6.insert('privateholder', [copy]) 
      }
    },

    selectPeople(event, isNew) {
      this.people = event
      this.radio = this.choices.find(v=>v.code==='no')
      this.date = undefined
      this.position = undefined
      this.relativePeople = [{other: undefined, type: undefined}]
      this.holder = {}
      this.manageData = [{}]
      if(isNew) return
      this.connection.getApi(
        [{name: 'management', path: 'path', params: {filter: {people: event.id, company: this.$route.query.company}}},
        {name: 'relation', path: 'path', params: {values: 'id,people,other,other__uid,other__name,type', filter: {people: event.id}}},
        {name: 'privateholder', path: 'path', params: {filter: {company: this.$route.query.company, people: event.id}}}
      ])
    },

    createRelation(event) {
      this.addRelation.other = event
      this.relativePeople = this.$copy(this.relativePeople)
      this.addRelation = undefined
    },

    addPosition() {
      this.manageData.push({})
    },

    removePosition(v, i) {
      if(v.id) {
        this.connection5.delete('management', v.id)
        let copy = this.$copy(this.pagetask.data)
        let idx = copy.findIndex(v=>v.id===v.id)
        this.$delete(copy, idx)
        this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      }
      this.$delete(this.manageData, i)
      if(this.manageData.length===0) this.manageData = [{}]
    },

    close() {
      this.open = false
      this.manageData = [{}]
    },

    filterPosition(text) {
      this.positionData = this.$empty(text)? this.positions :
      this.positions.filter(v=>v.value.toLowerCase().indexOf(text.toLowerCase())>=0)
    },

    filterRelation(text) {
      this.relationData = this.$empty(text)? this.relations :
      this.relations.filter(v=>v.value.toLowerCase().indexOf(text.toLowerCase())>=0)
    },

    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Xóa ' + this.people.name,
        message: 'Bạn có chắc chắn muốn xóa <b>' + this.people.name + '</b>? Toàn bộ thông tin về cá nhân, chức vụ, sở hữu, quan hệ sẽ bị xóa.',
        confirmText: 'Xác nhận',
        cancelText: 'Hủy bỏ',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.connection9.delete('people', [{id: this.people.id}])
      })
    },

    deleteHolder() {
      if(this.holder.id) this.connection10.delete('privateholder', this.$copy(this.holder.id))
      this.holder = {}
    }
  }
}
</script>