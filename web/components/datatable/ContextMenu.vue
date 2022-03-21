<template>
  <div class="fs14 has-text-weight-normal">
    <div>
      <a @click="checkFilter(field)? false : $emit('dosort', 'az')">
        <span class="icon is-medium fs22 mr-1" :class="checkFilter(field)? 'has-text-grey-light' : ''">
          <i class="mdi mdi-sort-alphabetical-ascending" />
        </span>
      </a>
      <a @click="checkFilter(field)? false : $emit('dosort', 'za')">
        <span class="icon is-medium fs22 mr-1" :class="checkFilter(field)? 'has-text-grey-light' : '' " >
          <i class="mdi mdi-sort-alphabetical-descending" />
        </span>
      </a>

      <a>
        <span class="icon is-medium fs22 mr-1" @click="moveLeft()">
          <i class="mdi mdi-arrow-left" />
        </span>
      </a>
          <a>
        <span class="icon is-medium fs22 mr-1" @click="moveRight()">
          <i class="mdi mdi-arrow-right"/>
        </span>
      </a>
      <a @click="hideField(field)">
        <span class="icon is-medium fs22 mr-1">
          <i class="mdi mdi-eye-off-outline"/>
        </span>
      </a>
      <a>
        <span class="icon is-medium fs22 mr-1" @click="doRemove(field)">
          <i class="mdi mdi-delete-outline"/>
        </span>
      </a>
      <a :class="field.format==='number'? null : 'has-text-grey-light'">
        <span class="icon is-medium fs20 mr-1" @click="field.format==='number'? $emit('copyfield', field) : false">
          <i class="mdi mdi-content-copy"/>
        </span>
      </a>
      <a>
        <span class="icon is-medium fs22" @click="$emit('showsidebar', {field: field, name: 'option'})">
         <i class="mdi mdi-dots-grid"/>
        </span>
      </a>
    </div>
  
  <div class="field mt-2 mb-2" v-if="field.disable? field.disable.indexOf('search') <0 : true">
    <div :class="loading? 'control is-loading' : 'control'">
      <input class="input is-rounded fs13" type="text" v-model="search" @keyup="startSearch" @keypress.enter="pressEnter"
      :placeholder="'Tìm kiếm: ' + (field.label.indexOf('<')>=0? field.name : field.label)"
      @focus="doFocus(field)" :ref="field.name">
    </div>
  </div>
  <p class="has-text-danger fs14 mt-2" v-else>
    {{field.label.indexOf(">")>=0? field.name : field.label}}
  </p>

    <p class="panel-tabs mb-2">
      <a v-for="(v,i) in getMenu(field).filter(x=>field.format==='number'? (field.formula? true : x.code!=='formula') 
        : !['filter','formula'].find(y=>y===x.code))" :key="i"
      :class="selectTab.code===v.code? 'is-active' : ''" @click="selectTab=v"> {{v.name}}
      </a>
    </p>

      <template v-if="selectTab.code==='value'">
        <a class="panel-block px-0" v-for="(row,key) in filterData.slice((current-1)*10, current*10)" 
          :key="key" @click="$emit('doselect', row[field.name])">
          {{row[field.name]? row[field.name] : 'n/a' }}
          <span class="icon has-text-primary" v-if="checkSelected(field, row[field.name])"> <i class="mdi mdi-check"/> </span>
        </a>
      </template>
      
      <template v-else-if="selectTab.code==='display'">
        <div class="field is-horizontal border-bottom pb-0 mb-1">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Màu nền </label>
              <p class="control fs14">
                <b-radio v-for="(v,i) in colorchoice" :key="i" v-model="radioBGcolor"
                  :native-value="v" @input="changeBGColor(field)">
                    {{v.name}}
                  </b-radio>
              </p>
            </div>
            <div class="field" v-if="radioBGcolor? radioBGcolor.code==='option' : false">
              <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <input type="color" v-model="bgcolor" @change="changeBGColor(field)">
              </p>
            </div>
            <div class="field" v-if="radioBGcolor? radioBGcolor.code==='condition' : false">
              <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <a class="button is-small is-primary is-outlined is-rounded" @click="doAdvance('bgcolor', field)"> Nâng cao </a> 
              </p>
            </div>
          </div>
        </div>

        <div class="field is-horizontal border-bottom pb-0 mb-1">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Màu chữ </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice" :key="i" v-model="radioColor"
                      :native-value="v" @input="changeColor(field)">
                    {{v.name}}
                  </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioColor? radioColor.code==='option' : false">
            <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
            <input type="color" v-model="color" @change="changeColor(field)">
            </p>
          </div>
          <div class="field" v-if="radioColor? radioColor.code==='condition' : false">
              <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <a class="button is-small is-primary is-outlined is-rounded" @click="doAdvance('color', field)"> Nâng cao </a> 
              </p>
            </div>
        </div>
      </div>

      <div class="field is-horizontal border-bottom pb-0 mb-1">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Cỡ chữ </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice" :key="i" v-model="radioSize"
                  :native-value="v" @input="changeSize(field)">
                  {{v.name}}
                </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioSize? radioSize.code==='option' : false">
            <label class="label fs14"> Cỡ chữ <span class="has-text-danger"> * </span> </label>
            <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="textsize" @change="changeSize(field)">
            </p>
          </div>
          <div class="field" v-if="radioSize? radioSize.code==='condition' : false">
              <label class="label fs14"> Cỡ chữ <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <a class="button is-small is-primary is-outlined is-rounded" @click="doAdvance('textsize', field)"> Nâng cao </a> 
              </p>
            </div>
        </div>
      </div>

      <div class="field is-horizontal pb-0 mb-1 border-bottom">
      <div class="field-body">
        <div class="field">
          <label class="label fs14">Vị trí text</label>
          <p class="control fs14">
            <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioAlign"
                    :native-value="v" @input="changeAlign(field)">
                  {{v.name}}
                </b-radio>
          </p>
        </div>
        <div class="field is-narrow" v-if="radioAlign? radioAlign.code==='option' : false">
          <label class="label fs14"> Chọn vị trí <span class="has-text-danger"> * </span> </label>
          <p class="control fs14">
            <b-autocomplete
              size="is-small"
              icon-right="magnify"
              :value="selectAlign? selectAlign.name : ''"
              placeholder=""
              :keep-first=true
              :open-on-focus=true
              :data="textalign"
              field="name"
              @select="option => { selectAlign = option; changeAlign(field)}">
            </b-autocomplete>
          </p>
        </div>
      </div>
    </div>

    <div class="field is-horizontal border-bottom pb-0 mb-1">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Độ rộng nhỏ nhất</label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioWidth"
                :native-value="v" @input="changeWidth(field)">
                  {{v.name}}
                </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioWidth? radioWidth.code==='option' : false">
            <label class="label fs14"> Kích thước</label>
            <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="minwidth" @change="changeWidth(field)">
            </p>
          </div>
        </div>
      </div>
      <div class="field is-horizontal border-bottom pb-0 mb-1">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Độ rộng lớn nhất</label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioMaxWidth"
                      :native-value="v" @input="changeMaxWidth(field)">
                    {{v.name}}
                  </b-radio>
            </p>
          </div>
          <div class="field" v-if="radioMaxWidth? radioMaxWidth.code==='option' : false">
            <label class="label fs14"> Kích thước</label>
            <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="maxwidth" @change="changeMaxWidth(field)">
            </p>
          </div>
        </div>
      </div>
    </template>
    <template v-if="selectTab.code==='filter'">
      <div class="field mt-4">
        <label class="label fs14">
          Chọn điều kiện<span class="has-text-danger"> * </span>
        </label>
        <div class="control fs14">
          <b-radio
          @input="setFilter(field)"
            v-for="(v, i) in filterchoice"
            :key="i"
            v-model="radioFilter"
            :native-value="v"
          >
            <span>{{ v.name }}</span>
          </b-radio>
        </div>
      </div>
      
      <div class="field">
        <label class="label fs14"
          >{{ radioFilter.code === "range" ? "Nhập cận dưới" : "Nhập giá trị" }}
          <span class="has-text-danger"> * </span>
        </label>
        <div class="control">
          <input
            class="input is-small"
            ref="firstbox"
            type="text"
            @change="setFilter(field)"
            v-model="value1"
          />
          <p
            class="help is-danger"
            v-if="errors.find((v) => v.name === 'value1')"
          >
            {{ errors.find((v) => v.name === "value1").msg }}
          </p>
        </div>
      </div>

      <div class="field" v-if="radioFilter.code === 'range'">
        <label class="label fs14">
          Nhập cận trên<span class="has-text-danger"> * </span>
        </label>
        <div class="control fs14">
          <input
            class="input is-small"
            ref="secondbox"
            type="text"
            @change="setFilter(field)"
              v-model="value2"
          />
          <p
            class="help is-danger"
            v-if="errors.find((v) => v.name === 'value2')"
          >
            {{ errors.find((v) => v.name === "value2").msg }}
          </p>
        </div>
      </div>
      <p>
      </p>
    </template>

    <template v-if="selectTab.code==='detail'">
      <p class="fs14 mt-3"> <strong> Tên trường: </strong> {{field.name}}
      <a @click="copyContent(field.name)">
        <span class="icon">
          <i class="mdi mdi-content-copy"/>
        </span>
      </a>
      </p>
      <div class="field mt-3">
        <label class="label fs14"
          >Mô tả
          <span class="has-text-danger"> * </span>
        </label>
        <div class="control">
          <input
            class="input is-small"
            type="text"
            @change="changeLabel($event.target.value, field)"
            :value="field.label"
          />
          <p
            class="help is-danger"
            v-if="errors.find((v) => v.name === 'label')"
          >
            {{ errors.find((v) => v.name === "label").msg }}
          </p>
        </div>
      </div>

      <div class="field mt-3">
        <label class="label fs14"
          >Kiểu dữ liệu
          <span class="has-text-danger"> * </span>
        </label>
        <div class="control fs14 has-text-primary">
              <b-radio v-for="(v,i) in datatype" :key="i" v-model="radioType" :native-value="v" disabled>
              {{v.name}}
            </b-radio>
        </div>
      </div>

    <div class="field" v-if="field.format==='number'">
      <label class="label"> Đơn vị <span class="has-text-danger"> * </span> </label>
      <b-autocomplete
        size="is-small"
        icon-right="magnify"
        :value="selectUnit? selectUnit.name : ''"
        placeholder=""
        :keep-first=true
        :open-on-focus=true
        :data="moneyunit"
        field="name"
        @select="option => {selectUnit = option; changeUnit(field)}">
      </b-autocomplete>
        <p class="help has-text-danger" v-if="errors.find(v=>v.name==='unit')"> {{errors.find(v=>v.name==='unit').msg}} </p>
    </div>

      <div class="field is-horizontal mt-3">
        <div class="field-body">
          <div class="field">
            <label class="label fs14">Sử dụng template </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioTemplate"
                  :native-value="v" @input="changeTemplate(undefined, field)">
                {{v.name}}
                  <a @click="copyContent(field.template)" v-if="radioTemplate? radioTemplate.code===v.code && v.code==='option': false">
                  <span class="icon">
                    <i class="mdi mdi-content-copy"/>
                  </span>
                </a>
                <a @click="$emit('showsidebar', {name: 'template', field: field})"
                v-if="radioTemplate? radioTemplate.code===v.code && v.code==='option': false">
                  <span class="icon">
                    <i class="mdi mdi-square-edit-outline"/>
                  </span>
                </a>
              </b-radio>
            </p>
          </div>
        </div>
      </div>

        <p class="mt-3" v-if="radioTemplate? radioTemplate.code==='option' : false"> 
          <textarea class="textarea fs14" placeholder="" rows="3" 
          :value="field.template" @change="changeTemplate($event.target.value, field)"></textarea>
        </p>
      </template>

      <template v-if="selectTab.code==='tooltip'">
      <p class="mt-5 fs15 has-text-dark" v-if="field.template">
        Không thể sử dụng đồng thời template và tooltip 
      </p>
      <template v-else> 
      <div class="field mt-3">
        <label class="label fs14">Sử dụng tooltip</label>
        <p class="control fs14">
          <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioTooltip"
            :native-value="v" @input="changeTooltip(field)">
            {{v.name}}
          </b-radio>
        </p>
      </div>

      <div class="field" v-if="radioTooltip? radioTooltip.code==='option' : false">
      <label class="label fs14"> Chọn trường  <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <b-autocomplete
          size="is-small"
          icon-right="magnify"
          :value="selectField? selectField.label : ''"
          placeholder=""
          :keep-first=true
          :open-on-focus=true
          :data="pagedata.fields"
          field="label"
          @select="option => {selectField = option; changeTooltip(field)}">
        </b-autocomplete>
      </p>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='tooltip')"> {{errors.find(v=>v.name==='tooltip').msg}} </p>
    </div>

      <div class="field mt-3" v-if="radioTooltip? radioTooltip.code==='option' : false">
      <label class="label fs14"> Vị trí hiển thị <span class="has-text-danger"> * </span> </label>
      <p class="control">
        <b-autocomplete
         size="is-small"
          icon-right="magnify"
          :value="selectPlacement? selectPlacement.name : ''"
          placeholder=""
          :keep-first=true
          :open-on-focus=true
          :data="placement"
          field="name"
          @select="option => {selectPlacement = option; changeTooltip(field)}">
        </b-autocomplete>
      </p>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='placement')"> {{errors.find(v=>v.name==='placement').msg}} </p>
    </div>

    <div class="field mt-3" v-if="radioTooltip? radioTooltip.code==='option' : false">
      <label class="label fs14"> Bảng màu <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <b-autocomplete
         size="is-small"
          icon-right="magnify"
          :value="selectScheme? selectScheme.name : ''"
          placeholder=""
          :keep-first=true
          :open-on-focus=true
          :data="colorscheme"
          field="name"
          @select="option => {selectScheme = option; changeTooltip(field)}">
        </b-autocomplete>
      </p>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='tooltip')"> {{errors.find(v=>v.name==='tooltip').msg}} </p>
    </div>
      </template>
    </template>

     <template v-if="selectTab.code==='formula'">
        <div class="field mt-3 px-0 mx-0">
      <label class="label fs14"> Trường để tạo công thức <span class="has-text-danger"> * </span> </label>
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
            <span :class="tags.find(v=>v.name===props.option.name)? 'has-text-primary' : ''">
              {{props.option.text}}
            </span>
          </template>
          <template slot="empty">
            Không có trường thỏa mãn
          </template>
        </b-taginput>
      </div>
      <p class="help has-text-danger" v-if="errors.find(v=>v.name==='tags')"> {{errors.find(v=>v.name==='tags').message}} </p>
    </div>
    
    <div class="field mt-3" v-if="tags.length>0">
      <p class="help is-primary">Click đúp vào để thêm vào công thức tính.</p>
      <div class="tags">
        <a @dblclick="formula = formula? (formula + ' ' + y.name) : y.name" class="tag is-rounded" 
        v-for="(y,i) in tags" :key="i">{{y.name}}</a>
      </div>
    </div>

    <div class="field mt-3 px-0 mx-0">
        <label class="label fs14">Công thức tính <span class="has-text-danger"> * </span> </label>
        <p class="control">
          <textarea class="textarea is-small" rows="4" type="text" placeholder="Tạo công thức tại đây" v-model="formula"
          @change="changeFormula(field)"
          > </textarea>
        </p>
          <p class="help has-text-danger" v-if="errors.find(v=>v.name==='formula')"> {{errors.find(v=>v.name==='formula').message}} </p>
      </div>
    </template>

    <b-pagination v-if="selectTab.code==='value' && filterData.length>10" class="mt-2 pb-3"
      :total="filterData.length"
      v-model="current"
      :range-before="1"
      :range-after="1"
      :size="'is-small'"
      :rounded="true"
      :simple="true"
      :per-page="10"
      :icon-prev="'chevron-left'"
      :icon-next="'chevron-right'"
      aria-next-label="Next page"
      aria-previous-label="Previous page"
      aria-page-label="Page"
      aria-current-label="Current page">
    </b-pagination>
  </div>
