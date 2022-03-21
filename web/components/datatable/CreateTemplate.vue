<template>
  <div class="px-5">
    <div class="field is-horizontal">
  <div class="field-body">
    <div class="field">
      <label class="label">Đối tượng</label>
      <p class="control fs14">
          <b-radio v-for="(v,i) in types" :key="i" v-model="type"
          :native-value="v" @input="changeType(v)">
            {{v.name}}
          </b-radio>
      </p>
    </div>
        <div class="field">
      <label class="label">Kích cỡ</label>
      <p class="control fs14">
          <b-radio v-for="(v,i) in sizes.filter(v=>type? (type.code==='tag'? v.code!=='is-small' : 1>0) : true)" :key="i" v-model="size"
          :native-value="v" @input="changeType(v)">
            {{v.name}}
          </b-radio>
      </p>
    </div>
  </div>
</div>  

<div class="field is-horizontal" v-if="['tag', 'button'].find(v=>v===type.code)">
  <div class="field-body">
    <div class="field">
      <label class="label">Hình khối</label>
      <p class="control fs14">
          <b-radio v-for="(v,i) in shapes" :key="i" v-model="shape"
          :native-value="v" @input="changeType(v)">
            {{v.name}}
          </b-radio>
      </p>
    </div>
        <div class="field" v-if="type.code!=='tag'">
      <label class="label">Outline</label>
      <p class="control fs14">
        <b-radio v-for="(v,i) in outlines" :key="i" v-model="outline"
        :native-value="v" @input="changeType(v)">
          {{v.name}}
        </b-radio>
      </p>
    </div>
  </div>
</div>  

  <div class="buttons mt-5" v-if="type.code==='button'">
      <a :class="getClass(v)" v-for="(v,i) in colorscheme" :key="i" 
      @click="doSelect(v)" :ref="'button' + i"> {{v.name}} </a>
    </div>

    <div class="tags mt-5" v-else-if="type.code==='tag'">
      <a :class="getClass(v)" v-for="(v,i) in colorscheme" :key="i"
      @click="doSelect(v)" :ref="'tag' + i"> {{v.name}} </a>
    </div>

    <div class="mt-5" v-else-if="type.code==='span'">
      <a class="mr-5" :class="getSpanClass(v)" v-for="(v,i) in colorscheme" :key="i"
      @click="doSelectSpan(v)" :ref="'span' + i"> {{v.name}} </a>
    </div>

    <div class="tabs">
      <ul>
        <li :class="tab.code===v.code? 'is-active' : ''" 
        v-for="(v,i) in tabs" :key="i" @click="tab=v"><a>{{v.name}}</a>
        </li>
      </ul>
    </div>

  <template v-if="tab.code==='selected'">
    <a v-for="(v,i) in tags" :key="i" @click="selected=v">
      <div class="field is-grouped is-grouped-multiline mt-4">
    <p class="control">
      <a :class="v.class">
        {{v.name}}
      </a>
    </p>
    <p class="control">
      <input class="input is-small" type="text" v-model="v.name">
    </p>
    
    <p class="control">
      <a @click="remove(i)">
        <span class="icon has-text-danger fs26">
          <i class="mdi mdi-close"/>
        </span>
      </a>
    </p>
    <p class="control has-text-right ml-6" v-if="selected? selected.id===v.id : false">
      <span class="icon fs26">
        <i class="mdi mdi-check"/>
      </span>
    </p>
      </div>  
    </a>
  </template>

  <template v-else-if="tab.code==='condition'">
    <div v-if="selected">
      <b-radio v-for="(v,i) in conditions" :key="i" v-model="condition"
      :native-value="v" @input="changeCondition(v)">
        {{v.name}}
      </b-radio>
    </div>
    
    <template v-if="condition? condition.code==='yes' : false">
      <div class="field mt-3">
      <label class="label fs14"> Chọn trường để xây dựng biểu thức <span class="has-text-danger"> * </span> </label>
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
  
    <div class="field mt-1" v-if="tagsField.length>0">
          <p class="help is-primary"> Click đúp vào để thêm vào biểu thức.</p>
          <div class="tagsField">
            <a @dblclick="expression = expression? (expression + ' ' + v.name) : v.name" 
            class="tag is-rounded" v-for="(v,i) in tagsField" :key="i">{{v.name}}</a>
          </div>
        </div>
   
        <div class="field">
          <label class="label fs14">Biểu thức có dạng Đúng / Sai <span class="has-text-danger"> * </span> </label>
          <p class="control is-expanded">
            <input class="input is-small" type="text" v-model="expression" placeholder="Tạo biểu thức tại đây">
           </p>
            <p class="help has-text-danger" v-if="errors.find(v=>v.name==='expression')"> {{errors.find(v=>v.name==='expression').message}} </p>
        </div>
    
  </template>
  </template>
        
  <template v-else-if="tab.code==='option' && selected">
    <div class="field is-horizontal border-bottom pb-2 mt-1">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Màu nền </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioBGcolor"
                :native-value="v" @input="changeStyle()">
                  {{v.name}}
                </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioBGcolor? radioBGcolor.code==='option' : false">
            <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
              <input type="color" v-model="bgcolor" @change="changeStyle()">
            </p>
          </div>
        </div>
      </div>
      
      <div class="field is-horizontal border-bottom pb-2">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Màu chữ </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioColor"
                :native-value="v" @input="changeStyle()">
                {{v.name}}
              </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioColor? radioColor.code==='option' : false">
            <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
            <input type="color" v-model="color" @change="changeStyle()">
            </p>
          </div>
        </div>
      </div>

      <div class="field is-horizontal border-bottom pb-2">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Cỡ chữ </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioSize"
                  :native-value="v" @input="changeStyle()">
                  {{v.name}}
                </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioSize? radioSize.code==='option' : false">
            <label class="label fs14"> Cỡ chữ <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="textsize" @change="changeStyle()">
            </p>
          </div>
        </div>
      </div>
  </template>

  <template v-else-if="tab.code==='template'">
    <p class="mb-3">
     <a @click="copyContent()" class="mr-6">
        <span class="icon fs20">
          <i class="mdi mdi-content-copy"/>
        </span>
        copy
      </a>

      <a @click="changeTemplate()">
        <span class="icon fs20">
          <i class="mdi mdi-update"/>
        </span>
        Cập nhật
      </a>
    </p>
    <div>
      <textarea class="textarea fs14" rows="10" v-model="text"> </textarea>
    </div>
  </template>
  </div>
