/* eslint-disable */
import Connection from "~/assets/js/connection.js"

class Mixing {
	//====Globally Unique Identifier==============
	guid() {
		function s4() {
			return Math.floor((1 + Math.random()) * 0x10000)
			.toString(16)
			.substring(1);
		}
		return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
	}

	id() {
		return Math.random().toString(36).substr(2, 9)
	}

	yyyymmdd(date) {                                   
		var yyyy = date.getFullYear().toString();                                    
		var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based         
		var dd  = date.getDate().toString();						
		return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
	}

	getTime(date) {
		function checkTime(i) {return (i < 10) ? "0" + i : i}
		let h = checkTime(date.getHours())
		let m = checkTime(date.getMinutes())
		let s = checkTime(date.getSeconds())
		return  h + ":" + m + ":" + s;
	}

	yyyymmddhhmm(date) {
		function pad2(n) {  // always returns a string
			return (n < 10 ? '0' : '') + n
		}

		return date.getFullYear() + '-' +
			pad2(date.getMonth() + 1) + '-'  +
			pad2(date.getDate()) + ' ' +
			pad2(date.getHours()) + ':' +
			pad2(date.getMinutes())
	}

	yyyymmddhhmmss(date) {
		function pad2(n) {  // always returns a string
			return (n < 10 ? '0' : '') + n
		}

		return date.getFullYear() +
				pad2(date.getMonth() + 1) + 
				pad2(date.getDate()) +
				pad2(date.getHours()) +
				pad2(date.getMinutes()) +
				pad2(date.getSeconds());
	}
		