</template>

<script>


export default {
  props: ['pagename', 'field', 'filters', 'filterData', 'modal'],

  data() {
    return {
      search: undefined,
      loading: false,
      fields: [],
      current: 1,
      currentPage: 1,
      timer: undefined,
      selectTab: undefined,
      radioBGcolor: undefined,
      radioColor: undefined,
      radioSize: undefined,
      selectAlign: undefined,
      radioAlign: undefined,
      radioWidth: undefined,
      minwidth: undefined,
      color: undefined,
      bgcolor: undefined,
      textsize: undefined,
      showPage: 1,
      perPage: 30,
      radioFilter: undefined,
      value1: undefined,
      value2: undefined,
      errors: [],
      label: undefined,
      radioType: undefined,
      selectUnit: undefined,
      radioTemplate: undefined,
      currentField: undefined,
      selectPlacement: undefined,
      radioTooltip: undefined,
      selectScheme: undefined,
      selectField: undefined,
      tags: [],
      formula: undefined,
      radioMaxWidth: undefined,
      maxwidth: undefined,
      bgcolorFilter: [{id: this.$id()}],
      colorFilter: [{id: this.$id()}],
      sizeFilter: [{id: this.$id()}],
      connection: this.$connection(),
      tabs: [{code: 'expression', name: 'Biểu thức'}, {code: 'script', name: 'Mã lệnh'}],
      tab: undefined,
    }
  },
  
  created() {
    this.getFields()
    this.selectTab = this.getMenu(this.field)[0]
    this.tab = this.tabs.find(v=>v.code==='expression')
    this.radioFilter = this.filterchoice.find(v=>v.code==='bigger')
    if(this.modal) this.getDisplay(this.field)
  },
  
  watch: {
    'pagedata.fields': function(newVal) {
      newVal? this.getFields() : false
    },

    menuaction: function(newVal) {
      if(!newVal) return
      let name = newVal.field? newVal.field.name : undefined
      if(newVal.name==='display' && (name? this.field.name===name : false)) this.getDisplay(this.field)
    },

    selectTab: function(newVal) {
      if(newVal? newVal.code==='value' : false) {
        if(this.$refs[this.field.name]) this.$refs[this.field.name].focus()
      }
    }
  },

  computed: {
    pagedata: {
      get: function() {return this.$store.state[this.pagename]},
      set: function(val) {this.$store.commit('updateStore', {name: this.pagename, data: val})}
    },

    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    },

    colorchoice: {
      get: function() {return this.$store.state.colorchoice},
      set: function(val) {this.$store.commit("updateColorChoice", {colorchoice: val})}
    },

    textalign: {
      get: function() {return this.$store.state.textalign},
      set: function(val) {this.$store.commit("updateTextAlign", {textalign: val})}
    },

    filterchoice: {
      get: function () {return this.$store.state.filterchoice},
      set: function (val) {this.$store.commit("updateFilterChoice", { filterchoice: val })}
    },

    datatype: {
      get: function() {return this.$store.state.datatype},
      set: function(val) {this.$store.commit("updateDataType", {datatype: val})}
    },

    moneyunit: {
      get: function() {return this.$store.state.moneyunit},
      set: function(val) {this.$store.commit("updateMoneyUnit", {moneyunit: val})}
    },

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit("updateMenuAction", {menuaction: val})}
    },

    placement: {
      get: function() {return this.$store.state.placement},
      set: function(val) {this.$store.commit("updatePlacement", {placement: val})}
    },

    colorscheme: {
      get: function() {return this.$store.state.colorscheme},
      set: function(val) {this.$store.commit("updateColorScheme", {colorscheme: val})}
    },

    menuchoice: {
      get: function() {return this.$store.state.menuchoice},
      set: function(val) {this.$store.commit("updateMenuChoice", {menuchoice: val})}
    }
  },

  methods: {
    getMenu(field) {
      let arr = field.disable? field.disable.split(',') : undefined
      return arr? this.menuchoice.filter(v=>arr.findIndex(x=>x===v.code) <0) : this.menuchoice
    },

    getFields() {
      this.fields = this.pagedata? this.$copy(this.pagedata.fields) : []
      this.fields.map(v=>v.caption = (v.label? v.label.indexOf('<')>=0 : false)? v.name : v.label)
    },

    getDisplay(field) {
      this.current = 1
      this.currentField = this.$copy(field)
      this.value1 = undefined
      this.value2 = undefined
      this.radioType = this.datatype.find(v=>v.code===field.format)
      if(field.format==='number') this.selectUnit = this.moneyunit.find(v=>v.detail===field.unit)
      this.bgcolor = undefined
      this.radioBGcolor = this.colorchoice.find(v=>v.code==='none')
      this.color = undefined
      this.radioColor = this.colorchoice.find(v=>v.code==='none')
      this.textsize = undefined
      this.radioSize = this.colorchoice.find(v=>v.code==='none')
      this.minwidth = undefined
      this.radioWidth = this.colorchoice.find(v=>v.code==='none')
      this.radioMaxWidth = this.colorchoice.find(v=>v.code==='none')
      this.maxwidth = undefined
      this.selectAlign = undefined
      this.radioAlign = this.colorchoice.find(v=>v.code==='none')
      this.radioTemplate = this.colorchoice.find(v=>v.code=== (field.template? 'option' : 'none'))
      this.selectPlacement = this.placement.find(v=>v.code==='is-right')
      this.selectScheme = this.colorscheme.find(v=>v.code==='is-primary')
      this.radioTooltip = this.colorchoice.find(v=>v.code==='none')
      this.selectField = undefined
      this.tags = field.tags? field.tags.map(v=>this.fields.find(x=>x.name===v)) : []
      this.formula = field.formula? field.formula : undefined
      let shortmenu = this.menuchoice.filter(x=>field.format==='number'? (field.formula? true : x.code!=='formula') 
        : !['filter','formula'].find(y=>y===x.code))
      this.selectTab = shortmenu.find(v=>this.selectTab.code===v.code)? this.selectTab : this.menuchoice.find(v=>v.code==='value')
      this.radioFilter = this.filterchoice.find(v=>v.code==='bigger')
      let found = this.filters.find(v=>v.name===field.name)
      this.search = undefined
      if(found? found.filter : false) {
        this.radioFilter = this.filterchoice.find(v=>v.code===found.filter)
        this.value1 = found.value1
        this.value2 = found.value2
      }
      if(this.selectTab.code==='value') {
        let self = this
        setTimeout(function() {self.$refs[field.name]? self.$refs[field.name].focus() : false}, 50)
      }

      this.bgcolorFilter = [{id: this.$id()}]
      if(field.bgcolor) {
        if(Array.isArray(field.bgcolor)) {
          this.radioBGcolor = this.colorchoice.find(v=>v.code==='condition')
          this.bgcolorFilter = this.$copy(field.bgcolor)
        } else {
          this.radioBGcolor = this.colorchoice.find(v=>v.code==='option')
          this.bgcolor = field.bgcolor 
        }
      }

       this.colorFilter = [{id: this.$id()}]
      if(field.color) {
        if(Array.isArray(field.color)) {
          this.radioColor = this.colorchoice.find(v=>v.code==='condition')
          this.colorFilter = this.$copy(field.color)
        } else {
          this.radioColor = this.colorchoice.find(v=>v.code==='option')
          this.color = field.color
        }
      }
      
      this.sizeFilter = [{id: this.$id()}]
      if(field.textsize) {
        if(Array.isArray(field.textsize)) {
          this.radioSize = this.colorchoice.find(v=>v.code==='condition')
          this.sizeFilter = field.textsize
        } else {
          this.radioSize = this.colorchoice.find(v=>v.code==='option')
          this.textsize = field.textsize
        }
      }

      if(field.textalign) {
        this.radioAlign = this.colorchoice.find(v=>v.code==='option')
        this.selectAlign = this.textalign.find(v=>v.code===field.textalign)
      }
      
      if(field.minwidth) {
        this.radioWidth = this.colorchoice.find(v=>v.code==='option')
        this.minwidth = field.minwidth
      }

      if(field.maxwidth) {
        this.radioMaxWidth = this.colorchoice.find(v=>v.code==='option')
        this.maxwidth = field.maxwidth
      }

      if(field.tooltip) {
        this.radioTooltip = this.colorchoice.find(v=>v.code==='option')
        this.selectPlacement = this.placement.find(v=>v.code===field.tooltip.placement)
        this.selectField = this.pagedata.fields.find(v=>v.name===field.tooltip.field)
        this.selectScheme = this.colorscheme.find(v=>v.code===field.tooltip.type)
      }
    },

    moveLeft() {
      let i = this.pagedata.fields.findIndex(v=>v.name===this.field.name)
      let copy = this.$copy(this.pagedata.fields)
      let idx = i-1>=0? i - 1 : copy.length - 1
      copy = this.$arrayMove(copy, i, idx)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    moveRight() {
      let i = this.pagedata.fields.findIndex(v=>v.name===this.field.name)
      let copy = this.$copy(this.pagedata.fields)
      let idx = copy.length-1>i? i + 1 : 0
      copy = this.$arrayMove(copy, i, idx)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    doRemove(field) {
      let copy = this.$copy(this.pagedata.fields)
      let idx = copy.findIndex(v=>v.name===field.name)
      this.$delete(copy, idx)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    startSearch(event) {
      if (this.timer) clearTimeout(this.timer)
      let self = this
      this.timer = setTimeout(() => { self.$emit('dosearch', event.srcElement.value) }, 100)
    },

    pressEnter(event) {
      if(!this.$empty(event.srcElement.value) && this.filterData.length>0) this.$emit('doselect', this.filterData[0][this.field.name])
    },

    changeColor(field) {
      let copy = this.$copy(field)
      copy.color = this.radioColor.code==='none'? undefined : this.color
      this.updateFields(copy)
    },

    changeBGColor(field) {
      let copy = this.$copy(field)
      copy.bgcolor = this.radioBGcolor.code==='none'? undefined : this.bgcolor
      this.updateFields(copy)
    },

    checkSelected(field, value) {
      let found = this.filters.find(v=>v.name===field.name)
      let val = undefined
      !found? val = false
      : val = (found.select? found.select.find(x=>x===value) : false)
      return val
    },

    doAdvance(name, field) {
      let script = (field[name]? Array.isArray(field[name]) : false)? JSON.stringify(field[name]) : undefined
      this.$emit('showsidebar', {field: field, name: name, script: script, 
      radio: name==='bgcolor'? this.radioBGcolor : (name==='color'? this.radioColor : this.radioSize) })
    },

    changeSize(field) {
      let copy = this.$copy(field)
      if(this.radioSize.code==='option' && !this.$isNumber(this.textsize)) return
      copy.textsize = this.radioSize.code==='none'? undefined : this.textsize
      this.updateFields(copy)
    },

    changeAlign(field) {
      let copy = this.$copy(field)
      copy.textalign = this.radioAlign.code==='none'? undefined : (this.selectAlign? this.selectAlign.code : undefined)
      this.updateFields(copy)
    },

    changeWidth(field) {
      let copy = this.$copy(field)
      if(!this.$isNumber(this.minwidth)) return
      copy.minwidth = this.radioWidth.code==='none'? undefined : this.minwidth
      this.updateFields(copy)
    },

    changeMaxWidth(field) {
      let copy = this.$copy(field)
      if(!this.$isNumber(this.maxwidth)) return
      copy.maxwidth = this.radioMaxWidth.code==='none'? undefined : this.maxwidth
      this.updateFields(copy)
    },

    setFilter(field) {
      if (!this.checkValid()) return
      let filter = {name: field.name, label: field.label, filter: this.radioFilter.code, value1: this.$formatNumber(this.value1)}
      if(this.radioFilter.code==='range') filter.value2 = this.$formatNumber(this.value2)
      this.$emit('setfilter', filter)
    },

    copyContent(value) {
      this.$copyToClipboard(value)
    },

    changeLabel(value, field) {
      if(this.$empty(value)) return
      let copy = this.$copy(field)
      copy.label = value
      this.updateFields(copy)
    },

    changeUnit(field) {
      if(this.$empty(this.selectUnit)) return
      let copy = this.$copy(field)
      copy.unit = this.selectUnit.detail
      this.updateFields(copy)
      this.menuaction = {name: 'reload-data', time: new Date()}
    },

    changeTemplate(value, field) {
      if(this.radioTemplate.code==='none') value = undefined
      else if(this.$empty(value)) return
      let copy = this.$copy(field)
      copy.template = value
      this.updateFields(copy)
    },

    checkFilter(field) {
      if(!this.pagedata) return
      let found = this.pagedata.filters? this.pagedata.filters.find(v=>v.name===field.name) : undefined
      return found? (found.select || found.filter) : false
    },

    changeTooltip(field) {
      let copy = this.$copy(field)
      if(this.radioTooltip? this.radioTooltip.code==='none' : false) copy.tooltip = undefined
      else if(!(this.selectField && this.selectPlacement && this.selectScheme)) return
      else {copy.tooltip = {field: this.selectField.name, placement: this.selectPlacement.code, type: this.selectScheme.code}}
      this.updateFields(copy)
    },

    changeFormula(field) {
      //check formula
      this.errors = []
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
      if(this.errors.length>0) return
      let copyField = this.$copy(field)
      copyField.formula = this.formula.trim()
      copyField.tags = this.tags.map(v=>v.name)
      copyField.level = Math.max(...this.tags.map(v=>v.level? v.level : 0)) + 1
      this.updateFields(copyField)
      this.$calculateFields(this.pagename)
    },

    updateFields(field) {
      let copy = this.$copy(this.pagedata.fields)
      let idx = copy.findIndex(v=>v.name===field.name)
      copy[idx] = field
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    doFocus() {
      if(this.selectTab.code!=='value') this.selectTab = this.menuchoice.find(v=>v.code==='value')
    },

    hideField(field) {
      let copy = this.$copy(this.pagedata.fields)
      let found = copy.find(v=>v.name===field.name)
      found.show = false
      this.$store.commit('updateState', {name: this.pagename, key: 'fields', data: copy})
    },

    checkValid() {
      this.errors = [];
      if (this.$isNumber(this.value1))
        this.value1 = this.$numtoString(this.value1);
      else
        this.errors.push({
          name: "value1",
          msg: "Giá trị phải là số",
        });

      if (this.radioFilter.code === "range") {
        if (this.$isNumber(this.value2))
          this.value2 = this.$numtoString(this.value2);
        else
          this.errors.push({
            name: "value2",
            msg: "Giá trị phải là số",
          });
      }
      return this.errors.length>0? false : true
    }
  }
}
</script>