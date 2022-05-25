<template>
  <nav class="navbar is-dark is-fixed-top" role="navigation" aria-label="main navigation">
   <div class="navbar-brand">
  <div class="pl10">
<nuxt-link :to="{path: (login? '/' : '/login')}">
  <div class="is-vertical-center">
  <figure class="image is-48x48">
  <img :src="require('@/assets/images/logo.png')" alt="logo"  style="vertical-align: middle;">
  </figure>
  </div>
</nuxt-link> 
   </div>
<a role="button" class="navbar-burger" data-target="navMenu" aria-label="menu" aria-expanded="false" @click="responsiveMenu">
  <span aria-hidden="true"></span>
  <span aria-hidden="true"></span>
  <span aria-hidden="true"></span>
</a>
   </div>

<div id="navMenu" class="navbar-menu pl10">
<div class="navbar-start" style="flex-grow: 1; justify-content: center" v-if="currentType==='tophead'">
  <div class="navbar-item" style="font-size:18px" v-if="tophead? tophead.indexOf('<')>=0 : false">
    <component :is="compiledComponent(tophead)" @clickevent="$emit($event)"/>
  </div>
   <span class="navbar-item" style="font-size:18px" v-else> {{tophead===undefined? '' : tophead}}</span>
</div>

<div class="navbar-start" style="flex-grow: 1; justify-content: center" v-else-if="currentType==='search'">
<div class="navbar-item">
<div class="field has-addons has-addons-centered">
<p class="control">
  <span class="select is-warning">
  <select v-model="searchType">
    <option value="company">Mã CK</option>
    <option value="task">ID giao việc</option>
    <option value="account">Người nhập</option>
  </select>
  </span>
</p>

<div class="control has-icons-right" style="width:500px">
<b-autocomplete ref="searchbox" expanded
size="is-warning"
v-model="keyword"
:data="objectFilter"
keep-first
field="label"
@typing="objectFilterList"
@select="option => option===null? (selected=undefined) : (selected = option, startSearch())">
  <template slot-scope="props">
  <div class="media">
  <div class="media-left has-text-danger">
  {{ searchType==='company'?  props.option.stock_code :  props.option.id}}
  </div>
  <div class="media-content">
  {{ props.option.name}}
  </div>
  </div>
  </template>
  <template slot="empty">Không có giá trị thỏa mãn</template>
  </b-autocomplete>

<span class="icon is-right">
<i class="mdi mdi-magnify has-text-grey-light" style="font-size:22px;"></i>
</span>
</div>
</div>
</div>
<div class="navbar-item ml20" v-if="$route.name!=='search-result'">
<a class="button is-warning" @click="closeSearch()">
  <i class="mdi mdi-close is-size-5"></i>
