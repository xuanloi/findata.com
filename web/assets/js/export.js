/* eslint-disable */
export default class Export {
    data = []
    dataTypes = {}
    filename = ''
    fields = []

    pad2(n) { return n < 10 ? '0' + n : n }

    getdatetime() {
        var date = new Date()
        return date.getFullYear().toString() + this.pad2(date.getMonth() + 1) + this.pad2( date.getDate()) + this.pad2( date.getHours() ) + this.pad2( date.getMinutes() ) + this.pad2( date.getSeconds())
    }
   
    // set data object
    set (data, filename, dataTypes, fields) {
        this.data = data
        this.dataTypes = dataTypes
        this.filename = filename
        this.fields = fields
    }

    exportfile() {
        /* original data */
        var _filename  = this.getdatetime() + '-' + this.filename + '.xlsx'
        
        let list = []
        let ele = {}
        this.data.forEach(element => {
            Object.keys(this.dataTypes).forEach((type, index) => {
                ele[type] =  element[this.fields[index]]    
            })
            list.push(JSON.parse(JSON.stringify(ele)))
        })

        var XLSX = require('xlsx');

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

    exportItem() {
        var _filename  = this.getdatetime() + '-' + this.filename + '.xlsx'
        let val = ''
        let ele = {}
        let list = []

        this.data.forEach(element => {
            switch (element.level) {
                case 0:
                    val = ''
                    break;
                
                case 1:
                    val = '      '
                    break;

                case 2:
                    val = '            '
                    break;
                
                case 3:
                    val = '                  '
                    break;
                             
                case 4:
                    val = '                        '
                    break;

                case 5:
                    val = '                              '
                    break;
            
                default:
                    val = ''
                    break;
            }

            ele = {item: element.item, value: val + element.value, auto_calc: element.formula !== ''? '+' : '',
            input: element.formula === ''? null :  this.excelFormula(element.formula)}
            list.push(ele)
        })

        var XLSX = require('xlsx');

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

    excelFormula(val) {
        let str = val.replace(/-/g, '+')
        let array = str.split('+')
        let formula = val
        array.forEach(ele => {
           let index = this.data.findIndex(v=>v.item===ele)
           formula = formula.replace(new RegExp(ele, "g"), 'D' + (index+2).toString())
        })
        return {f: formula}
    }

    exportReport() {
        var _filename  = this.getdatetime() + '-' + this.filename + '.xlsx'
        let val = ''
        let ele = {}
        let list = []

        this.data.forEach(element => {
            switch (element.level) {
                case 0:
                    val = ''
                    break;
                
                case 1:
                    val = '      '
                    break;

                case 2:
                    val = '            '
                    break;
                
                case 3:
                    val = '                  '
                    break;
                             
                case 4:
                    val = '                        '
                    break;

                case 5:
                    val = '                              '
                    break;
            
                default:
                    val = ''
                    break;
            }

            ele = {item: element.item, value: val + element.value, auto_calc: element.formula? '+' : undefined, input: element.input}
            list.push(ele)
        })

        var XLSX = require('xlsx');

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
}
