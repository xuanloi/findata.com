import Vue from 'vue'
import Connection from "@/assets/js/connection.js"

Vue.use( {
  install(Vue){
    Vue.prototype.$langFind =  function(category, classify, code) {
      return this.$store.state.language.find(v=>v.category===category && (classify? v.classify===classify : true) 
      && (code? v.code===code : true))
    },
    
    Vue.prototype.$langFilter =  function(category, classify, code) {
      return this.$store.state.language.filter(v=>v.category===category && (classify? v.classify===classify : true) 
    && (code? v.code===code : true))
    },

    Vue.prototype.$langCode =  function(category, classify, code) {
      const found = this.$store.state.language.find(v=>v.category===category && (classify? v.classify===classify : true) 
      && (code? v.code===code : true))
      return found? found.category + '-' + found.classify + '-' + found.code : undefined
    },

    Vue.prototype.$langValue =  function(category, classify, code, key) {
      const found = this.$store.state.language.find(v=>v.category===category && (classify? v.classify===classify : true) 
      && (code? v.code===code : true))
      return found? found[key] : undefined
    },

    Vue.prototype.$empty = function(val) {
      if(val === undefined || val === null || val === '' || val==="") return true
      return false
    },

    Vue.prototype.$copy =  function(val) {
      if(val === undefined || val === null || val === '' || val==="") return val
      return JSON.parse(JSON.stringify(val))
    }

    Vue.prototype.$createField = function(name,label,format,show, minwidth, action) {
      let field = {name: name, label: label, format: format, show: show, minwidth: minwidth, action: action}
      if(format==='number') {
        field.unit = '1'
        field.textalign = 'right'
      }
      return field
    }

    Vue.prototype.$getLink = function(val) {
      if(val === undefined || val === null || val === '' || val==="") return ''
      let json = val.indexOf('{')>=0? JSON.parse(val) : {path: val} 
      return json
    }

    Vue.prototype.$id = function() {
      return Math.random().toString(36).substr(2, 9)
    }
  
    Vue.prototype.$timeFormat = function(startDate, endDate) {
      let milliseconds = startDate - endDate
      let secs = Math.floor(Math.abs(milliseconds) / 1000);
      let mins = Math.floor(secs / 60);
      let hours = Math.floor(mins / 60);
      let days = Math.floor(hours / 24);
      const millisecs = Math.floor(Math.abs(milliseconds)) % 1000;
      function pad2(n) { return (n < 10 ? '0' : '') + n }
      let display = undefined
  
      if(days>=1) {
        display = pad2(startDate.getHours()) + ':' + pad2(startDate.getMinutes()) + ' ' +  pad2(startDate.getDate()) + '/' + pad2(startDate.getMonth())
      }
      else if(hours>0) display = hours + 'h trước'
      else if(mins>0) display = mins + "' trước"
      else if(secs>0 || millisecs>0) display = 'Vừa xong'
    
      return {
        days: days,
        hours: hours % 24,
        minutes: mins % 60,
        seconds: secs % 60,
        milliSeconds: millisecs,
        display: display
      }
    }

    Vue.prototype.$errPhone = function(phone) {
      var text = undefined
      if (this.$empty(phone)) {
        text = 'Số điện thoại di động không được bỏ trống.'
      } else if (isNaN(phone)) {
        text = 'Số điện thoại di động không hợp lệ.'
      } else if(phone.length<9 || phone.length>11) {
        text = 'Số điện thoại di động phải có từ 9-11 số.'
      }
      return text
    },

    Vue.prototype.$errEmail = function(email) {
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      var text = undefined
      if (this.$empty(email)) {
       text = 'Email không được bỏ trống.'
      } else if (!(re.test(String(email).toLowerCase()))) {
        text = 'Email không hợp lệ.'
      }
      return text
    }

    Vue.prototype.$errPhoneEmail = function(contact) {
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      var text = undefined

      if (this.$empty(contact)) {
        text = 'Số điện thoại di động hoặc Email không được bỏ trống.'
      } else if (!(re.test(String(contact).toLowerCase()) || !isNaN(contact))) {
        text = 'Số điện thoại di động hoặc Email không hợp lệ.'
      } else if(!isNaN(contact) && (contact.length<9 || contact.length>11)) {
        text = 'Số điện thoại di động không hợp lệ.'
      }
      return text
    }

    Vue.prototype.$stripHtml = function(html, length) {
      if(html? html.indexOf('<')<0 : false) return html
      var tmp = document.createElement("DIV")
		  tmp.innerHTML = html
		  var val = tmp.textContent || tmp.innerText || ""
      return length? (val.length > length? val.substring(0, length) + '...' : val ) : val
    }

	  Vue.prototype.$dummy = function(data, count) {
      let list = this.$copy(data)
      for (let index = 0; index < count; index++) {
        if(data.length<index+1) list.push({dummy: true})
      }
      return list
    }

    Vue.prototype.$upload = function(file, type, user) {
      var fileFormat = [{type: 'image', format: ['.png', '.jpg', 'jpeg', '.bmp', '.gif', '.svg']},
        {type: 'video', format: ['.wmv', '.avi', '.mp4', '.flv', '.mov', '.mpg', '.amv', '.rm']}
      ]
      var valid = undefined
      if(type==='image' || type==='video') {
        valid = false
        let found = fileFormat.find(v=>v.type===type)
        found.format.map(x=>{
          if(file.name.toLowerCase().indexOf(x)>=0) valid = true
        })
      }
  
      if(valid===false) return {error: true, text: 'Định dạng file không hợp lệ'}
      if((type==='image' || type==='file') && file.size > 5242880) {
        return {error: true, text: 'Kích thước ' + (type==='image'? 'hình ảnh' : 'tài liệu') + ' phải dưới 5MB'}
      } else if(type==='video' && file.size > 1073741274) {
        return {error: true, text: 'Kích thước video phải dưới 1GB'}
      }
  
      let data = new FormData()
      let fileName = this.$dayjs(new Date()).format("YYYYMMDDhhmmss") + '-' + file.name	
      data.append('name', fileName)
      data.append('file', file)
      data.append('type', type)
      data.append('size', file.size)
      data.append('user', user)
      return {form: data, name: fileName, type: type, size: file.size, file: file}
    }

    Vue.prototype.$change = function(obj1, obj2, list) {
      var change = false
      if(list) {
        list.map(v=>{if(obj1[v]!==obj2[v]) change = true})
      } else {
        for (var k in obj1 ) {
          if(obj1[k]!==obj2[k]) change = true
        }
      }
      return change
    }

    Vue.prototype.$resetNull = function(obj) {
		  for(var key in obj) {
			  if (obj[key]==='' || obj[key]==="") obj[key] = null
		  }
		  return obj
	  }

    Vue.prototype.$responsiveMenu = function() {
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

    Vue.prototype.$copyToClipboard = function(text) {
      if (window.clipboardData && window.clipboardData.setData) {
        // IE specific code path to prevent textarea being shown while dialog is visible.
        return clipboardData.setData("Text", text); 
  
      } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in MS Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
          return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        } catch (ex) {
          console.warn("Copy to clipboard failed.", ex);
          return false;
        } finally {
          document.body.removeChild(textarea);
        }
      }
    }

    Vue.prototype.$companyFilter = function(companylist, text) {
      let list1 = companylist.filter(v=>v.stock_code.toLowerCase().indexOf(text.toLowerCase()) >= 0)
      list1.map(v=>v.index = v.stock_code.toLowerCase().indexOf(text.toLowerCase()))
      
      let list11 = list1.filter(v=>v.index===0)
      list11.sort((a,b) => (a.stock_code.length - b.stock_code.length))
      let list12 = list1.filter(v=>v.index>0)
      list12.sort((a,b) => (a.index - b.index))
      list1 = list11.concat(list12)

      let list2 = companylist.filter(v=>v.name.toLowerCase().indexOf(text.toLowerCase()) >= 0 
      && v.stock_code.toLowerCase().indexOf(text.toLowerCase()) <0)
      list2.map(v=>v.index = v.name.toLowerCase().indexOf(text.toLowerCase()))

      let list21 = list2.filter(v=>v.index===0)
      list21.sort((a,b) => (a.name.length - b.name.length))
      let list22 = list2.filter(v=>v.index>0)
      list22.sort((a,b) => (a.index - b.index))
      list2 = list21.concat(list22)
      return list1.concat(list2)
	  }

    Vue.prototype.$exportExcel = function(data, filename, fields, dataTypes) {
      var _filename  = this.$dayjs(new Date()).format("YYYYMMDDHHmmss") + '-' + filename + '.xlsx'
      let list = []
      let ele = {}

      data.forEach(element => {
        Object.keys(dataTypes).forEach((type, index) => {
            ele[type] =  element[fields[index]]    
        })
        list.push(JSON.parse(JSON.stringify(ele)))
      })

      var XLSX = require('xlsx')
      //workBook class
      function Workbook() {
          if(!(this instanceof Workbook)) return new Workbook();
          this.SheetNames = [];
          this.Sheets = {};
      }
      
      var exportBook = new Workbook();
      var worksheet =  XLSX.utils.json_to_sheet(list);    
      exportBook.SheetNames.push('sheet1');
      exportBook.Sheets.sheet1 = worksheet;
      XLSX.writeFile(exportBook, _filename);        
    }

    Vue.prototype.$nonAccent = function(str) {
      if(this.$empty(str)) return null
      str = str.toLowerCase();
      str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
      str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
      str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
      str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
      str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
      str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
      str = str.replace(/đ/g, "d");
      // Some system encode vietnamese combining accent as individual utf-8 characters
      str = str.replace(/\u0300|\u0301|\u0303|\u0309|\u0323/g, ""); // Huyền sắc hỏi ngã nặng 
      str = str.replace(/\u02C6|\u0306|\u031B/g, ""); // Â, Ê, Ă, Ơ, Ư
      str = str.split(' ').filter(s => s).join('-')
      return str
    }

    Vue.prototype.$linkID = function(link) {
      link = link? link : this.$route.params.slug
      if(this.$empty(link)) return
      let idx = link.lastIndexOf('-')
      let id = (idx>-1 && idx<link.length-1)? link.substring(idx+1, link.length) : undefined
      return id
    },

    Vue.prototype.$delete = function(arr, idx) {
      this.$delete(arr, idx)
    }
    
    Vue.prototype.$height = function(id) {
      let doc = document.getElementById(id)
      return doc? doc.clientHeight : undefined
    }
      
    Vue.prototype.$linkSetting = function(option) {
      var link = undefined
      let list = ['finance', 'industry-comparison', 'multidimensional-fa', 'dupont']
      let name = this.$nonAccent(option.name) + '-' + option.id
      if(option.stock_code) link = {path: '/company/' + option.stock_code}
      else if(option.classify__code==='priceboard') link = {path: '/priceboard/' + name }
      else if(option.classify__code==='screener') link = {path: '/screener/' + name }
      else if(option.classify__code==='industry-structure') link = {path: '/industry-analytics/' + name, query: {tab: 'structure'}}
      else if(option.classify__code==='industry-ratio') link = {path: '/industry-analytics/' + name, query: {tab: 'ratio'}}
      else if(list.findIndex(v=>v===option.classify__code)>=0) link = {path: '/company/' + name}
      else if(option.classify__code==='data-field') link = {path: '/data-field/', query: {setting: option.id}}
      else if(option.uid) link = {path: '/people/' + name}
      return link
    }

    Vue.prototype.$commConnection = function(connection, companyId, topicId, loginId) {
      let values = 'id,company,creator,creator__display_name,creator__avatar,image,create_time,parent,topic,comment'
      let found = this.$copy(connection.find('companycomment'))
      let filter = {company: companyId, deleted: 0, topic: topicId}
      found.params = {values: values, page: 1, perpage: 1, filter: filter, sort: this.sortaz? 'create_time' : '-create_time'}
      
      let conn1 = this.$copy(connection.find('companynote'))
      let values1 = 'id,company,creator,creator__display_name,creator__avatar,create_time,topic,comment'
      filter = {company: companyId, deleted: 0, creator: loginId, topic: topicId}
      conn1.params = {values: values1, page: 1, perpage: 1, filter: filter, sort: this.sortaz? 'create_time' : '-create_time'}
      return [found, conn1]
    }

    Vue.prototype.$clone = function(obj) {
      if (obj === null || typeof (obj) !== 'object' || 'isActiveClone' in obj)
          return obj;

      if (obj instanceof Date)
          var temp = new obj.constructor(); //or new Date(obj);
      else
          var temp = obj.constructor();
  
      for (var key in obj) {
          if (Object.prototype.hasOwnProperty.call(obj, key)) {
              obj['isActiveClone'] = null;
              temp[key] = this.$clone(obj[key]);
              delete obj['isActiveClone'];
          }
      }
      return temp
    }
    
    Vue.prototype.$openLink = function(newVal, event) {
      let url = undefined, link = '/company/' + newVal.company__stock_code
      if(event==='finance') url = {path: link}
      else if(event==='dupont') url = {path: link, query: {tab: 'finance', subtab: 'dupont'}}
      else if(event==='chart') url = {path: link,query: {tab: 'finance', subtab: 'structure'}}
      else if(event==='team') url = {path: link, query: {tab: 'company', subtab: 'team'}}
      if(url) {
        let routeData = this.$router.resolve(url)
        window.open(routeData.href, '_blank')
      }
    }

    Vue.prototype.$color = function(i) {
      var colors = ['#0F9D58','#ffd60a','#abc4ff','#C0E8D5','#B284BE','#72A0C1','#EDEAE0','#F0F8FF','#C46210','#EFDECD','#E52B50','#9F2B68','#F19CBB','#AB274F','#D3212D','#3B7A57','#FFBF00','#FF7E00','#9966CC','#3DDC84','#CD9575','#665D1E','#915C83','#841B2D','#FAEBD7']
      return i>=colors.length? ('#' + Math.floor(Math.random()*16777215).toString(16)) : colors[i]
    }
    
    Vue.prototype.$connectApi = function(report_name, company_type) {
      let name = '';
      if (report_name === "CDKT")
        name = "bs" + company_type.toLowerCase();
      else if (report_name === "KQKD" || report_name === "KQKD-LK")
        name = "bp" + company_type.toLowerCase();
      else if (report_name === "LCTT-TT" || report_name === "LCTT-TT-LK")
        name = "cftt" + company_type.toLowerCase();
      else if (report_name === "LCTT-GT" || report_name === "LCTT-GT-LK")
        name = "cfgt" + company_type.toLowerCase()
      else if(report_name==='TKGIA')
        name = 'stockprice'
      else if(report_name==='TKLENH')
        name = 'stockorder'
      else if(report_name==='DTNNLENH')
        name = 'foreignorder'
      else if(report_name==='DTNNTT')
        name = 'foreigndeal'
      else if(report_name==='GIA')
        name = 'pricelive'
      return name
    }

    Vue.prototype.$connection = function(buefy) {
      return new Connection(this.$store, buefy)
    }

    Vue.prototype.$setLanguage = function() {
      let vi = {}, en = {}, ja = {}
      this.$store.state.language.map(v=>{
        vi[v.category + '-' + v.classify + '-' + v.code] = v.vi
        en[v.category + '-' + v.classify + '-' + v.code] = v.en
        ja[v.category + '-' + v.classify + '-' + v.code] = v.ja
      })
      this.$i18n.setLocaleMessage('vi', vi)
      this.$i18n.setLocaleMessage('en', en)
      this.$i18n.setLocaleMessage('ja', ja)
    }

    Vue.prototype.$setLogin = function() {
      if(this.$store.state.login) return true
      else if(this.$route.query.username) {
        let obj = {id: Number(this.$route.query.userid), username: this.$route.query.username, fullname: this.$route.query.fullname}
        this.$store.commit("updateLogin", {login: obj})
        this.$router.push('/')
        return true
      } else {
        window.location.href = 'https://login.findata.vn/signin?link=' + window.location.origin
        return false
      }
    }
  }
})