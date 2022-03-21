<!-- eslint-disable -->
<template>
<div>
    <TopMenu v-bind="{type: 'tophead', tophead: tophead}"></TopMenu>
    <div class="pt60"/>
    <div class="columns">
    <div class="column is-9 pl30">
    <div class="box">
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
            <div class="control is-expanded">
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
            <div class="select font-smaller is-fullwidth">
                <select v-model="bank" @focus="info('bank')">
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
                <input class="input font-smaller" type="text" placeholder="" v-model="email"  @focus="info('email')">


            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='email')!==undefined">{{msgList.find(v=>v.name==='email').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Mật khẩu</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="password" placeholder="" v-model="password"  @focus="info('password')">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='password')!==undefined">{{msgList.find(v=>v.name==='password').message}}</p>
            </div>
        </div>

             <div class="column is-4 has-text-left mt5"> 
            <div class="field ml10">
            <label class="label">Nhập lại mật khẩu</label>
            <div class="control has-icons-right">
                <input class="input font-smaller" type="password" placeholder="" v-model="passwordretype"  @focus="info('password-retype')">
            </div>
               <p class="help is-danger" v-if="msgList.find(v=>v.name==='passwordretype')!==undefined">{{msgList.find(v=>v.name==='passwordretype').message}}</p>
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

        <div v-if="account===undefined">
            <div class="buttons is-centered" :class="message===undefined? 'mt50': ''">
                <button class="button is-primary is-outlined" @click="checkData()">Lưu lại</button>
                <button class="button is-primary is-outlined ml20" @click="reset()">Nhập lại</button>
            </div>
        </div>
        <div class="notification is-primary is-light" v-else>
            Thông tin tài khoản đã được lưu trong hệ thống. Bộ phận chuyên môn của chúng tôi sẽ sớm phản hồi yêu cầu của bạn. Xin cảm ơn.   
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
import axios from 'axios'

