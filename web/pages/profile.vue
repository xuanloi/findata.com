<!-- eslint-disable -->
<template>
<div>
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <div class="columns mt70 mb40" v-if="account!==undefined">
    <div class="column is-9">
    <div class="mx-3">
    <div class="columns is-multiline">
        <div class="column is-4 has-text-left"> 
            <div class="field ml10">
            <label class="label">Họ và tên</label>
            <div class="control has-icons-right">
            <input class="input font-smaller" type="text" placeholder="" v-model="name" @focus="info('name')" ref="name">
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='name')!==undefined">{{msgList.find(v=>v.name==='name').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left"> 
            <div class="field ml10">
            <label class="label">Ngày sinh</label>
            <div class="control">
            <div>
                <b-datepicker   size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="dob"
                    @focus="info('dob')"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='dob')!==undefined">{{msgList.find(v=>v.name==='dob').message}}</p>
            </div> 
            </div>
        </div>

        <div class="column is-4 has-text-left"> 
            <div class="field ml10">
            <label class="label">Giới tính</label>
            <div class="control has-icons-right">
                 <div class="block">
            <b-radio v-model="sex"
                native-value="male">
                Nam
            </b-radio>
            <b-radio v-model="sex" class="ml30"
                native-value="female">
                Nữ
            </b-radio>
                 </div>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='sex')!==undefined">{{msgList.find(v=>v.name==='sex').message}}</p>
            </div>
         </div>

               <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Chứng minh thư/hộ chiếu</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="identity" @focus="info('identity')">
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='identity')!==undefined">{{msgList.find(v=>v.name==='identity').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Ngày cấp</label>
            <div class="control">
            <div>
                <b-datepicker   size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="issuedate"
                     @focus="info('issue-date')"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='issuedate')!==undefined">{{msgList.find(v=>v.name==='issuedate').message}}</p>
            </div> 
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Nơi cấp</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="issueplace" @focus="info('issue-place')">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='issueplace')!==undefined">{{msgList.find(v=>v.name==='issueplace').message}}</p>
            </div>
        </div>

              <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Điện thoại</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="phone" @focus="info('phone')">
            </div>
          <p class="help is-danger" v-if="msgList.find(v=>v.name==='phone')!==undefined">{{msgList.find(v=>v.name==='phone').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Nơi ở hiện tại</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="address" @focus="info('address')">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='address')!==undefined">{{msgList.find(v=>v.name==='address').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Tỉnh/thành phố</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="city"   @focus="info('city')">
                <option selected disabled value="">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','city')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='city')!==undefined">{{msgList.find(v=>v.name==='city').message}}</p>
            </div>
        </div>

              <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Số tài khoản ngân hàng</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="bankaccount" @focus="info('bank-account')">
            </div>
                <p class="help is-danger" v-if="msgList.find(v=>v.name==='bankaccount')!==undefined">{{msgList.find(v=>v.name==='bankaccount').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Tên tài khoản</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="bankaccountname" @focus="info('bank-account-name')">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='bankaccountname')!==undefined">{{msgList.find(v=>v.name==='bankaccountname').message}}</p>
            </div>
        </div>

        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Ngân hàng</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-expanded">
                <select v-model="bank"   @focus="info('bank')">
                <option selected disabled value="">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','bank')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
                <p class="help is-danger" v-if="msgList.find(v=>v.name==='bank')!==undefined">{{msgList.find(v=>v.name==='bank').message}}</p>
            </div>
        </div>

              <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Email (để đăng nhập) </label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="email"  @focus="info('email')" disabled>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='email')!==undefined">{{msgList.find(v=>v.name==='email').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Vị trí công việc</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="type" :disabled="checkLocked()">
                <option selected disabled value="">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','account-type')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='city')!==undefined">{{msgList.find(v=>v.name==='city').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Nhóm</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="team" :disabled="checkLocked()">
                <option selected disabled value="">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','team')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='city')!==undefined">{{msgList.find(v=>v.name==='city').message}}</p>
            </div>
        </div>
    </div>
    </div>
    </div>
    <div class="column is-3">
          <article class="message is-success mt20" v-if="api.getbyid(account.approve).code==='yes'">
              <div class="message-body pt20 pb20 has-text-left">
                  <nav class="level">
                    <div class="level-item has-text-centered">
                        <span class="icon"> <i class="mdi mdi-check is-size-3"> </i> </span>
                    </div>
                    <div class="level-item has-text-centered">
                        <span class="is-size-5"> {{selected.value}} </span>
                    </div>
                  </nav>
        </div>
          </article>
        <article class="message is-primary mt20" v-else>
              <div class="message-body pt10 pb10 has-text-left">
                    <label class="label is-medium pb5">{{this.api.getvalue(this.api.find3var('information','approved','label'))}}</label>
                <div class="field has-addons">
                    <div class="control is-expanded">
                        <div class="select is-fullwidth">
                        <select name="country" v-model="selected">
                            <option v-for="(item,key) in api.filter2var('list', 'approve')" :key="key" :value="item">{{api.getvalue(item)}}</option>
                        </select>
                        </div>
                    </div>
                    <div class="control">
                        <button type="submit" class="button is-primary" @click="approve()">{{this.api.getvalue(this.api.find3var('information','choose','label'))}}</button>
                    </div>
                    </div>
              </div>
        </article>

        <article class="message is-primary mt20" v-if="message!==undefined" :class="message!==undefined? message.type: ''">
        <div class="message-body font-smaller pl15 has-text-justified">
            {{message.message}}
        </div>  
        </article>

        <div>
            <div class="buttons is-centered" :class="message===undefined? 'mt50': ''">
                <button class="button is-primary is-outlined" @click="save()">Lưu lại</button>
            </div>
        </div>
        
        <div class="notification is-warning mt40" v-if="login.type.code==='admin' || login.type.code==='manager'">
            <p class="pb15"> <span class="has-text-dark"> {{account.enable===true? 'Tài khoản đang hoạt động' : 'Tài khoản đang bị khóa' }}</span> </p>
            <button class="button is-outlined is-dark " @click="openAndLock()">{{account.enable===true? 'Khóa tài khoản' : 'Mở tài khoản'}}</button>
        </div>
    </div>
    </div>
    <Footer> </Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'

import mixing from "@/assets/js/mixing.js";
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'

Vue.component('topmenu', TopMenu)
Vue.component('Footer', Footer)

export default {
  data() {
    return {
      tophead: 'Thay đổi thông tin tài khoản',
      content: '',
      message: undefined,
      msgList: [],
      link: '',
      email: undefined,
      name: '',
      dob: undefined,
      sex: '',
      identity: '',
      issuedate: undefined,
      issueplace: '',
      phone: '',
      address: '',
      city: '',
      bankaccount: '',
      bankaccountname: '',
      bank: '',
      password: '',
      passwordretype: '',
      team: '',
      type: '',
      messageError: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      account: undefined,
      selected: undefined
    }
  },

  head() {
    return {
      title: 'Hồ sơ nhân viên'
    }
  },
    
  created() {
    let array = this.connection.checkDataReady(['accountlist'])
    let list = array.filter(v=>v.ready===false)
    if(list.length>0) this.connection.getApi(list)
    else this.fillData()
  },

  mounted() {
    if(this.$refs['name']!== undefined && this.company===undefined) this.$refs['name'].focus()
  },

  watch: {
    'connection.getdataReady' : function(newVal) {
      if(newVal==='success') this.fillData()
      else if(newVal==='error') this.$router.push({ name: 'error'})
    },

    'connection1.getupdateStatus': function(newVal, oldVal) {
      if(newVal===true) {
        this.account = this.connection1.updateRecord
        this.selected = this.$empty(this.account.approve)===true? undefined : this.api.getbyid(this.account.approve)
        this.message = {message: 'Thay đổi thông tin tài khoản thành công', type: 'is-success'}
      }
      else if(newVal==false)
        this.message = {message: 'Có lỗi xẩy ra. Thay đổi thông tin không thành công', type: 'is-danger'}
    }
  },

  computed: {
    api: {
      get: function() {return this.$store.state.api},
      set: function(val) {this.$store.commit('updateApi', {api: val})}
    },

    accountlist: {
      get: function() {return this.$store.state.accountlist},
      set: function(val) {this.$store.commit('updateAccountList', {accountlist: val})}
    },

    login: {
      get: function() {return this.$store.state.login},
      set: function(val) {this.$store.commit("updateLogin", { login: val })}
    },
  },

  methods: {
    openAndLock() {
      var data = JSON.parse(JSON.stringify(this.account))
      data.enable = !data.enable
      this.connection1.update('accountlist', data)
    },

    approve() {
      var data = JSON.parse(JSON.stringify(this.account))
      data.approve = this.selected.id
      this.connection1.update('accountlist', data)
    },

    checkLocked() {
      return (this.login.type.code==='admin' || this.login.type.code==='manager')? false : true
    },

    fillData() {
      if(this.accountlist.length===0) return
      this.account = this.accountlist.find(v=>v.id===parseInt(this.$route.query.id? this.$route.query.id : this.login.id))
      this.selected = this.$empty(this.account.approve)===true? undefined : this.api.getbyid(this.account.approve)
      this.email = this.account.email
      this.name=  this.account.name
      this.dob=  new Date(this.account.dob)
      this.sex=  this.account.sex
      this.identity= this.account.identity
      this.issuedate= new Date(this.account.issue_date)
      this.issueplace= this.account.issue_place
      this.phone= this.account.phone
      this.address= this.account.address
      this.city= this.api.getbyid(this.account.city)
      this.bankaccount= this.account.bank_account
      this.bankaccountname= this.account.bank_account_name
      this.bank= this.$empty(this.account.bank)===true? undefined : this.api.getbyid(this.account.bank)
      this.team = this.$empty(this.account.team)===true? undefined : this.api.getbyid(this.account.team)
      this.type = this.$empty(this.account.type)===true? undefined : this.api.getbyid(this.account.type)
      this.messageError = undefined
      this.msgList = []
    },

    save() {
      this.verified()
      if(this.msgList.length>0) return
      var data = JSON.parse(JSON.stringify(this.account))

      data.name = this.name,
      data.dob = mixing.yyyymmdd(this.dob),
      data.sex = this.sex,
      data.identity = this.identity,
      data.issue_date = mixing.yyyymmdd(this.issuedate),
      data.issue_place = this.issueplace,
      data.phone = this.phone,
      data.address = this.address,
      data.city = this.city.id,
      data.bank_account = this.$empty(this.bank)===true? undefined : this.bankaccount,
      data.bank_account_name = this.bankaccountname,
      data.bank = this.bank===undefined? undefined : this.bank.id,
      data.type = this.type===undefined? undefined : this.type.id
      data.team = this.team===undefined? undefined : this.team.id
      this.connection1.update('accountlist', data)
    },

    info(val) {
      var text = this.api.getvalue(this.api.find3var('information','account-register',val))
      if((text === '' || text === null || text === undefined) === false) {
          this.message =  {message: text, type: 'is-primary'}
      }
    },

    verified() {
      //this.message = undefined
      this.messageError = undefined
      this.msgList = []
      //Name is empty
      if(this.$empty(this.name)===true) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','name-empty'))
          this.msgList.push({name: 'name', message: this.messageError})
      }
      //Name too short
      else if(this.name.trim().length < 5) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','name-invalid'))
          this.msgList.push({name: 'name', message: this.messageError})
      }

      //Date of birth is empty
      if(this.$empty(this.dob)===true) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','dob-empty'))
          this.msgList.push({name: 'dob', message: this.messageError})
      }

      //Date of birth is invalid
      else if(!((new Date(this.dob) !== "Invalid Date") && !isNaN(new Date(this.dob)))) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','dob-invalid'))
          this.msgList.push({name: 'dob', message: this.messageError})
      }
      else {
          var timeDiff = Math.abs(new Date().getTime() - new Date(this.dob).getTime());
          var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24))

          if(diffDays < 15*365) {
              this.messageError =  this.api.getvalue(this.api.find3var('inform','account','dob-15year'))
              this.msgList.push({name: 'dob', message: this.messageError})
          }
      }

      //Sex is empty
      if(this.$empty(this.sex) === true) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','sex-nochoice'))
          this.msgList.push({name: 'sex', message: this.messageError})
      }

      //Indentity is empty
      if(this.$empty(this.identity)===true) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','identity-empty'))
          this.msgList.push({name: 'identity', message: this.messageError})
      }

      //Indentity is too short
      else if(this.identity.trim().length <8) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','identity-length-invalid'))
          this.msgList.push({name: 'identity', message: this.messageError})
      }
      
      //Issue date is empty
      if(this.$empty(this.issuedate)===true) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','identity-issue-empty'))
          this.msgList.push({name: 'issuedate', message: this.messageError})
      }

      //Issue date is invalid
      else if(!((new Date(this.issuedate) !== "Invalid Date") && !isNaN(new Date(this.issuedate)))) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','identity-issue-invalid'))
          this.msgList.push({name: 'issuedate', message: this.messageError})
      }

      //Issue place is empty
      if(this.$empty(this.issueplace)===true) {
        this.messageError = this.api.getvalue(this.api.find3var('inform','account','identity-place-empty'))
        this.msgList.push({name: 'issueplace', message: this.messageError})
      }

      //Phone is empty
      if(this.$empty(this.phone)===true) {
        this.messageError = this.api.getvalue(this.api.find3var('inform','account','phone-empty'))
        this.msgList.push({name: 'phone', message: this.messageError})
      }

      //Phone is invalid

      //Address is empty
      if(this.$empty(this.address)===true) {
        this.messageError = this.api.getvalue(this.api.find3var('inform','account','address-empty'))
        this.msgList.push({name: 'address', message: this.messageError})
      }

      //City is not selected
      if(this.$empty(this.city)===true) {
        this.messageError = this.api.getvalue(this.api.find3var('inform','account','city-empty'))
        this.msgList.push({name: 'city', message: this.messageError})
      }

      if(this.$empty(this.bankaccount)===false) {
          //check is number
        if(isNaN(this.bankaccount)===true || this.bankaccount.toString().trim().length <6) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','bank-account-invalid'))
          this.msgList.push({name: 'bankaccount', message: this.messageError})
        }

        if(this.bankaccountname === '') {
          this.messageError = this.api.getvalue(this.api.find3var('inform','account','account-name-empty'))
          this.msgList.push({name: 'bankaccountname', message: this.messageError})
        }

        if(this.bank === '') {
            this.messageError = this.api.getvalue(this.api.find3var('inform','account','bank-nochoice'))
            this.msgList.push({name: 'bank', message: this.messageError})
        }
      }
    }
  }
}
</script>