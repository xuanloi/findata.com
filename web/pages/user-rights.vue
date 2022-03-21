<template>
<div>
    <TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}" />
    <div class="pt60"/>
    <section class="hero">
  <div class="hero-body pt10 pb20">
    <div class="columns">
    <div class="column is-9">
    <div class="table-container">
    <table class="table" style="margin-left: auto; margin-right: auto;" ref="table">
     <tbody>
        <tr>
        <td>
              <b-tooltip :label="expanded? 'Thu gọn' : 'Mở rộng'"
            position="is-bottom">
            <a @click="expanded===true? collapseAll() : expandAll()">
            <i :class="expanded===true? 'mdi mdi-chevron-double-up' : 'mdi mdi-chevron-double-down'"  class="has-text-dark " style="font-size:34px;"> </i>
            </a>
        </b-tooltip>
        </td>
        <td> 
            Chức năng
        </td>
        <td> Cộng tác viên</td>
        <td> Nhân viên</td>
        <td> Trưởng nhóm </td>
        <td> Quản lý </td>
        <td> Quản trị hệ thống </td>
        </tr>

        <template v-for="(ele) in data">
            <tr :key="ele.id"  @click="toggle(ele)" v-if="api.filter2var('function', ele.code).length>0"> 
            <td  style="width:10px; height: 10px;">
            <div class="vertical-center" > <span class="icon">
            <i :class="ele.expanded? 'mdi mdi-chevron-up fs28 has-text-primary' : 'mdi mdi-chevron-down fs28'" :ref="'icon' + ele.id"> 
            </i> 
            </span>
            </div>
                </td>
            <td  style="min-width:200px">
            <div class="vertical-center">
                <span :class="ele.expanded? 'has-text-primary fb500' : ''"> {{ele.value}} </span>
            </div> </td>
            <td> </td>
            <td> </td>
            <td> </td>
            <td> </td>
            <td> </td>
            </tr>
            <tr :key="ele.id" v-else>
            <td  style="width:10px; height: 10px;"></td>
            <td  style="min-width:200px">
            <div class="vertical-center"><span> {{ele.value}} </span>
            </div> </td>

          <td class="is-centered">
              <b-checkbox v-model="modelsCTV[ele.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
          </td>
          <td><div class="has-text-centered">
            <b-checkbox v-model="modelsNV[ele.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
            </div>  </td>
            
            <td><div class="has-text-centered">
                <b-checkbox v-model="modelsTN[ele.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>  
            </div>
            </td>
            <td><div class="has-text-centered">
                <b-checkbox v-model="modelsQL[ele.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox> 
            </div>
            </td>
            <td><div class="has-text-centered">
            <b-checkbox v-model="modelsAD[ele.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
            </div>
            </td>
          </tr>

          <template v-for="(ele1) in api.filter2var('function', ele.code)">
            <tr :key="ele1.id" v-if="ele.expanded"> 
              <td> </td>
              <td> <span class="pl20"/> <div class="vertical-center">
                <span> {{ele1.value}} </span> </div> </td>
              <td class="is-centered">
                  <b-checkbox v-model="modelsCTV[ele1.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
              </td>
              <td><div class="has-text-centered">
                  <b-checkbox v-model="modelsNV[ele1.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
              </div>  </td>
              
              <td><div class="has-text-centered">
                  <b-checkbox v-model="modelsTN[ele1.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>  
              </div>
              </td>
              <td><div class="has-text-centered">
                  <b-checkbox v-model="modelsQL[ele1.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox> 
              </div>
              </td>
              <td><div class="has-text-centered">
                  <b-checkbox v-model="modelsAD[ele1.id]" class="font-smaller has-text-link" type='is-primary'></b-checkbox>
                  </div>
                </td>
            </tr>
          </template>
        </template>     
    </tbody>
    </table>
    </div>
    </div>

      <div class="column is-3">
        <div class="buttons is-centered mt10">
            <button class="button is-primary is-outlined" @click="save()">Lưu lại</button>
        </div>

        <article class="message is-primary mt30" v-if="message!==undefined" :class="message!==undefined? message.type: ''">
        <div class="message-body pl15 has-text-justified">
            {{message.message}}
        </div>  
        </article>
      </div>
      </div>
    </div>
  </section>
  <Footer> </Footer>
</div>
</template>