export default {
    components: {
      TopMenu,
      Footer
    },

    data() {
        return {
            tophead: 'Mở tài khoản mới',
            subject: undefined,
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
            messageError: undefined,
            connection: this.$connection(),
            connection1: this.$connection(),
            connection2: this.$connection(),
            connection3: this.$connection(),
            connection4: this.$connection(),
            connection5: this.$connection(),
            account: undefined
        }
    },

    head() {
        return {
            title: 'Đăng ký tài khoản'
        }
    },

    created() {
        this.subject =  this.api.getvalue(this.api.find3var('subtitle','account','link'))
        let array = this.connection.checkDataReady(['accountlist'])
        let list = array.filter(v=>v.ready===false)
        if(list.length>0) this.connection.getApi(list)
    },

    mounted() {
        if(this.$refs['name']!== undefined && this.company===undefined) this.$refs['name'].focus()
    },

    watch: {
        'connection1.getupdateStatus': function(newVal, oldVal) {
            if(newVal) {
                this.account = this.connection1.updateRecord
                this.message = {message: 'Tạo tài khoản mới thành công.', type: 'is-success'}
                this.sendEmail()
                this.setLinkExpiry()
            }
            else if(newVal==false)
                this.message = {message: 'Lỗi. Tạo tài khoản không thành công', type: 'is-danger'}
        },

        'connection3.getdataReady' : function(newVal) {
            if (newVal==='success') {
                let data = this.connection3.getbatchData[0].data
                let found  = data.length>0? data[0] : undefined
                if(found!==undefined) {
                    found.enable = false
                    this.connection4.update('link', found)
                }
            }
        },

        'connection5.getdataReady' : function(newVal) {
            if (newVal==='success') {
                const hash = this.connection5.getbatchData.find(v=>v.name==='hash').data[0]
                var data =  {
                'name': this.name,
                'dob': mixing.yyyymmdd(this.dob),
                'sex': this.sex,
                'identity': this.identity,
                'issue_date': mixing.yyyymmdd(this.issuedate),
                'issue_place': this.issueplace,
                'phone': this.phone,
                'address': this.address,
                'city': this.city.id,
                'bank_account': (this.bankaccount === ''? null: this.bankaccount),
                'bank_account_name': this.bankaccountname,
                'bank':  this.bank.id,
                'email': this.email.toLowerCase(),
                'password': hash,
                'approve': this.api.getval(this.api.find3var('list','approve','wait'),'id'),
                'type': this.api.getval(this.api.find3var('list','account-type','ctv'),'id')
                }
                this.connection1.insert('accountlist', data)
            }
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
    },

    methods: {
        checkData() {
            if(!this.verified()) return
            let found = {name: 'hash', url: 'get-hash/' + this.password, params: {}}
            this.connection5.getApi([found])
        },

        reset() {
            this.email = ''
            this.name= ''
            this.dob= undefined
            this.sex= ''
            this.identity= ''
            this.issuedate= undefined
            this.issueplace=
            this.phone= ''
            this.address= ''
            this.city= ''
            this.bankaccount= ''
            this.bankaccountname= ''
            this.bank= ''
            this.password= ''
            this.passwordretype= ''
            this.messageError = undefined
            this.msgList = []
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
                if( isNaN(this.bankaccount.trim()) === true || this.bankaccount.trim().length <6) {
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

            //Email is empty
            if(this.$empty(this.email)===true) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','email-empty'))
                this.msgList.push({name: 'email', message: this.messageError})
            }
            else {
                //Email is invalid
                var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                if(re.test(String(this.email).toLowerCase()) === false) {
                    this.messageError = this.api.getvalue(this.api.find3var('inform','account','email-invalid'))
                    this.msgList.push({name: 'email', message: this.messageError})
                }
            
                //Email is existed
                if(re.test(String(this.email).toLowerCase())===true && this.accountlist!==undefined) {
                    if(this.accountlist.find(v=>v.email===this.email.trim().toLowerCase()) !== undefined) {
                        this.messageError = this.api.getvalue(this.api.find3var('inform','account','email-existed'))
                        this.msgList.push({name: 'email', message: this.messageError})
                    }
                }
            }

            //Password is empty
            if(this.$empty(this.password)===true) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','password-empty'))
                this.msgList.push({name: 'password', message: this.messageError})
            }

            //Password is invalid
            else if(this.password.trim().length < 6) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','password-invalid'))
                this.msgList.push({name: 'password', message: this.messageError})
            }

            //Password retype is empty
            if(this.$empty(this.passwordretype)===true) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','password-retype-empty'))
                this.msgList.push({name: 'passwordretype', message: this.messageError})
            }

            //Password retype is invalid
            else if(this.passwordretype.trim().length < 6) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','password-retype-invalid'))
                this.msgList.push({name: 'passwordretype', message: this.messageError})
            }

            //Password retype & password is difference
            else if(this.passwordretype !== this.password) {
                this.messageError = this.api.getvalue(this.api.find3var('inform','account','password-retype-difference'))
                this.msgList.push({name: 'passwordretype', message: this.messageError})
            }

            return this.msgList.length>0? false : true
        },

        sendEmail() {
            //send email inform to manager
            let  headers = {"Content-Type": "application/json"}
            let data = {
                'subject': this.api.getvalue(this.api.find3var('email','register-inform-user','subject')),
                'content': this.api.getvalue(this.api.find3var('email','register-inform-user','content')),
                'to': this.email
            }
            axios.post(this.connection.path + 'send-email/', data, headers)
            
            var content  = this.api.getvalue(this.api.find3var('email','register-inform-manager','content'))
            content += '\n'
            content += this.createlink()
            content += '\n\n'
            content += this.api.getvalue(this.api.find3var('footer','company','name'))
            
            data = {
                'subject': this.api.getvalue(this.api.find3var('email','register-inform-manager','subject')),
                'content': content,
                'to': this.api.getvalue(this.api.find3var('email','register-new','receiver')),
            }
            axios.post(this.connection.path + 'send-email/', data, headers)
        },

        createlink() {
            var key =  this.api.guid()
            let routeData = this.$router.resolve({path: '/profile', query: {id: this.account.id, token: key}});
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

            this.connection2.insert('link', data)
            return href
        },

        setLinkExpiry() {
            let token = this.$route.query.token
            let found = {name: 'link', link: 'Link', params: {type: 'serializer', filter:{'guid' : token}}}
            this.connection3.getApi([found])
        }
    }
}
</script>