</a>
</div>
 </div>

  <div class="navbar-start" v-else>
  <router-link :to="{ path: '/finance/task-list'}" class="navbar-item">
  <span class="font-smaller"> {{api.find3var('menu', 'menu', 'menu2').value}}</span>
  <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined is-warning is-rounded is-small font-smaller" v-html="numList"> </a> </span>
   </router-link>

  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','not-yet-entered').id}}"  
  class="navbar-item">
  <span class="font-smaller"> {{api.find3var('menu','menu','menu4').value}} </span>
   <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined is-warning is-rounded is-small font-smaller" v-html="numPending"> </a> </span></router-link>
  
  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','entered').id}}"
   class="navbar-item"><span class="font-smaller"> {{api.find3var('list','task-status','entered').value}} </span>
     
 <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined is-warning is-rounded is-small font-smaller" v-html="numTyping"> </a> </span></router-link>

  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','waiting-approve').id}}"
   class="navbar-item"> <span class="font-smaller"> {{api.find3var('list','task-status','waiting-approve').value}} </span>  
    <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined is-warning  is-rounded is-small font-smaller" v-html="numWaiting1"> </a> </span></router-link>
   
  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','waiting-approve-2').id}}"
   class="navbar-item"> <span class="font-smaller"> {{api.find3var('list','task-status','waiting-approve-2').value}} </span>
    <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined  is-warning is-rounded is-small font-smaller" v-html="numWaiting2"> </a> </span></router-link>
  
  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','approved').id}}" 
  class="navbar-item">
   <span class="font-smaller"> {{api.find3var('menu','menu','menu3').value}}  </span>
  <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined  is-warning is-rounded is-small font-smaller" v-html="numApproved"> </a> </span>
  </router-link>

  <router-link :to="{ path: '/finance/task-list', query: {status: api.find3var('list','task-status','retype').id}}"
   class="navbar-item"> <span class="font-smaller"> {{api.find3var('list','task-status','retype').value}} </span>
    <span class="ml5 is-size-7">
   <a class="button pl7 pr7 is-outlined is-warning is-rounded is-small font-smaller" v-html="numRetype"> </a> </span></router-link>
  </div>

  <div class="navbar-end" v-if="login">
  <a @click="openSearch()" class="navbar-item">
  <i class="mdi mdi-magnify" style="font-size:23px;"> </i>    
  </a>

    <div class="navbar-item px-4">
  <div class="dropdown is-hoverable is-boxed mt5" :class="ismobile? 'is-left' : 'is-right'">
  <div class="dropdown-trigger">
          <span class="icon" v-if="notification? notification.length>0: 1<0">
        <i class="mdi mdi-bell-ring-outline has-text-warning fs26"></i>
      </span>
              <span class="icon" v-else>
        <i class="mdi mdi-bell-outline has-text-white fs26"></i>
      </span>
  </div>
  <div class="dropdown-menu" id="dropdown-menu4" role="menu">
    <div class="dropdown-content pt20 pb20" style="width:320px; max-height: 90vh;">
         <div class="px-3 py-2">
        <template v-if="notification? notification.length>0 : 1<0">
            <a class="media" v-for="(v,i) in notification" :key="i" @click="openlink(v, i)">
    <figure class="media-left">
 <div class="number-circle" style="width:40px; height:40px; padding:4px" v-if="!v.sender__avatar">
      <div class="is-vertical-center">
         <b-tooltip :label="v.sender__name" type="is-dark">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + v.sender__name.substring(0,1).toLowerCase() + ' fs30'"></i>
      </span>
         </b-tooltip>
      </div>
      </div>
     <figure class="image" style="width:40px; height:40px" v-else>
       <b-tooltip :label="v.sender__name" type="is-dark">
      <img class="is-rounded" :src="connection.path + 'static/images/' + v.sender__avatar"/>
       </b-tooltip> 
    </figure>
  </figure>
  <div class="media-content">
      <p class="fs15 has-text-dark" v-html="v.type__value"></p>
       <p class="has-text-dark fs13 fb500 has-text-primary">{{formatDate(v.create_time)}}</p>
  </div>
  </a>
      </template>
        <template v-else>
         <p class="fs16 has-text-primary has-text-centered"> Hết thông báo </p>
        </template>
          </div>
    </div>
    </div>
    </div>
  </div>

  <router-link :to="{ path: '/help/page'}" class="navbar-item">
  <span class="is-vertical-center">
   <i class="mdi mdi-help" style="font-size:24px;"> </i>  
  </span>
  </router-link>

  <a @click="action()" class="navbar-item" v-if="enableDownload">
    <span class="icon"> <i class="mdi mdi-arrow-collapse-down" style="font-size:25px;"></i> </span>
  </a>

    <div class="vertical-center ml10 mr10">
  <div class="dropdown is-hoverable is-boxed mt5" :class="ismobile? 'is-left' : 'is-right'">
  <div class="dropdown-trigger">
      <div class="number-circle" style="width:36px; height:36px;padding:1px;" v-if="!login.avatar">
      <div class="is-vertical-center">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + login.name.substring(0,1).toLowerCase() + ' is-size-2'"></i>
      </span>
      </div>
    </div>

  <figure class="image" style="width:36px; height:36px" v-else>
    <img class="is-rounded" :src="connection.path + 'static/images/' + login.avatar"/>
    </figure>
  </div>
  <div class="dropdown-menu" id="dropdown-menu4" role="menu">
    <div class="dropdown-content pt20 pb20" style="width:250px">
            <div class="field is-grouped is-grouped-centered mt10">
            <div class="number-circle" style="width:50px; height:50px;padding:3px;" v-if="!login.avatar">
      <div class="is-vertical-center">
        <span class="icon has-text-primary">
        <i :class="'mdi mdi-alpha-' + login.name.substring(0,1).toLowerCase() + ' is-size-2'"></i>
      </span>
      </div>
  </div>
  <figure class="image" style="width:80px; height:80px" v-else>
    <img class="is-rounded" :src="connection.path + 'static/images/' + login.avatar"/>
    </figure>
   </div>
    <p class="fb500 fs16 has-text-centered has-text-primary"> {{login.name}}
      <nuxt-link to="/avatar"> <span class="icon fs20"> <i class="mdi mdi-camera-outline"/> </span></nuxt-link>
    </p>
  <div class="field is-grouped is-grouped-centered mt5">
  <div class="control">
          <p class="mt20">
          <a @click="$router.push({path: '/change-password'})">
            <span class="icon">
      <i class="mdi mdi-lock-outline fs24"/>
    </span>
    <span class="ml10"> Đổi mật khẩu </span>
          </a>
      </p>
    </div>
    </div>
    <div class="field is-grouped is-grouped-centered">
  <div class="control">
      <p class="mt10">
      <a @click="login=undefined; $router.push({path: '/login'})">
        <span class="icon">
      <i class="mdi mdi-arrow-left fs24"/>
    </span>
    <span class="ml10"> Đăng xuất </span>
          </a>
      </p>
    </div>
    </div>
    </div>
    </div>
  </div>
  </div>
  </div>
   </div>
  </nav> 
