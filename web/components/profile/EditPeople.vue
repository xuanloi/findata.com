<template>
<div>
    <div class="field is-horizontal">
    <div class="field-body">
      <div class="field">
      <label class="label">Họ và tên <strong class="has-text-danger">*</strong></label>
      <div class="control">
         <input class="input" type="text" placeholder="Không được bỏ trống thông tin này" v-model="record.name">
      </div>
    </div>

    <div class="field">
      <label class="label">Ngày sinh</label>
      <div class="control">
         <b-datepicker
            locale="en-GB"
            placeholder="Chọn ngày"
            v-model="record.dob"
            editable
        />
      </div>
    </div>
    </div>
      </div>

  <div class="field is-horizontal">
    <div class="field-body">
      <div class="field">
        <label class="label">Chứng minh thư / Hộ chiếu <strong class="has-text-danger">*</strong></label>
        <p class="control">
          <input class="input" type="text" placeholder="Nếu không có CMT, Hộ chiếu hãy tick (Không có  CMT / Hộ chiếu)" v-model="record.legal_id">
        </p>
      </div>
      <div class="field is-narrow">
        <p class="control mt-5 pt-4">
          <b-field>
            <b-checkbox v-model="nonLegalID" :disabled="people? true : false">Không có  CMT / Hộ chiếu</b-checkbox>
          </b-field>
        </p>
      </div>
    </div>
  </div>

  <div class="field">
      <label class="label">Nơi sinh / Nguyên quán</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.domicile">
      </div>
    </div>

    <div class="field">
      <label class="label">Địa chỉ / Thường trú</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.address">
      </div>
    </div>

    <div class="field">
      <label class="label">Trình độ</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.degree">
      </div>
    </div>

     <div class="field">
      <label class="label">Hình đại diện</label>
      <div class="control">
        <input class="input" type="text" placeholder="" v-model="record.avatar">
      </div>
    </div>

    <div class="mt-5">
      <a class="button is-primary" @click="updatePeople()"> {{people? 'Cập nhật' : 'Thêm mới'}} </a>
      <a class="button is-dark ml-3" @click="$emit('closeform', true)"> Đóng lại </a>
    </div>
    </div>
</template>

<script>
export default {
  props: ['people'],

  data() {
    return {
      record: {},
      nonLegalID: false,
      connection: this.$connection(this.$buefy)
    }
  },

  created() {
    if(!this.people) return
    this.record = this.$copy(this.people)
    this.record.dob = this.record.dob? new Date(this.record.dob) : undefined
  },

  watch: {
    'connection.getupdateRecord': function(newVal) {
      if(newVal) {
        this.record = {}
        this.$emit('newpeople', newVal)
      }
    },

    people: function(newVal) {
      if(!newVal) this.record = {}
      else {
        this.record = this.$copy(this.people)
        if(this.record.dob) this.record.dob = new Date(this.record.dob)
      }
    }
  },

  methods: {
    updatePeople() {
      let data = this.$resetNull(this.$copy(this.record))
      if(!this.$empty(data.dob)) data.dob = this.$dayjs(new Date(data.dob)).format("YYYY-MM-DD")
      if(data.id) {
        if(!this.$empty(data.legal_id)) data.uid = data.legal_id
        this.connection.update('people', data)
      } else {
        data.uid = this.nonLegalID? this.$dayjs().format('YYYYMMDDHHmmss') : data.legal_id
        this.connection.insert('people', data)
      }
    }
  }
}
</script>
