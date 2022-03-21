<template>
<div>
  <div class="field is-horizontal  mt-4 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Màu nền background <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
       <input type="color" :value="tablesetting.find(v=>v.code==='background').detail" 
       @change="changeSetting($event.target.value, 'background')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Màu nền bảng <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
       <input type="color" :value="tablesetting.find(v=>v.code==='table-background').detail" 
       @change="changeSetting($event.target.value, 'table-background')">
      </p>
    </div>
      <div class="field">
      <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
       <input type="color" :value="tablesetting.find(v=>v.code==='table-font-color').detail" 
       @change="changeSetting($event.target.value, 'table-font-color')">
      </p>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Chiều cao container <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
         <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='container-height').detail" 
       @change="changeSetting($event.target.value, 'container-height')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Cỡ chữ của bảng <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
       <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='table-font-size').detail" 
       @change="changeSetting($event.target.value, 'table-font-size')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Số dòng trên 1 trang <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='per-page').detail" 
       @change="changeSetting($event.target.value, 'per-page')">
      </p>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Chiều rộng menu <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='menu-width').detail" 
       @change="changeSetting($event.target.value, 'menu-width')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Chiều cao menu (nhỏ nhất) <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='menu-min-height').detail" 
       @change="changeSetting($event.target.value, 'menu-min-height')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Chiều cao menu (lớn nhất) <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='menu-max-height').detail" 
       @change="changeSetting($event.target.value, 'menu-max-height')">
      </p>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Cỡ chữ tiêu đề <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
         <p class="control fs14">
        <input class="input is-small" type="text" :value="tablesetting.find(v=>v.code==='header-font-size').detail" 
       @change="changeSetting($event.target.value, 'header-font-size')">
      </p>
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Màu chữ tiêu đề <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
          <input type="color" :value="tablesetting.find(v=>v.code==='header-font-color').detail" 
       @change="changeSetting($event.target.value, 'header-font-color')">
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Màu nền tiêu đề <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
          <input type="color" :value="tablesetting.find(v=>v.code==='header-background').detail" 
       @change="changeSetting($event.target.value, 'header-background')">
      </p>
    </div>
  </div>
</div>

<div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Mũi tên trỏ xuống<span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
         <b-radio v-model="radioArrow" native-value="yes">
                  Có
                </b-radio>
                <b-radio v-model="radioArrow" native-value="no">
                  Không
                </b-radio>
      </p>
    </div>

    <div class="field">
      <label class="label fs14"> Màu chữ khi filter<span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input type="color" :value="tablesetting.find(v=>v.code==='header-filter-color').detail" 
       @change="changeSetting($event.target.value, 'header-filter-color')">
      </p>
    </div>

    <div class="field" >
      <label class="label fs14"> Hiển thị menu <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <b-radio v-model="radioMenu" native-value="yes">
          Có
        </b-radio>
        <b-radio v-model="radioMenu" native-value="no">
          Không
        </b-radio>
      </p>
    </div>
  </div>
</div>

<div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field is-narrow">
      <label class="label fs14"> Sử dụng ghi chú<span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <b-radio v-model="radioNote" native-value="no">
          Không
        </b-radio>
         <b-radio v-model="radioNote" native-value="yes">
          Có
        </b-radio>
      </p>
    </div>
        <div class="field ml-5" v-if="radioNote==='yes'">
      <label class="label fs14"> Ghi chú (nằm dưới bảng giá) <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
        <input class="input is-small" type="text" 
        :value="tablesetting.find(v=>v.code==='note')? tablesetting.find(v=>v.code==='note').detail.replace('@', '') : ''" 
       @change="changeSetting($event.target.value, 'note')">
      </p>
    </div>
  </div>
</div>

  <div class="field is-horizontal mt-3 pb-2">
  <div class="field-body">
    <div class="field" >
      <label class="label fs14"> Đường viền <span class="has-text-danger"> * </span> </label>
      <p class="control fs14">
         <input class="input is-small" type="text"
         :value="tablesetting.find(v=>v.code==='td-border')? tablesetting.find(v=>v.code==='td-border').detail : undefined" 
       @change="changeSetting($event.target.value, 'td-border')">
      </p>
    </div>
  </div>
</div>
 </div>
</template>

<script>
export default {
  props: ['focus'],
  data() {
    return {
      errors: [],
      radioArrow: 'yes',
      radioMenu: 'yes',
      radioNote: 'no'
    }
  },

  created() {
    this.readSetting()
  },

  watch: {
    radioArrow: function(newVal) {
      this.changeSetting(newVal, 'header-arrow')
    },

    radioMenu: function(newVal) {
      this.changeSetting(newVal, 'show-menu')
    },

    radioNote: function(newVal) {
      if(newVal==='no') this.changeSetting('@', 'note')
    },

    focus: function(newVal) {
      this.readSetting()
    }
  },

  computed: {
    tablesetting: {
      get: function() {return this.$store.state.tablesetting},
      set: function(val) {this.$store.commit("updateTableSetting", {tablesetting: val})}
    },

    originsetting: {
      get: function() {return this.$store.state.originsetting},
      set: function(val) {this.$store.commit("updateOriginSetting", {originsetting: val})}
    }
  },

  methods: {
    readSetting() {
      this.radioArrow = this.tablesetting.find(v=>v.code==='header-arrow').detail
      this.radioMenu = this.tablesetting.find(v=>v.code==='show-menu')? this.tablesetting.find(v=>v.code==='show-menu').detail : this.radioMenu
      let found = this.tablesetting.find(v=>v.code==='note')
      if(found? found.detail!=='@' : false) this.radioNote = 'yes'
    },

    changeSetting(value, code) {
      if(code==='note' && this.$empty(value)) return
      let copy = this.$copy(this.tablesetting)
      let found = copy.find(v=>v.code===code)
      if(found) found.detail = value
      else {
        found = this.$copy(this.originsetting.find(v=>v.code===code))
        found.detail = value
        copy.push(found)
      }
      this.tablesetting = copy
    }
  }
}
</script>