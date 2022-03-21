<template>
<div v-if="pageData">
  <div class="tabs is-boxed px-3 mb-1">
    <ul>
      <li :class="tab===v.code? 'is-active fs13' : 'fs13'" @click="tab=v.code"
      v-for="(v,i) in tabs" :key="i"><a class="py-1"> {{v.name}} </a></li>
      </ul>
    </div>
      <b-table v-if="tab==='list'"
        class="fs12 px-3"
        :data="fields"
        draggable
        @dragstart="dragstart"
        @drop="drop"
        @dragover="dragover"
        @dragleave="dragleave"
      >
        <b-table-column field="index" label="Stt" numeric v-slot="props" class="td-default">
          {{ props.index + 1 }}
        </b-table-column>
        <b-table-column field="label" label="Tên trường" v-slot="props">
          <a @click="currentField=props.row">{{ props.row.name }}</a> 
          <a @click="copyContent(props.row.name)">
          <span class="icon">
            <i class="mdi mdi-content-copy"/>
          </span>
        </a>
        </b-table-column>

        <b-table-column>
        <template v-slot:header="{}">
          Mô tả
          <a @click="edit=!edit">
            <span class="icon has-text-grey-darker">
              <i class="mdi mdi-square-edit-outline fs18" />
            </span>
          </a>
      </template>

       <template v-slot="props" v-if="edit">
         <input class="input is-small" type="text" placeholder="" v-model="props.row.label" @change="checkChange(props.row)">
       </template>

      <template v-slot="props" v-else>
         {{$stripHtml(props.row.label, 40)}}
       </template>
       </b-table-column>

        <b-table-column field="check" width="70px">
        <template v-slot:header="{}">
          <b-checkbox
            class="fs10 px-0 mx-0"
            v-model="checkAll"
          ></b-checkbox>
          <a @click="deleteConfirm()"> 
            <i class="mdi mdi-delete-outline has-text-danger fs17" />
          </a>
      </template>
      <template v-slot="props">
          <b-checkbox
            class="fs11 my-0 py-0 mx-0"
            v-model="props.row.show"
            @input="checkChange(props.row)"
          ></b-checkbox>
           <a v-if="!(props.row.required || props.row.mandatory)" @click="deleteRow(props.index)">
            <span class="icon fs16 has-text-grey-darker">
              <i class="mdi mdi-delete-outline" />
            </span>
          </a>
      </template>
    </b-table-column>
    </b-table>
  
    <CreateField v-else-if="tab==='create-field'" class="mx-6" v-bind="{pagename: pagename}"> </CreateField>

    <TableSetting v-else-if="tab==='option'" class="mx-5" v-bind="{pagename: pagename}"> </TableSetting>

     <MenuSave v-else-if="tab==='save'" class="mx-6" v-bind="{pagename: pagename, classify: settingclass.find(v=>v.code=='data-field').id}"> </MenuSave>

    <template v-else-if="tab==='export'">
      <div class="mt-5 ml-6">
        <p>Xuất dữ liệu ra file Microsoft Excel.</p>
        <p class="mt-5">
          <a class="button is-primary is-rounded" @click="exportData()">Xuất dữ liệu</a>
        </p>
      </div>
    </template>


  <div class="modal is-active" v-if="currentField">
    <div class="modal-background" style="opacity:0.7 !important;"></div>
    <div class="modal-card" :style="ismobile? '' : 'width:35%'">
    <p class="has-text-right">
      <button class="delete is-large has-background-black" aria-label="close" 
      @click="currentField=undefined"></button>
    </p>
    <section class="modal-card-body" style="min-height:300px">
      <FieldAttribute :field="currentField" @close="currentField=undefined" @update="updateField" />
    </section>
  </div>
  </div>
</div>
</template>

<script>
import CreateField from "@/components/datatable/CreateField"
import TableSetting from "@/components/datatable/TableSetting"
import FieldAttribute from "@/components/datatable/FieldAttribute"
import MenuSave from "@/components/menu/MenuSave"

