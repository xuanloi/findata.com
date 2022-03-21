<template>
  <div>
    <p class="is-help mt-2"> Tạo trường dữ liệu mới để thêm vào bảng.</p>
     <p class="panel-tabs mb-5">
            <a v-for="(v,i) in fieldType" :key="i"
            :class="selectType.code===v.code? 'is-active' : ''"
            @click="selectType = v"
            >
              {{v.name}}
            </a>
          </p>
     <template v-if="selectType.code==='formula'">
    <div class="field px-0 mx-0">
      <label class="label fs14"> Chọn trường để tạo công thức <span class="has-text-danger"> * </span> </label>
      <div class="control">
        <b-taginput
        size="is-small"
          v-model="tags"
          :data="fields.filter(v=>v.format==='number')"
          type="is-primary is-light"
          autocomplete
          :open-on-focus="true"
          field="caption"
          icon="plus"
          placeholder="Chọn trường"
         >
          <template slot-scope="props">
            <span class="mr-3 has-text-danger has-text-weight-bold"> {{props.option.name}}</span> 
            <span :class="tags.find(v=>v.id===props.option.id)? 'has-text-primary' : ''"> {{props.option.label}} </span>
          </template>
          <template slot="empty">
            Không có trường thỏa mãn
          </template>
        </b-taginput>
      </div>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='tags')"> {{errors.find(v=>v.name==='tags').message}} </p>
    </div>

          <div class="field mt-3" v-if="tags.length>0">
          <p class="help is-primary"> Click đúp vào để thêm vào công thức tính.</p>
          <div class="tags">
            <a @dblclick="formula = formula? (formula + ' ' + v.name) : v.name" class="tag is-rounded" v-for="(v,i) in tags" :key="i">{{v.name}}</a>
          </div>
        </div>
            <div class="field mt-3 px-0 mx-0">
              <label class="label fs14">Công thức tính <span class="has-text-danger"> * </span> </label>
              <p class="control">
              <textarea class="textarea is-small" rows="3" type="text" placeholder="Tạo công thức tại đây" v-model="formula"> </textarea>
              </p>
                <p class="help has-text-danger" v-if="errors.find(v=>v.name==='formula')"> {{errors.find(v=>v.name==='formula').message}} </p>
            </div>
            <div class="field mt-3 px-0 mx-0">
              <label class="label fs14"> Hiển thị trên bảng giá theo <span class="has-text-danger"> * </span> </label>
              <b-autocomplete
                size="is-small"
                icon-right="magnify"
                :value="selectUnit? selectUnit.name : ''"
                placeholder=""
                :keep-first=true
                :open-on-focus=true
                :data="moneyunit"
                field="name"
                @select="option => selectUnit = option">
              </b-autocomplete>
            </div>
            </template>

            <div class="field px-0 mx-0">
            <label class="label fs14">Tên trường <span class="has-text-danger"> * </span> </label>
            <p class="control">
              <input class="input is-small" type="text" placeholder="Tên trường phải là duy nhất" v-model="name" 
              :readonly="selectType? selectType.code==='formula': false">
            </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='name')"> {{errors.find(v=>v.name==='name').message}} </p>
            <p class="help has-text-primary" v-else> Tên trường do hệ thống tự sinh.</p>
          </div>

          <div class="field mt-3">
            <label class="label fs14"> Mô tả <span class="has-text-danger"> * </span> </label>
            <p class="control is-expanded">
              <input class="input is-small" type="text" placeholder="" v-model="label">
            </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='label')"> {{errors.find(v=>v.name==='label').message}} </p>
          </div>
          
           <div class="field mt-3" v-if="selectType.code==='empty'">
          <label class="label fs14"
            >Kiểu dữ liệu
            <span class="has-text-danger"> * </span>
          </label>
          <div class="control fs14">
               <b-radio v-for="(v,i) in datatype.filter(x=>x.code!=='date')" :key="i" v-model="radioType" :native-value="v">
                {{v.name}}
              </b-radio>
          </div>
        </div>
        <ChartField v-bind="{fields: columns}" @chartoption="getOption" @changefields="changeFields"
          v-if="selectType.code==='chart'"/> 
          <div class="field mt-4">
            <p class="control">
              <a class="button is-primary is-small is-outlined is-rounded" 
              @click="selectType.code==='formula'? createField() : createEmptyField()"> Tạo trường</a>
            </p>
          </div>   
        </div>
</template>

<script>


