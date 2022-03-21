/* eslint-disable */

export default class Api {
  data = []
  langguage = 'vietnamese'
  ready = undefined

  // set data object
  set (ele) {
	if (ele === null || ele === undefined) return
	if(ele instanceof Array) {
	  this.data = ele
	} else {
	  this.data = []
	  this.data.push(ele)
	}
  }

  //============Get object by index or id==================
  // get by index
  getbyindex (index) {
	return this.data[index]
  }

  // get by id
  getbyid (id) {
	return this.data.find(function (element) {
	  return element.id == id
	})
  }
//========end================================================

  getvalue (obj) {
	if (obj === undefined || obj === null) return ''
	if (obj.enable !== true) return ''
	return (this.langguage === 'vietnamese' ? obj.value : obj.value1)
  }

  getlist (obj) {
	if (obj === undefined) return []
	return obj
  }

  getval (obj, field) {
	if (obj === undefined || obj === null) return ''
	var val = ''

	switch (field) {
	  case 'id':
		val =  obj.id
		break
	  case 'category':
		val = obj.category
		break
	  case 'classify':
		val = obj.classify
		break;
	  case 'code':
		val = obj.code
		break
	  case 'value':
		val = (this.langguage === 'vietnamese' ? obj.value : obj.value1)
		break
	  case 'detail':
		val = obj.detail
		break;
	  case 'icon':
		val = obj.icon
		break;
	  case 'image':
		val = []
		val.push(obj.image)
		break
	  case 'link':
		val = obj.link
		break;
	  case 'enable':
		val = obj.enable
		break
	  default:
		if(obj[field] !== undefined) val = obj[field]
		break
	}

	return val
  }

  getvallist (obj, field) {
	if (obj === undefined) return ''
	var val = []

	obj.forEach(ele => {
	  if(ele.hasOwnProperty(field)){
		val.push(ele[field])
	  }
	});
	return val
  }

//=======Find objects=======================
  find1var (category) {
	return this.data.find(function (element) {
	  return element.category === category
	})
  }

  find2var (category, classify) {
	return this.data.find(function (element) {
	  return element.category === category && element.classify === classify
	})
  }

  find3var (category, classify, code) {
	return this.data.find(function (element) {
	  return element.category === category && element.classify === classify && element.code === code
	})
  }
//======End find====================

//======Filter======================
  filter1var (category) {
	return this.data.filter(ele => (ele.category === category))
  }

  filter2var (category, classify) {
	return this.data.filter(ele => (ele.category === category && ele.classify === classify))
  }

  filter3var (category, classify, code) {
	return this.data.filter(ele => (ele.category === category && ele.classify === classify && ele.code === code))
  }
//====End filter==============================

//====Globally Unique Identifier==============
  guid() {
	function s4() {
		return Math.floor((1 + Math.random()) * 0x10000)
		.toString(16)
		.substring(1);
	}
	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
  }

  yyyymmdd(date) {                                   
	var yyyy = date.getFullYear().toString();                                    
	var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based         
	var dd  = date.getDate().toString();             
						
	return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
  }

  checkisNumber(val) {
	if(val === undefined || val === null || val === '') return false
	val = val.toString().replace(/,/g, "")
	return !isNaN(val)
  }

  formatNumtoString(val) {
	if(val === undefined || val === '' || val === null) return
		val = val.toString().replace(/,/g, "")
	if(isNaN(val)) return
	return Number(val).toLocaleString()
  }

  formatNumber(val) {
	if(val === undefined || val === null) return
	val = val.toString().replace(/,/g, "")
	return Number(val)
  }

  delay = ( function() {
	var timer = 0;
	return function(callback, ms) {
		clearTimeout (timer);
		timer = setTimeout(callback, ms);
		}
	})()

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
}
