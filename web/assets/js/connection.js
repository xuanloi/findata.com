/* eslint-disable */
import axios from 'axios'
import Vue from 'vue'

export default class Connnection {
    requirelist = [
        {id: 1, name: 'syspara', commit: 'updateSystemParameter', url: 'data/Classification/', url_detail: 'data-detail/Classification/', params: {sort: 'index'}},
        {id: 2, name: 'rights', commit: undefined, url: 'data/Rights/', url_detail:'data-detail/Rights/', params: {}},
        {id: 3, name: 'accountlist', commit: 'updateAccountList', url: 'data/Account/',  url_detail:'data-detail/Account/', params: {}},
        {id: 4, name: 'tasklist' , commit: undefined, url: 'data/Task/', url_detail: 'data-detail/Task/', params: {}},
        {id: 5, name: 'reportperiod', commit: 'updateReportPeriod', url: 'data/Report_Period/', params: {token:'', type: 'viewserializer', filter:{data_ready:1}}},
        {id: 6, name: 'reportitem', url: 'data/Report_Item/', params: {page: -1}},
        
        {id: 13, name: 'bssxreport', commit: undefined, url: 'data/BSSX/', url_detail: 'data-detail/BSSX/', params:  {}},
        {id: 14, name: 'bpsxreport', commit: undefined, url: 'data/BPSX/',  url_detail: 'data-detail/BPSX/', params:  {}},
        {id: 15, name: 'cfttsxreport', commit: undefined, url: 'data/CFTTSX/', url_detail: 'data-detail/CFTTSX/', params:  {}},
        {id: 16, name: 'cfgtsxreport', commit: undefined, url: 'data/CFGTSX/', url_detail: 'data-detail/CFGTSX/', params:  {}},
       
        {id: 17, name: 'bsnhreport', commit: undefined, url: 'data/BSNH/', url_detail: 'data-detail/BSNH/', params:  {}},
        {id: 18, name: 'bpnhreport', commit: undefined, url: 'data/BPNH/', url_detail: 'data-detail/BPNH/', params:  {}},
        {id: 19, name: 'cfttnhreport', commit: undefined, url: 'data/CFTTNH/', url_detail: 'data-detail/CFTTNH/', params:  {}},
        {id: 20, name: 'cfgtnhreport', commit: undefined, url: 'data/CFGTNH/', url_detail: 'data-detail/CFGTNH/', params:  {}},

        {id: 21, name: 'bsckreport', commit: undefined, url: 'data/BSCK/', url_detail: 'data-detail/BSCK/', params:  {}},
        {id: 22, name: 'bpckreport', commit: undefined, url: 'data/BPCK/', url_detail: 'data-detail/BPCK/', params:  {}},
        {id: 23, name: 'cfttckreport', commit: undefined, url: 'data/CFTTCK/', url_detail: 'data-detail/CFTTCK/', params:  {}},
        {id: 24, name: 'cfgtckreport', commit: undefined, url: 'data/CFGTCK/', url_detail: 'data-detail/CFGTCK/', params:  {}},

        {id: 25, name: 'bsbhreport', commit: undefined, url: 'data/BSBH/', url_detail: 'data-detail/BSBH/', params:  {}},
        {id: 26, name: 'bpbhreport', commit: undefined, url: 'data/BPBH/', url_detail: 'data-detail/BPBH/', params:  {}},
        {id: 27, name: 'cfttbhreport', commit: undefined, url: 'data/CFTTBH/', url_detail: 'data-detail/CFTTBH/', params:  {}},
        {id: 28, name: 'cfgtbhreport', commit: undefined, url: 'data/CFGTBH/', url_detail: 'data-detail/CFGTBH/', params:  {}},

        {id: 63, name: 'taskobj', commit: undefined, url: 'data/Task/', url_detail: 'data-detail/Task/', params:  {}},
        {id: 29, name: 'companylist', commit: 'updateCompanyList', url: 'data/Company/', params:  {page: -1, values: 'id,name,short_name,address,tax_code,stock_code,listed,listed_on,create_time,enable,detail,type,type__code,update_time,factor,industry,industry__level1_name,industry__level1_code,industry__level2_name,industry__level2_code,industry__level3_name,industry__level3_code'}},    
        {id: 54, name: 'email', commit: undefined, url: 'send-email/', params: {}},
        {id: 55, name: 'authentication', commit: undefined, url: 'data/Authentication/', params: {}},
        {id: 56, name: 'messagelist', commit: 'updateMessageList', url: 'data/Message/', params: {}},
        {id: 62, name: 'itemchangelist' , commit: undefined, url: 'data/Item_Change/', url_detail: 'data-detail/Item_Change/', params: {}},
        {id: 64, name: 'link', commit: undefined, url: 'data/Link/', url_detail: 'data-detail/Link/', params:  {}},
        {id: 65, name: 'leavelist', commit: 'updateLeaveList', url: 'data/Leave/', url_detail: 'data-detail/Leave/', params:  {}},
        {name: 'image', commit: undefined , url: 'data/Image/', url_detail: 'data-detail/Image/', params:  {}},
        {name: 'file', commit: undefined , url: 'data/File/', url_detail: 'data-detail/File/', params:  {}},
        {name: 'taskimage', commit: undefined , url: 'data/Task_Image/', url_detail: 'data-detail/Task_Image/', params:  {}},
        {name: 'taskrelated', commit: undefined , url: 'data/Task_Related/', url_detail: 'data-detail/Task_Related/', params:  {}},
        {name: 'helpcategory', commit: 'updateHelpCategory', url: 'data/Help_Category/', url_detail: 'data-detail/Help_Category/', params: {}},
        {name: 'help', commit: undefined, url: 'data/Help/', url_detail: 'data-detail/Help/', params: {}},
        {name: 'helpcomment', commit: undefined, url: 'data/Help_Comment/', url_detail: 'data-detail/Help_Comment/', params: {}},
        {name: 'helplike', commit: undefined, url: 'data/Help_Like/', url_detail: 'data-detail/Help_Like/', params: {}},   
        {name: 'news', commit: undefined, url: 'data/News/', url_detail: 'data-detail/News/', params: {}},
        {name: 'newscomment', commit: undefined, url: 'data/News_Comment/', url_detail: 'data-detail/News_Comment/', params: {}},
        {name: 'newslike', commit: undefined, url: 'data/News_Like/', url_detail: 'data-detail/News_Like/', params: {}},
        {name: 'category', commit: 'updateCategory', url: 'data/Category/', url_detail: 'data-detail/Category/', params: {}},
        {name: 'stockprice', commit: undefined, url: 'data/Stock_Price/', url_detail: 'data-detail/Stock_Price/', params: {}},
        {name: 'stockorder', commit: undefined, url: 'data/Stock_Order/', url_detail: 'data-detail/Stock_Order/', params: {}},
        {name: 'foreignorder', commit: undefined, url: 'data/Foreign_Order/', url_detail: 'data-detail/Foreign_Order/', params: {}},
        {name: 'foreigndeal', commit: undefined, url: 'data/Foreign_Deal/', url_detail: 'data-detail/Foreign_Deal/', params: {}},
        {name: 'taskstock', commit: undefined, url: 'data/Task_Stock/', url_detail: 'data-detail/Task_Stock/', params: {}},
        {name: 'notification', commit: undefined, url: 'data/Notification/', url_detail: 'data-detail/Notification/', params: {values: 'id,sender,sender__name,sender__avatar,receiver,type,type__value,seen,refid,link,create_time'}},
        {name: 'violate', commit: undefined, url: 'data/Violate/', url_detail: 'data-detail/Violate/', params: {}},
        {name: 'industry', commit: 'updateIndustry', url: 'data/Industry/', url_detail: 'data-detail/Industry/', params: {}},
        {name: 'pricelive', commit: undefined, url: 'data/Price_Live/', url_detail: 'data-detail/Price_Live/', params: {}},

        //Datatable
        {name: 'moneyunit', commit: 'updateMoneyUnit', url: 'data/Money_Unit/', url_detail: 'data-detail/Money_Unit/', params: {}},
        {name: 'datatype', commit: 'updateDataType', url: 'data/Data_Type/', url_detail: 'data-detail/Data_Type/', params: {sort: 'id'}},
        {name: 'settingtype', commit: 'updateSettingType', url: 'data/Setting_Type/', url_detail: 'data-detail/Setting_Type/', params: {}},
        {name: 'colorchoice', commit: 'updateColorChoice', url: 'data/Color_Choice/', url_detail: 'data-detail/Color_Choice/', params: {sort: 'id'}},
        {name: 'filterchoice', commit: 'updateFilterChoice', url: 'data/Filter_Choice/', url_detail: 'data-detail/Filter_Choice/', params: {sort: 'id'}},
        {name: 'textalign', commit: 'updateTextAlign', url: 'data/Text_Align/', url_detail: 'data-detail/Text_Align/', params: {sort: 'id'}},
        {name: 'placement', commit: 'updatePlacement', url: 'data/Placement/', url_detail: 'data-detail/Placement/', params: {sort: 'id'}},
        {name: 'colorscheme', commit: 'updateColorScheme', url: 'data/Color_Scheme/', url_detail: 'data-detail/Color_Scheme/', params: {sort: 'id'}},
        {name: 'textcolor', commit: 'updateTextColor', url: 'data/Text_Color/', url_detail: 'data-detail/Text_Color/', params: {sort: 'id'}},
        {name: 'filtertype', commit: 'updateFilterType', url: 'data/Filter_Type/', url_detail: 'data-detail/Filter_Type/', params: {sort: 'id'}},
        {name: 'sorttype', commit: 'updateSortType', url: 'data/Sort_Type/', url_detail: 'data-detail/Sort_Type/', params: {sort: 'id'}},
        {name: 'tablesetting', commit: 'updateTableSetting', url: 'data/Table_Setting/', url_detail: 'data-detail/Table_Setting/', params: {sort: 'id', values: 'id,code,name,detail'}},
        {name: 'settingchoice', commit: 'updateSettingChoice', url: 'data/Setting_Choice/', url_detail: 'data-detail/Setting_Choice/', params: {sort: 'id'}},
        {name: 'sharechoice', commit: 'updateShareChoice', url: 'data/Share_Choice/', url_detail: 'data-detail/Share_Choice/', params: {}},
        {name: 'menuchoice', commit: 'updateMenuChoice', url: 'data/Menu_Choice/', url_detail: 'data-detail/Menu_Choice/', params: {}},
        {name: 'settingclass', commit: 'updateSettingClass', url: 'data/Setting_Class/', url_detail: 'data-detail/Setting_Class/', params: {}},
        {name: 'usersetting', commit: undefined, url: 'data/User_Setting/', url_detail: 'data-detail/User_Setting/', params: {sort: '-update_time', values: 'id,name,detail,user,type,type__code,type__name,note,default,create_time,update_time,classify,classify__name'}},
        //end
        {name: 'analysisreport', url: 'data/Analysis_Report/', url_detail: 'data-detail/Analysis_Report/', params: {values:'id,name,file,issue_date,company,company__stock_code,company__name,ticker,expert,content,create_time,create_time__date'}},
    ]

