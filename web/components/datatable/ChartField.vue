<template>
  <div>
    <p class="panel-tabs">
      <a
        v-for="(v, i) in types"
        :key="i"
        :class="
          selectType
            ? selectType.code === v.code
              ? 'is-active'
              : ''
            : ''
        "
        @click="selectType = v"
      >
        {{ v.name }}
      </a>
    </p>

      <template v-if="selectType? selectType.code==='color' : false">
          <div class="field is-horizontal pb-1 mt-2">
            <div class="field-body">
              <div class="field">
                <label class="label fs14">Màu nền </label>
                <p class="control fs14">
                  <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioBGcolor"
                    :native-value="v" @input=" v.code==='none'? update('chart', 'backgroundColor', '#313131') : false">
                      {{v.name}}
                    </b-radio>
                </p>
              </div>
              <div class="field" v-if="radioBGcolor? radioBGcolor.code==='option' : false">
                <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
                <p class="control fs14">
                  <input type="color" v-model="bgcolor" @input="update('chart', 'backgroundColor', $event.target.value)">
                </p>
              </div>
            </div>
          </div>

          <div class="field mt-1">
          <label class="label fs14">Tiêu đề </label>
          <p class="control fs14">
            <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioTitle"
                :native-value="v" @input="update('title', 'style', v.code==='none'? {display: 'none'} : undefined)">
                {{v.name}}
              </b-radio>
          </p>
        </div>

        <div class="field is-horizontal mt-1" v-if="radioTitle? radioTitle.code==='option' : false">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Cỡ chữ </label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="titleSize"
              @change="changeTitle('textsize', $event.target.value)">
            </p>
            </div>
            <div class="field">
              <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <input type="color" @change="changeTitle('color', $event.target.value)" v-model="titleColor">
              </p>
            </div>
          </div>
        </div>

        <div class="field mt-1" v-if="radioTitle? radioTitle.code==='option' : false">
          <label class="label fs14">Text</label>
          <p class="control fs14">
            <input class="input is-small" type="text" placeholder="Nhập số" v-model="title"
            @change="update('title', 'text', $event.target.value)">
          </p>
        </div>
      
        <div class="field mt-1">
          <label class="label fs14">Legend </label>
          <p class="control fs14">
            <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioLegend"
                :native-value="v" @input="update('legend', 'enabled', v.code==='none'? false : true)">
                {{v.name}}
              </b-radio>
          </p>
        </div>
        <div class="field is-horizontal mt-2" v-if="radioLegend? radioLegend.code==='option' : false">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Cỡ chữ </label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="legendSize"
              @change="changeLegend('textsize', $event.target.value)">
            </p>
    
            </div>
            <div class="field">
              <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <input type="color" @change="changeLegend('color', $event.target.value)" v-model="legendColor">
              </p>
            </div>
          </div>
        </div>
        <div class="field is-horizontal mt-2">
            <div class="field-body">
              <div class="field">
                <label class="label fs14">Màu cột</label>
                <p class="control fs14">
                  <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioSeriesColor"
                    :native-value="v" @input=" v.code==='none'? updateSeriesColor() : false">
                      {{v.name}}
                    </b-radio>
                </p>
              </div>
              <div class="field" v-if="radioSeriesColor? radioSeriesColor.code==='option' : false">
                <label class="label fs14"> Mã màu <span class="has-text-danger"> * </span> </label>
                <p class="control fs14">
                  <input type="color" v-model="seriesColor" @input="updateSeriesColor($event.target.value)">
                </p>
              </div>
            </div>
          </div>
                <div class="field is-horizontal mt-2">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Lề (margin)</label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="margin"
              @change="update('chart', 'margin', $event.target.value)">
            </p>
            </div>
            <div class="field">
              <label class="label fs14">Chiều rộng</label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="width"
              @change="update('chart', 'width', $event.target.value)">
            </p>
            </div>
            <div class="field">
              <label class="label fs14">Chiều cao</label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="height"
              @change="update('chart', 'height', $event.target.value)">
            </p>
            </div>
            
          </div>
        </div>
      </template>

        <template v-if="selectType? selectType.code==='xaxis' : false">
           <div class="field mt-3">
          <label class="label fs14">Nhãn </label>
          <p class="control fs14">
            <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioXaxis"
                :native-value="v" @input="changeXaxis(v.code, true)">
                {{v.name}}
              </b-radio>
          </p>
        </div>
        <template v-if="radioXaxis? radioXaxis.code==='option' : false">
        <div class="field is-horizontal mt-2">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Cỡ chữ </label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="xaxisSize"
              @change="changeXaxis('textsize', $event.target.value)">
            </p>
    
            </div>
            <div class="field">
              <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <input type="color" @change="changeXaxis('color', $event.target.value)" v-model="xaxisColor">
              </p>
          </div>
        </div>
        </div>

          <div class="field mt-2">
            <label class="label fs14">Góc nghiêng </label>
                <p class="control fs14">
            <input class="input is-small" type="text" placeholder="Nhập số" v-model="xaxisRotation"
            @change="update3key('xAxis', 'labels', 'rotation' , $event.target.value)">
          </p>
          </div>
        </template>
        </template>

         <template v-if="selectType? selectType.code==='yaxis' : false">
           <div class="field mt-3">
          <label class="label fs14">Nhãn </label>
          <p class="control fs14">
            <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioYaxis"
                :native-value="v" @input="changeYaxis(v.code, true)">
                {{v.name}}
              </b-radio>
          </p>
        </div>
        <template v-if="radioYaxis? radioYaxis.code==='option' : false">
        <div class="field is-horizontal mt-2">
          <div class="field-body">
            <div class="field">
              <label class="label fs14">Cỡ chữ </label>
                  <p class="control fs14">
              <input class="input is-small" type="text" placeholder="Nhập số" v-model="yaxisSize"
              @change="changeYaxis('textsize', $event.target.value)">
            </p>
    
            </div>
            <div class="field">
              <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
              <p class="control fs14">
                <input type="color" @change="changeYaxis('color', $event.target.value)" v-model="yaxisColor">
              </p>
            </div>
          </div>
        </div>
          <div class="field mt-2">
            <label class="label fs14">Góc nghiêng </label>
                <p class="control fs14">
            <input class="input is-small" type="text" placeholder="Nhập số" v-model="yaxisRotation"
            @change="update3key('yAxis', 'labels', 'rotation' , $event.target.value)">
          </p>
          </div>
        </template> 
        </template>

         <template v-if="selectType? selectType.code==='value' : false">
            <div class="field mt-3">
            <label class="label fs14">Nhãn </label>
            <p class="control fs14">
              <b-radio v-for="(v,i) in colorchoice.filter(v=>v.code!=='condition')" :key="i" v-model="radioValue"
                  :native-value="v" @input="changeValue(v.code, true)">
                  {{v.name}}
                </b-radio>
            </p>
          </div>
          <template v-if="radioValue? radioValue.code==='option' : false">
          <div class="field is-horizontal mt-2">
            <div class="field-body">
              <div class="field">
                <label class="label fs14">Cỡ chữ </label>
                    <p class="control fs14">
                <input class="input is-small" type="text" placeholder="Nhập số" v-model="valueSize"
                @change="changeValue('textsize', $event.target.value)">
              </p>
              </div>
                   <div class="field">
            <label class="label fs14">Góc nghiêng </label>
                <p class="control fs14">
            <input class="input is-small" type="text" placeholder="Nhập số" v-model="valueRotation"
            @change="update4key('plotOptions', 'column', 'dataLabels', 'rotation', $event.target.value)">
          </p>
          </div>
            <div class="field" style="width:30%">
                <label class="label fs14"> Màu chữ <span class="has-text-danger"> * </span> </label>
                <p class="control fs14">
                  <input type="color" @change="changeValue('color', $event.target.value)" v-model="valueColor">
                </p>
              </div>
            </div>
          </div>
          </template>
          <p><label class="label fs14">Chọn cột hiển thị</label></p>
          <div class="field is-grouped is-grouped-multiline mt-2">
           <div class="control" v-for="(v,i) in args" :key="i">
          <div class="tags has-addons">
            <a class="tag is-primary">{{v.label}}</a>
            <a class="tag is-delete" @click="remove(args, i)"></a>
          </div>
      </div>
          </div>
          </template>
        </div>