</template>

<script>
import mixing from '@/assets/js/mixing.js'
import socket from '~/plugins/socket.io.js'
export default {
props: ['type', 'tophead', 'enableDownload'],
  data() {
    return {
      numApproved: 0,
      numWaiting1: 0,
      numWaiting2: 0,
      numPending: 0,
      numTyping: 0,
      numRetype: 0,
      numList: 0,
      point: 0,
      item: undefined,
      connection: this.$connection(),
      connection1: this.$connection(),
      keyword: undefined,
      objectFilter: [],
      selected: undefined,
      currentType: undefined,
      searchType: 'company',
    }
  },

  beforeMount () {
    socket.on('new-message', (message) => {
      if(message.name==='notification') {
        let filter = message.data.filter(v=>v.receiver===this.login.id)
        if(filter.length>0) {
          if(this.notification? this.notification.find(v=>v.id===message.data.id) : false) return
          this.notification = filter.concat(this.notification)
          if(!this.hasnews) this.hasnews = true
          let self = this
          this.$buefy.snackbar.open({
            duration: 10000,
            message: this.notification[0].sender__name + ' ' + this.notification[0].type__value,
            type: 'is-primary',
            position: 'is-bottom-right',
            actionText: 'Mở',
            queue: false,
            onAction: () => self.openlink(self.notification[0], 0)
        })
        }
      } else if(message.name==='update-task' && this.$route.name==='finance-task-list' && this.pagetask) {
        this.updateTask(this.$copy(message.data))
      }
    })
  },

  created() {
    if(this.type!==undefined) this.currentType = this.$copy(this.type)
    if(!this.login) return
    //get task summary
    var roleid = this.$empty(this.login.type)===false? this.login.type.id : ''
    var teamid = this.$empty(this.login.team)===false? this.login.team.id : ''
    var condition = ''
    if(this.api.getval(this.api.find3var('list','account-type','admin'), 'id') === roleid || 
    this.api.getval(this.api.find3var('list','account-type','manager'), 'id') === roleid) {
      condition = '1=1'
    }
    else if(this.api.getval(this.api.find3var('list','account-type','teamlead'), 'id') === roleid) {
      condition = 'team_id=' +  teamid
    }
    else { condition ='recipient_id=' +  this.login.id }
    let obj = {code: 'summary', url: 'task-summary/' + condition + '/', params: {}}
    this.connection.getApi([obj])
  },

  mounted() {
    let array = this.connection1.checkDataReady(['companylist', 'accountlist'])
    let list = array.filter(v=>v.ready===false)
    if(list.length>0) this.connection1.getApi(list)
  },

  watch: {
    "connection.getdataReady": function(newVal) {
      if(newVal==='success') this.getData()
      else if(newVal==='error') this.$router.push({ name: 'error'})
    },

    currentType : function(newVal) {
      if(newVal!=='search') return
      let self = this
      mixing.delay(function(){if(self.$refs['searchbox'] !== undefined) self.$refs['searchbox'].focus()}, 10)
      let array = this.connection1.checkDataReady(['companylist', 'accountlist'])
      let list = array.filter(v=>v.ready===false)
      if(list.length>0) this.connection1.getApi(list)
    },

    searchType : function(newVal, oldVal) {
      if(oldVal===undefined) return
      this.keyword = undefined
      let self = this
      mixing.delay(function(){if(self.$refs['searchbox'] !== undefined) self.$refs['searchbox'].focus()}, 10)
    }
  },

computed: {
  api: {
    get: function() {return this.$store.state.api},
    set: function(val) {this.$store.commit("updateApi", {api: val})}
  },
  rights: {
    get: function() {return this.$store.state.rights },
    set: function(val) {this.$store.commit('updateRights', {rights: val})}
  },
  login: {
    get: function() {return this.$store.state.login},
    set: function(val) {this.$store.commit("updateLogin", { login: val })}
  },
  menuaction: {
    get: function() {return this.$store.state.menuaction},
    set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
  },
  companylist: {
    get: function() {return this.$store.state.companylist},
    set: function(val) {this.$store.commit('updateCompanyList', {companylist: val})}
  },
  accountlist: {
    get: function() {return this.$store.state.accountlist},
    set: function(val) {this.$store.commit('updateAccountList', {accountlist: val})}
  },
  ismobile: {
    get: function() {return this.$store.state.ismobile},
    set: function(val) {this.$store.commit('updateIsMobile', {ismobile: val})}
  },
  notification: {
    get: function() {return this.$store.state.notification},
    set: function(val) {this.$store.commit('updateNotification', {notification: val})}
  },
  hasnews: {
    get: function() {return this.$store.state.hasnews},
    set: function(val) {this.$store.commit('updateHasNews', {hasnews: val})}
  },
  pagetask: {
    get: function() {return this.$store.state.pagetask},
    set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
  }
},

 methods: {
  compiledComponent(value) {
    return {
      template: `${value}`
    }
  },
  formatDate(v) {
    return mixing.yyyymmddhhmm(new Date(v))
  },
  openlink(v, i) {
    let ele = this.$copy(v)
    if(!ele.seen) {
      ele.seen = true
      let copy = this.$copy(this.notification)
      copy[i] = ele
      this.notification = copy
      let values = 'id,receiver,sender,sender__name,sender__avatar,link,type,type__value,seen,refid,create_time,update_time'
      this.connection1.update('notification', ele, values)
    }
    var link = JSON.parse(ele.link)
    this.$router.push(link)
  },

  openSearch() {
    this.currentType = 'search'
  },

  closeSearch() {
    this.currentType = this.type===undefined? undefined : JSON.parse(JSON.stringify(this.type))
  },

  startSearch() {
    if(this.$route.name==='search-result')
    this.$router.replace({ name: 'search-result', query: {keyword: this.selected.id, type: this.searchType}})
    else
    this.$router.push({ name: 'search-result', query: {keyword: this.selected.id, type: this.searchType}})
  },

  objectFilterList(text) {
    let self = this
    if(this.searchType==='company' && this.companylist) {
      mixing.delay(function() {self.objectFilter = mixing.companyFilter(self.companylist, text, 'full')}, 20)
    } else if(this.searchType==='account' && this.accountlist) {
      mixing.delay(function() {self.objectFilter = self.accountlist.filter(v=>v.name.toLowerCase().indexOf(text)>=0 || v.id.toString().indexOf(text>=0))}, 20)
    } else  if(this.searchType==='task') {
      self.objectFilter = [{id: text}]
    }
  },

  action() {
    this.menuaction = {id: mixing.id(), action: 'download'}
  }, 

  getData() {
    let data = this.connection.getbatchData[0].data
    this.numApproved = data.find(v=>v.code==='approved')===undefined? 0 : data.find(v=>v.code==='approved').count
    this.numWaiting1 = data.find(v=>v.code==='waiting-approve')==undefined? 0 : data.find(v=>v.code==='waiting-approve').count
    this.numWaiting2 = data.find(v=>v.code==='waiting-approve-2')==undefined? 0 : data.find(v=>v.code==='waiting-approve-2').count
    this.numPending = data.find(v=>v.code==='not-yet-entered')===undefined? 0 : data.find(v=>v.code==='not-yet-entered').count
    this.numRetype = data.find(v=>v.code==='retype')===undefined? 0 : data.find(v=>v.code==='retype').count
    this.numTyping = data.find(v=>v.code==='entered')===undefined? 0 : data.find(v=>v.code==='entered').count
    this.point =  data.find(v=>v.code==='approved')===undefined? 0 : data.find(v=>v.code==='approved').point
    this.numList = this.numApproved + this.numWaiting1 + this.numWaiting2 +  this.numPending +  this.numRetype + this.numTyping
  },

  updateTask(task) {
    if(this.pagetask.models.find(v=>v===true)) return
    task.assign_date = mixing.yyyymmdd(new Date(task.assign_date))
    task.due_date = mixing.yyyymmdd(new Date(task.due_date))
    task.entry_time = this.$empty(task.entry_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.entry_time))
    task.waiting1_time = this.$empty(task.waiting1_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting1_time))
    task.waiting2_time = this.$empty(task.waiting2_time)===true? 'n/a' : mixing.yyyymmdd(new Date(task.waiting2_time))
    task.approve_time = this.$empty(task.approve_time)===false? mixing.yyyymmdd(new Date(task.approve_time)) : undefined
    let index = this.pagetask.data.findIndex(v=>v.id===task.id)
    let self = this
    
    if(index>=0) {
      let copy = this.$copy(this.pagetask.data)
      copy[index] = task
      mixing.arrayMove(copy,index,0)
      if(this.pagetask.currentFilter? this.pagetask.currentFilter.length>0 : false) {
        this.$store.commit('updateState', {name: 'pagetask', key: 'filterby', data: this.$copy(this.pagetask.currentFilter)})
      }
      this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      mixing.delay(function(newVal) {
        self.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
      },100)
    }
    else {
      if(this.pagetask.currentFilter? this.pagetask.currentFilter.length>0 : false) return
      if(this.$route.query.status? parseInt(this.$route.query.status)!==task.status : false) return

      //check right
      if(this.login.id===task.assigner || this.login.id===task.recipient) {var isOK = true} 
      else if(this.login.type.code==='admin' || this.login.type.code==='manager') {var isOK = true}
      
      if(isOK===undefined) return //exit
      let copy = this.$copy(this.pagetask.data)
      copy.splice(0, 0, task)
      this.$store.commit('updateState', {name: 'pagetask', key: 'data', data: copy})
      mixing.delay(function(newVal) {
        self.$store.commit('updateState', {name: 'pagetask', key: 'highlight', data: task.id})
      },100)
    }
  },

  responsiveMenu() {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
    // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
        })
      }
    }
  }
}
</script>