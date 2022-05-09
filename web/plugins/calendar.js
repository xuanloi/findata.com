import Vue from 'vue'
Vue.use( {
  install(Vue){
    Vue.prototype.$daysInMonth = function(year, month) {
      let arr = []
      let startDate = this.$dayjs(new Date(year, month, 1))
      let endDate = this.$dayjs(new Date(year, month, 1))
      while (endDate.month()===startDate.month()) {
        arr.push(endDate)
        endDate = endDate.add(1, 'day')
      }
      return arr
    }

    Vue.prototype.$fromToDate = function(start, end) {
      let startDate = this.$dayjs(start)
      let endDate = this.$dayjs(end)
      let arr = []
      while (endDate.diff(startDate, 'day')>=0) {
        arr.push(startDate)
        startDate = startDate.add(1, 'day')
      }
      return arr
    }

    Vue.prototype.$calendarMonth = function(year, month) {
      var createDate = function(v, x, y) {
        return v + '/' + (x<10? '0' + x.toString() : x.toString()) + '/' + (y<10? '0' + y.toString() : y.toString())
      }
      var weekday = require('dayjs/plugin/weekday')
      this.$dayjs.extend(weekday)
      var weekOfYear = require('dayjs/plugin/weekOfYear')
      this.$dayjs.extend(weekOfYear)

      let days = Array.from({length: this.$dayjs(createDate(year, month, 1)).daysInMonth()}, (_, i) => i + 1)
      let arr = []
      days.map(v=>{
          for (let i = 0; i < 7; i++) { 
          let thedate = this.$dayjs(createDate(year, month, v)).weekday(i)
          let date = this.$dayjs(new Date(thedate.$d)).format("YYYY/MM/DD")
          let dayPrint = this.$dayjs(new Date(thedate.$d)).format("DD")
          let monthOfDate = this.$dayjs(date).month() + 1         
          let found = arr.find(x=>x.date===date)
          if(!found) {
            let dayOfWeek = this.$dayjs(date).day() 
            let week = this.$dayjs(date).week() 
            let ele = {date: date, week: week, day: v, dayOfWeek: dayOfWeek, dayPrint: dayPrint, monthOfDate: monthOfDate, currentMonth: month}
            arr.push(ele)
          }
        }
      })
      return arr
    }
  }
})