	dateDiffCalc(startDate, endDate) {
		let milliseconds = startDate - endDate
		let secs = Math.floor(Math.abs(milliseconds) / 1000);
		let mins = Math.floor(secs / 60);
		let hours = Math.floor(mins / 60);
		let days = Math.floor(hours / 24);
		const millisecs = Math.floor(Math.abs(milliseconds)) % 1000;
		function pad2(n) { return (n < 10 ? '0' : '') + n }
		let display = undefined

		if(days>1) {
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
  
	isEmpty(val) {
		if(val === undefined || val === null || val === '' || val==="") return true
		return false
	}

	copy(obj) {
		if(this.isEmpty(obj)) return obj
		return JSON.parse(JSON.stringify(obj))
	}

	resetEmptyString(obj) {
		for(var key in obj) {
			if (obj[key]==='' || obj[key]==="") obj[key] = null
		}
		return obj
	}

	isNumber(val) {
		if(val === undefined || val === null || val === '') return false
		val = val.toString().replace(/,/g, "")
		return !isNaN(val)
	}
	
	isDate(date) {
		if(this.isEmpty(date)) return false
		return !isNaN(new Date(date).getDate());
	}

	percentage(a,b) {
		if(a===undefined && b===undefined) return undefined
		else if(this.formatNumber(b) === undefined) return undefined

		let c = this.formatNumber(a)
		let d = this.formatNumber(b)
		c = c===undefined? 0 : c
		d = d===undefined? 0 : d
		return ((c-d)*100/d).toFixed(1)
	}

	minus(a, b) {
		if(a===undefined && b===undefined) return undefined
		let c = this.formatNumber(a)
		let d = this.formatNumber(b)
		return (c===undefined? 0 : c) - (d===undefined? 0 : d)
	}

	numbertoString(val) {
		if(val === undefined || val === "" || val==='' || val === null) return
		val = val.toString().replace(/,/g, "")
		if(isNaN(val)) return
		return Number(val).toLocaleString('en-EN')
	}

	formatNumber(val) {
		if(val === undefined || val === "" || val==='' || val === null) return
		val = val.toString().replace(/,/g, "")
		return Number(val)
	}

	unique(arr, keyProps) {
		const kvArray = arr.map(entry => {
		const key = keyProps.map(k => entry[k]).join('|');
		return [key, entry];
		});
		const map = new Map(kvArray);
		return Array.from(map.values());
	}

	multiSort(array, sortObject = {}, format = {}) {
		const sortKeys = Object.keys(sortObject)
		
        // Return array if no sort object is supplied.
        if (!sortKeys.length) return array

        // Change the values of the sortObject keys to -1, 0, or 1.
        for (let key in sortObject)
            sortObject[key] = sortObject[key] === 'desc' || sortObject[key] === -1 ? -1 : (sortObject[key] === 'skip' || sortObject[key] === 0 ? 0 : 1)

        const keySort = (a, b, direction) => {
            direction = direction !== null ? direction : 1
            if (a === b) return 0

            // If b > a, multiply by -1 to get the reverse direction.
            return a > b ? direction : -1 * direction;
        }

        return array.sort((a, b) => {
            let sorted = 0, index = 0

            // Loop until sorted (-1 or 1) or until the sort keys have been processed.
            while (sorted === 0 && index < sortKeys.length) {
                const key = sortKeys[index]
                if (key) {
					const direction = sortObject[key]
					let val1 = format[key]==='number'? (this.isEmpty(a[key]) || a[key]==='n/a'? 0 :  this.formatNumber(a[key]))
								: (format[key]==='%'? (this.isEmpty(a[key]) || a[key]==='n/a'? 0 : this.formatNumber(a[key].replace('%', ''))) : a[key])

					let val2 = format[key]==='number'? (this.isEmpty(b[key]) || b[key]==='n/a'? 0 :  this.formatNumber(b[key]))
					: (format[key]==='%'? (this.isEmpty(b[key]) || b[key]==='n/a'? 0 : this.formatNumber(b[key].replace('%', ''))) : b[key])

                    sorted = keySort(val1, val2, direction)
                    index++
                }
            }
            return sorted
		})
	}

	arrayMove(arr, old_index, new_index) {
		if (new_index >= arr.length) {
			var k = new_index - arr.length + 1;
			while (k--) {
				arr.push(undefined);
			}
		}
		arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
		return arr; // for testing
	}

	calc(fn) {
		return new Function('return ' + fn)()
	}

	createField(name,label,format,filter,show,width, action,span,tooltip) {
		let obj = {}
		obj['name'] = name
		obj['label'] = label
		obj['format'] = format
		obj['filter'] = filter
		obj['show'] = show
		obj['min-width'] = width
		obj['action'] = action
		obj['span'] = span
		obj['tooltip'] = tooltip
		return obj
	}

	delay = ( function() {
	var timer = 0;
	return function(callback, ms) {
		clearTimeout (timer);
		timer = setTimeout(callback, ms);
		}
	})()

	download(url) {
		var link=document.createElement('a')
		document.body.appendChild(link)
		link.href=url
		link.click()
		document.body.removeChild(link)
	}

	checkChange(obj1, obj2, list) {
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

	sendMessage(sender, receiver, subject, content, sentto_all, type) {
		let connection = this.$connection()        
		let data = {
			sender: sender,
			receiver: sentto_all==='yes'? receiver : receiver,
			subject: subject,
			content: content,
			sentto_all: sentto_all==='yes'? true: false, 
			type: type
		}
		if(sentto_all==='yes')
			connection.insert('messagelist', data, 'all', true)
		else 
			connection.insert('messagelist', data, receiver, true)
	}

	upload(file, type, user) {
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
		let fileName = this.yyyymmddhhmmss(new Date()) + '-' + file.name	
		data.append('name', fileName)
		data.append('file', file)
		data.append('type', type)
		data.append('size', file.size)
		data.append('user', user)
		return {form: data, name: fileName, type: type, size: file.size, file: file}
	}

	render(docid, file) {
        var reader = new FileReader()
        reader.onload = function(){
		  var output = document.getElementById(docid)
          output.src = reader.result
        }
        reader.readAsDataURL(file)
	}
  
	openGallery(source, target) {
		var input = document.getElementById(source)
		var output = document.getElementById(target)
		if(input && output) output.setAttribute('src', input.getAttribute('src'))
	}

	stripHtml(html)
	{
		var tmp = document.createElement("DIV")
		tmp.innerHTML = html
		return tmp.textContent || tmp.innerText || ""
	}

    checkExternalLink(content) {
		var external = false
		var urlRegex = /(https?:\/\/[^\s]+)/g;
		content.replace(urlRegex, function(url) {
			if(!(url.indexOf('localhost')>=0 || url.indexOf('daytot.edu.vn')>=0)) external = true
		})
		return external? {result: true, text: 'Nội dung chứa đường link ra bên ngoài website'} : {result: false}
    }

	shuffle(array) {
		var currentIndex = array.length, temporaryValue, randomIndex;
	  
		// While there remain elements to shuffle...
		while (0 !== currentIndex) {
	  
		  // Pick a remaining element...
		  randomIndex = Math.floor(Math.random() * currentIndex);
		  currentIndex -= 1;
	  
		  // And swap it with the current element.
		  temporaryValue = array[currentIndex];
		  array[currentIndex] = array[randomIndex];
		  array[randomIndex] = temporaryValue;
		}
	  
		return array
	}

	dummyData(data, count) {
		let list = this.copy(data)
		for (let index = 0; index < count; index++) {
		  if(data.length<index+1) list.push({dummy: true})
		}
		return list
	}
	
	scrollFunction() {
		var button = document.getElementById("returnTop")
		window.onscroll = function() {scrollFunction()}
		function scrollFunction() {
			if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
					button.style.display = "block";
			} else {
					button.style.display = "none";
			}
		}
	}

	checkPhone(contact) {
		var obj = {name: 'contact', text: undefined}
		if (this.isEmpty(contact)) {
			obj = { name: 'contact', text: 'Số điện thoại di động không được bỏ trống.' }
		} else if (!this.isNumber(contact)) {
			obj = { name: 'contact', text: 'Số điện thoại di động không hợp lệ.' }
		} else if(contact.length<9 || contact.length>11) {
			obj = { name: 'contact', text: 'Số điện thoại di động phải có từ 9-11 số.' }
		}
		return obj
	}

	checkEmailPhone(contact) {
		const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
		var obj = {name: 'contact', text: undefined}
		if (this.isEmpty(contact)) {
			obj = { name: 'contact', text: 'Email hoặc số điện thoại di động không được bỏ trống.' }
		} else if (!re.test(String(contact).toLowerCase()) && !this.isNumber(contact)) {
			obj = { name: 'contact', text: 'Email hoặc số điện thoại di động không hợp lệ.' }
		} else if(this.isNumber(contact) && (contact.length<9 || contact.length>11)) {
			obj = { name: 'contact', text: 'Số điện thoại di động không hợp lệ.' }
		}
		return obj
	}

	convert(d) {
	// Converts the date in d to a date-object. The input can be:
	//   a date object: returned without modification
	//  an array      : Interpreted as [year,month,day]. NOTE: month is 0-11.
	//   a number     : Interpreted as number of milliseconds
	//                  since 1 Jan 1970 (a timestamp) 
	//   a string     : Any format supported by the javascript engine, like
	//                  "YYYY/MM/DD", "MM/DD/YYYY", "Jan 31 2009" etc.
	//  an object     : Interpreted as an object with year, month and date
	//                  attributes.  **NOTE** month is 0-11.
		return (
				d.constructor === Date ? d :
				d.constructor === Array ? new Date(d[0],d[1],d[2]) :
				d.constructor === Number ? new Date(d) :
				d.constructor === String ? new Date(d) :
				typeof d === "object" ? new Date(d.year,d.month,d.date) :
				NaN
			)
	}

	compare(a,b) {
	// Compare two dates (could be of any type supported by the convert
	// function above) and returns:
	//  -1 : if a < b
	//   0 : if a = b
	//   1 : if a > b
	// NaN : if a or b is an illegal date
	// NOTE: The code inside isFinite does an assignment (=).
	return (
			isFinite(a=this.convert(a).valueOf()) &&
			isFinite(b=this.convert(b).valueOf()) ?
			(a>b)-(a<b) :
			NaN
		)
	}
	
	connection(report_name, company_type) {
		let name = "";
		if (report_name === "CDKT")
		  name = "bs" + company_type.toLowerCase();
		else if (report_name === "KQKD" || report_name === "KQKD-LK")
		  name = "bp" + company_type.toLowerCase();
		else if (report_name === "LCTT-TT" || report_name === "LCTT-TT-LK")
		  name = "cftt" + company_type.toLowerCase();
		else if (report_name === "LCTT-GT" || report_name === "LCTT-GT-LK")
		  name = "cfgt" + company_type.toLowerCase();
	
		return name
	}

	companyFilter(companylist, text, type) {
		if(companylist===undefined) return

		let list1 = companylist.filter(v=>v.stock_code.toLowerCase().indexOf(text.toLowerCase()) >= 0)
		list1.map(v=>v.index = v.stock_code.toLowerCase().indexOf(text.toLowerCase()))
		
		let list11 = list1.filter(v=>v.index===0)
		list11.sort((a,b) => (a.stock_code.length - b.stock_code.length))
		let list12 = list1.filter(v=>v.index>0)
		list12.sort((a,b) => (a.index - b.index))
		list1 = list11.concat(list12)

		let list2 = companylist.filter(v=>v.name.toLowerCase().indexOf(text.toLowerCase()) >= 0 && v.stock_code.toLowerCase().indexOf(text.toLowerCase()) <0)
		list2.map(v=>v.index = v.name.toLowerCase().indexOf(text.toLowerCase()))

		let list21 = list2.filter(v=>v.index===0)
		list21.sort((a,b) => (a.name.length - b.name.length))
		let list22 = list2.filter(v=>v.index>0)
		list22.sort((a,b) => (a.index - b.index))
		list2 = list21.concat(list22)

		let list = list1.concat(list2)
		if(type==='full') {
			let array = JSON.parse(JSON.stringify(list))
			array.map(v=>v.label = v.stock_code + ' | ' + v.name)
			return array
		} else return list
	}
}

const mixing = new Mixing()
export default mixing