<script>
export default {
    data() {
      return {
        tophead: 'Phân quyền người sử dụng',
        data: [],
        expanded: false,
        modelsCTV: [],
        modelsNV: [],
        modelsTN: [],
        modelsQL: [],
        modelsAD: [],
        rightlist: undefined,
        change: false,
        message: undefined,
        connection: this.$connection(),
        connection1: this.$connection(),
        connection2: this.$connection(),
        newlist: [],
        rights: []
      }
    },

    head() {
      return {
        title: 'Phân quyền người sử dụng'
      }
    },

    created() {
      let found = this.connection.requirelist.find(v=>v.name==='rights')
      this.connection.getApi([found])
    },

    watch: {
      modelsCTV : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.updateChange(newVal, 'ctv')
      },

      modelsNV : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.updateChange(newVal, 'staff')
      },

      modelsTN : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.updateChange(newVal, 'teamlead')
      },
    
      modelsQL : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.updateChange(newVal, 'manager')
      },
                      
      modelsAD : function(newVal, oldVal) {
        if(oldVal===undefined) return
        this.updateChange(newVal, 'admin')
      },

      'connection.getdataReady' : function(newVal) {
        if(newVal==='success') this.fillData()
      },

      'connection1.getupdateStatus': function(newVal, oldVal) {
        if(newVal===true) {                
          this.message = {message: 'Cập nhật phân quyền thành công', type: 'is-success'}
          let connlist = [{name: 'rights', url: 'data/Classification',
          params: {sort: 'index', filter: {function__account_type: this.login.type.id, function__enable: 1, enable: 1}}}]
          this.connection2.getApi(connlist)
        }
        else if(newVal==false) {
          this.message = {message: 'Có lỗi xẩy ra. Cập nhật phân quyền thất bại', type: 'is-danger'}
        }
      },

      "connection2.getdataReady": function(newVal) {
        if (newVal==="success") {
          let data = this.connection2.getbatchData.find(v=>v.name==='rights').data
          data.filter(v=>v.category==='function').map(v=>{
            let found = this.api.find3var('functions','admin', v.classify)
            if(found? (found.enable? !data.find(x=>x.id===found.id): false) : false) data.push(found)
          })
          this.$multiSort(data, {index: 'asc'})
          this.$store.commit('updateRights', {rights: data})
        }
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.state.api},
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },
      login: {
        get: function() {return this.$store.state.login},
        set: function(val) {this.$store.commit("updateLogin", {login: val})}
      }
    },

    methods: {
      fillData() {
        this.rights = this.connection.getbatchData[0].data
        this.rightlist = this.$copy(this.rights)
        this.data = this.api.filter2var('functions', 'admin')
        let fid = this.api.find3var('list', 'account-type', 'ctv').id
        let filter = this.rights.filter(v=>v.account_type===parseInt(fid))
        filter.map(v=>this.modelsCTV[v.function]=v.enable)
        
        fid = this.api.find3var('list', 'account-type', 'staff').id
        filter = this.rights.filter(v=>v.account_type===parseInt(fid))
        filter.map(v=>this.modelsNV[v.function]=v.enable)

        fid = this.api.find3var('list', 'account-type', 'teamlead').id
        filter = this.rights.filter(v=>v.account_type===parseInt(fid))
        filter.map(v=>this.modelsTN[v.function]=v.enable)

        fid = this.api.find3var('list', 'account-type', 'manager').id
        filter = this.rights.filter(v=>v.account_type===parseInt(fid))
        filter.map(v=>this.modelsQL[v.function]=v.enable)

        fid = this.api.find3var('list', 'account-type', 'admin').id
        filter = this.rights.filter(v=>v.account_type===parseInt(fid))
        filter.map(v=>this.modelsAD[v.function]=v.enable)
        this.expandAll()
      },

        updateChange(newVal, name) {
          let fid = parseInt(this.api.find3var('list', 'account-type', name).id)
          newVal.forEach((element,id) => {
            if(element!==undefined)  {
              let found = this.rightlist.find(v=>parseInt(v.account_type)===parseInt(fid) && parseInt(v.function)===parseInt(id))
              if(found!==undefined) found.enable = element
              else {
                let obj = this.newlist.find(v=>v.account_type===fid && v.function===id)
                if(obj===undefined) this.newlist.push({account_type: fid, function: id, enable: element, create_time: new Date()})
              }
            }   
          })
          this.change = true
        },

      save() {
        if(!this.change) {
          this.message  = {message: 'Bạn chưa thay đổi thông tin', type: 'is-primary'}
          return
        }
        //get changes
        let changelist = []
        this.rightlist.forEach(element => {
          let found = this.rights.find(v=>parseInt(v.id)===parseInt(element.id))
          if(found? found.enable!==element.enable : false) changelist.push(element)
        })
        this.connection1.insert('rights',  changelist.concat(this.newlist))
      },

      toggle(ele) { 
        ele.expanded = ele.expanded===true? false : true
        this.data = JSON.parse(JSON.stringify(this.data))
      },

      expandAll() {
        this.expanded = true
        this.data.forEach(element => {element.expanded = true})
        this.expanded = true
      },

      collapseAll() {
        this.data.forEach(element => {element.expanded = false})
        this.expanded = false
      }
    }
}
</script>