    //path = 'http://61.28.238.196:8000/' //'http://data.findata.com.vn/' 
    path = 'http://127.0.0.1:8000/'
    batchApi = []
    batchStatus = []
    batchData = []
    updateRecord = undefined
    updateStatus = undefined
    store = {}
    notif = undefined
    timer = undefined

    constructor(store, buefy) {
        if(store) this.store = store 
        if(buefy) this.buefy = buefy 
    }

    find(name) {
        return this.requirelist.find(v=>v.name===name)
    }

    checkDataReady(list) {
        var array = []
        list.forEach(element => {
            let found = this.requirelist.find(v=>v.name===element)
            if(found!==undefined) {
                let ele = JSON.parse(JSON.stringify(found))
                ele.ready = this.store.state[element]? true : false
                array.push(ele)
            }
        })
       return array
    }

    get getbatchStatus() {return this.batchStatus}
    
    get getbatchData() {return this.batchData}

    get getdataReady() {
        if(this.batchStatus.length===0) return 'wait'
        return this.batchData.length===this.batchStatus.length? (this.batchStatus.find(v=>v.ready===false)? 'error' : 'success')  : 'loading'
    } 
    
    getApi(list) {
        this.batchApi = []
        this.batchStatus = []
        this.batchData = []
        let startTime = new Date().getTime()
        if(this.timer) clearInterval(this.timer)
        if(this.notif) this.notif.close()

        list.forEach(element => {
            let found = this.requirelist.find(v=>v.name===element.name)
            let url = (element.path? this[element.path] : this.path) + (element.url? element.url : found.url)
            let params = element.params? element.params : (found.params===undefined? {} : found.params)
            params.login = this.store.state.login===undefined? undefined : this.store.state.login.id
            if(element.method==='post') this.batchApi.push(axios.post(url, element.data))
            else this.batchApi.push(axios.get(url, {params: params}))
            this.batchStatus.push({name: element.name, ready: false, url: (element.url? element.url : found.url), path: 'dataPath', params: params, commit: found? found.commit : undefined})
        })
        
        let self = this, duration = 0 //, notif = undefined
        this.timer = setInterval(function() {
            duration++
            if(duration===2) self.notif = self.loadingMessage()
        }, 1000)

        this.batchApi.forEach((obj,id) => {
        obj.then(function (response) {
            self.batchStatus[id].ready = true
            self.batchStatus[id].full_data = response.data.full_data
            self.batchStatus[id].total_rows = response.data.total_rows
            self.batchStatus[id].duration = (new Date().getTime() - startTime)/1000

            let f = {}, payload =  {}
            f = {name: self.batchStatus[id].name, data: response.data.rows? response.data.rows : response.data }
            payload[self.batchStatus[id].name] = response.data.rows? response.data.rows : response.data
            if(self.batchStatus[id].commit!==undefined) {
                self.store.commit(self.batchStatus[id].commit, payload)
            }
         
            self.batchData.push(f)
            clearInterval(self.timer)
            if(self.notif) self.notif.close()
        }
        , function (error) {
                self.batchStatus[id].ready = false
                self.batchStatus[id].duration = (new Date().getTime() - startTime)/1000
                let f = {name: self.batchStatus[id].name, data: undefined} 
                self.batchData.push(f)
                clearInterval(self.timer)
                if(self.notif) self.notif.close()
            })
        })
    }