</template>

<script>
export default {
  props: ['fields'],

  data() {
    return {
      args: [],
      radioSeriesColor: undefined,
      radioBGcolor: undefined,
      selectType: {code: 'color', name: 'Hiển thị'},
      types: [{code: 'color', name: 'Hiển thị'}, {code: 'xaxis', name: 'X axis'}, 
      {code: 'yaxis', name: 'Y axis'}, {code: 'value', name: 'Giá trị'}],
      bgcolor: undefined,
      radioLegend: undefined,
      titleSize: undefined,
      titleColor: undefined,
      radioTitle: undefined,
      title: undefined,
      legendSize: undefined,
      legendColor: undefined,
      xaxisSize: undefined,
      xaxisColor: undefined,
      radioXaxis: undefined,
      xaxisRotation: undefined,
      yaxisSize: undefined,
      yaxisColor: undefined,
      radioYaxis: undefined,
      yaxisRotation: undefined,
      valueSize: undefined,
      valueColor: undefined,
      radioValue: undefined,
      valueRotation: undefined,
      isSwitched: false,
      chartType: [{code: 'column', name: 'Dạng cột'}, {code: 'cylinder', name: 'Hình trụ'}, 
      {code: 'spline', name: 'Đường thẳng'}],
      showChart: [{code: 'no', name: 'Không'}, {code: 'yes', name: 'Có'}], 
      radioType: undefined,
      radioShow: undefined,
      chartoption: undefined,
      margin: 0,
      width: 50,
      height: 26,
      seriesColor: '#ebebeb',
      colors: ['#0F9D58','#ffd60a','#abc4ff','#C0E8D5','#B284BE','#72A0C1','#EDEAE0','#F0F8FF','#C46210','#EFDECD','#E52B50','#9F2B68','#F19CBB','#AB274F','#D3212D','#3B7A57','#FFBF00','#FF7E00','#9966CC','#3DDC84','#CD9575','#665D1E','#915C83','#841B2D','#FAEBD7']
    }
  },

  created() {
    this.args = this.$copy(this.fields)
    this.getData()
  },

  watch:  {
    chartoption: function(newVal) {
      if(newVal) this.$emit('chartoption', newVal)
    }
  },

  computed: {
    reporttype: {
      get: function () {
        return this.$store.state.reporttype;
      },
      set: function (val) {
        this.$store.commit("updateReportType", { reporttype: val });
      },
    },

    reportperiod: {
      get: function () {
        return this.$store.state.reportperiod;
      },
      set: function (val) {
        this.$store.commit("updateReportPeriod", { reportperiod: val });
      }
    },

    colorchoice: {
      get: function() {return this.$store.state.colorchoice},
      set: function(val) {this.$store.commit("updateColorChoice", {colorchoice: val})}
    },

    pagedata: {
      get: function() {return this.$store.state.pagedata},
      set: function(val) {this.$store.commit('updatePageData', {pagedata: val})}
    },
  },

  methods: {
    remove(args, i) {
      this.$delete(args, i)
      this.$emit('changefields', args)
    },

    getData() {
      this.seriesColor = this.colors[Math.floor(Math.random()*this.colors.length)]
      this.setOption()
      this.radioSeriesColor = this.colorchoice.find(v=>v.code==='option')
      this.radioBGcolor = this.colorchoice.find(v=>v.code==='none')
      this.radioLegend = this.colorchoice.find(v=>v.code==='none')
      this.radioTitle = this.colorchoice.find(v=>v.code==='none')
      this.radioXaxis = this.colorchoice.find(v=>v.code==='none')
      this.radioYaxis = this.colorchoice.find(v=>v.code==='none')
      this.radioZaxis = this.colorchoice.find(v=>v.code==='none')
      this.radioValue = this.colorchoice.find(v=>v.code==='none')
      this.radioType = this.chartType.find(v=>v.code===(this.chartoption? this.chartoption.chart.type : 'column'))
      this.radioShow = this.showChart.find(v=>v.code===(this.chartoption? 'yes' : 'no'))
      
      this.title = this.chartoption.title.text? this.chartoption.title.text : undefined
      this.titleSize = this.chartoption.title.style.fontSize? this.chartoption.title.style.fontSize : undefined
      this.titleSize = this.titleSize? this.titleSize.replace('px', '') : undefined
      this.titleColor = this.chartoption.title.style.color? this.chartoption.title.style.color : undefined
      this.legendColor = this.chartoption.legend.itemStyle.color? this.chartoption.legend.itemStyle.color : undefined
      this.legendSize = this.chartoption.legend.itemStyle.fontSize? this.chartoption.legend.itemStyle.fontSize : undefined
      this.legendSize = this.legendSize? this.legendSize.replace('px', '') : undefined
      this.xaxisColor = this.chartoption.xAxis.labels.style.color? this.chartoption.xAxis.labels.style.color : undefined
      this.xaxisSize = this.chartoption.xAxis.labels.style.fontSize? this.chartoption.xAxis.labels.style.fontSize : undefined
      this.xaxisSize = this.xaxisSize? this.xaxisSize.replace('px', '') : undefined
      this.xaxisRotation = this.chartoption.xAxis.labels.rotation? this.chartoption.xAxis.labels.rotation : undefined
      this.yaxisColor = this.chartoption.yAxis.labels.style.color? this.chartoption.yAxis.labels.style.color : undefined
      this.yaxisSize = this.chartoption.yAxis.labels.style.fontSize? this.chartoption.yAxis.labels.style.fontSize : undefined
      this.yaxisSize = this.yaxisSize? this.yaxisSize.replace('px', '') : undefined
      this.yaxisRotation = this.chartoption.yAxis.labels.rotation? this.chartoption.yAxis.labels.rotation : undefined
      this.valueColor = this.chartoption.plotOptions.column.dataLabels.style.color? this.chartoption.plotOptions.column.dataLabels.style.color : undefined
      this.valueSize = this.chartoption.plotOptions.column.dataLabels.style.fontSize? this.chartoption.plotOptions.column.dataLabels.style.fontSize : undefined
      this.valueSize = this.valueSize? this.valueSize.replace('px', '') : undefined
      this.valueRotation = this.chartoption.plotOptions.column.dataLabels.rotation? this.chartoption.plotOptions.column.dataLabels.rotation : undefined
      this.valueRotation = this.valueRotation? Number(this.valueRotation) : undefined
    },

    changeTitle(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.title.style.color = value : copy.title.style.fontSize = value + 'px'
      this.chartoption = copy
    },

    changeLegend(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.legend.itemStyle.color = value : copy.legend.itemStyle.fontSize = value + 'px'
      this.chartoption = copy
    },
    
    update(key1, key2, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      key2? copy[key1][key2] = value : copy[key1] = value
      this.chartoption = copy
    },

    update3key(key1, key2, key3, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      copy[key1][key2][key3] = key3==='rotation'? Number(value) : value
      this.chartoption = copy
    },

    update4key(key1, key2, key3, key4, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      copy[key1][key2][key3][key4] = value
      this.chartoption = copy
    },

    changeZaxis(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.zAxis.labels.style.color = value : false
      type==='textsize'? copy.zAxis.labels.style.fontSize = value + 'px' : false
      copy.zAxis.labels.enabled = type==='none'? false : true
      this.chartoption = copy
    },

    changeXaxis(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.xAxis.labels.style.color = value : false
      type==='textsize'? copy.xAxis.labels.style.fontSize = value + 'px' : false
      copy.xAxis.labels.enabled = type==='none'? false : true
      this.chartoption = copy
    },

    changeYaxis(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.yAxis.labels.style.color = value : false
      type==='textsize'? copy.yAxis.labels.style.fontSize = value + 'px' : false
      copy.yAxis.labels.enabled = type==='none'? false : true
      this.chartoption = copy
    },

    changeValue(type, value) {
      if(this.$empty(value)) return
      let copy = this.$clone(this.chartoption)
      type==='color'? copy.plotOptions.column.dataLabels.style.color = value : false
      type==='textsize'? copy.plotOptions.column.dataLabels.style.fontSize = value + 'px' : false
      if(type==='none' || type==='option') {
        copy.plotOptions.column.dataLabels.enabled = type==='none'? false : true
        copy.plotOptions.series.dataLabels.enabled = type==='none'? false : true
      }
      this.chartoption = copy
    },

    updateSeriesColor(v) {
      this.chartoption.series[0].color = v? v : this.colors[Math.floor(Math.random()*this.colors.length)]
    },

    openChart(value) {
      if(value==='no') this.chartoption = undefined
      else if(value==='yes') {
        this.setOption()
        this.$emit('redraw')
      }
    },

    setOption() {
      let self = this
      this.chartoption = {
        chart: {
          type: 'column',
          backgroundColor: 'white',
          margin: this.margin, width:this.width, height: this.height
        },
        legend: {
          align: 'left',
          verticalAlign: 'top',
          layout: 'vertical',
          enabled: false,
          itemStyle: {color: '#FFFFFF', fontSize: '10px'}
        },
        credits: {
          enabled: false
        },
        title: {
          text: null,
          style: {display: 'none', fontSize: '20px', color: '#FFFFFF'}
        },
        tooltip: {enabled: false},
        yAxis: {
          title: {
            enabled: false
          },
          labels: {
            rotation: 0,
            style:{
              fontSize:'12px',
              color: '#FFFFFF'
            },
            formatter: function() {
               return self.$numtoString(this.value)
            }
          }
        },

        xAxis: {
          categories: [],
          gridLineWidth: 1,
          labels: {
            rotation: -30,
            style:{
              fontSize:'10px',
              color: '#FFFFFF'
            }
          }
        },

        plotOptions: {
          column: {
            dataLabels: {
              rotation: 10,
              enabled: false,
              formatter:function() {
                let found = self.pagedata.fields.find(v=>v.name===this.key || v.label===this.key)
                found = found? found : {}
                return found.unit==='0.01'? (this.y? (this.y*100).toFixed(1) + '%' : '') : self.$numtoString(this.y)
              },
              style: {
                fontWeight: 'normal',
                fontSize:'10px',
                color: 'white'
              }
            }
          },
          series: {
            dataLabels: {
              enabled: false
            }
          }
        },
        series: [{name: 'series1', color: this.seriesColor}],
        lang: {
          viewFullscreen: 'Xem toàn màn hình',
          printChart: 'In biểu đồ',
          downloadPNG: 'Tải file PNG',
          downloadPDF: 'Tải file PDF',
          exitFullscreen: 'Thu nhỏ'
        },
        exporting: {
          enabled: false,
          buttons: {
            contextButton: {
              menuItems: ["viewFullscreen", "printChart", "downloadPNG", "downloadPDF"]
            }
          }
        }
      }
    }
  }
}
</script>