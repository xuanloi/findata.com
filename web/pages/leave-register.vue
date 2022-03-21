<!-- eslint-disable -->
<template>
<div>
    <topmenu v-bind="{type: 'tophead', tophead: this.tophead}"></topmenu>
    <div class="pt60"/>
    
    <section class="hero is-paddingless is-marginless">
    <div class="hero-body pt30 pb30 pl0 pr0">
        <div class="columns">
            <div class="column is-8 is-offset-2">
            <div class="columns is-multiline">
             <div class="column is-4 has-text-left mt5"> 

        <div class="field ml10">
            <label class="label">Từ ngày</label>
            <div class="control">
            <div>
                <b-datepicker size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="fdate"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='fdate')!==undefined">{{msgList.find(v=>v.name==='fdate').message}}</p>
            </div> 
            </div>

        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Đến ngày</label>
            <div class="control">
            <div>
                <b-datepicker   size="font-datepicker"
                    ref="datepicker"
                    placeholder="Chọn ngày"
                    v-model="tdate"
                    >
                </b-datepicker>
            </div>
            <p class="help is-danger" v-if="msgList.find(v=>v.name==='tdate')!==undefined">{{msgList.find(v=>v.name==='tdate').message}}</p>
            </div> 
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Loại nghỉ phép</label>
            <div class="control is-expanded is-fullwidth">
            <div class="select font-smaller is-fullwidth">
                <select v-model="type">
                <option selected disabled value="undefined">Chọn... </option>
                <option v-for="(v,i) in api.filter2var('list','leave-type')" :key="i" :value="v">{{v.value}}</option>
                </select>
            </div>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='type')!==undefined">{{msgList.find(v=>v.name==='type').message}}</p>
            </div>
        </div>
        </div>
        
        <div class="column is-12 has-text-left  mt5">
             <div class="field">
            <label class="label">Lý do</label>
            <div class="control is-expanded is-fullwidth">
             <textarea class="textarea" rows="2" placeholder="" v-model="reason"></textarea>
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='city')!==undefined">{{msgList.find(v=>v.name==='city').message}}</p>
            </div>

            <p class="mt20" v-if="message!==undefined">
               <span :class="message.type"> {{message.message}}</span>
            </p>
           
        </div>
            <div class="column is-12 has-text-left  mt5">
                <div class="buttons is-centered mt10">
                    <button class="button is-primary is-outlined" @click="register()">Lưu lại</button>
                    <button class="button is-primary is-outlined ml20" @click="reset()">Nhập lại</button>
                </div>
            </div>
        </div>
        </div>
    </div>
    </section>

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
            tophead: 'Đăng ký nghỉ phép',
            msgList: [],
            reason: undefined,
            fdate: undefined,
            tdate: undefined,
            type: undefined,
            messageInfo: undefined,
            message: undefined,
            connection: this.$connection(),
            connection1: this.$connection()
        }
    },

    head() {
        return {
            title: 'Đăng ký nghỉ phép'
        }
    },
    
    created() {
        let array = this.connection.checkDataReady(['leavelist'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) this.connection.getApi(list)
    },

    watch: {
        'connection1.getupdateStatus': function(newVal, oldVal) {
            if(newVal) {
                this.account = this.connection1.updateRecord
                this.message = {message: 'Đăng ký nghỉ phép thành công', type: 'has-text-primary'}
            }
            else if(newVal==false)
                this.message = {message: 'Có lỗi xẩy ra. Đăng ký nghỉ phép không thành công', type: 'has-text-danger'}
        }
    },

    computed: {
        api: {
            get: function() {return this.$store.state.api},
            set: function(val) {this.$store.commit('updateApi', {api: val})}
        },

        leavelist: {
            get: function() {return this.$store.state.leavelist},
            set: function(val) {this.$store.commit("updateLeaveList", { leavelist: val })}
        },

        login: {
            get: function() {return this.$store.state.login},
            set: function(val) {this.$store.commit('updateLogin', {login: val})}
        },
    },

    methods: {
        reset() {
            this.fdate = undefined
            this.tdate = undefined
            this.type = undefined
            this.reason = undefined
            this.message = undefined
            this.msgList = []
        },

        register() {
            this.validate()
            if(this.msgList.length>0) return
            let data = {}

            //update api
            data.account = this.login.id
            data.type = this.type.id
            data.start_date = mixing.yyyymmdd(new Date(this.fdate)),
            data.end_date 	=  mixing.yyyymmdd(new Date(this.tdate)),
            data.reason 	=  this.reason,
            data.status 	=  this.api.getval(this.api.find3var('list', 'approve', 'wait'), 'id')
            this.connection1.insert('leavelist', data)
        },

        validate() {
            this.msgList = []
            this.message = undefined
            if(this.$empty(this.fdate)===true) {
                this.messageInfo = this.api.getvalue(this.api.find3var('inform','task','date-invalid'))
                this.msgList.push({name: 'fdate', message: this.messageInfo, type: 'error'})
            }

            if(this.$empty(this.tdate)===true) {
                this.messageInfo = this.api.getvalue(this.api.find3var('inform','task','from-to-date'))
                this.msgList.push({name: 'tdate', message: this.messageInfo, type: 'error'})
            }

            if(this.msgList.length===0) {
                if(mixing.compare(this.fdate, this.tdate)===1) {
                    this.messageInfo = 'Giá trị [Đến ngày] phải lớn hơn [Từ ngày]'
                    this.msgList.push({name: 'tdate', message: this.messageInfo, type: 'error'})
                }
            }

            if(this.$empty(this.type)) {
                this.messageInfo = this.api.getvalue(this.api.find3var('inform','leave','type'))
                this.msgList.push({name: 'type', message: this.messageInfo, type: 'error'})
            }
            
            //Check existeds
            if(this.leavelist===undefined) return
            var filter = this.leavelist.filter(v => (v.account === this.login.id))

            filter.forEach(v => {
                let r11 = mixing.compare(new Date(v.start_date), new Date(mixing.yyyymmdd(this.fdate)))
                let r12 =  mixing.compare(new Date( v.end_date), new Date(mixing.yyyymmdd(this.fdate)))
                let r21 = mixing.compare(new Date(v.start_date), new Date(mixing.yyyymmdd(this.tdate)))
                let r22 = mixing.compare(new Date( v.end_date), new Date(mixing.yyyymmdd(this.tdate)))

                if((r11===0 || r12===0) || (r11===1 && r12===-1)) {
                    this.messageInfo = this.api.getvalue(this.api.find3var('inform','leave','existed'))
                    this.msgList.push({name: 'fdate', message: this.messageInfo, type: 'error'})
                } 
  
                if((r21===0 || r22===0) || (r21===1 && r22===-1))  {
                    this.messageInfo = this.api.getvalue(this.api.find3var('inform','leave','existed'))
                    this.msgList.push({name: 'tdate', message: this.messageInfo, type: 'error'})
                }
            })
        }
    }
}
</script>