    //update data
    get getupdateRecord() {return this.updateRecord}
    get getupdateStatus() {return this.updateStatus}
    
    update(name, data, values, affect, notify, message) {
        let found = this.requirelist.find(v=>v.name===name)
        this.updateRecord = undefined
        this.updateStatus = undefined
        let _params = typeof values==='string'? {values: values} : values

        let rs = axios.put(this.path + found.url_detail + data.id + '/', data, {params: _params})
        rs.then((respond) => {
            this.updateRecord = respond.data
            this.updateStatus = true

            if(found.commit!==undefined) {
                let index = this.store.state[found.name]===undefined? -1 : this.store.state[found.name].findIndex(v=>v.id===respond.data.id)
                if(index>=0) {
                    var copy = JSON.parse(JSON.stringify(this.store.state[found.name]))
                    if(Array.isArray(respond.data)===false) Vue.set(copy, index, respond.data)
                    else {
                        respond.data.forEach(element => {
                            let index = copy.findIndex(v=>v.id===element.id)
                            if(index>=0) Vue.set(copy, index, element)
                        })
                    }
                    this.store.commit('updateStore', {name: found.name, data: copy})
                }
                //this.store.state['datachanged'] = {name: name, data: this.store.state[found.name], type: 'updatelist', affect: affect, notify: notify}
            }
            this.showMessage('is-success', 'update', message) 
        })
        .catch(error => {
            this.updateStatus = false
            this.showMessage('is-danger', 'update', message) 
        })
    }

