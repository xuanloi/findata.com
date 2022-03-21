<template>
  <div>
    <section class="hero" v-if="pagedata? (pagedata.showFilter && filters.length>0) : false">
      <div class="hero-body pt-0 pb-2">
        <div class="columns">
          <div class="column is-11">
            <div class="field is-grouped is-grouped-multiline" v-if="filters? filters.length>0 : false">
                <div class="control mr-5">
                <div class="tags has-addons is-marginless">
                  <span class="icon has-text-danger fb500"> <i class="mdi mdi-sigma fb500"> </i> 
                  {{pagedata.api? (pagedata.api.full_data? data.length : pagedata.api.total_rows) : 0}} </span>
                </div>
                 <p class="help">
                  <a class="has-text-danger" @click="filters=[]; doFilter([])"> Bỏ lọc </a>
               </p>
              </div>

              <div class="control" v-for="(v,i) in filters" :key="i">
                <div class="tags has-addons is-marginless">
                  <span class="tag is-light is-marginless has-text-black-bis">{{v.label.indexOf('>')>=0? $stripHtml(v.label,30) : v.label}}</span>
                  <a class="tag is-delete is-marginless has-text-black-bis" @click="removeFilter(i)"></a>
                </div>
                <span class="help has-text-black-bis">
                  {{v.sort? v.sort : (v.select? ('[' + (v.select.length>0? v.select[0] : '') + '...&#931;' + v.select.length + ']') :
                  (v.filter==='less'? '&#60; ' + v.value1 : (v.filter==='bigger'? '> ' + v.value1 : '[' + v.value1 + ',' + v.value2 + ']')))}}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  <div class="table-container" :style="getSettingStyle('container')" ref="container">
  <table class="table is-bordered is-narrow is-hoverable" ref="table"
  :style="getSettingStyle('table')"
  >
  <thead>
    <tr>
    <th v-for="(field,i) in fields.filter(v=>v.show)" :key="i" :ref="'th' + field.name"
    :style="getSettingStyle('header', field)">
     <div v-if="field.name==='action'">
        <b-checkbox
          class="mx-0 px-0 fs14"
          v-model="selectall"
          v-if="field.action.indexOf('select')>=0"
        ></b-checkbox>
        <a @click="doAction('insert')" v-if="field.action.indexOf('insert')>=0">
          <span class="icon">
            <i class="mdi mdi-plus fs24" />
          </span>
        </a>
     </div>
    <div v-else-if="field.menu==='no' || (tablesetting.find(v=>v.code==='show-menu')? tablesetting.find(v=>v.code==='show-menu').detail==='no' : false)"
    :style="getSettingStyle('dropdown', field)"> 
      <template v-if="field.label.indexOf('<')<0"> {{field.label}} </template>
      <component v-bind="{row: field}" v-if="field.label" 
        :is="compiledComponent(field.label)" @clickevent="doAction($event, field)"
     />
    </div>

    <div class="dropdown is-hoverable" :class="menuPos" style="width:100%; cursor:pointer;" v-else @mouseenter="showContextMenu(field)">
      <div class="dropdown-trigger">
      <div style="background-color:transparent" :style="getSettingStyle('dropdown', field)">
        <span v-if="field.label.indexOf('<')<0"> {{field.label}}
          <i class="mdi mdi-chevron-down fs16" aria-hidden="true" v-if="tablesetting.find(v=>v.code==='header-arrow').detail==='yes'"></i>
        </span>
      <component v-bind="{row: field}" v-else 
        :is="compiledComponent(field.label)" @clickevent="doAction($event, field)"
     />
    </div>
    </div>

    <div class="dropdown-menu" :style="getSettingStyle('menu', field)" v-if="!ismobile"  style="background-color:#d3d3d3">
      <ContextMenu class="px-2" v-bind="{pagename: 'pagedata', field: field, filters: filters, filterData: filterData}"
        @dosearch="doSearch(field, $event)" @doselect="doSelect(field, $event)" @dosort="doSort(field, $event)" @setfilter="setFilter(field, $event)" 
        @showsidebar="showSidebar($event)" @copyfield="copyField" />
      </div>
      </div>
    </th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(v,i) in data.filter((ele,index) => (index>=(showPage-1)*perPage && index<showPage*perPage))" :key="i">
      <td v-for="(field, j) in fields.filter(v=>v.show)" :key="j" :ref="'cell' + i + j" 
        :style="getStyle(field, v, 'cell' + i + j)"
      >
      <div class="field has-addons" v-if="field.name==='action'">
      <p class="control" v-if="field.action.indexOf('select')>=0">
        <b-checkbox class="mx-0 px-0 fs14"
          type="is-primary"
        ></b-checkbox>
      </p>
      <p class="control" v-if="field.action.indexOf('open')>=0">
        <a @click="doAction('open', v)">
          <span class="icon">
            <i class="mdi mdi-open-in-new fs22" />
          </span>
        </a>
      </p>
      <p class="control" v-if="field.action.indexOf('edit')>=0">
        <a @click="doAction('edit', v)" class="ml-2">
          <span class="icon">
            <i class="mdi mdi-square-edit-outline fs22" />
          </span>
        </a>
      </p>
       <p class="control" v-if="field.action.indexOf('delete')>=0">
        <a @click="doAction('delete', v)" class="ml-2">
          <span class="icon has-text-danger">
            <i class="mdi mdi-delete-outline fs22" />
          </span>
        </a>
      </p>
    </div>
        <component v-bind="{row: v, field: field}" v-else-if="field.template" 
          :is="compiledComponent(field.template)" @clickevent="doAction($event, v, field)"
        />
        <template v-else-if="field.tooltip">
          <b-tooltip :label="v[field.tooltip.field]"
            :position="field.tooltip.placement"
            :type="field.tooltip.type">
          {{v[field.name]}}
            </b-tooltip>
          </template>
          <template v-else> {{v[field.name]}} </template>
        </td>
      </tr>
    </tbody>
  </table>

    <div
      class="mt-3 px-3"
      v-if="pagedata.pagination!==false && (pagedata.api.full_data? data.length>perPage :  pagedata.api.total_rows > perPage)"
    >
      <b-pagination
        :total="pagedata.api.full_data? data.length : pagedata.api.total_rows"
        :current.sync="currentPage"
        :order="'is-centered'"
        :rounded="true"
        :per-page="perPage"
      >
      </b-pagination>
    </div>
    </div>
    <div class="mt-5 py-2 px-6 has-text-white fs14 has-background-warning-dark"
    v-if="tablesetting.find(v=>v.code==='note')? tablesetting.find(v=>v.code==='note').detail !== '@' : false">
    {{tablesetting.find(v=>v.code==='note').detail}}
    </div>
  
    <section>
      <b-sidebar v-if="openSidebar"
      type="has-sidebar-color"
        :fullheight="true"
        :fullwidth="ismobile? true : false"
        :overlay="false"
        :right="true"
        v-model="openSidebar"
      >
        <div class="field is-grouped mb-1" style="border-bottom: 1px solid white;">
    <div class="control is-expanded">
      <strong class="ml-4">Bảng điều khiển tham số</strong>
    </div>
    <p class="control">
      <a class="icon mr-2 has-text-dark" @click="openSidebar=false"><i class="mdi mdi-close-thick fs22"></i></a>
      </p>
    </div>
    <div class="field is-horizontal mb-0">
      <div class="field-body">
      <div class="field">
        <div class="tabs" v-if="['bgcolor', 'color', 'textsize'].find(x=>x===sideBar)">
          <ul> <li v-for="(v,i) in tabs" :key="i" :class="tab.code===v.code? 'is-active' : ''" @click="tab=v">
            <a>{{v.name}}</a></li> </ul>
          </div>
        </div>
        </div>
      </div>

      <template v-if="tab.code==='expression' && ['bgcolor', 'color', 'textsize'].find(x=>x===sideBar)">
      <template v-if="radio? (radio.code==='condition' && sideBar==='bgcolor') : false">
      <div v-for="(v,i) in bgcolorFilter" :key="v.id" class="px-4">
        <FilterOption v-bind="{filterObj: v, filterType: 'color', pagename: pagename, field: openField}" :ref="v.id" 
        @databack="doConditionFilter($event, 'bgcolor', v.id)" /> 
        <p class="fs14 mt-1" :class="currentField.format==='string'? 'mb-1' : 'mb-2'"> 
          <a class="has-text-primary mr-5" @click="addCondition(bgcolorFilter)" v-if="bgcolorFilter.length<=30"> Thêm </a>
          <a class="has-text-danger" @click="removeCondition(bgcolorFilter, i)" v-if="bgcolorFilter.length>1"> Bớt </a>
        </p>
      </div>
    </template>

      <template v-else-if="radio? (radio.code==='condition' && sideBar==='color') : false">
      <div v-for="(v,i) in colorFilter" :key="v.id" class="px-4">
        <FilterOption v-bind="{filterObj: v, filterType: 'color', pagename: pagename, field: openField}" :ref="v.id" 
        @databack="doConditionFilter($event, 'color', v.id)"/> 
        <p class="fs14 mt-1" :class="currentField.format==='string'? 'mb-1' : 'mb-2'"> 
          <a class="has-text-primary mr-5" @click="addCondition(colorFilter)" v-if="colorFilter.length<=30"> Thêm </a>
          <a class="has-text-danger" @click="removeCondition(colorFilter,i)" v-if="colorFilter.length>1"> Bớt </a>
        </p>
      </div>
    </template>

    <template v-else-if="radio? (radio.code==='condition' && sideBar==='textsize') : false">
    <div v-for="(v, i) in sizeFilter" :key="v.id" class="px-4">
      <FilterOption v-bind="{filterObj: v, filterType: 'size', pagename: pagename, field: openField}" :ref="v.id" 
      @databack="doConditionFilter($event, 'textsize', v.id)"/> 
      <p class="fs14 mt-1" :class="currentField.format==='string'? 'mb-1' : 'mb-2'"> 
        <a class="has-text-primary mr-5" @click="addCondition(sizeFilter)" v-if="sizeFilter.length<=30"> Thêm </a>
        <a class="has-text-danger" @click="removeCondition(sizeFilter, i)" v-if="sizeFilter.length>1"> Bớt </a>
      </p>
    </div>
    </template>
    </template>

    <template v-else-if="tab.code==='script' && ['bgcolor', 'color', 'textsize'].find(x=>x===sideBar)">
      <p class="my-3 mx-4">
      <a @click="copyContent(script? script : '')" class="mr-6">
          <span class="icon fs20">
            <i class="mdi mdi-content-copy"/>
          </span>
          copy
        </a>
        <a @click="changeScript()">
          <span class="icon fs20">
            <i class="mdi mdi-update"/>
          </span>
          Cập nhật
        </a>
      </p>
      <div class="mx-4">
        <textarea class="textarea fs14" rows="15" v-model="script" @change="checkScript()"> </textarea>
      </div>
    </template>
    <TableOption v-bind="{pagename: pagename}" v-else-if="sideBar==='option'"> </TableOption>
    <CreateTemplate v-else-if="sideBar==='template'" v-bind="{pagename: pagename, field: openField}"> </CreateTemplate>
    </b-sidebar>
  </section>

  <div class="modal is-active" v-if="openModal">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:25%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="openModal=false"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <ContextMenu class="px-3" v-bind="{pagename: 'pagedata', field: currentField, filters: filters, filterData: filterData, modal: openModal}"
      @dosearch="doSearch(currentField, $event)" @doselect="doSelect(currentField, $event)" @dosort="doSort(currentField, $event)" 
      @setfilter="setFilter(currentField, $event)" @showsidebar="showSidebar($event)" />
    </section>
    </div>
  </div>
  </div>
