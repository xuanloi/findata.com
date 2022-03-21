import Vue from 'vue'
Vue.use( {
  install(Vue) {

    //==========Convert=================
    Vue.prototype.$isNumber = function(val) {
      if(val === undefined || val === null || val === '' || val==="") return false
      val = val.toString().replace(/,/g, "")
      return !isNaN(val)
    }

    Vue.prototype.$numtoString = function(val, type) {
      if(val === undefined || val === "" || val==='' || val === null) return
      val = val.toString().replace(/,/g, "")
      if(isNaN(val)) return
      return type? Number(val).toLocaleString(type) : Number(val).toLocaleString('en-EN')
    }

    Vue.prototype.$formatNumber = function(val) {
      if(val === undefined || val === "" || val==='' || val === null) return
      val = val.toString().replace(/,/g, "")
      val = val.indexOf('%') >0? Number(val.toString().replace(/%/g, "")) / 100 : Number(val)
      return val
    }

    Vue.prototype.$formatUnit = function(val, unit, decimal, string) {
      val = this.$formatNumber(val)
      if(!val) return
      let percentage = (unit===0.01 || unit==="0.01")? '%' : ''
      val = (val/(unit? Number(unit) : 1)).toFixed(decimal? decimal : 2)
      return string? (this.$numtoString(val) + percentage) : val
    }
  
  //==========Calculate=================
    Vue.prototype.$calc = function(fn) {
      return new Function('return ' + fn)()
    }

    Vue.prototype.$calculate = function(row, tags, formula, decimal, unit) {
      let val = this.$copy(formula)
      tags.forEach(v => {
        let myRegExp = new RegExp(v, 'g')
        val = val.replace(myRegExp, this.$formatNumber(row[v]))			
      })
      
      try {
        let value = this.$calc(val)
        if(isNaN(value) || value===Number.POSITIVE_INFINITY || value===Number.NEGATIVE_INFINITY) {
          var result = {success: false, value : value}
        } else {
          if(unit==='%' || unit==='0.01') {
            value = this.$numtoString(this.$formatNumber((value*100).toFixed(decimal? decimal : 1))) + '%'
          } else if(decimal) value = this.$numtoString(this.$formatNumber(value.toFixed(decimal)))
          var result = {success: true, value: value}
        }
      }
      catch(err) {
        var result = {success: false, value : undefined}
      }
		  return result
	  }

    Vue.prototype.$summary = function(arr, fields, type) {
      let obj = {}
      if(type==='total') {
        fields.map(x=> obj[x] = arr.map(v=>v[x]? v[x] : 0).reduce((a, b) => a + b, 0))
      } else if(type==='min') {
        fields.map(x=>obj[x] = Math.min(...arr.map(v=>v[x])))
      }
      else if(type==='max') {
        fields.map(x=>obj[x] = Math.max(...arr.map(v=>v[x])))
      }
      else if(type==='count') {
        fields.map(x=>obj[x] = arr.map(v=>!this.$empty(v[x])).length)
      }
      return obj
    }

    Vue.prototype.$calculateFields = function(pagename) {
      var pagedata = this.$store.state[pagename]
      let arr = pagedata.fields.filter(h=>h.formula)
      if(arr.length===0) return
      arr = this.$multiSort(arr, {level: 'asc'})
      let copy = this.$copy(pagedata.data)
      copy.map(v=>{
        arr.map(x=>{
          let res = this.$calculate(v, x.tags, x.formula)
          if(res? res.success : false) v[x.name] = this.$formatUnit(res.value, x.unit, x.decimal, true)
        })
      })
      this.$store.commit('updateState', {name: pagename, key: 'data', data: copy})
    }

  //==========Array====================
    Vue.prototype.$formatArray = function(data, fields) {
      let args = fields.filter(v=>v.format==='number')
      data.map(v=>{
        args.map(x=>{
          v[x.name] = v[x.name]? (this.$numtoString((v[x.name]/x.unit).toFixed(1)) + (x.unit==='0.01'? '%' : '')) : undefined
        })
      })
      return data
    }

    Vue.prototype.$unique = function(arr, keyProps) {
      const kvArray = arr.map(entry => {
      const key = keyProps.map(k => entry[k]).join('|');
      return [key, entry];
      });
      const map = new Map(kvArray);
      return Array.from(map.values());
    }
    
    Vue.prototype.$arrayMove = function(arr, old_index, new_index) {
      if (new_index >= arr.length) {
        var k = new_index - arr.length + 1;
        while (k--) {
          arr.push(undefined);
        }
      }
      arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
      return arr; // for testing
    }

    Vue.prototype.$multiSort = function(array, sortObject = {}, format = {}) {
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
        let val1 = format[key]==='number'? (this.$empty(a[key])? 0 :  this.$formatNumber(a[key].replace('%', ''))) : a[key]
        let val2 = format[key]==='number'? (this.$empty(b[key])? 0 :  this.$formatNumber(b[key].replace('%', ''))) : b[key]
                  sorted = keySort(val1, val2, direction)
                  index++
              }
          }
        return sorted
      })
    }
  }
})