    //insert data
    insert(name, data, values, affect, notify, message) {
        let found = this.requirelist.find(v=>v.name===name)
        this.updateRecord = undefined
        this.updateStatus = undefined
        let _params = typeof values==='string'? {values: values} : values

        if (!Array.isArray(data))
            var rs = axios.post(this.path + found.url, data, {params: _params})
        else {
            let params = {action: 'import', values: values}
            rs = axios.post(this.path + 'import-data/' + found.url.substring(5, found.url.length-1) + '/', data, {params: params})
        }
 
        rs.then((respond) => {
            this.updateRecord = respond.data
            this.updateStatus = true
            if(found.commit!==undefined) {
                if(this.store.state[found.name] !==undefined) {
                    let copy = JSON.parse(JSON.stringify(this.store.state[found.name]))
                    let rows = Array.isArray(respond.data)? respond.data : [respond.data]
                    rows.map(v=>{
                        if(v.id && !v.error) {
                            let idx = copy.findIndex(x=>x.id===v.id)
                            if(idx>=0) copy[idx] = v
                            else copy.push(v)
                        } 
                    })
                    this.store.commit('updateStore', {name: found.name, data: copy})
                    //this.store.state['datachanged'] = {name: name, data: this.store.state[found.name], type: 'requirelist', affect: affect, notify: notify}
                }
            }
            this.showMessage('is-success', 'update', message)
        })
        .catch(error => {
            this.updateStatus = false
            this.showMessage('is-danger', 'update', message)
        })
    }

