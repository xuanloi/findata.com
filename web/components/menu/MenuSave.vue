<template>
  <div>
    <template
      v-if="currentsetting? currentsetting.user === login.id : false">
      <p class="fs16 has-text-primary">Bạn đang mở thiết lập:</p>
      <p class="mt-2">{{ currentsetting.name }}</p>
    </template>

    <div class="field mt-4 px-0 mx-0">
      <label class="label fs14"
        >Chọn chế độ lưu <span class="has-text-danger"> * </span>
      </label>
      <p class="control is-expanded fs14">
        <b-radio v-model="radioSave" native-value="overwrite" v-if="isOverrite()">
          Ghi đè
        </b-radio>
        <b-radio v-model="radioSave" native-value="new">
          Tạo mới
        </b-radio>
      </p>
    </div>

    <template v-if="radioSave === 'new'">
      <div class="field mt-4 px-0 mx-0">
        <label class="label fs14"
          >Tên thiết lập <span class="has-text-danger"> * </span>
        </label>
        <p class="control">
          <input
            class="input is-small"
            type="text"
            placeholder=""
            v-model="name"
            ref="name"
          />
        </p>
        <p
          class="help has-text-danger"
          v-if="errors.find((v) => v.name === 'name')"
        >
          {{ errors.find((v) => v.name === "name").msg }}
        </p>
      </div>

      <div class="field mt-4 px-0 mx-0">
        <label class="label fs14"> Mô tả </label>
        <p class="control is-expanded">
          <input
            class="input is-small"
            type="text"
            placeholder=""
            v-model="note"
          />
        </p>
      </div>

      <div class="field mt-4 px-0 mx-0">
        <label class="label fs14"
          >Loại thiết lập <span class="has-text-danger"> * </span>
        </label>
        <p class="control is-expanded fs14">
          <b-radio
            v-for="(v, i) in settingtype"
            :key="i"
            v-model="radioType"
            :native-value="v"
          >
            {{ v.name }}
          </b-radio>
        </p>
      </div>

      <div class="field mt-4 px-0 mx-0">
        <label class="label fs14"
          >Mặc định <span class="has-text-danger"> * </span>
        </label>
        <p class="control is-expanded fs14">
          <b-radio v-model="radioDefault" :native-value="0">
            Không
          </b-radio>
          <b-radio v-model="radioDefault" :native-value="1"> Có </b-radio>
        </p>
      </div>
    </template>

    <div class="field mt-5 px-0 mx-0">
      <label
        class="label fs14"
        v-if="status !== undefined"
        :class="status ? 'has-text-primary' : 'has-text-danger'"
      >
        {{
          status
            ? "Lưu thiết lập thành công."
            : "Lỗi. Lưu thiết lập thất bại."
        }}
      </label>
      <p class="control is-expanded">
        <a
          class="button is-primary is-small is-outlined is-rounded"
          @click="saveSetting()"
        >
          Lưu lại</a
        >
      </p>
    </div>
  </div>
</template>

<script>
;

export default {
  props: ['pagename', 'classify', 'option', 'company', 'data', 'focus'],

  data() {
    return {
      selectType: undefined,
      connection: this.$connection(),
      errors: [],
      radioType: undefined,
      radioDefault: 0,
      radioSave: "overwrite",
      note: undefined,
      status: undefined,
      name: undefined,
    };
  },

  created() {
    this.status = undefined;
    this.radioType = this.settingtype.find((v) => v.code === "private");
    if (!this.currentsetting) this.radioSave = "new"
    else if(this.currentsetting.user!==this.login.id) this.radioSave = "new"
  },

  watch: {
    "connection.getupdateStatus": function (newVal) {
      if (newVal === true) {
        this.status = true
        this.name = undefined
        this.note = undefined
      }
      else if (newVal === false) this.status = false
      if(this.status) {
        let self = this
        setTimeout(function() {self.status=undefined}, 3000)
      }
    },

    radioSave: function(newVal) {
      newVal? this.doFocus() : false
    },

    focus: function(newVal) {
      if(this.$refs.name) this.$refs.name.focus()
    }
  },

  computed: {
    login: {
      get: function () {
        return this.$store.state.login;
      },
      set: function (val) {
        this.$store.commit("updateLogin", { login: val });
      },
    },

    tablesetting: {
      get: function () {
        return this.$store.state.tablesetting;
      },
      set: function (val) {
        this.$store.commit("updateTableSetting", { tablesetting: val });
      },
    },

    originsetting: {
      get: function () {
        return this.$store.state.originsetting;
      },
      set: function (val) {
        this.$store.commit("updateOriginSetting", { originsetting: val });
      },
    },

    usersetting: {
      get: function () {
        return this.$store.state.usersetting;
      },
      set: function (val) {
        this.$store.commit("updateUserSetting", { usersetting: val });
      },
    },

    settingtype: {
      get: function () {
        return this.$store.state.settingtype;
      },
      set: function (val) {
        this.$store.commit("updateSettingType", { settingtype: val });
      },
    },

    settingclass: {
      get: function () {
        return this.$store.state.settingclass;
      },
      set: function (val) {
        this.$store.commit("updateSettingClass", { settingclass: val });
      },
    },

    pageData: {
      get: function() {return this.$store.state[this.pagename]},
      set: function(val) {this.$store.commit('updateStore', {name: this.pagename, data: val})}
    },

    currentsetting: {
      get: function() {return this.$store.state.currentsetting},
      set: function(val) {this.$store.commit("updateCurrentSetting", {currentsetting: val})}
    }
  },

  methods: {
    isOverrite() {
      let val = this.currentsetting? (this.currentsetting.user===this.login.id) : false
      if(val) val = this.currentsetting.classify===this.classify? true : false
      if(!val) this.radioSave = 'new'
      return val
    },

    doFocus() {
      let self = this
      setTimeout(function(){
        self.$refs.name? self.$refs.name.focus() : false
      }, 50)
    },

    saveSetting() {
      this.errors = [];
      let detail = {fields: this.pageData.fields};
      if(this.tablesetting!==this.originsetting) detail.tablesetting = this.tablesetting
      if (this.pageData.filters ? this.pageData.filters.length > 0 : false) {
        detail.filters = this.pageData.filters;
      }
      if(this.option) detail.option = this.option
      if(this.company) detail.company = this.company.id
      if(this.data) detail.data = this.data

      let data = {
        user: this.login.id,
        name: this.name,
        detail: JSON.stringify(detail),
        note: this.note,
        type: this.radioType.id,
        classify: this.classify? this.classify : this.settingclass.find(v=>v.code==='data-field').id,
        default: this.radioDefault,
        update_time: new Date(),
      };
      if (this.radioSave === "new") {
        if (this.$empty(this.name)) {
          this.errors.push({
            name: "name",
            msg: "Tên thiết lập không được bỏ trống",
          });
          return;
        }
        this.connection.insert("usersetting", data);
      } else {
        let copy = this.$copy(this.currentsetting);
        copy.detail = JSON.stringify(detail);
        copy.update_time = new Date();
        this.connection.update("usersetting", copy);
      }
    },
  },
};
</script>