</template>

<script>
export default {
  props: ['pagename', 'field'],

  data() {
    return {
      type: undefined,
      size: undefined,
      types: [{code: 'span', name: 'span'}, {code: 'tag', name: 'tag'}, {code: 'button', name: 'button'}],
      sizes: [{code: 'is-small', name: 'Nhỏ', value: 'is-size-6'}, {code: 'is-normal', name: 'Bình thường', value: 'is-size-5'}, 
      {code: 'is-medium', name: 'Trung bình', value: 'is-size-4'}, {code: 'is-large', name: 'Lớn', value: 'is-size-3'}],
      shapes: [{code: 'default', name: 'Mặc định'}, {code: 'is-rounded', name: 'Tròn góc'}],
      shape: undefined,
      outlines: [{code: 'default', name: 'Mặc định'}, {code: 'is-outlined', name: 'Outline'}],
      outline: undefined,
      conditions: [{code: 'no', name: 'Không áp dụng'}, {code: 'yes', name: 'Có áp dụng'}],
      condition: undefined,
      tags: [],
      selected: undefined,
      tabs: [{code: 'selected', name: 'Đã chọn'}, {code: 'condition', name: 'Điều kiện'}, {code: 'option', name: 'Tùy chọn'},
      {code: 'template', name: 'Template'}],
      tab: undefined,
      tagsField: [],
      errors: [],
      expression: '',
      text: undefined,
      radioBGcolor: undefined,
      radioColor: undefined,
      radioSize: undefined,
      bgcolor: undefined,
      color: undefined,
      textsize: undefined
    }
  },

  created() {
    this.type = this.types.find(v=>v.code==='tag')
    this.size = this.sizes.find(v=>v.code==='is-normal')
    this.shape = this.shapes.find(v=>v.code==='is-rounded')
    this.outline = this.shapes.find(v=>v.code==='default')
    if(this.$empty(this.field.template)) this.tab = this.tabs.find(v=>v.code==='selected')
    else {
      this.text = this.$copy(this.field.template)
      this.tab = this.tabs.find(v=>v.code==='template')
    }
    this.condition = this.conditions.find(v=>v.code==='no')
  },

  watch: {
    expression: function(newVal) {
      if(this.$empty(newVal)) return
      else this.checkExpression()
    },

    tab: function(newVal, oldVal) {
      if(oldVal===undefined) return

      if(newVal.code==='template') {
        let value = '<p>'
        this.tags.map((v,i)=>{
          value += '<span class="' + v.class + (this.tags.length>i+1? ' mr-2' : '') + '" '
          if(v.style) value += 'style="' +  v.style + '" '
          value += (v.expression? ' v-if="' + v.expression +  '"' : '') + '>' + v.name + '</span>' 
        })
        value += '</p>'
        this.text = value

      } else if(newVal.code==='option') {
        if(!this.selected) return
        this.radioBGcolor = this.selected.bgcolor? this.colorchoice.find(v=>v.code==='option') : this.colorchoice.find(v=>v.code==='none')
        this.radioColor = this.selected.color? this.colorchoice.find(v=>v.code==='option') : this.colorchoice.find(v=>v.code==='none')
        this.radioSize = this.selected.textsize? this.colorchoice.find(v=>v.code==='option') : this.colorchoice.find(v=>v.code==='none')
        this.bgcolor = this.selected.bgcolor? this.selected.bgcolor : undefined
        this.color = this.selected.color? this.selected.color : undefined
        this.textsize = this.selected.textsize? this.selected.textsize : undefined

      } else if(newVal.code==='condition') {
        this.condition =  this.conditions.find(v=>v.code==='no')
        this.tagsField = []
        this.expression = ''
        if(this.selected? this.selected.expression : false) {
          this.condition = this.conditions.find(v=>v.code==='yes')
          this.tagsField = this.$copy(this.selected.tags)
          this.expression = this.$copy(this.selected.formula)
        }
      }
    }
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
      this.selected.bgcolor = this.selected.color = this.selected.textsize = this.selected.style = undefined
      let style = ''
      if(this.radioBGcolor.code==='option'? !this.$empty(this.bgcolor) : false) {
        this.selected.bgcolor = this.bgcolor
        style += 'background-color: ' + this.bgcolor + ' !important;; '
      }

      if(this.radioColor.code==='option'? !this.$empty(this.color) : false) {
        this.selected.color = this.color
        style += 'color: ' + this.color + ' !important; '
      }
      
      if(this.radioSize.code==='option'? this.$isNumber(this.textsize) : false) {
        this.selected.textsize = this.textsize
        style += 'font-size: ' + this.textsize + 'px !important; '
      }

      this.$empty(style)? false : this.selected.style = style
    },

    changeCondition(v) {
      if(v.code==='no') this.selected.expression = undefined
    },

    copyContent() {
      this.$copyToClipboard(this.text)
    },

    changeTemplate() {
      let copy = this.$copy(this.pageData.fields)
      let found = copy.find(v=>v.name===this.field.name)
      found.template = this.text
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    checkExpression() {
      this.errors = []
      let val = this.$copy(this.expression)
      let exp = this.$copy(this.expression)
			this.tagsField.forEach(v => {
				let myRegExp = new RegExp(v.name, 'g')
        val = val.replace(myRegExp, Math.random())
        exp = exp.replace(myRegExp, "formatNumber(row['" + v.name + "'])")		
      })

			try {
        let value = this.$calc(val)
				if(isNaN(value) || value===Number.POSITIVE_INFINITY || value===Number.NEGATIVE_INFINITY) {
					this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
				} else if(!(eval(value)===true || eval(value)===false)) {
          this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
        } else if(this.selected) {
          this.selected.expression = exp
          this.selected.formula = this.expression
          this.selected.tags = this.$copy(this.tagsField)
        }
			}
			catch(err) {
				this.errors.push({name: 'expression', message: 'Biểu thức không hợp lệ'})
      }
      return this.errors.length>0? false : true
    },

    changeType(v) {

    },

    doSelect(v) {
      this.tags.push({id: this.$id(), name: v.name, class: this.getClass(v)})
      this.tab = this.tabs.find(v=>v.code==='selected')
    },

    doSelectSpan(v) {
      this.tags.push({id: this.$id(), name: v.name, class: this.getSpanClass(v)})
      this.tab = this.tabs.find(v=>v.code==='selected')
    },

    selectButton() {

    },

    remove(i) {
      this.$delete(this.tags, i)
    },

    getClass(v) {
      let value = this.type.code + ' ' + v.code +  ' ' + this.size.code + (this.shape.code==='default'? '' : ' ' + this.shape.code)
      value += (this.outline.code==='default'? '' : ' ' + this.outline.code)
      return value
    },

    getSpanClass(v) {
      let value = 'has-text-' + v.name.toLowerCase() + ' ' + this.size.value
      return value
    }
  }
}
</script>