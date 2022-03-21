<!-- eslint-disable -->
<template>
<div v-if="dataready===true">
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <div class="pt60"/>
    <div class="columns">
    <div class="column is-9 pl30">
    <div class="mt20 pt20 pb50">
    <div class="columns is-multiline">
            <div class="column is-7 has-text-left"> 
            <div class="field ml10">
            <label class="label">Công ty </label>
            <div class="control has-icons-right">
                <b-autocomplete ref="searchcompany" expanded
                    size="font-datepicker"
                    v-model="company_name"
                    :data="companyFilter"
                    keep-first
                    placeholder="Tìm theo mã hoặc tên"
                    field="label"
                    @typing="companyFilterList"
                    @select="option => option===null? (company_type=undefined) : (company = option, company_type=api.getbyid(company.type).value)">
                    <template slot-scope="props">
                    <div class="media">
                        <div class="media-left has-text-danger">
                            {{ props.option.stock_code }}
                        </div>
                        <div class="media-content">
                            {{ props.option.name}}
                        </div>
                    </div>
                    </template>
                    <template slot="empty">Không có giá trị thỏa mãn</template>
                    </b-autocomplete>
            </div>
             <p class="help is-danger" v-if="msgList.find(v=>v.name==='company')!==undefined">{{msgList.find(v=>v.name==='company').message}}</p>
            </div>
        </div>

        <div class="column is-3 has-text-left"> 
            <div class="field ml10">
            <label class="label">Loại doanh nghiệp </label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="company_type" disabled>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='company_type')!==undefined">{{msgList.find(v=>v.name==='company_type').message}}</p>
            </div>
        </div>

        <div class="column is-2 has-text-left"> 
            <div class="field ml10">
            <label class="label">Năm</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="text" placeholder="" v-model="year">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='year')!==undefined">{{msgList.find(v=>v.name==='year').message}}</p>
            </div>
        </div>

        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Kỳ báo cáo</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="report_period">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','report-period')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='report_period')!==undefined">{{msgList.find(v=>v.name==='report_period').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Loại báo cáo</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="report_type">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','report-type')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='report_type')!==undefined">{{msgList.find(v=>v.name==='report_type').message}}</p>
            </div>
        </div>

        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Tên báo cáo</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="report_name">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in report_list" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='report_name')!==undefined">{{msgList.find(v=>v.name==='report_name').message}}</p>
            </div>
        </div>
        
        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Ngày giao việc</label>
            <div class="control">
            <div>
                <b-datepicker   size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="assign_date"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='assign_date')!==undefined">{{msgList.find(v=>v.name==='assign_date').message}}</p>
            </div> 
            </div>
        </div>
        
        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Ngày đến hạn</label>
            <div class="control">
            <div>
                <b-datepicker   size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="due_date"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='due_date')!==undefined">{{msgList.find(v=>v.name==='due_date').message}}</p>
            </div> 
            </div>
        </div>
 
        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
             <b-checkbox type='is-primary' class="mt30" v-model="priority"><span class="ml5"> Ưu tiên cao </span></b-checkbox>
            </div>
        </div>

        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Người giao việc</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="assigner">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in accountlist.filter(v=>v.enable===true)" :key="i" :value="v">{{v.name}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='assigner')!==undefined">{{msgList.find(v=>v.name==='assigner').message}}</p>
            </div>
        </div>

        <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Người nhận việc</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="recipient">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in accountlist.filter(v=>v.enable===true)" :key="i" :value="v">{{v.name}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='recipient')!==undefined">{{msgList.find(v=>v.name==='recipient').message}}</p>
            </div>
        </div>
    </div>
    </div>
    </div>
    <div class="column is-3">
        <article class="message is-primary mt20" v-if="message!==undefined" :class="message!==undefined? message.type: ''">
        <div class="message-body font-smaller pl15 has-text-justified">
            {{message.message}}
        </div>  
        </article>

        <div>
            <div class="buttons is-centered" :class="message===undefined? 'mt50': ''">
                <button class="button is-primary is-outlined" @click="save()">Lưu lại</button>
                <button class="button is-primary is-outlined ml20" @click="reset()">Nhập lại</button>
            </div>
        </div>
    </div>
    </div>
    <div class="mt20 pb5"/>
    <Footer> </Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'