export default {
  components: {
    CreateField,
    TableSetting,
    FieldAttribute,
    MenuSave
  },

  props: ['pagename'],

  data() {
    return {
      fields: [],
      draggingRow: undefined,
      draggingRowIndex: undefined,
      checkAll: false,
      change: false,
      edit: false,
      tab: 'list',
      tabs: [{code: 'list', name: 'Danh sách trường'}, {code: 'create-field', name: 'Tạo trường'}, 
      {code: 'option', name: 'Tùy chọn'}, {code: 'save', name: 'Lưu thiết lập'},  {code: 'export', name: 'Xuất dữ liệu'}],
      currentField: undefined
    }
  },

  created() {
    if (this.pageData) this.fields = this.$copy(this.pageData.fields)
  },

  watch: {
    'pageData.fields': function(newVal) {
      if(this.change) this.change = false
      else this.fields = this.$copy(this.pageData.fields)
    },

    checkAll: function(newVal) {
      this.fields.filter((v) => !v.mandatory).map((x) => (x.show = newVal));
      this.fields = this.$copy(this.fields);
      this.change = true
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: this.$copy(this.fields)})
    }
  },

  computed: {
    pageData: {
      get: function() {return this.$store.state[this.pagename]},
      set: function(val) {this.$store.commit('updateStore', {name: this.pagename, data: val})}
    },

    ismobile: {
      get: function() {return this.$store.state.ismobile},
      set: function(val) {this.$store.commit("updateIsMobile", { ismobile: val })}
    },

    settingclass: {
      get: function() {return this.$store.state.settingclass},
      set: function(val) {this.$store.commit("updateSettingClass", { settingclass: val })}
    }
  },

  methods: {
    deleteConfirm() {
      this.$buefy.dialog.confirm({
        message: 'Bạn có chắc chắc muốn xóa tất cả các trường không?.',
        confirmText: 'Có',
        cancelText: 'Không',
        onConfirm: () => {this.deleteFields()}
      })
    },

    copyContent(value) {
      this.$copyToClipboard(value)
    },

    checkChange(row) {
      this.change = true
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: this.$copy(this.fields)})
    },

    deleteRow(idx) {
      this.change = true
      this.$delete(this.fields, idx)
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: this.$copy(this.fields)})
    },

    deleteFields() {
      let filter = this.fields.filter(
        (v) => v.show && !v.mandatory && !v.required
      );
      if (filter.length === 0) return;
      filter.map((v) => {
        let idx = this.fields.findIndex((x) => x.name === v.name);
        if (idx >= 0) this.$delete(this.fields, idx);
      });
      this.change = true
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: this.$copy(this.fields)})
    },

    dragstart(payload) {
      this.draggingRow = payload.row;
      this.draggingRowIndex = payload.index;
      payload.event.dataTransfer.effectAllowed = "copy";
    },

    dragover(payload) {
      payload.event.dataTransfer.dropEffect = "copy";
      payload.event.target.closest("tr").classList.add("is-selected");
      payload.event.preventDefault();
    },

    dragleave(payload) {
      payload.event.target.closest("tr").classList.remove("is-selected");
      payload.event.preventDefault();
    },

    drop(payload) {
      payload.event.target.closest("tr").classList.remove("is-selected")
      this.$arrayMove(this.fields, this.draggingRowIndex, payload.index)
      this.change = true
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: this.$copy(this.fields)})
    },

    exportData() {
      let fields = this.pageData.fields.map(v=>v.name)
      let dataType = {}
      this.fields.map(v=>dataType[v.label.indexOf('>')>=0? v.name : v.label] = 'String')
      let data = this.pageData.data
      if(this.pageData.filters? this.pageData.filters.length>0 : false) data = this.pageData.dataFilter
      this.$exportExcel(data, 'data-export', fields, dataType)
    },

    updateField(field) {
      let copy = this.$copy(this.pageData.fields)
      let idx = copy.findIndex(v=>v.name===field.name)
      copy[idx] = field
      this.$store.commit("updateState", {name: this.pagename, key: "fields", data: copy})
      this.currentField = undefined
    }
  }
}
</script>

<style scoped>
  * >>> .table tbody tr td {
    height: 14px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
  }
</style>