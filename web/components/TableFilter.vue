<!-- eslint-disable -->
<template>
  <div ref="table">
    <section class="hero" v-if="filters.length>0 && showFilter">
      <div class="hero-body py-2">
        <div class="columns">
          <div class="column is-11">
            <div class="field is-grouped is-grouped-multiline" v-if="filters? filters.length>0 : false">
                <div class="control mr-5">
                <div class="tags has-addons is-marginless">
                  <span class="icon has-text-danger fb500"> <i class="mdi mdi-sigma fb500"> </i> 
                  {{pageData.api? (pageData.api.full_data? optiondata.length : pageData.api.total_rows) : 0}} </span>
                </div>
                 <p class="help">
                  <a class="has-text-danger" @click="filters=[]"> Bỏ lọc </a>
               </p>
              </div>

              <div class="control" v-for="(v,i) in filters" :key="i">
                <div class="tags has-addons is-marginless">
                  <span class="tag is-light is-marginless">{{v.label}}</span>
                  <a class="tag is-delete is-marginless" @click="removeFilter(i)"></a>
                </div>
                <span
                  class="has-text-dark help"
                >{{v.type==='sort'? 'sort: ' + v.value : (v.type==='filter'? (v.sub==='less'? '&#60; ' + v.value1 : (v.sub==='bigger'? '> ' + v.value1 : '[' + v.value1 + ',' + v.value2 + ']')) : v.value)}}</span>
              </div>
            </div>
          </div>
          <div class="column is-1">
            <div class="field has-addons">
              <p class="control">
                <a class="button is-white is-small" @click="filters=[]">
                  <i class="icon-delete has-text-dark" style="font-size:24px"></i>
                </a>
              </p>
              <p class="control">
                <a class="button is-white is-small" @click="showFilter=false">
                  <i class="icon-eye-slash has-text-dark" style="font-size:24px"></i>
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div v-if="lookupType==='search'">
      <div class="columns my-1">
        <div class="column is-4 has-text-right">
          <span class="has-text-primary fb500">{{this.searchField.label}}</span>
        </div>
        <div class="column is-5">
          <b-field type="is-primary">
            <b-autocomplete
              ref="searchbox"
              expanded
              v-model="localSearch"
              :data="searchData"
              keep-first
              placeholder="Nhập thông tin cần tìm tại đây"
              :field="searchField.name"
              @typing="filterFieldData"
              @select="option => option===null? 1===1 : searchSelected()"
            >
              <template slot="empty" v-if="pageData.api.full_data">Không có giá trị thỏa mãn</template>
            </b-autocomplete>
          </b-field>
        </div>
        <div class="column is-2">
          <p class="buttons is-centered">
            <a class="tag is-medium is-outlined is-primary" @click="lookupType=undefined">
              <span>Đóng lại</span>
            </a>
          </p>
        </div>
      </div>
    </div>

    <div v-if="lookupType==='filter'">
      <div class="columns mt-3 pb20">
        <div class="column is-3 has-text-right fb500">
          <span class="has-text-primary">{{this.searchField.label}}</span>
        </div>
        <div class="column is-4">
          <div class="block">
            <b-radio v-model="radio" class="pl5 pr5" native-value="less">
              <span>Nhỏ hơn</span>
            </b-radio>
            <b-radio v-model="radio" class="pl5 pr5" native-value="bigger">
              <span>Lớn hơn</span>
            </b-radio>
            <b-radio v-model="radio" class="pl5 pr5" native-value="range">
              <span>Trong khoảng</span>
            </b-radio>
          </div>
        </div>
        <div class="column is-2">
          <div class="field">
            <div class="control">
              <div class="control">
                <input
                  class="input is-focused"
                  ref="firstbox"
                  type="text"
                  @keyup="format()"
                  :placeholder="radio==='range'? 'Nhập giá trị cận dưới' : 'Nhập giá trị'"
                  v-model="value1"
                />
                <p
                  class="help is-danger"
                  v-if="errList.find(v=>v.name==='value1')"
                >{{errList.find(v=>v.name==='value1').message}}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-2" v-if="radio==='range'">
          <div class="field">
            <div class="control">
              <div class="control">
                <input
                  class="input is-focused"
                  ref="secondbox"
                  type="text"
                  @keyup="format()"
                  :placeholder="radio==='range'? 'Nhập giá trị cận trên' : 'Nhập giá trị'"
                  v-model="value2"
                />
                <p
                  class="help is-danger"
                  v-if="errList.find(v=>v.name==='value2')"
                >{{errList.find(v=>v.name==='value2').message}}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-1">
          <a class="tag is-medium is-primary" @click="lookupType=undefined">Đóng lại</a>
        </div>
      </div>
    </div>

    <nav class="panel my-4" v-if="selectedlist.length>0 
      && ['data/Task/', 'data/Task_Stock', 'data/Report_Item/'].findIndex(y=>y===pageData.api.url)<0">
      <div class="columns is-multiline">
        <div class="column is-1 is-offset-1"></div>
        <div class="column is-3">
          <span class="has-text-primary fb500">{{selectedlist.length + ' bản ghi được chọn' }}</span>
        </div>
        <div class="column is-3">
            <a v-if="pageData? pageData.enableDelete : false"
              class="tag is-medium is-danger"
              @click="selectedAction('delete')"
            >Xóa dữ liệu</a>
        </div>
        <div class="column is-2">
          <a class="delete is-medium has-background-grey" @click="clearSelect()"></a>
        </div>
        <div class="column is-10 is-offset-1" v-if="selectedRows.length>0">
          <article class="message is-primary">
            <div class="message-body has-background-light">
              <nav class="level" v-if="selectedRows.length>0">
                <!-- Left side -->
                <div class="level-left">
                  <div class="level-item">
                    <p class="ml20">
                      <span class="tag is-medium is-primary mr20">{{selectedRows.length}}</span>
                      <span
                        v-if="relation===false"
                      >Bản ghi không có tham chiếu đến, sẵn sàng để xóa.</span>
                      <span
                        class="has-text-danger"
                        v-else
                      >Bản ghi có tham chiếu. Xoá bản ghi và dữ liệu tham chiếu đến.</span>
                    </p>
                  </div>
                  <div class="level-item">
                    <p class="ml40">
                      <a
                        class="tag is-medium is-danger"
                        @click="confirmDelete()"
                      >Thực hiện</a>
                    </p>
                  </div>
                </div>
                <div class="level-right">
                  <div class="level-item">
                    <span
                      v-if="msgInfo.length>0"
                      :class="msgInfo.length>0? msgInfo[0].type : ''"
                    >{{msgInfo[0].message}}</span>
                  </div>
                </div>
              </nav>
            </div>
          </article>
        </div>
    </div>
    </nav>

    <TaskAction v-bind="{selectedlist: selectedlist}" v-else-if="selectedlist.length>0 && ['data/Task/', 'data/Task_Stock'].findIndex(y=>y===pageData.api.url)>=0" />
    <EnableAction v-bind="{selectedlist: selectedlist}" v-else-if="selectedlist.length>0 && pageData.api.url==='data/Report_Item/'" />
  
    <div class="table-container" style="min-height: 220px; overflow-x:auto">
      <table class="table is-narrow is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th
              class="has-text-weight-semibold"
              v-for="(field,key) in optionfields.filter(col => col.show===true)"
              :key="key"
              :style="field['min-width']? 'min-width:' + field['min-width'] : ''"
            >
              <div class="dropdown is-hoverable" ref="dropdown" v-if="field.name!=='action'">
                <div class="dropdown-trigger">
                  <p aria-haspopup="true" aria-controls="dropdown-menu4">
                    <span
                      v-if="field['span']===true"
                      class="tag is-rounded mb5 fs14"
                      :class="filters.find(v=>v.name===field.name)? 'has-text-primary' : 'has-text-dark'"
                    >{{ field.label }}</span>
                    <span
                      class="fs14"
                      :class="filters.find(v=>v.name===field.name)? 'has-text-primary' : 'has-text-dark'"
                    >{{ field.label }}</span>
                  </p>
                </div>

                <div
                  class="dropdown-menu"
                  id="dropdown-menu4"
                  role="menu"
                  v-if="showDropdown===true"
                >
                  <div class="dropdown-content">
                    <a
                      class="dropdown-item pt3 pb3"
                      v-for="(item, id) in filterOption(field)"
                      :key="id"
                      @click="setfilter(field, item)"
                    >
                      <i
                        v-if="item['icon'] !==undefined"
                        v-bind:class="item['icon']"
                        class="has-text-primary fs20"
                      ></i>
                      <span
                        v-if="item['icon'] !==undefined && item['disp']==='both'"
                        class="fs14 subtitle"
                      >{{item[field.name]}}</span>
                      <span class="fs14 subtitle" v-if="item['icon']===undefined">{{item.value}}</span>
                    </a>
                  </div>
                </div>
              </div>
              <div class="vertical-center" v-else-if="field.name==='action'">
                <b-checkbox
                  class="has-text-link is-vertical-center fs14"
                  type="is-primary"
                  v-model="selectall"
                  v-if="field.action.indexOf('select')>=0"
                ></b-checkbox>
                <a
                  class="has-text-dark is-vertical-center"
                  @click="openRecord({}, 'insert')"
                  v-if="field.action.indexOf('insert')>=0"
                >
                  <span class="icon">
                    <i class="mdi mdi-plus fs26" />
                  </span>
                </a>
              </div>
            </th>
          </tr>
        </thead>

        <tbody v-if="optiondata.length>0">
          <tr
            v-for="(ele,i) in optiondata.filter((ele,index) => (index>=(showPage-1)*perPage && index<showPage*perPage))"
            :key="i" :ref="'tr' + i"
          >
            <td
              class="has-text-weight-normal fs14"
              v-for="(field,key) in optionfields.filter(col => col.show===true)"
              :key="key"
            >
              <div class="field has-addons" v-if="field.name==='action'">
                <p class="control">
                  <b-checkbox
                    class="is-vertical-center fs14 pl0 pr0 pt0 pb0 ml0 mr0 mt0 mb0"
                    type="is-primary"
                    v-model="models[ele.id]"
                  ></b-checkbox>
                </p>
                <p class="control" v-if="field.action.indexOf('open')>=0">
                  <a class="is-vertical-center has-text-dark" @click="openRecord(ele, 'open')">
                    <span class="icon">
                      <i class="mdi mdi-open-in-new fs22" />
                    </span>
                  </a>
                </p>
                <p class="control" v-if="field.action.indexOf('edit')>=0">
                  <a
                    class="is-vertical-center has-text-dark ml3"
                    @click="openRecord(ele, 'edit')"
                  >
                    <span class="icon">
                      <i class="mdi mdi-square-edit-outline fs22" />
                    </span>
                  </a>
                </p>
              </div>
              <span v-else-if="field.tooltip!==undefined && ele[field.name]!==undefined">
                <b-tooltip
                  :label="ele[field.tooltip.field]"
                  type="is-dark"
                  :position="field.tooltip.position"
                >
                  <span class="fs14" :class="field.tooltip.class">{{ele[field['name']]}}
                    <i class="mdi mdi-star ml-1 fs17 has-text-danger" v-if="ele.priority===true && (field.name==='company__stock_code' || field.name==='report_name__code')"> </i>
                    <i class="mdi mdi-flag ml-1 fs17 has-text-danger" v-else-if="ele.marked_fields>0 && field.name==='report_type__code'"> </i> 
                  </span>
                </b-tooltip>
              </span>

              <span
                v-else-if="field.style!==undefined"
                :class="getStyle(field,ele)"
                @click="field.style['click']===true? openRecord(ele, 'show') : 0===0"
              >{{ ele[field['name']]}}</span>
              <span v-else>{{ele[field['name']]}}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div
      class="pt15"
      v-if="pageData.pagination!==false && (pageData.api.full_data? optiondata.length>perPage : 1===1)"
    >
      <b-pagination
        :total="pageData.api.full_data? optiondata.length : pageData.api.total_rows"
        :current.sync="currentPage"
        :order="'is-left'"
        :rounded="true"
        :per-page="perPage"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from "vue"