import mixing from "@/assets/js/mixing.js";
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'
import axios from 'axios'

Vue.component('topmenu', TopMenu)
Vue.component('Footer', Footer)

export default {
  data() {
    return {
      tophead: 'Giao việc mới',
      company: undefined,
      message: undefined,
      msgList: [],
      report_name: undefined,
      report_type: undefined,
      report_period: undefined,
      assign_date: undefined,
      due_date: undefined,
      company_type: undefined,
      priority: undefined,
      company_name: undefined,
      recipient: undefined,
      assigner: undefined,
      year: undefined,
      messageError: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      connection2: this.$connection(),
      dataready: undefined,
      companyFilter: [],
      report_list: []
    }
  },
  
  head() {
    return {
      title: 'Thêm mới công việc nhập dữ liệu'
    }
  },

  created() {
    let array = this.connection.checkDataReady(['accountlist', 'companylist'])
    let list = array.filter(v=>v.ready===false)
    if(list.length>0) this.connection.getApi(list)
    else this.dataready = true
    this.report_list = this.api.data.filter(v=>v.category==='list' && v.classify==='report-name' && (v.code!=='TMTC'))
  },

  mounted() {
    if(this.$refs['name']!== undefined && this.company===undefined) this.$refs['name'].focus()
  },

    watch: {
      'connection.getdataReady' : function(newVal) {
        if(newVal==="success") this.dataready = true
        else if(newVal==="error") this.$router.push({path: "/error"})
      },

      'connection1.getdataReady' : function(newVal) {
        if(newVal==="success") {
          let list = this.connection1.getbatchData[0].data
          let task = list.length>0? list[0] : undefined
          if(task===undefined) this.insertData()
          else this.message = {message: 'Công việc này đã cồn tại. Giao việc không thành công', type: 'is-danger'}
        }
        else if(newVal==="error") this.$router.push({path: "/error"})
      },

      'connection2.getupdateStatus': function(newVal, oldVal) {
        if(newVal) {                
          this.message = {message: 'Giao việc mới thành công', type: 'is-success'}
        }
        else if(newVal==false)
          this.message = {message: 'Có lỗi xẩy ra. Giao việc mới không thành công', type: 'is-danger'}
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

      companylist: {
        get: function() {return this.$store.state.companylist},
        set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
      }
    },

    methods: {
      reset() {
        this.company =  undefined
        this.message =  undefined
        this.msgList =  []
        this.report_name =  undefined
        this.report_type =  undefined
        this.report_period =  undefined
        this.assign_date =  undefined
        this.due_date =  undefined
        this.company_type =  undefined
        this.priority =  undefined
        this.company_name =  undefined
        this.recipient =  undefined
        this.assigner =  undefined
        this.year =  undefined
        this.messageError =  undefined
      },

      companyFilterList(text) {
        let self = this
        mixing.delay(function() {
          self.companyFilter = mixing.companyFilter(self.companylist, text, 'full')}, 20)
      },

      save() {
        this.verified()
        if(this.msgList.length>0) return
        //check is existed
        let filter = {year: this.year, report_name: this.report_name.id, report_type: this.report_type.id,
        report_period: this.report_period.id, company: this.company.id}
        let found = {name: 'tasklist', url: 'data/Task', params: {filter:filter}}
        this.connection1.getApi([found])
      },

      insertData() {
        let name = this.report_name.code
        if(name==='LCTT-TT' || name==='LCTT-GT') name = 'LCTT'

        let unit = this.api.find3var('unit-price',this.api.getbyid(this.company.type).code, name).value
        let data = {
            "Id" : '',
            "company": this.company.id,
            "year": this.year,
            "report_period": this.report_period.id,
            "report_type": this.report_type.id,
            "report_name": this.report_name.id,
            "assigner":  this.assigner.id,
            "recipient": this.recipient.id,
            "assign_date": new Date(this.assign_date),
            "due_date": new Date(this.due_date),
            "status": this.api.find3var('list', 'task-status', 'not-yet-entered').id,
            "priority": this.priority,
            company_factor: this.company.factor,
            unit_price: unit,
            into_money : this.company.factor * unit
        }
        this.connection2.insert('tasklist', data)
      },

        verified() {
          this.message = undefined
          this.messageError = undefined
          this.msgList = []
          
            //company
          if(this.$empty(this.company)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','company'))
            this.msgList.push({name: 'company', message: this.messageError})
          }
          
          //year
          if(this.$empty(this.year)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','year'))
            this.msgList.push({name: 'year', message: this.messageError})
          }
          else if(mixing.isNumber(this.year)===false || this.year<1980) {
            this.msgList.push({name: 'year', message: 'Năm không hợp lệ'})
          }

          //report-period
          if (this.$empty(this.report_period)) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','report-period'))
            this.msgList.push({name: 'report_period', message: this.messageError})
          }

          //report_type
          if(this.$empty(this.report_type) === true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','report-type'))
            this.msgList.push({name: 'report_type', message: this.messageError})
          }

          //report_name is empty
          if(this.$empty(this.report_name)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','report-name'))
            this.msgList.push({name: 'report_name', message: this.messageError})
          }

          //assigner
          if(this.$empty(this.assigner)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','assigner'))
            this.msgList.push({name: 'assigner', message: this.messageError})
          }

          //recipient
          if(this.$empty(this.recipient)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','recipient'))
            this.msgList.push({name: 'recipient', message: this.messageError})
          }

           //assign date
        if(this.$empty(this.assign_date)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','assign-date'))
            this.msgList.push({name: 'assign_date', message: this.messageError})
        }
        //assign date is invalid
        else if(!((new Date(this.assign_date) !== "Invalid Date") && !isNaN(new Date(this.assign_date)))) {
          this.messageError = this.api.getvalue(this.api.find3var('inform','task','assign-date-invalid'))
          this.msgList.push({name: 'assign_date', message: this.messageError})
        }

        if(this.$empty(this.due_date)===true) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','due-date'))
            this.msgList.push({name: 'due_date', message: this.messageError})
        }

        //due date is invalid
        else if(!((new Date(this.due_date) !== "Invalid Date") && !isNaN(new Date(this.due_date)))) {
            this.messageError = this.api.getvalue(this.api.find3var('inform','task','due-date-invalid'))
            this.msgList.push({name: 'due_date', message: this.messageError})
        }

        else if(this.msgList.find(v=>v.name==='assign_date')===undefined) {
            if(mixing.compare(this.assign_date, this.due_date)===1) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','task','due-date-greater'))
                this.msgList.push({name: 'due_date', message: this.messageError})
            }
        }
      },

      sendEmail() {
        //send email inform to manager
        let  headers = {"Content-Type": "application/json"}
        let data = {
            'subject': this.api.getvalue(this.api.find3var('email','register-inform-user','subject')),
            'content': this.api.getvalue(this.api.find3var('email','register-inform-user','content')),
            'to': this.email
        }
        axios.post(mixing.path + 'send-email/', data, headers)
        
        var content  = this.api.getvalue(this.api.find3var('email','register-inform-manager','content'))
        content += '\\n'
        content += this.createlink()
        content += '\\n\\n'
        content += this.api.getvalue(this.api.find3var('footer','company','name'))
        
        data = {
            'subject': this.api.getvalue(this.api.find3var('email','register-inform-manager','subject')),
            'content': content,
            'to': this.api.getvalue(this.api.find3var('email','register-new','receiver')),
        }
        axios.post(mixing.path + 'send-email/', data, headers)
      },

      createlink() {
        var key =  this.api.guid()
        let routeData = this.$router.resolve({name: 'account-edit', query: {account: this.account.id, token: key}});
        var href = window.location.href 
        href = href.substring(0, href.indexOf(this.$route.path)) + routeData.href

        var data =  {
          'guid' : key,
          'route_name': 'account-register',
          'query': 'token: ' + key,
          'link': href,
          'valid_from':  new Date(),
          'valid_to':  new Date(Date.now() + 2 * 24*60*60*1000),
          'action_result': this.api.getval(this.api.find3var('list','action-result','initialize'), 'id'),
          'detail': 'Account register link'
        }

        this.connection2.insert('link', data, 'all', false)
        return href
      },
    }
}
</script>