    //delete data
    delete(name, id, affect, notify, message) {
        let found = this.requirelist.find(v=>v.name===name)
        this.updateRecord = undefined
        this.updateStatus = undefined
      
        if (!Array.isArray(id))
            var rs = axios.delete(this.path + found.url_detail + id)
        else {
            let params = {action: 'delete'}
            rs = axios.post(this.path + 'import-data/' + found.url.substring(5, found.url.length-1) + '/', id, {params: params})
        }

        rs.then((respond) => {
            this.updateRecord = respond.data
            this.updateStatus = true

            if(found.commit!==undefined) {
                let copy = JSON.parse(JSON.stringify(this.store.state[found.name]))
                if (!Array.isArray(id)) {
                    let index = copy.findIndex(v=>v.id===id)
                    if(index>=0) this.$delete(copy, index)
                } else  {
                    respond.data.forEach(element => {
                        let index = copy.findIndex(v=>v.id===element.id)
                        if(index>=0) this.$delete(copy, index)
                    })
                }
                this.store.commit('updateStore', {name: found.name, data: copy})
                //this.store.state['datachanged'] = {name: name, data: this.store.state[found.name], type: 'updatelist', affect: affect, notify: notify}
            }
            this.showMessage('is-success', 'delete', message)  
        })
        .catch(() => {
            this.updateStatus = false
            this.showMessage('is-danger', 'delete', message)  
        })
    }

    showMessage(type, action, message) {
        if(this.buefy===undefined) return
        if (message) {
            if(message.show===false) return
            else if (message.success && message.error) {
                var text = type==='is-success'? message.success : message.error
            }
        }

        if(text===undefined) {
            let list = [
                {type: 'is-success', action: 'update', text: 'Lưu dữ liệu thành công.'},
                {type: 'is-danger', action: 'update', text: 'Lỗi. Lưu dữ liệu thất bại.'},
                {type: 'is-success', action: 'delete', text: 'Xoá dữ liệu thành công.'},
                {type: 'is-danger', action: 'delete', text: 'Lỗi. Xoá dữ liệu thất bại.'},
            ]
            text = list.find(v=>v.type===type && v.action===action).text
        }
        let info = {duration: 4000, type: type, hasIcon: false, message: text}
        this.buefy.notification.open(info)
    }

    loadingMessage() {
        if(this.buefy===undefined) return
        let text = 'Đang tải dữ liệu vui lòng chờ trong giây lát'
        let info = {duration: 1000000, type: 'is-success', hasIcon: false, message: text}
        return this.buefy.notification.open(info)
    }
}