export default {
  props: ['pagename'],

  components: {
    ChartField: () => import('@/components/datatable/ChartField')
  },
  
  data() {
    return {
      selectUnit: undefined,
      connection: this.$connection(),
      data: [],
      current: 1,
      filterData: [],
      loading: false,
      fieldType: [{code: 'formula', name: 'Công thức'}, {code: 'empty', name: 'Trường rỗng'}, {code: 'chart', name: 'Biểu đồ'}],
      errors: [],
      tags: [],
      formula: undefined,
      name: 'f' + this.$dayjs(new Date()).format("hhmmss"),
      label: undefined,
      errors: [],
      selectType: undefined,
      radioType: undefined,
      fields: [],
      options: undefined,
      columns: []
    }
  },

  created() {
    this.columns = this.$copy(this.pagedata.fields.filter(v=>v.format==='number'))
    this.radioType = this.datatype.find(v=>v.code==='string')
    this.selectType = this.fieldType.find(v=>v.code==='formula')
    this.selectUnit = this.moneyunit.find(v=>v.code==='one')
    this.getFields()
  },

  watch: {
    'pagedata.fields': function(newVal) {
      newVal? this.getFields() : false
    }
  },

  computed: {
    moneyunit: {
      get: function() {return this.$store.state.moneyunit},
      set: function(val) {this.$store.commit("updateMoneyUnit", {moneyunit: val})}
    },

    pagedata: {
      get: function() {return this.$store.state[this.pagename]},
      set: function(val) {this.$store.commit('updateStore', {name: this.pagename, data: val})}
    },

    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    },

    datatype: {
      get: function() {return this.$store.state.datatype},
      set: function(val) {this.$store.commit("updateDataType", {datatype: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", { ismobile: val })}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
    }
  },

  methods: {
    getOption(v) {
      this.options = v
    },

    changeFields(v) {
      this.columns = this.$copy(v)
    },

    getFields() {
      this.fields = this.pagedata? this.$copy(this.pagedata.fields) : []
      this.fields.map(v=>v.caption = (v.label? v.label.indexOf('<')>=0 : false)? v.name : v.label)
    },

    checkValid() {
			this.errors = []
			if(this.tags.length===0) {
        this.errors.push({name: 'tags', message: 'Chưa chọn trường xây dựng công thức.'})
      }
			
			if(!this.$empty(this.formula)? this.$empty(this.formula.trim()) : true) {
        this.errors.push({name: 'formula', message: 'Công thức không được bỏ trống.'})
      }

      if(!this.$empty(this.label)? this.$empty(this.label.trim()) : true )
        this.errors.push({name: 'label', message: 'Mô tả không được bỏ trống.'})
      else if(this.pagedata.fields.find(v=>v.label.toLowerCase()===this.label.toLowerCase())) {
        this.errors.push({name: 'label', message: 'Mô tả bị trùng. Hãy đặt mô tả khác.'})
      }

      if(this.errors.length>0) return false 
      //check formula
      let val = this.$copy(this.formula)
			this.tags.forEach(v => {
				let myRegExp = new RegExp(v.name, 'g')
				val = val.replace(myRegExp, Math.random())				
			})

			try {
				let value = this.$calc(val)
				if(isNaN(value) || value===Number.POSITIVE_INFINITY || value===Number.NEGATIVE_INFINITY) {
					this.errors.push({name: 'formula', message: 'Công thức không hợp lệ'})
				}
			}
			catch(err) {
				this.errors.push({name: 'formula', message: 'Công thức không hợp lệ'})
      }
      return this.errors.length>0? false : true
		},

    createField() {
      if(!this.checkValid()) return
      let field = this.$createField(this.name.trim(), this.label.trim(), 'number', true)
      field.formula = this.formula.trim()
      field.tags = this.tags.map(v=>v.name)
      field.level = Math.max(...this.tags.map(v=>v.level? v.level : 0)) + 1
      field.unit = this.selectUnit.detail
      let copy = this.$copy(this.pagedata.fields)
      copy.push(field)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
      this.$emit('newfield', field)
      this.$calculateFields(this.pagename)
      if(this.pagedata.filters? this.pagedata.filters.length>0 : false) {
        this.$store.commit("updateState", {name: this.pagename, key: "filterby", data: this.pagedata.filters})
      }
      this.tags = []
      this.formula = undefined
      this.label = undefined
      this.name = 'f' + this.$dayjs(new Date()).format("hhmmss")
    },

    createEmptyField() {
      this.errors = []
       if(!this.$empty(this.name)? this.$empty(this.name.trim()) : true )
        this.errors.push({name: 'name', message: 'Tên không được bỏ trống.'})
      else if(this.pagedata.fields.find(v=>v.name.toLowerCase()===this.name.toLowerCase())) {
        this.errors.push({name: 'name', message: 'Tên trường bị trùng. Hãy đặt tên khác.'})
      }

      if(!this.$empty(this.label)? this.$empty(this.label.trim()) : true )
        this.errors.push({name: 'label', message: 'Mô tả không được bỏ trống.'})
      else if(this.pagedata.fields.find(v=>v.label.toLowerCase()===this.label.toLowerCase())) {
        this.errors.push({name: 'label', message: 'Mô tả bị trùng. Hãy đặt mô tả khác.'})
      }
      if(this.errors.length>0) return
      let field = this.$createField(this.name.trim(), this.label.trim(), this.radioType.code, true)
      if(this.selectType.code==='chart') {
        field = this.$createField(this.name.trim(), this.label.trim(), 'string', true)
        let text = JSON.stringify(this.options)
        text = text.replaceAll('"', "'")
        let val = JSON.stringify(this.columns.map(v=>v.name))
        val = val.replaceAll('"', "'")
        field.template =`<Chart v-bind="{row: row, fields: ${val} , options: ${text}}" />`
      }
      let copy = this.$copy(this.pagedata.fields)
      copy.push(field)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
      this.$emit('newfield', field)
      this.label = undefined
      this.name = 'f' + this.$dayjs(new Date()).format("hhmmss")
    }
  }
}
</script>