</template>

<script>
import Vue from 'vue'

import ContextMenu from "@/components/datatable/ContextMenu"
import FilterOption from "@/components/datatable/FilterOption"
import TableOption from "@/components/datatable/TableOption"
import CreateTemplate from "@/components/datatable/CreateTemplate"

export default {
  components: {
    ContextMenu,
    FilterOption,
    TableOption,
    CreateTemplate,
  },

  props: ['pagename'],
  
  data() {
    return {
      data: [],
      fields: [],
      search: '',
      filters: [],
      current: 1,
      currentPage: 1,
      filterData: [],
      timer: undefined,
      showPage: 1,
      perPage: 30,
      currentField: undefined,
      rectTB: undefined,
      menuPos: 'is-left',
      connection: this.$connection(),
      flagSearch: false,
      resetPage: false,
      selectall: undefined,
      openModal: false,
      script: undefined,
      openSidebar: false,
      sideBar: undefined,
      tabs: [{code: 'expression', name: 'Biểu thức'}, {code: 'script', name: 'Mã lệnh'}],
      tab: undefined,
      radio: undefined,
      bgcolorFilter: [{id: this.$id()}],
      colorFilter: [{id: this.$id()}],
      sizeFilter: [{id: this.$id()}],
      scrollbar: undefined
    }
  },

  created() {
    if(this.pagedata.data) this.data = this.$copy(this.pagedata.data)
    if(this.pagedata.fields) this.fields = this.$copy(this.pagedata.fields)
    this.perPage = this.pagedata.perPage? this.pagedata.perPage : this.$formatNumber(this.tablesetting.find(v=>v.code==='per-page').detail)
      
  },

  mounted() {
    if(this.$refs['container']) this.rectTB = this.$refs['container'].getBoundingClientRect()
    this.scrollbarVisible()
  },

  watch: {
    'pagedata.data': function(newVal) {
      this.data = this.$copy(newVal)
      if(this.currentField) this.filterData = this.$unique(newVal, [this.currentField.name])
      this.$emit('changedata', newVal)
      let self = this
      setTimeout(function(){self.scrollbarVisible()}, 100) 
    },

    'pagedata.fields': function(newVal) {
      this.fields = this.$copy(newVal)
      this.$emit('changefield', newVal)
      let self = this
      setTimeout(function(){self.scrollbarVisible()}, 100) 
    },

    'pagedata.filterby': function(newVal) {
      this.filters = this.$copy(newVal)
      this.doFilter(this.filters)
    },

    currentPage: function(newVal) {
      if(this.resetPage) {
        this.resetPage = false
        return
      }
      window.scroll({top: this.$refs["table"].offsetTop - 80, left: 0, behavior: "smooth"})
      if (this.pagedata.api.full_data) {
        this.showPage = newVal
        return;
      }

      this.showPage = 1
      let copy = this.$copy(this.pagedata.api)
      copy.params.page = newVal
      this.connection.getApi([copy])
    },

    tablesetting: function(newVal) {
      this.perPage = this.$formatNumber(this.tablesetting.find(v=>v.code==='per-page').detail)
    },

    "connection.getdataReady": function(newVal) {
      if (newVal === "success") {
        if(this.flagSearch) {
          this.flagSearch = false
          var rows =  this.connection.getbatchData[0].data
          if(this.currentField) this.filterData = this.$unique(rows, [this.currentField.name])
          return
        }
        this.$store.commit("updateState", {name: this.pagename, key: "data", data: this.$copy(this.connection.getbatchData[0].data)})
        this.$store.commit("updateState", {name: this.pagename, key: "api", data: this.$copy(this.connection.getbatchStatus[0])})
      }
    },

    menuaction: function(newVal) {
      if(this.$empty(newVal)) return
      if(newVal.name==='export-excel' && (newVal.pagename? newVal.pagename===this.pagename : true)) {
        let fields = this.fields.map(v=>v.name)
        let dataType = {}
        this.fields.map(v=>dataType[v.label.indexOf('>')>=0? v.name : v.label] = 'String')
        this.$exportExcel(this.data, this.menuaction.file, fields, dataType)
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

    menuaction: {
      get: function() {return this.$store.state.menuaction},
      set: function(val) {this.$store.commit("updateMenuAction", {menuaction: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", { ismobile: val })}
    },

    colorchoice: {
      get: function() {return this.$store.state.colorchoice},
      set: function(val) {this.$store.commit("updateColorChoice", {colorchoice: val})}
    }
  },

  methods: {
    compiledComponent(value) {
      return {
      	template: `${value}`,
        props: ['row', 'field'],
        methods: {
          formatNumber(val) {
            return this.$formatNumber(val)
          },
          compare(a, b) {
            let c = this.$formatNumber(a)
            let d = this.$formatNumber(b)
            if(!c || !d) return  'invalid'
            return c>d? 1 : (c<d? -1 : 0)
          }
        }
      }
    },

    showContextMenu(field) {
      if(this.ismobile) this.openModal = true
      this.tab = this.tabs.find(v=>v.code==='expression')
      this.currentField = field
      this.filterData = this.$unique(this.data, [field.name])
      let doc = this.$refs['th' + field.name][0]
      let rectTH = doc? doc.getBoundingClientRect() : undefined
      this.menuPos = (doc? this.rectTB.width - rectTH.left>320 : false)? 'is-left' : 'is-right'
      this.menuaction = {name: 'display', key: this.$id(), field: field}
    },

    copyContent(value) {
      this.$copyToClipboard(value)
    },

    addCondition(arr) {
      arr.push({id: this.$id()})
    },

    removeCondition(arr, i) {
      this.$delete(arr, i)
    },

    doConditionFilter(v, type, id) {
       v.id = id
       let copy = this.$copy(this.currentField)
      if(copy[type]? Array.isArray(copy[type]) : false) {
        let idx = copy[type].findIndex(x=>x.id===id)
        idx>=0? Vue.set(copy[type], idx, v) : copy[type].push(v)
      }
      else copy[type] = [v]
      this.currentField = copy
      this.updateFields(copy)
    },

    checkScript() {
      if(this.$empty(this.script)) return
      try {
        JSON.parse(this.script)
      } catch (e) {
          return false;
      }
      return true;
    },

    changeScript() {
      if(!this.checkScript()) return
      let copy = this.$copy(this.openField)
      copy[this.sideBar] = JSON.parse(this.script)
      this.updateFields(copy)
    },

    showSidebar(event) {
      this.openField = event.field
      this.sideBar = event.name
      this.script = event.script
      this.radio = event.radio
      let field = event.field
      this.bgcolorFilter = [{id: this.$id()}]
      if(field.bgcolor) {
        if(Array.isArray(field.bgcolor)) this.bgcolorFilter = this.$copy(field.bgcolor)
      }

      this.colorFilter = [{id: this.$id()}]
      if(field.color) {
        if(Array.isArray(field.color)) this.colorFilter = this.$copy(field.color)
      }
      
      this.sizeFilter = [{id: this.$id()}]
      if(field.textsize) {
        if(Array.isArray(field.textsize)) this.sizeFilter = field.textsize
      }
      this.openSidebar = true
      if(this.ismobile) this.openModal = false
    },

    getStyle(field, record, cell) {      
      var live = record.livedata? record.livedata.find(x=>x[field.name]===this.pagedata.batch) : false
      var live_bgcolor = undefined
      var live_color = undefined
      var stop = false
      let val = this.tablesetting.find(v=>v.code==='td-border')? this.tablesetting.find(v=>v.code==='td-border').detail 
      : 'border: solid 1px rgb(44, 44, 44);'
      if(field.bgcolor? !Array.isArray(field.bgcolor) : false) {
        val += 'background-color: ' + field.bgcolor + '; '
      } else if(field.bgcolor? Array.isArray(field.bgcolor) : false) {
        field.bgcolor.map(v=>{
          if(v.type==='search') {
            if(record[field.name] && !stop? record[field.name].toLowerCase().indexOf(v.keyword.toLowerCase())>=0 : false) {
              val += 'background-color: ' + v.color + '; '
              stop = true
              live_bgcolor = 'background-color: ' + v.color + '; '
            }
          } else {
            let res = this.$calculate(record, v.tags, v.expression)
            if(res.success && res.value && !stop) {
              val += 'background-color: ' + v.color + '; '
              stop = true
              live_bgcolor = 'background-color: ' + v.color + '; '
            }
          }
        })
      }
      
      stop = false
      if(field.color? !Array.isArray(field.color) : false) {
        val += 'color: ' + field.color + '; '
      } else if(field.color? Array.isArray(field.color) : false) {
        field.color.map(v=>{
          if(v.type==='search') {
            if(record[field.name] && !stop? record[field.name].toLowerCase().indexOf(v.keyword.toLowerCase())>=0 : false) {
              val += 'color: ' + v.color + '; '
              stop = true
              live_color = 'color: ' + v.color + '; '
            }
          } else {
            let res = this.$calculate(record, v.tags, v.expression)
            if(res.success && res.value && !stop) {
              val += 'color: ' + v.color + '; '
              stop = true
              live_color = 'color: ' + v.color + '; '
            }
          }
        })
      }

      stop = false
      if(field.textsize? !Array.isArray(field.textsize) : false) {
        val += 'font-size: ' + field.textsize + 'px; '
      } else if(field.textsize? Array.isArray(field.textsize) : false) {
        field.textsize.map(v=>{
           if(v.type==='search') {
            if(record[field.name] && !stop? record[field.name].toLowerCase().indexOf(v.keyword.toLowerCase())>=0 : false) {
              val += 'font-size: ' + v.size + 'px; '
              stop = true
            }
          } 
          else {
            let res = this.$calculate(record, v.tags, v.expression)
            if(res.success && res.value && !stop) {
                val += 'font-size: ' + v.size + 'px; '
                stop = true
              }
            }
        })
      } else val += this.tablesetting.find(v=>v.code==='table-font-size').detail + ';'

      if(field.textalign) val += 'text-align: ' + field.textalign + '; '
      if(field.minwidth) val += ' min-width: ' + field.minwidth + 'px; '
      if(field.maxwidth) val += ' max-width: ' + field.maxwidth + 'px; '
      if(!live) return val

       var _style = live_bgcolor? val.replace(live_bgcolor, live.bgcolor) : val + live.bgcolor
      _style =  live_color? _style.replace(live_color, ' color: white !important;') : _style + ' color: white !important;'
      setTimeout(() => {
        this.$refs[cell][0].style = val
      }, 1500)
     
      return _style
    },

    getSettingStyle(name, field) {
      let value = ''
      if(name==='container') {
        value = 'min-height:' + this.tablesetting.find(v=>v.code==='container-height').detail + 'rem; '
      } else if(name==='table') {
        value += 'background-color:' + this.tablesetting.find(v=>v.code==='table-background').detail + '; '
        value += 'font-size:' + this.tablesetting.find(v=>v.code==='table-font-size').detail + 'px;'
        value += 'color:' + this.tablesetting.find(v=>v.code==='table-font-color').detail + '; '
      } else if(name==='header') {
        value += 'background-color:' + this.tablesetting.find(v=>v.code==='header-background').detail + '; '
        if(field.minwidth) value += ' min-width: ' + field.minwidth + 'px; '
        if(field.maxwidth) value += ' max-width: ' + field.maxwidth + 'px; '
      } else if(name==='menu') {
        let arg = this.tablesetting.find(v=>v.code==='menu-width').detail
        arg = field? (field.menuwidth? field.menuwidth : arg) : arg
        value += 'width:'  + arg + 'rem; '
        value += 'min-height:'  + this.tablesetting.find(v=>v.code==='menu-min-height').detail + 'rem; '
        value += 'max-height:'  + this.tablesetting.find(v=>v.code==='menu-max-height').detail + 'rem; '
        value += "overflow:auto; "
      }  else if(name==='dropdown') {
        value += 'font-size:' + this.tablesetting.find(v=>v.code==='header-font-size').detail + 'px; '
        let found = this.filters.find(v=>v.name===field.name)
        found? value += 'color:' + this.tablesetting.find(v=>v.code==='header-filter-color').detail + '; '
        :value += 'color:' + this.tablesetting.find(v=>v.code==='header-font-color').detail + '; '
      }
      return value
    },

    removeFilter(i) {
      this.$delete(this.filters, i)
      this.doFilter(this.filters)
    },

    updateFields(field) {
      let copy = this.$copy(this.pagedata.fields)
      let idx = copy.findIndex(v=>v.name===field.name)
      Vue.set(copy, idx, field)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
    },

    doAction(event, row, field) {
      let name = typeof event === "string"? event : event.name
      let data =  typeof event === "string"? event : event.data
      this.$store.commit('updateState', {name: this.pagename, key: 'action', data: {event: name, row: row, field: field, data: data, time: new Date()}})
      this.$emit(name, row, field, data)
    },

    doSort(field, type) {
      let filter = {name: field.name, label: field.label, sort: type, format: field.format}
      let idx = this.filters.findIndex(v=>v.name===field.name)
      if(idx>=0) Vue.set(this.filters, idx, filter)
      else this.filters.push(filter)
      this.doFilter(this.filters)
    },

    doSearch(field, search) {
      let copy = this.$copy(this.filters)
      let idx = copy.findIndex(v=>v.name===field.name)
      if(idx>=0) this.$delete(copy, idx)

      if(this.pagedata.origin_api.full_data) {
        let data = this.frontendFilter(copy)
        let rows = this.$empty(search)? data
        : data.filter(v=>v[field.name]? v[field.name].toString().toLowerCase().indexOf(search.toLowerCase())>=0 : false)
        this.filterData = this.$unique(rows, [field.name])
      } else {
        copy.push({name: field.name, label: field.label, search: search.toLowerCase(), format: field.format})
        this.flagSearch = true
        this.backendFilter(copy)
      }
    },

    doSelect(field, value) {
      let found = this.filters.find(v=>v.name===field.name)
      if(found) {
        !found.select? found.select = [] : false
        let idx = found.select.findIndex(x=>x===value)
        idx>=0? this.$delete(found.select, idx) : found.select.push(value)
        if(found.select.length===0) {
          idx = this.filters.findIndex(v=>v.name===field.name)
          if(idx>=0) this.$delete(this.filters, idx)
        }
      } else {
        this.filters.push({name: field.name, label: field.label, select: [value], format: field.format})
      }
      this.doFilter(this.filters)
    },

    setFilter(field, filter) {  
      let idx = this.filters.findIndex(v=>v.name===field.name)
      if(idx<0) this.filters.push(filter)
      else Vue.set(this.filters, idx, filter)
      this.doFilter(this.filters)
    },

    doFilter(newVal) {
      if(this.currentPage>1) {
        this.resetPage = true
        this.currentPage = 1
        this.showPage = 1
      }
      if (this.pagedata.origin_api.full_data) {
        this.data = this.frontendFilter(newVal);
        this.$store.commit("updateState", {name: this.pagename, key: "dataFilter", data: this.$copy(this.data)})
        this.$emit('changedata', newVal)
      }
      else {
        if (this.timer) clearTimeout(this.timer)
        this.timer = setTimeout(() => {
          this.backendFilter(newVal)
        }, 200)
      }
      this.$store.commit("updateState", {name: this.pagename, key: "filters", data: this.$copy(newVal)})
      this.$emit('changefilter', newVal? newVal.length>0 : false)
    },

    frontendFilter(newVal) {
      newVal = this.$copy(newVal)
      var data = this.$copy(this.pagedata.data)
      newVal.filter(m=>m.select || m.filter).map(v => {
        if(v.select) {
          data = data.filter(x => v.select.findIndex(y => this.$empty(y)? this.$empty(x[v.name]) : (y===x[v.name])) >-1)
        } else if(v.filter==='less') {
          data = data.filter(x =>
          this.$empty(x[v.name])? false
          : this.$formatNumber(x[v.name]) < this.$formatNumber(v.value1))
        } else if(v.filter==='bigger') {
          data = data.filter(x =>
          this.$empty(x[v.name])? false
          : this.$formatNumber(x[v.name]) > this.$formatNumber(v.value1))
        } else if(v.filter==='range') {
          data = data.filter(x =>
          this.$empty(x[v.name])? false
          : this.$formatNumber(x[v.name]) >= this.$formatNumber(v.value1)
          && this.$formatNumber(x[v.name]) <= this.$formatNumber(v.value2)) 
        }
      })

      let sort = {},
      format = {};
      let list = this.filters.filter(x=>x.sort)
      list.map(v=>{
        sort[v.name] = v.sort === "az" ? "asc" : "desc"
        format[v.name] = v.format;
      })
      return list.length>0?  this.$multiSort(data, sort, format) : data 
    },

    // Sử dụng backend filter
    backendFilter(newVal) {
      let params = this.pagedata.origin_api.params? this.$copy(this.pagedata.origin_api.params) : {};
      var where = params.filter? params.filter : {}
      var sort = []
      var filter = newVal.filter(v=>!v.formula)
        
      if (this.pagedata.origin_api.url.indexOf("data/") >= 0) {
        filter.forEach(v => {
          if(v.search) where[v.name + "__icontains"] = v.search
          else if (v.select) where[v.name + "__in"] = v.select
          else if (v.filter === "less")
            where[v.name + "__lt"] = this.$formatNumber(v.value1)
          else if (v.filter === "bigger")
            where[v.name + "__gt"] = this.$formatNumber(v.value1)
          else if (v.filter === "range") {
            where[v.name + "__gte"] = this.$formatNumber(v.value1)
            where[v.name + "__lte"] = this.$formatNumber(v.value2)
          } else if (v.sort)
            sort.push(v.sort === "az" ? v.name : "-" + v.name)
        })
        params.filter = Object.keys(where).length>0? where : undefined
        params.sort = sort.length === 0 ? undefined : sort.toString()
      }

      // Tải lại dữ liệu
      let copy = this.$copy(this.pagedata.api)
      copy.params = params
      this.connection.getApi([copy])
    },

    scrollbarVisible() {
      let element = this.$refs['container']
      let result = element.scrollWidth > element.clientWidth? true : false
      if(this.scrollbar) {
        element.parentNode.removeChild(this.scrollbar)
        this.scrollbar = undefined
      }
      if(result) this.doubleScroll(element)
    },

    doubleScroll(element) {
      var scrollbar= document.createElement('div');
      scrollbar.appendChild(document.createElement('div'));
      scrollbar.style.overflow= 'auto';
      scrollbar.style.overflowY= 'hidden';
      scrollbar.firstChild.style.width= element.scrollWidth+'px';
      scrollbar.firstChild.style.height = '1px'
      scrollbar.firstChild.appendChild(document.createTextNode('\xA0'));
      var running = false;
      scrollbar.onscroll= function() {
        if(running) {
          running = false;
          return;
        }
        running = true;
        element.scrollLeft= scrollbar.scrollLeft;
      };
      element.onscroll= function() {
        if(running) {
          running = false;
          return;
        }
        running = true;
        scrollbar.scrollLeft= element.scrollLeft;
      }
      element.parentNode.insertBefore(scrollbar, element)
      scrollbar.scrollLeft= element.scrollLeft
      this.scrollbar = scrollbar
    },

    copyField(field) {
      let newField = this.$copy(field)
      newField.formula = field.name
      newField.tags = [field.name]
      newField.name = 'f' + this.$dayjs(new Date()).format("hhmmss")
      newField.label = field.label + '-copy'
      newField.unit = field.unit==='0.01'? field.unit : '1'
      let copy = this.$copy(this.pagedata.fields)
      let idx = copy.findIndex(v=>v.name===field.name)
      copy.splice(idx+1, 0, newField)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
      this.$calculateFields(this.pagename)
      if(this.pagedata.filters? this.pagedata.filters.length>0 : false) {
        this.$store.commit("updateState", {name: this.pagename, key: "filterby", data: this.pagedata.filters})
      }
    }
  }
}
</script>

<style>
  .table tbody tr:hover td, .table tbody tr:hover th {
    background-color: hsl(0, 0%, 29%);
    color: white;
  }
  .has-background-ceiling {background-color: rgb(214, 2, 227); color: white !important;}
  .has-background-floor {background-color: rgb(8, 207, 218); color: white  !important;}
  .has-background-up {background-color: rgb(9, 176, 7); color: red  !important;}
  .has-background-down {background-color: rgb(	223, 3, 37); color: white  !important;}
  .has-background-keep {background-color: white; color: black;}
  .has-sidebar-color {background-color: #d3d3d3 !important;}
</style>