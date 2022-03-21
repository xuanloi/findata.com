<template>
  <div>
    
      <div class="field mt-3 mb-1" v-if="field.format==='number'">
      <label class="label fs14"> Trường để xây dựng biểu thức <span class="has-text-danger"> * </span> </label>
      <div class="control">
        <b-taginput
        size="is-small"
          v-model="tagsField"
          :data="pageData? pageData.fields.filter(v=>v.format==='number') : []"
          type="is-primary is-light"
          autocomplete
          :open-on-focus="true"
          field="label"
          icon="plus"
          placeholder="Chọn trường"
         >
          <template slot-scope="props">
            <span class="mr-3 has-text-danger has-text-weight-bold"> {{props.option.name}}</span> 
            <span :class="tagsField.find(v=>v.id===props.option.id)? 'has-text-primary' : ''"> {{props.option.label}} </span>
          </template>
          <template slot="empty">
            Không có trường thỏa mãn
          </template>
        </b-taginput>
      </div>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='tagsField')"> {{errors.find(v=>v.name==='tagsField').message}} </p>
    </div>  

    <div v-if="tagsField.length>0">
      <a @dblclick="expression = expression? (expression + ' ' + v.name) : v.name" 
      class="tag is-rounded" v-for="(v,i) in tagsField" :key="i">{{v.name}}</a>
    </div>

      <div class="field is-horizontal mt-3">
        <div class="field-body">
        <div class="field" v-if="field.format==='number'">
          <label class="label fs14">Biểu thức có dạng Đúng / Sai <span class="has-text-danger"> * </span> </label>
          <p class="control is-expanded">
            <input class="input is-small" type="text" v-model="expression">
           </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='expression')"> {{errors.find(v=>v.name==='expression').message}} </p>
        </div>

        <div class="field" v-else>
          <label class="label"> Chuỗi kí tự <span class="has-text-danger"> * </span>
          </label>
          <p class="control">
            <input
              class="input is-small"
              type="text"
              placeholder=""
              v-model="searchText"
              @change="changeStyle()"
            />
          </p>
          <p
            class="help has-text-danger"
            v-if="errors.find((v) => v.name === 'searchText')"
          >
            {{ errors.find((v) => v.name === "searchText").msg }}
          </p>
        </div>

        <div class="field is-narrow" v-if="filterType==='color'">
            <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
              <input type="color" v-model="color" @change="changeStyle()">
            </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='color')"> {{errors.find(v=>v.name==='color').message}} </p>
          </div>

        <div class="field is-narrow" v-else-if="filterType==='size'">
            <label class="label fs14"> Cỡ chữ <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
            <input class="input is-small" type="text" placeholder="Nhập số" v-model="size" @change="changeStyle()">
            </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='size')"> {{errors.find(v=>v.name==='size').message}} </p>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  props: ['filterObj', 'filterType', 'pagename', 'field'],

  data() {
    return {
      tagsField: [],
      expression: undefined,
      form: undefined,
      color: undefined,
      size: undefined,
      errors: [],
      searchText: undefined
    }
  },

  created() {
    this.color = this.filterObj.color
    this.size = this.filterObj.size
    this.expression = this.filterObj.expression? this.filterObj.expression : this.field.name
    if(this.filterObj.tags) {
      this.filterObj.tags.map(v=>{
        this.tagsField.push(this.pageData.fields.find(x=>x.name===v))
      })
    } else if(this.field.format==='number') this.tagsField.push(this.pageData.fields.find(v=>v.name===this.field.name))
  },

  watch: {
    expression: function(newVal) {
      if(this.$empty(newVal)) return
      else this.changeStyle()
    },
  },

  computed: {
    colorscheme: {
      get: function() {return this.$store.state.colorscheme},
      set: function(val) {this.$store.commit("updateColorScheme", {colorscheme: val})}
    },

    pageData: {
      get: function() {return this.$store.state[this.pagename]},
      set: function(val) {this.$store.commit('updateStore', {name: this.pagename, data: val})}
    },

    colorchoice: {
      get: function() {return this.$store.state.colorchoice},
      set: function(val) {this.$store.commit("updateColorChoice", {colorchoice: val})}
    }
  },

  methods: {
    changeStyle() {
      let check = this.field.format==='number'? this.checkExpression() : this.checkCondition()
      if(!check) return

      var row = this.field.format==='number'? {expression: this.expression, tags: this.tagsField.map(v=>v.name)}
      : {keyword: this.searchText, type: 'search'}
      this.filterType==='color'? row.color = this.color : row.size = this.size
      this.$emit('databack', row)
    },

    checkCondition() {
      this.errors = []
      if(this.filterType==='color' && this.$empty(this.color)) this.errors.push({name: 'color', message: 'Chọn màu'})
      if(this.filterType==='size' && this.$empty(this.size)) this.errors.push({name: 'size', message: 'Nhập cỡ chữ'})
      if(this.$empty(this.searchText))  this.errors.push({name: 'searchText', message: 'Chưa nhập chuỗi kí tự'})
      return this.errors.length>0? false : true
    },

    checkExpression() {
      this.errors = []
      if(this.filterType==='color' && this.$empty(this.color)) this.errors.push({name: 'color', message: 'Chọn màu'})
      if(this.filterType==='size' && this.$empty(this.size)) this.errors.push({name: 'size', message: 'Nhập cỡ chữ'})

      let val = this.$copy(this.expression)
      let exp = this.$copy(this.expression)
			this.tagsField.forEach(v => {
				let myRegExp = new RegExp(v.name, 'g')
        val = val.replace(myRegExp, Math.random())
        exp = exp.replace(myRegExp, "field.formatNumber(row['" + v.name + "'])")		
      })

			try {
        let value = this.$calc(val)
				if(isNaN(value) || value===Number.POSITIVE_INFINITY || value===Number.NEGATIVE_INFINITY) {
					this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
				} else if(!(eval(value)===true || eval(value)===false)) {
          this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
        }
			}
			catch(err) {
				this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
      }
      return this.errors.length>0? false : true
    }
  }
}
</script>