import mixing from "@/assets/js/mixing.js"
import Connection from "@/assets/js/connection.js"
import axios from "axios"
import TaskAction from '@/components/TaskAction'
import EnableAction from '@/components/EnableAction'

export default {
  props: ["name"],

  components: {
    TaskAction,
    EnableAction
  },
  
  data() {
    return {
      perPage: 20,
      currentPage: 1,
      showDropdown: true,
      lookupType: undefined,
      localSearch: "",
      searchData: [],
      searchField: undefined,
      radio: "less",
      value1: undefined,
      value2: undefined,
      connection: this.$connection(),
      errList: [],
      selectedlist: [],
      selectedRows: [],
      flagFilter: false,
      selectall: false,
      models: [],
      msgInfo: [],
      optiondata: undefined,
      optionfields: undefined,
      search: undefined,
      relation: false,
      showPage: 1,
      filters: [],
      timer: undefined,
      showFilter: true,
      flagModel: false,
      deleteType: undefined,
      before: undefined,
      myVar : undefined
    };
  },

  created() {
    if (this.pageData.data) this.optiondata = this.pageData.data;
    if (this.pageData.fields) this.optionfields = this.pageData.fields;
    if (this.pageData.models) this.models = this.pageData.models;
    if (this.pageData.pagination === false) this.perPage = 1000000000000;
    if (this.pageData.filterby) this.filters = this.pageData.filterby;
  },

  watch: {
    "pageData.data": function(newVal) {
      this.optiondata = newVal;
      this.models = [];
      this.showPage = 1;
    },

    "pageData.fields": function(newVal) {
      this.optionfields = newVal;
      let _filters = this.$copy(this.filters);
      _filters.map(v => {
        if (newVal.find(x => x.name === v.name) === undefined) {
          let index = this.filters.findIndex(y => y.name === v.name);
          if (index >= 0) this.$delete(this.filters, index);
        }
      });
    },

    "pageData.filterby": function(newVal) {
      this.filters = newVal
    },

    "pageData.highlight": function(newVal) {
      if(newVal===undefined || this.$refs['tr0']===undefined) return
      let el = this.$refs['tr0'][0]
      if(this.myVar) clearInterval(this.myVar)
      
      var ofs = 1;
      this.myVar = window.setInterval(function(){
          el.style.background = 'rgba(255,255,0,'+Math.abs(Math.sin(ofs))+')';
          ofs += 0.01;
      }, 10)

      let self = this
      mixing.delay(function(){
          clearInterval(self.myVar)
          el.style.background = null
          self.$store.commit("updateState", {name: self.name, key: "highlight", data: undefined})
      }, 4000)
    },

    "pageData.models": function(newVal) {
      if (newVal) {
        this.flagModel = true
        this.models = this.$copy(newVal)
      }
    },

    models: function(newVal) {
      if(this.flagModel) this.flagModel = false
      else this.modelsChange(newVal)
    },

    selectall: function(newVal) {
      let data = [];
      this.optiondata.forEach(element => {
        data[element.id] = newVal;
      });
      this.models = data;
    },

    optiondata: function(newVal) {
      this.$store.commit("updateState", {
        name: this.name,
        key: "filter",
        data: newVal
      });
    },

    currentPage: function(newVal) {
      if (!this.lookupType)
        window.scroll({
          top: this.$refs["table"].offsetTop - 80,
          left: 0,
          behavior: "smooth"
        });
      this.showPage = newVal;
      if (this.pageData.api.full_data) return;
      this.showPage = 1;
      let copy = this.$copy(this.pageData.api)
      copy.params.page = newVal;
      this.$store.commit("updateState", {name: this.name, key: "api", data: copy})
      this.$store.commit("updateState", {name: this.name, key: "reload", data: this.pageData.reload + 1})
    },

    localSearch: function(newVal) {
      let index = this.filters.findIndex(v => v.name === this.searchField.name);

      if (index >= 0) {
        let filters = this.$copy(this.filters);
        if (this.$empty(newVal)) this.$delete(filters, index);
        else Vue.set(filters[index], "value", newVal);
        this.filters = filters;
      } else {
        if (!this.$empty(newVal)) {
          let filters = this.$copy(this.filters);
          filters.push({
            name: this.searchField.name,
            label: this.searchField.label,
            format: this.searchField.format,
            value: newVal,
            field: this.searchField,
            type: "search"
          });
          this.filters = filters;
        }
      }
    },

    radio: function() {
      this.searchAdvance();
    },

    "connection.getupdateStatus": function(newVal) {
      if(newVal===true) {
        var data = this.$copy(this.connection.getupdateRecord);
        var message = "Dữ liệu xóa thành công sẽ biến mất trên màn hình sau 5s";
        const num_error = data.filter(v => v.error).length

        let text =
          (num_error===0 ? "Hoàn thành." : "Có lỗi.") +
          " Đã xoá " +
          data.filter(v => v.error === undefined).length +
          "/" +
          data.length;
        let type = num_error===0 ? "has-text-primary" : "has-text-danger";
        this.msgInfo = [{name: this.deleteType,  message: text, type: type }];
        const datalist = this.$copy(this.pageData.data)

        if (data.filter(v => v.error === undefined).length > 0)
          this.$buefy.snackbar.open({
            duration: 5000,
            message: message,
            type: "is-success",
            position: "is-bottom"
          });

          this.connection.getupdateRecord.forEach(v => {
            if(!v.error) {
              let index = datalist.findIndex(x => x.id === v.id)
              if (index >= 0) this.$delete(datalist, index)
            }
          })
      
        let self = this
        mixing.delay(function() {
          self.$store.commit("updateState", {name: self.name, key: "data", data: datalist})
        }, 5000)
      }
    },

    filters: {
      immediate: true,
      deep: true,
      handler(newVal) {
        if (!this.showFilter) this.showFilter = true;
        if (newVal.length === 0) {
          if (this.pageData.origin_api.full_data)
            this.optiondata = this.$copy(this.pageData.data);
          else this.$store.commit("updateState", {name: this.name, key: "reload", data: 0})
        } else if (this.pageData.origin_api.full_data)
          this.frontendFilter(newVal);
        else {
          let self = this,
            duration = 0;
          if (this.timer) clearInterval(this.timer);
          this.timer = setInterval(function() {
            duration++;
            if (duration === 1) self.backendFilter(newVal);
            else if (duration > 1) clearInterval(this.timer);
          }, 500);
        }
        this.$store.commit("updateState", {
          name: this.name,
          key: "currentFilter",
          data: newVal
        });
      }
    }
  },

  computed: {
    pageData: {
      get: function() {return this.$store.state[this.name]},
      set: function(val) {this.$store.commit('updateStore', {name: this.name, data: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", {login: val})}
    },
  },

  methods: {
    searchSelected() {
      const filters = this.$copy(this.filters);
      let found = filters.find(v => v.name === this.searchField.name);
      if (found) Vue.set(found, "type", "select");
      this.filters = filters;
    },

    removeFilter(i) {
      const filters = this.$copy(this.filters);
      this.$delete(filters, i);
      this.filters = filters;
    },

    frontendFilter(newVal) {
      var data = this.$copy(this.pageData.data);
      this.currentPage = 1;
      newVal = JSON.parse(JSON.stringify(newVal));
      newVal.map(v => {
        if (v.format === "number" && v.type === "filter") {
          v.value1 = mixing.formatNumber(v.value1);
          v.value2 = mixing.formatNumber(v.value2);
        }
      });

      newVal.map(v => {
        if (v.type === "search")
          data = data.filter(
            x =>
              (this.$empty(x[v.name]) ? "" : x[v.name])
                .toString()
                .toLowerCase()
                .indexOf(v.value.toLowerCase()) >= 0
          );
        else if (v.type === "filter" && v.sub === "less") {
          data = data.filter(x =>
            this.$empty(x[v.name] === "n/a" ? undefined : x[v.name])
              ? 1 < 0
              : mixing.formatNumber(x[v.name]) < mixing.formatNumber(v.value1)
          );
        } else if (v.type === "filter" && v.sub === "bigger")
          data = data.filter(x =>
            this.$empty(x[v.name] === "n/a" ? undefined : x[v.name])
              ? 1 < 0
              : mixing.formatNumber(x[v.name]) > mixing.formatNumber(v.value1)
          );
        else if (v.type === "filter" && v.sub === "range") {
          data = data.filter(x =>
            this.$empty(x[v.name] === "n/a" ? undefined : x[v.name])
              ? 1 < 0
              : mixing.formatNumber(x[v.name]) >= mixing.formatNumber(v.value1)
          );
          data = data.filter(x =>
            this.$empty(x[v.name] === "n/a" ? undefined : x[v.name])
              ? 1 < 0
              : mixing.formatNumber(x[v.name]) <= mixing.formatNumber(v.value2)
          );
        } else if (v.type === "select")
          data = data.filter(x => x[v.name] === v.value);
      });

      let sort = {},
        format = {};
      newVal.map(v => {
        if (v.value === "a-z" || v.value === "z-a") {
          sort[v.name] = v.value === "a-z" ? "asc" : "desc";
          format[v.name] = v.format;
        }
      });

      data = mixing.multiSort(data, sort, format);
      this.optiondata = data;
    },

    backendFilter(newVal) {
      let filter = this.$copy(newVal);
      filter.map(v => {
        if (v.format === "number") {
          if (v.type === "search" || v.type === "select")
            v.value = mixing.formatNumber(v.value);
          else if (v.type === "filter") {
            v.value1 = mixing.formatNumber(v.value1);
            v.value2 = mixing.formatNumber(v.value2);
          }
        }
      });

      this.currentPage = 1;
      let params = this.pageData.origin_api.params? this.$copy(this.pageData.origin_api.params) : {};
      var where = params.filter? params.filter : {}
      var sort = []

      //Tìm kiếm sử dụng lệnh sql
      if (
        this.pageData.api.url.indexOf("query-data/") >= 0 ||
        this.pageData.api.url.indexOf("fetch-data/") >= 0
      ) {
        /*
          where = 'where', sort = ' order by'
          filter.forEach(v => {
              if(v.type==='search') where += ' LOWER("' + v.name + '"::text) ~* ' + "'"  + v.value.toString().toLowerCase() + "' and"
              else if(v.type==='select') where += ' LOWER("' + v.name + '"::text) like ' + "'" + v.value.toString().toLowerCase() + "' and"
              else if(v.type==='filter' && v.sub==='less') where += ' ' + v.name + ' <' + v.value1 + " and"
              else if(v.type==='filter' && v.sub==='bigger') where += ' ' + v.name + ' >' + v.value1 + " and"
              else if(v.type==='filter' && v.sub==='range') where += ' ' + v.name + ' >=' + v.value1 + " and " + v.name + ' <=' + v.value2 + " and"
              else if(v.type==='sort') sort += ' ' + v.name + (v.value==='a-z'? ' asc ' : ' desc ') + ' ,'
          })
          params.filter = (where==='where'? '' : where.substring(0, where.length-4))  + (sort===' order by'? '' : sort.substring(0, sort.length-1))
          */
        filter.map(v => delete v.field);
        params.filter = JSON.stringify(filter);
      }

      // Tìm kiếm sử dụng backend filter
      else if (this.pageData.origin_api.url.indexOf("data/") >= 0) {
        filter.forEach(v => {
          if (v.type === "search") where[v.name + "__icontains"] = v.value;
          else if (v.type === "select") where[v.name] = v.value;
          else if (v.type === "filter" && v.sub === "less")
            where[v.name + "__lt"] = v.value1;
          else if (v.type === "filter" && v.sub === "bigger")
            where[v.name + "__gt"] = v.value1;
          else if (v.type === "filter" && v.sub === "range") {
            where[v.name + "__gte"] = v.value1;
            where[v.name + "__lte"] = v.value2;
          } else if (v.type === "sort")
            sort.push(v.value === "a-z" ? v.name : "-" + v.name);
        });
        params.filter = Object.keys(where).length>0? where : undefined;
        params.sort = sort.length === 0 ? undefined : sort.toString();
      }

      // Tải lại dữ liệu
      let copy = this.$copy(this.pageData.api)
      copy.params = params
      this.$store.commit("updateState", {name: this.name, key: "api", data: copy})
      this.$store.commit("updateState", {name: this.name, key: "reload", data: this.pageData.reload + 1})
    },

    modelsChange(newVal) {
      this.selectedlist = newVal.filter(v => v === true);
      if (this.selectedlist.length === 0) this.selectall = false;
      else if (this.selectedlist.length === this.optiondata.length) {
        this.selectall = true;
      }
      this.$store.commit("updateState", {name: this.name, key: "models", data: newVal})
      this.selectedRows = []
    },

    confirmDelete() {
      this.connection.delete(this.pageData.api.name, this.selectedRows);
    },

    selectedAction(type) {
      this.msgInfo = [];
      let data = [];
      this.models.forEach((element, id) => {
        if (element === true) {
          let found = this.optiondata.find(v => parseInt(v.id) === parseInt(id));
          data.push(found);
        }
      })
      this.selectedRows = type === "delete" ? data : []
      let found = this.connection.requirelist.find(
        v => v.name === this.pageData.api.name
      );
      axios
        .post(
          this.connection.path +
            "check-model-relation/" +
            (found !== undefined
              ? found.url.substring(5, found.url.length - 1)
              : this.pageData.api.name) +
            "/"
        )
        .then(response => {
          this.relation = response.data["relation"];
        });
    },

    clearSelect() {
      this.$store.commit("updateState", {name: this.name, key: "data", data: this.$copy(this.pageData.data)})
    },

    getStyle(field, record) {
      let style = this.$copy(field.style)
      let found = style.list.find(v => v.value === record[style.condition]);
      return found === undefined ? undefined : found.class;
    },

    getval(obj, field) {
      if (obj === undefined || obj === null) return "";
      return obj[field] === undefined ? "" : obj[field];
    },

    format() {
      this.errList = [];
      if (mixing.isNumber(this.value1))
        this.value1 = mixing.numbertoString(this.value1);
      else
        this.errList.push({
          name: "value1",
          message: "Giá trị tìm kiếm phải là số"
        });

      if (this.radio === "range") {
        if (mixing.isNumber(this.value2))
          this.value2 = mixing.numbertoString(this.value2);
        else
          this.errList.push({
            name: "value2",
            message: "Giá trị tìm kiếm phải là số"
          });
      }

      if (this.errList.length == 0) {
        this.currentPage = 1;
        this.searchAdvance();
      }
    },

    searchAdvance() {
      let index = this.filters.findIndex(v => v.name === this.searchField.name)
      let copy = this.$copy(this.filters)

      if (this.radio === "less" || this.radio === "bigger") {
        if (!mixing.isNumber(this.value1)) {
          if (index >= 0) this.$delete(copy, index);
        } else {
          if (index >= 0) {
            copy[index].value1 = this.value1;
            copy[index].sub = this.radio;
            copy[index].type = "filter";
          } else
            copy.push({
              name: this.searchField.name,
              value1: this.value1,
              type: "filter",
              sub: this.radio,
              format: this.searchField.format,
              label: this.searchField.label
            })
        }
        
      } else {
        if (mixing.isNumber(this.value1) && mixing.isNumber(this.value2)) {
          if (index >= 0) {
            (copy[index].value1 = this.value1), (copy[index].value2 = this.value2);
            (copy[index].sub = this.radio), (copy[index].type = "filter");
          } else
            copy.push({
              name: this.searchField.name,
              value1: this.value1,
              value2: this.value2,
              format: this.searchField.format,
              label: this.searchField.label,
              type: "filter",
              sub: this.radio
            });
        }
      }
      this.$store.commit("updateState", {name: this.name, key: "filters", data: copy})
      this.filters = copy
    },

    filterOption(field) {
      var array = [];
      if (this.pageData.api.full_data) {
        var filter = this.optiondata
          .map(item => item[field["name"]])
          .filter(
            (v, idx, self) =>
              self.indexOf(this.$empty(v) ? "n/a" : v) === idx
          );
        array = filter.map(v => ({ value: v }));
      }

      var element = {};
      var ele = JSON.parse(JSON.stringify(element));
      (ele[field.name] = "z-a"),
        (ele["added"] = true),
        (ele["disp"] = "icon"),
        (ele["icon"] =
          field["format"] === "string"
            ? "mdi mdi-sort-alphabetical-descending"
            : "mdi mdi-sort-numeric-descending");
      array.unshift(ele);

      ele = JSON.parse(JSON.stringify(element));
      (ele[field.name] = "a-z"),
        (ele["added"] = true),
        (ele["disp"] = "icon"),
        (ele["icon"] =
          field["format"] === "string"
            ? "mdi mdi-sort-alphabetical-ascending"
            : "mdi mdi-sort-numeric-ascending");
      array.unshift(ele);

      if (field["format"] !== "string") {
        ele = JSON.parse(JSON.stringify(element));
        (ele[field.name] = "filter"),
          (ele["added"] = true),
          (ele["disp"] = "icon"),
          (ele["icon"] = "mdi mdi-filter-outline");
        array.unshift(ele);
      }

      ele = JSON.parse(JSON.stringify(element));
      (ele[field.name] = "search"),
        (ele["added"] = true),
        (ele["disp"] = "icon"),
        (ele["icon"] = "mdi mdi-magnify");
      array.unshift(ele);

      return array;
    },

    setfilter(field, ele) {
      this.showDropdown = false;
      this.searchField = field;
      let found = this.filters.find(v => v.name === field.name);

      //-- Search case
      if (ele[field.name] === "search") {
        this.lookupType = "search";
        this.localSearch = "";
      }
      //-- Filter case
      else if (ele[field.name] === "filter") {
        this.lookupType = "filter";
        (this.value1 = null), (this.value2 = null);
      }
      //-- Sort case
      else if (ele[field.name] === "a-z" || ele[field.name] === "z-a") {
        if (found) {
          Vue.set(found, "value", ele[field.name]);
          Vue.set(found, "type", "sort");
        } //this.filters.push({name: field.name, value: ele[field.name], format: field.format, label: field.label, type: 'sort'})
        else {
          const filters = this.$copy(this.filters);
          filters.push({
            name: field.name,
            value: ele[field.name],
            format: field.format,
            label: field.label,
            type: "sort"
          });
          this.filters = filters;
        }
      }
      //-- select
      else {
        if (found) {
          Vue.set(found, "value", ele.value);
          Vue.set(found, "type", "select");
        } //this.filters.push({name: field.name, value: ele.value, type: 'select', format: field.format, label: field.label})
        else {
          const filters = this.$copy(this.filters);
          filters.push({
            name: field.name,
            value: ele.value,
            type: "select",
            format: field.format,
            label: field.label
          });
          this.filters = filters;
        }
      }
      //this.activeDropdown()
      let self = this;
      mixing.delay(function() {
        self.showDropdown = true;
        if (self.$refs["searchbox"]) self.$refs["searchbox"].focus();
        if (self.$refs["firstbox"]) self.$refs["firstbox"].focus();
      }, 50);
      this.$store.commit("updateState", {name: this.name, key: "currentFilter", data: this.filters})
    },

    clearFilter() {
      this.optionfields.forEach(element => {
        if (element.filter) {
          element.filter = false;
          element.select = undefined;
        }
      });
    },

    openRecord(ele, action) {
      this.$store.commit("updateState", {name: this.name, key: "action", data: action})
      this.$store.commit("updateState", {name: this.name, key: "record", data: ele})
    },

    filterFieldData(text) {
      if (!this.pageData.api.full_data) return [];
      if (this.$empty(text)) return;
      let list = mixing.unique(this.optiondata, [this.searchField.name]);
      this.searchData = list.filter(
        v =>
          (this.$empty(v[this.searchField.name])
            ? ""
            : v[this.searchField.name]
          )
            .toString()
            .toLowerCase()
            .indexOf(text.toLowerCase()) >= 0
      );
    }
  }
};
</script>

<style scoped>
.dropdown-content {
  margin: 0;
  padding: 0;
  height: 10em;
  overflow: auto;
}

tr:hover {
  background-color: #f5f5f5;
}

td,
th {
  height: 33px !important;
  padding-top: 3px !important;
  padding-bottom: 3px !important;
  vertical-align: middle;
  max-width: 450px;
  word-wrap: break-word;
}
</style>