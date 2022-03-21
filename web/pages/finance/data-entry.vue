<!-- eslint-disable -->
<template>
<div v-if="dataready===true">
<TopMenu v-bind="{type: 'tophead', tophead: this.tophead, enableDownload: true}"></TopMenu>
<div class="pt60"/>

<section class="hero">
  <div class="hero-body is-marginless pl0 pr0 pt7 pb40">
    <div class="columns is-multiline is-mobile">
<div class="column is-10">
<div class="steps">
  <div class="step-item" :class="result.find(v=>v.name==='assign') !==undefined? result.find(v=>v.name==='assign').value : ''">
    <div class="step-marker">1</div>
    <div class="step-details">
      <p class="step-title is-size-5"><span class="font-smaller"> Giao việc </span></p>
    <p class="is-size-7 pt5 has-text-grey"> {{showTime(task.assign_date)}} </p>
    </div>
  </div>
  <div class="step-item" :class="result.find(v=>v.name==='entered') !==undefined? result.find(v=>v.name==='entered').value : ''">
    <div class="step-marker">2</div>
    <div class="step-details">
      <p class="step-title is-size-5"> <span class="font-smaller"> Đang nhập </span></p>
    <p class="is-size-7 pt5 has-text-grey"> {{task.entry_time===null? undefined : showTime(task.entry_time)}} </p>
    </div>
  </div>
<div class="step-item" :class="result.find(v=>v.name==='waiting-approve') !==undefined? result.find(v=>v.name==='waiting-approve').value : ''">
    <div class="step-marker">3</div>
    <div class="step-details">
      <p class="step-title is-size-5"> <span class="font-smaller"> Chờ duyệt 1</span></p>
       <p class="is-size-7 pt5 has-text-grey">{{task.waiting1_time===null? undefined : showTime(task.waiting1_time)}} </p>    
    </div>
  </div>

  <div class="step-item" :class="result.find(v=>v.name==='waiting-approve-2') !==undefined? result.find(v=>v.name==='waiting-approve-2').value : ''">
    <div class="step-marker">4</div>
    <div class="step-details">
    <p class="step-title is-size-5"><span class="font-smaller"> Chờ duyệt 2</span></p>
        <p class="is-size-7 pt5 has-text-grey">{{task.waiting2_time===null? undefined : showTime(task.waiting2_time)}} </p>    
    </div>
  </div>

    <div class="step-item" :class="result.find(v=>v.name==='approved') !==undefined? result.find(v=>v.name==='approved').value : ''">
    <div class="step-marker">5</div>
    <div class="step-details">
    <p class="step-title is-size-5"><span class="font-smaller"> Đồng ý</span></p>
    <p class="is-size-7 pt5 has-text-grey">{{task.approve_time===null? undefined : showTime(task.approve_time)}} </p>    
    </div>
  </div>
</div>
 </div>
 <div class="column is-2">
    <span class="button is-primary is-outlined pl5 pr5 pt0 pb0" @click="closeWindow()">
        <i class="mdi mdi-close is-size-4"></i>
    </span>
 </div>

<div class="column is-10 pt3">
<nav class="level is-mobile">
    <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Mã</p>
      <p class="font-smaller mt5">{{task.id}}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Công ty</p>
      <p class="font-smaller mt5">{{task.company__stock_code}}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Loại</p>
      <p class="font-smaller mt5">{{task.company__type__code}}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Năm</p>
      <p class="font-smaller mt5">{{task.year}}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Kỳ báo cáo</p>
      <p class="font-smaller mt5">{{task.report_period__value}}</p>
    </div>
  </div>
    <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Tên báo cáo</p>
      <p class="font-smaller mt5">{{task.report_name__value}}</p>
    </div>
  </div>
      <div class="level-item has-text-centered">
    <div>
     <p class="is-size-7">Loại báo cáo</p>
      <p class="font-smaller mt5">{{task.report_type__value}}</p>
    </div>
  </div>
    <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Người giao</p>
      <p class="font-smaller mt5">{{task.assigner__name}}</p>
    </div>
  </div>
      <div class="level-item has-text-centered">
    <div>
      <p class="is-size-7">Người nhận</p>
      <p class="font-smaller mt5">{{task.recipient__name}}</p>
    </div>
  </div>
</nav>
</div>

  <div class="is-2 pt3">
    <div class="buttons is-centered">
        <div class="control tooltip is-tooltip-left ml20" data-tooltip="Tải lên file excel">
            <div class="file has-name is-right" ref='file'>
        <label class="file-label">
            <input class="file-input" type="file" id="fileUpload" v-on:change="uploadFile()">
            <a class="button is-white" v-if="editable===true">
                <i class="mdi mdi-arrow-up is-size-3 has-text-primary"></i>
            </a>
      </label>
        </div>
        </div>
      
      <button class="button is-white ml20 pl15 pr15 pt0 tooltip is-tooltip-left" 
              data-tooltip="Tải xuống file template" @click="getfileTemplate()">
          <span class="icon">
          <i class="mdi mdi-arrow-down is-size-3 has-text-primary"></i>
          </span>
      </button>
    </div>
  </div>

<div class="column is-7 is-offset-1 pt3">
    <nav class="level">
        <div class="level-item has-text-centered">
            <div class="tags has-addons">
                <span class="tag">Đã nhập</span>
                <span class="tag is-primary">{{numberFieldEntered}}</span>
            </div>
        </div>
                <div class="level-item has-text-centered">
            <div class="tags has-addons">
                <span class="tag">Còn lại</span>
                <span class="tag is-primary">{{numberFieldPending}}</span>
            </div>
                </div>

                            <div class="level-item has-text-centered">
            <div class="tags has-addons">
                <span class="tag">Tỷ lệ</span>
                <span class="tag is-primary">{{percentage + '%'}}</span>
            </div>
                            </div>


            <div class="level-item has-text-centered">
            <div class="tags has-addons">
                <span class="tag">Điều chỉnh</span>
                <span class="tag is-warning">{{numberFieldLocked}}</span>
            </div>
        </div>
        
        <div class="level-item has-text-centered">
            <div class="tags has-addons">
                <span class="tag">Lỗi</span>
                <span class="tag is-danger">{{numberFieldError}}</span>
            </div>
        </div>
    </nav>
</div>

<div class="column is-8">
    <div class="table-container">
<!-- <div class="table-container" v-if="dataready===true"> -->
    <table class="table" style="margin-left: auto; margin-right: auto;" ref="table">
     <tbody>
        <tr>
        <td>
            <a @click="expanded===true? collapseAll() : expandAll()" class="tooltip is-tooltip-right" :data-tooltip="expanded===true? 'Thu gọn' : 'Mở rộng'">
            <i :class="expanded===true? 'mdi mdi-chevron-double-up' : 'mdi mdi-chevron-double-down'"  class="has-text-dark " style="font-size:34px;"> </i>
            </a>
        </td>
        <td> 
            <p class="has-text-right" v-if="editable===true">      
             <a @click="preview=!preview" class="tooltip is-tooltip-right" :data-tooltip="preview===true? 'Chế độ sửa đổi' : 'Chế độ xem trước'">
            <i :class="preview===true? 'mdi mdi-eye-outline' : 'mdi mdi-eye-off-outline'"  class="font-color-light has-text-weight-light" style="font-size:30px;"> </i>
             </a>
            </p>
        </td>

        <td> <!--
            <div class="has-text-dark is-size-6 has-text-dark has-text-weight-bold"> 
            <p class="font-smaller has-text-right">  {{task.year + '/Q' + api.getbyid(task.report_period).code}} </p> 
            <p class="is-size-7 pt3 has-text-right">  {{api.getbyid(task.report_type).code}}</p> 
            </div>-->
        </td>
        <td>  </td>
        </tr>

            <template v-for="(ele) in data.filter(v => v.level===0)">
              <tr :key="ele.id"  @click="toggle(ele)"> 
                <td style="width:10px; height: 10px;"> <div class="vertical-center"> <span v-if="ele.child!==undefined">
                    <i :class="ele.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele.id"  :style="getstyleicon(ele)"> </i> </span>
                </div>
                  </td>
                <td  style="min-width:365px"> <div class="vertical-center"> <span :style="getstyle(ele)"> {{ele.value}} </span> </div> </td>
                <td :class="ele.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele.locked==true? ele.edit_note : ''">
                    <div class="vertical-center-right">
                      <span :style="getstyle(ele)" v-if="ele.formula!=='' || preview===true || ele.readonly">{{models[ele.id]}}</span>
                        <div class="field" v-else>
                        <div class="control is-paddingless">
                            <input class="input font-small has-text-right" type="text" v-model="models[ele.id]" @keyup="checkValue(ele)">
                        </div>
                        </div>
                      </div>
                </td>
                <td> <div class="vertical-center"> 
                    <span class="icon has-text-danger" v-if="ele.error===true">
                        <i class="mdi mdi-close-circle-outline"></i>
                    </span>
                    <a class="ml10" v-if="ele.formula!=='' && editable===true" @click="openEditForm(ele)">
                        <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                    </a>
                    </div>    
                  </td>
            </tr>
                
            <template v-for="(ele1) in data.filter(v=> v.parent===ele.item)">
              <tr :key="ele1.id" v-if="ele.expanded===true"  @click="toggle(ele1)"> 
                <td> <div class="vertical-center"> <span v-if="ele1.child!==undefined">
                      <i :class="ele1.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele1.id"  :style="getstyleicon(ele1)"> </i> </span> 
                </div>
                </td>
                <td> <span class="pl20"/> <div class="vertical-center"><span :style="getstyle(ele1)"> {{ele1.value}} </span> </div> </td>
                  <td :class="ele1.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele1.locked==true? ele1.edit_note : ''">
               <div class="vertical-center-right">
                  <span :style="getstyle(ele1)" v-if="ele1.formula!=='' || preview===true"> {{models[ele1.id]}}</span>
                    <div class="field" v-else>
                    <div class="control is-paddingless">
                        <input class="input font-small has-text-right" type="text" v-model="models[ele1.id]" @keyup="checkValue(ele1)">
                    </div>
                    </div>
                  </div>
                </td>
                  <td> <div class="vertical-center"> 
                    <span class="icon has-text-danger" v-if="ele1.error===true">
                        <i class="mdi mdi-close-circle-outline"></i>
                    </span>
                    <a class="ml10" v-if="ele1.formula!=='' && editable===true" @click="openEditForm(ele1)">
                        <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                    </a>
                    </div>    
                  </td>
            </tr>

            <template v-for="(ele2) in data.filter(v=> v.parent===ele1.item)">
              <tr :key="ele2.id" v-if="ele1.expanded===true"  @click="toggle(ele2)"> 
                <td>  <div class="vertical-center"> <span v-if="ele2.child!==undefined">
                      <i :class="ele2.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele2.id"  :style="getstyleicon(ele2)"> </i> </span> </div></td>
                <td> <div class="vertical-center">  <span class="pl40"/><span :style="getstyle(ele2)"> {{ele2.value}} </span> </div></td>
                  <td :class="ele2.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele2.locked==true? ele2.edit_note : ''">
                  <div class="vertical-center-right">  
                        <span :style="getstyle(ele2)" v-if="ele2.formula!=='' || preview===true">{{models[ele2.id]}}</span>
                        <div class="field" v-else>
                        <div class="control is-paddingless">
                            <input class="input font-small has-text-right" type="text" v-model="models[ele2.id]" @keyup="checkValue(ele2)">
                        </div>
                        </div>
                      </div>
                </td>
                  <td> <div class="vertical-center"> 
                    <span class="icon has-text-danger" v-if="ele2.error===true">
                        <i class="mdi mdi-close-circle-outline"></i>
                    </span>
                    <a class="ml10" v-if="ele2.formula!=='' && editable===true" @click="openEditForm(ele2)">
                        <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                    </a>
                    </div>    
                  </td>
            </tr>

              <template v-for="(ele3) in data.filter(v=> v.parent===ele2.item)">
              <tr :key="ele3.id" v-if="ele2.expanded===true"  @click="toggle(ele3)"> 
                <td><div class="vertical-center"><span v-if="ele3.child!==undefined">
                      <i :class="ele3.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele3.id"  :style="getstyleicon(ele3)"> </i> </span> </div> </td>
                <td> <div class="vertical-center"> <span class="pl60"/> <span :style="getstyle(ele3)"> {{ele3.value}} </span> </div> </td>
                <td :class="ele3.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele3.locked==true? ele3.edit_note : ''">
                  <div class="vertical-center-right"> 
                        <span :style="getstyle(ele3)" v-if="ele3.formula!=='' || preview===true"> {{models[ele3.id]}}</span>
                        <div class="field" v-else>
                        <div class="control is-paddingless">
                            <input class="input font-small has-text-right" type="text" v-model="models[ele3.id]" @keyup="checkValue(ele3)">
                        </div>
                        </div>
                      </div>
                </td>
                  <td> <div class="vertical-center"> 
                    <span class="icon has-text-danger" v-if="ele3.error===true">
                        <i class="mdi mdi-close-circle-outline"></i>
                    </span>
                      <a class="ml10" v-if="ele3.formula!=='' && editable===true" @click="openEditForm(ele3)">
                        <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                    </a>
                    </div>    
                  </td>
            </tr>

            <template v-for="(ele4) in data.filter(v=> v.parent===ele3.item)">
              <tr :key="ele4.id" v-if="ele3.expanded===true" @click="toggle(ele4)"> 
                <td><div class="vertical-center"> <span v-if="ele4.child!==undefined">
                      <i :class="ele4.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele4.id"  :style="getstyleicon(ele4)"> </i> </span> </div> </td>
                <td><div class="vertical-center"> <span class="pl80"/> <span :style="getstyle(ele4)"> {{ele4.value}} </span></div></td>
                <td :class="ele4.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele4.locked==true? ele4.edit_note : ''">
                <div class="vertical-center-right">
                        <span :style="getstyle(ele4)" v-if="ele4.formula!=='' || preview===true"> {{models[ele4.id]}} </span>
                        <div class="field" v-else>
                        <div class="control is-paddingless">
                            <input class="input font-small has-text-right" type="text" v-model="models[ele4.id]" @keyup="checkValue(ele4)">
                        </div>
                        </div>
                </div>
                </td>
                  <td> <div class="vertical-center"> 
                    <span class="icon has-text-danger" v-if="ele4.error===true">
                        <i class="mdi mdi-close-circle-outline"></i>
                    </span>
                    <a class="ml10" v-if="ele4.formula!=='' && editable===true" @click="openEditForm(ele4)">
                        <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                    </a>
                    </div>    
                  </td>
            </tr>

              <template v-for="(ele5) in data.filter(v=> v.parent===ele4.item)">
                <tr :key="ele5.id" v-if="ele4.expanded===true"  @click="toggle(ele5)"> 
                  <td><div class="vertical-center"><span v-if="ele5.child!==undefined">
                      <i :class="ele5.expanded===true? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'" :ref="'icon' + ele5.id"  :style="getstyleicon(ele5)"> </i> </span> </div> </td>
                  <td><div class="vertical-center">  <span class="pl100"/> <span :style="getstyle(ele5)">  {{ele5.value}} </span></div></td>
                    <td :class="ele5.locked===true? 'bg-yellow tooltip' : ''" :data-tooltip="ele5.locked==true? ele5.edit_note : ''">
                    <div class="vertical-center-right">
                      <span :style="getstyle(ele5)" v-if="ele5.formula!=='' || preview===true"> {{models[ele5.id]}} </span>
                          <div class="field" v-else>
                          <div class="control is-paddingless">
                              <input class="input font-small has-text-right" type="text" v-model="models[ele5.id]" @keyup="checkValue(ele5)">
                          </div>
                          </div>
                        </div>
                  </td>
                    <td> <div class="vertical-center"> 
                      <span class="icon has-text-danger" v-if="ele5.error===true">
                          <i class="mdi mdi-close-circle-outline"></i>
                      </span>
                      <a class="ml10" v-if="ele5.formula!=='' && editable===true" @click="openEditForm(ele5)">
                          <i class="mdi mdi-square-edit-outline fs22 has-text-dark"></i>
                      </a>
                      </div>    
                    </td>
              </tr>
          </template>
        </template>
        </template>
        </template>
        </template>
        </template>         
    </tbody>
    </table>
    </div>
    </div>

    <div class="column is-4">
        <div class="tabs mt5">
        <ul>
            <li :class="activeTab==='action'? 'is-active' : ''"><a @click="activeTab='action'">Hoạt động</a></li>
            <li :class="activeTab==='history'? 'is-active' : ''"><a @click="activeTab='history'">{{'Chỉnh sửa' + (history.length>0? '(' + history.length + ')' : '')}}</a></li>
            <li :class="activeTab==='file'? 'is-active' : ''"><a @click="activeTab='file'">{{file? 'File gốc(1)' : 'File gốc'}}</a></li>
            <li :class="activeTab==='image'? 'is-active' : ''"><a @click="activeTab='image'">{{images.length===0? 'Hình ảnh' : ('Hình ảnh(' + images.length + ')')}}</a></li>
        </ul>
        </div>

    <div v-if="activeTab==='action'">
    <div class="notification pt10 pb10 mb10 is-dark" v-if="msgLocked.length>0">
    <button class="delete" @click="msgLocked=[]"></button>
    <article class="media pt3 pb3 is-marginless" v-for="(ele,key) in msgLocked" :key="key">
    <figure class="media-left">
            <i :class="ele.type==='success'? 'icon-check2 has-text-primary' : ele.type==='error'? 'icon-cross2 has-text-danger' : 'icon-warning has-text-warning'"> </i>
    </figure>
    <div class="media-content">
        <div class="content">
        <p class="font-smaller" :class="ele.type==='success'? 'has-text-primary' : ele.type==='error'? 'has-text-danger' : 'has-text-warning'">  {{ele.message}} </p>
        </div>
    </div>
    </article>
    </div>

     <div class="pb5" v-if="rightApprove===true">
        <article class="message is-light">
            <div class="message-body pt5 pb5 has-text-left">
              <label class="label is-medium pb5">{{this.api.getvalue(this.api.find3var('information','approved','label'))}}</label>
              <div class="field has-addons">
                <div class="control is-expanded">
                  <div class="select is-fullwidth">
                  <select name="country" v-model="selected">
                    <option v-for="(item,key) in approvelist" :key="key" :value="item">{{api.getvalue(item)}}</option>
                  </select>
                  </div>
                </div>
                <div class="control">
                    <button type="submit" class="button is-primary" @click="approveTask()">{{this.api.getvalue(this.api.find3var('information','choose','label'))}}</button>
                </div>
                </div>
            </div>
        </article>

        <div class="field" v-if="selected? selected.code==='retype' : 1<0">
          <div class="control">
            <textarea class="textarea is-primary" v-model="retypeReason" rows="4" :placeholder="api.getvalue(api.find3var('information','reason','label'))"></textarea>
          </div>
        </div>
    </div>

    <div class="notification pt10 pb10 mb10 is-white" v-if="msgInfo.length>0">
    <button class="delete" @click="msgInfo=[]"></button>
    <article class="media pt3 pb3 is-marginless" v-for="(ele,key) in msgInfo" :key="key">
    <figure class="media-left">
            <i :class="ele.type==='success'? 'mdi mdi-check has-text-primary' : ele.type==='error'? 'mdi mdi-alert-circle-outline has-text-danger' : 'icon-warning has-text-warning'"> </i>
    </figure>
    <div class="media-content">
        <div class="content">
        <p class="font-smaller" :class="ele.type==='success'? 'has-text-primary' : ele.type==='error'? 'has-text-danger' : 'has-text-warning'">  {{ele.message}} </p>
        </div>
    </div>
    </article>
    </div>

<div class="notification pt10 pb10 mb10 is-white" v-if="fillType!==undefined">
        <button class="delete" @click="fillType=undefined"></button>
        <div class="block">
            <b-radio v-model="fillType"
                type ="is-info"
                name="name"
                native-value="fill-all">
                Lấp đầy
            </b-radio>
            <b-radio v-model="fillType" class="ml30"
                type="is-info"
                name="name"
                native-value="calculation">
                Tính toán
            </b-radio>
            </div>
        </div>

        <div class="buttons mt30 is-centered">
          <button class="button is-primary font-smaller" @click="loginForm=true" v-if="retype===false">Sửa báo cáo</button>
          <button class="button is-primary font-smaller" v-if="api.getbyid(task.status).code==='entered' || api.getbyid(task.status).code==='retype'" @click="sendReport()">Gửi báo cáo</button>
          <button class="button is-primary is-outlined font-smaller" @click="saveData()" v-if="editable===true">Lưu lại</button>
          <button class="button is-primary is-outlined font-smaller" @click="hasNewItem=true">Chỉ tiêu mới</button>
        </div>

        <div class="field pt20" v-if="hasNewItem === true">
              <article class="message is-primary">
            <div class="message-body has-text-left">
             {{ api.getvalue(api.find3var('information','new-item','desc')) }}
            </div>
         </article>

            <div class="control">
                <textarea class="textarea is-primary" v-model="newItem" rows="3" :placeholder="api.getvalue(api.find3var('information','content','label'))"></textarea>
            </div>

            <p class="pt15 is-size-6 has-text-left has-text-danger" v-if="newItemMsg!==undefined"> {{newItemMsg}} </p>

            <div class="pt15">
                <a class="button is-primary" @click="informNewItem()">
                    {{api.getvalue(api.find3var('information','inform','label'), 'value')}}
                </a>
                 <span class="pr5 pl5"> </span>
                <a class="button is-primary" @click="hasNewItem = false, newItem = undefined, newItemMsg = undefined">
                {{api.getvalue(api.find3var('form','account-register','cancel'), 'value')}}
                </a>
            </div>
        </div>

        <div class="mt30" v-if="quarterly">
          <p>
           <b-radio v-model="radio"
              native-value="quarterly">
              Lưu theo Quý
            </b-radio>
          </p>
          <p class="mt-3">  
          <b-radio v-model="radio"
              native-value="accumulate">
              Lưu theo Lũy kế
          </b-radio>
          </p>
        </div>
         <div class="mt30 notification" v-if="taskRelated">
          <p> Công việc có liên quan 
          <nuxt-link class="tag is-primary has-text-white" :to="{path: '/finance/data-entry', query: {task: (task.id===taskRelated.task? taskRelated.related : taskRelated.task),type: task.company__type__code, company: task.company, report: taskRelated.related__report_name__code}}" target='_blank'>
        {{task.id===taskRelated.task? taskRelated.related : taskRelated.task}} </nuxt-link>

        <nuxt-link class="tag is-primary has-text-white ml-3" v-if="taskPrev" :to="{path: '/finance/data-entry', query: {task: taskPrev.id ,type: taskPrev.company__type__code, company: taskPrev.company, report: taskPrev.report_name__code}}" target='_blank'>
        {{taskPrev.id}} </nuxt-link>
        </p>
        </div>

        <!-- Block --
        <div v-else-if="radio==='accumulate' && taskArr">
          <p class="mt-3 ml-5 fb500" v-if="taskArr.find(v=>v.valid)"> {{'Chọn báo cáo trong Q' + (parseInt(task.report_period__code) -1) + ':'}} </p>
          <p class="mt-3 ml-5 has-text-danger" v-else> {{'Q' + (parseInt(task.report_period__code) -1) + ' không có báo cáo thỏa mãn.'}} </p>
          <p class="mt-3 ml-5" v-for="(v,i) in taskArr" :key="i">
            <a class="mr-3" @click="openReport(v)"> 
            {{v.id + '/' + v.company__stock_code + '/' + v.year + '/Q' + v.report_period__code  + '/' +  v.report_name__code + '/' + v.report_type__code }} </a>
            <b-radio v-model="radioTask" v-if="v.valid"
              :native-value="v.id">
            </b-radio>
          </p>
        </div> -->
    </div>

    <div v-else-if="activeTab==='history'">
        <article class="message is-warning"  v-for="(v,i) in history" :key="i">
        <div class="message-body pt10 pb10 has-background-white">
          <p class="font-smaller has-text-dark has-text-left">   {{'Báo cáo được yêu cầu sửa lại với lý do : ' +  v.message}} </p>
           <nav class="level is-mobile mt5">
      <div class="level-left">
        <a class="level-item" style="text-decoration: none">
          <span class="icon is-small"><i class="icon-clock2"></i></span>
          <span class="font-small ml10"> {{v.time}} </span>
        </a>
      </div>
    </nav>
    </div>
    </article>
    </div>

    <div v-else-if="activeTab==='file'">
       <div class="mb-5" v-if="task.data_file"> File dữ liệu đã tải lên:
       <p class="mt-2"> <a @click="downloadDataFile()"> {{task.data_file}} </a> </p>
      </div>
      <article class="message is-primary">
      <div class="message-body has-background-white py-3 has-text-dark">
        Vui lòng đính kèm file gốc (pdf, word) của báo cáo để  thuận tiện cho việc đối chiếu kết quả.
      </div>
    </article>
     
      <p v-if="file"><a @click="download()"> {{file.file}} </a> 
      <a class="ml-3" @click="file=undefined" v-if="editable">
        <span class="icon fs24 has-text-danger"> <i class="mdi mdi-close"> </i> </span> </a> </p>
      <a v-if="editable && !file" class="button is-primary is-light"
      @click="media = {component: componentid, name: 'file', type: 'file', open: true}"> Chọn file gốc </a>
    </div>

  <div v-else-if="activeTab==='image'">
    <article class="message is-primary">
  <div class="message-body has-background-white py-3 has-text-dark">
    Hình ảnh minh họa, thuyết minh, chú thích, những điểm cần lưu ý sẽ rất hữu ích cho các nhà đầu tư trong việc lựa chọn cổ phiếu tốt. Hãy đính kèm nếu bạn có các thông tin đó.
  </div>
  </article>
  <div class="columns is-multiline is-mobile" v-if="images.length>0">
  <div class="column is-one-quarter" v-for="(v,i) in images" :key="i">
    <figure class="image">
    <a @click="gallery=v.file"> <img :src="connection.path + 'static/images/' + v.file"> </a>
     <p> <a @click="removeImage(v,i)" v-if="editable"> <span class="icon fs24 has-text-danger"> <i class="mdi mdi-close"> </i> </span> </a></p>
    </figure>
  </div>
  </div>
  <a class="button is-primary is-light mt-3" v-if="editable"
  @click="media = {component: componentid, name: 'image', type: 'image', open: true}"> Hình ảnh (nếu có) </a>
  </div>
    </div>
    </div>
</div>
</section>

<div class="modal" :class="editItem!==undefined? 'is-active' : ''" v-if="editItem!==undefined">
    <div class="modal-card">
        <div class="columns">
        <div class="column is-8 is-offset-2">
        <section class="modal-card-body has-background-dark">
        <p class="modal-card-title has-text-white"><span class="font-smaller"> Thay đổi giá trị chỉ tiêu </span></p>
        <div class="field mt40">
        <p class="font-smaller has-text-white has-text-left">{{editItem.value}}</p>
        <div class="control mt5">
            <input class="input has-text-white" type="text" placeholder="" v-model="editItem.edit_value" @keyup="checkEditValid(editItem)">
        </div>
        </div>

        <div class="field mt30">
        <div class="control">
            <textarea class="textarea" placeholder="Lý do thay đổi" rows="3" v-model="editItem.edit_note" @keyup="checkEditValid(editItem)"></textarea>
        </div>
        </div>
        <p class="has-text-danger has-text-left font-smaller" v-if="editItem.edit_valid===false"> 
            Giá trị phải là số và lý do không được bỏ trống
        </p>

        <p class="pt20">
            <span class="button is-outlined is-white font-smaller" @click="saveEditItem()">Lưu lại</span>
            <span class="button is-danger font-smaller ml20" v-if="editItem.locked===true" @click="deleteEditItem()">Xóa bỏ</span>
            <span class="button is-outlined is-white font-smaller ml20" @click="editItem=undefined">Đóng lại</span>
        </p>
        </section>
        </div>
        </div>
      </div>
    </div>
    
  <div class="modal" :class="loginForm!==undefined? 'is-active' : ''" v-if="loginForm!==undefined">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content my-0 py-0">
    <login v-bind="{modal: true}"> </login>
    </div>
    <button class="modal-close is-large has-background-dark" aria-label="close" @click="loginForm=undefined"></button>
  </div>

  <div class="modal is-active" v-if="openMedia===componentid">
    <div class="modal-background has-background-white"></div>
    <div class="modal-content" style="position: absolute; top: 0px">
        <media v-bind="{mediatype: media.type, modal: true}" />
     </div>
    <button @click="media=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
  </div>

  <div class="modal is-active" v-else-if="gallery">
  <div class="modal-background"></div>
  <div class="modal-content">
   <div class="tile is-ancestor ml10 mr10 mt10 mb10">
  <div class="tile is-2"></div>
  <div class="tile is-8">
    <img v-lazy="connection.path + 'static/images/' + gallery" class="mt0 mb0 pt0 pb0">
    </div>
  </div>
</div>  
<button @click="gallery=undefined" class="modal-close is-large has-background-dark" aria-label="close"></button>
</div>
 <Footer></Footer>
</div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import Export from '@/assets/js/export.js'
import mixing from '@/assets/js/mixing.js'

import axios from 'axios'
import "bulma-extensions/bulma-steps/dist/css/bulma-steps.min.css"
import login from '@/pages/login.vue'
import TopMenu from '@/components/TopMenu'
import Footer from '@/components/Footer'
import media from '@/pages/media.vue'
import socket from '~/plugins/socket.io.js'

Vue.component('Topmenu', TopMenu)
Vue.component('Footer', Footer)
Vue.component('login', login)
Vue.component('media', media)

export default {
   data() {
      return {
        data: [],
        fields: [],
        company: undefined,
        stock_code: undefined,
        dataready: false,
        expanded: false,
        connection: this.$connection(),
        connection1: this.$connection(),
        connection2: this.$connection(),
        connection3: this.$connection(),
        connection4: this.$connection(),
        connection5: this.$connection(),
        connection6: this.$connection(),
        connection7: this.$connection(),
        connection8: this.$connection(),
        connection9: this.$connection(),
        connection10: this.$connection(),
        connection11: this.$connection(),
        connection12: this.$connection(),
        result: [],
        models: [],
        datafile: undefined,
        msgInfo: [],
        fillType: undefined,
        report: undefined,
        task: undefined,
        sending: false,
        msgLocked: [],
        preview: false,
        editable: true,
        dldata: true,
        rightApprove: false,
        selected: undefined,
        changeStatus: undefined,
        retype: undefined,
        retypeReason: '',
        mdlactive: undefined,
        editItem: undefined,
        loginForm: undefined,
        history: [],
        message: [],
        activeTab: 'action',
        tophead: 'Nhập dữ liệu báo cáo tài chính',
        hasNewItem: false,
        newItem: undefined,
        newItemMsg: undefined,
        approve_time: undefined,
        accountlist: [],
        componentid: mixing.id(),
        file: undefined,
        images: [],
        gallery: undefined,
        values: undefined,
        radio: 'quarterly',
        taskRelated: undefined,
        taskRef: undefined,
        reportRef: undefined,
        taskPrev: undefined,
        reportPrev: undefined,
        firstUpdate: false,
        reportitem: undefined,
        dataFile: undefined,
        itemchangelist: undefined,
        taskArr: undefined,
        radioTask: undefined
      }
    },
    
    head() {
      return {
        title: 'Nhập báo cáo tài chính'
      }
    },

    created() {
      if(!this.login) {
        let query = {to: this.$route.path}
        query.params = JSON.stringify(this.$route.query)
        return this.$router.push({path: '/login', query: query})
      }
      if(this.$route.query.report.indexOf('LCTT')>=0) this.radio = 'accumulate'
      let connName = mixing.connection(this.$route.query.report.replace('-LK', ''), this.$route.query.type)
      let list = [{name: connName, url: 'data/' + connName.toUpperCase(), params: {filter:{task: this.$route.query.task}}}]
      this.values = 'id,company,company__type__code,company__stock_code,company__name,report_period,report_period__code,report_period__value,year,report_type,report_type__code,report_type__value,report_name,report_name__code,report_name__value,assigner,recipient,assign_date,due_date,status,status__code,status__value,create_time,update_time' 
      this.values += ',approve_time,enable,detail,priority,company_factor,unit_price,into_money,total_fields,entered_fields,pending_fields,percentage,marked_fields,entry_time,waiting1_time,waiting2_time,history,message,file,file__file,data_file' 
      this.values += ',assigner__name,recipient__name,accumulate'

      let found = {name: 'task', url: 'data/Task', params: {values: this.values, filter: {id: this.$route.query.task}}}
      list.push(found)

      found = {name: 'taskrelated', url: 'data/Task_Related', params: {values: 'id,task,related,related__report_name__code,task_prev', filter_or: {task: this.$route.query.task, related: this.$route.query.task}}}
      list.push(found)

      found = {name: 'taskimage', url: 'data/Task_Image', params: {values: 'id,task,image,image__file', filter_or: {task: this.$route.query.task}}}
      list.push(found)

      found = {name: 'reportitem', url: 'data/Report_Item', params: {filter:{company_type: this.$route.query.type, report_name:  this.$route.query.report.replace('-LK', ''), enable: 1}}}
      list.push(found)

      found = {name: 'itemchange', url: 'data/Item_Change', params: {filter:{task: this.$route.query.task}}}
      list.push(found)
      this.connection.getApi(list)
    },

    mounted() {
      if(this.dataready) this.expandAll()
    },

    watch: {
      "connection.getdataReady": function(newVal) {
        if(newVal==='success') {
          let datalist = this.connection.getbatchData
          this.reportitem = datalist.find(v=>v.name==='reportitem').data
          let list = datalist.find(v=>v.name==='task').data
          this.task = list.length>0? list[0] : undefined
          if(this.task===undefined) {
              this.$buefy.snackbar.open({
                duration: 5000,
                message: 'Công việc không tồn tại. Hệ thống chuyển hướng đến trang chủ sau 5s',
                position: 'is-bottom',
              })
              let self = this
              mixing.delay(function(){self.$router.push({name: 'index'})}, 5000)
              return
          } else if(this.task.file) this.file = {id: this.task.file, file: this.task.file__file}

          this.images = datalist.find(v=>v.name==='taskimage').data
          this.images.map(v=>{
            v.file = v.image__file
            v.imageID = v.image
          })
          list = datalist.find(v=>v.name==='taskrelated').data
          if(list.length>0) this.taskRelated = list[0]
          this.reportitem = datalist.find(v=>v.name==='reportitem').data
          this.itemchangelist = datalist.find(v=>v.name==='itemchange').data
          this.getTaskInfo()
          this.taskStatus()
          this.checkRights()
          this.getReportData()
          //this.getTaskRef() //Blocked
        }
        else if(newVal==='error') this.$router.push({ name: 'error'})
      },

      'connection1.getupdateStatus': function(newVal, oldVal) {
        if(newVal===true) {
          this.report = this.connection1.updateRecord
          this.updateTask()
        }
        else if(newVal==false) {
          this.msgInfo.push({message: 'Cập nhật dữ liệu thất bại', type: 'error'})
        }
      },

      'connection2.getupdateStatus': function(newVal, oldVal) {
        if(newVal===true) {
          let message = this.sending===false? 'Cập nhật dữ liệu thành công' : 'Gửi báo cáo đi thành công'
          if(this.changeStatus!==undefined) message = this.changeStatus.msgSuccess
          this.msgInfo.push({message: message, type: 'success'} )
          this.task = this.$copy(this.connection2.updateRecord)
          //send message
          socket.emit('send-message', {name: 'update-task', data: this.task})
         
          let data = []
          this.images.map(v=>{data.push({id: v.id, task: this.task.id, image: v.imageID})})
          this.connection5.insert('taskimage', data)
         
          /*
          Block
         if(this.radio==='accumulate') {
            let copy = this.$copy(this.task)
            copy.id = undefined
            copy.report_name = this.api.find3var('list', 'report-name', copy.report_name__code.replace('-LK', '')).id
            copy.assigner = 1
            copy.recipient = 1
            copy.detail = 'Báo cáo được hệ thống tự sinh ra'
            if(!this.taskRelated) this.connection7.insert('taskobj', copy, this.values)
          } */
          this.getTaskHistory()
          //if(this.reportPrev) this.updateTaskRef() //Block
        }
        else if(newVal==false)  {
          let message = this.sending===false? 'Cập nhật dữ liệu thất bại' : 'Gửi báo cáo đi thất bại'
          if(this.changeStatus!==undefined) message = this.changeStatus.msgError
          this.msgInfo.push({message: message, type: 'error'} )
        }
        if(this.sending===true) this.sending = false
        if(this.changeStatus!==undefined) this.changeStatus = undefined
      },

      'connection3.getupdateStatus': function(newVal) {
        if(newVal==false) this.msgInfo.push({message: 'Cập nhật điều chỉnh cho chỉ tiêu thất bại', type: 'error'} )
      },

      'connection7.getupdateStatus': function(newVal) {
        if(newVal) {
          let data = {task: this.task.id, related: this.connection7.getupdateRecord.id, task_prev: this.radioTask}
          this.connection8.insert('taskrelated', data, 'id,task,related,related__report_name__code,task_prev')
        }
      },

      'connection8.getupdateStatus': function(newVal) {
        if(newVal) {
          this.taskRelated = this.connection8.getupdateRecord
          this.firstUpdate = true
          this.getTaskRef()
        }
      },

      "connection9.getdataReady": function(newVal) {
        if(newVal==='success') {
          let connName = mixing.connection(this.$route.query.report, this.$route.query.type)
          let found = this.connection9.getbatchData.find(v=>v.name==='taskref')
          if(found) this.taskRef = found.data.length>0? found.data[0] : undefined

          found = this.connection9.getbatchData.find(v=>v.name===connName + 'ref')
          if(found) this.reportRef = found.data.length>0? found.data[0] : undefined

          found = this.connection9.getbatchData.find(v=>v.name==='taskprev')
          if(found) this.taskPrev = found.data.length>0? found.data[0] : undefined

          found = this.connection9.getbatchData.find(v=>v.name===connName + 'prev')
          if(found) this.reportPrev = found.data.length>0? found.data[0] : undefined

          if(this.firstUpdate) {
            this.firstUpdate = false
            if(this.reportPrev) this.updateTaskRef()
          }
        }
      },

      'connection10.getupdateStatus': function(newVal) {
        if(newVal) {
          this.reportRef = this.connection10.getupdateRecord
          let data = this.$copy(this.taskRef)
          data.update_time = new Date()
          data.entry_time = this.task.entry_time 
          data.waiting1_time = this.task.waiting1_time
          data.waiting2_time = this.task.waiting2_time
          data.approve_time = this.task.approve_time
          data.total_fields = this.numberFieldEntered + this.numberFieldPending,
          data.entered_fields = this.numberFieldEntered,
          data.pending_fields = this.numberFieldPending,
          data.percentage = this.percentage
          data.status = this.task.status
          this.connection11.update('taskobj', data, this.values)
        }
      },

      'connection11.getupdateStatus': function(newVal) {
        if(newVal) {
          this.taskRef = this.connection11.getupdateRecord
        }
      },

      "connection12.getdataReady": function(newVal) {
        if(newVal==='success') {
          this.taskArr = this.$copy(this.connection12.getbatchData[0].data)
          if(this.taskArr.length===0) return
          let filter = this.taskArr.filter(v=>v.report_type__code.indexOf(this.task.report_type__code.substring(0,3))>=0)
          if(parseInt(this.task.report_period__code)>2) {
            filter = filter.filter(v=>v.report_name__code.indexOf('-LK')>=0)
          }
          if(filter.length===0) return
          filter.map(v=>v.valid = true)
          let found = filter.find(v=>v.report_type__code.indexOf('-SX')>0)
          if(!found) found = filter[0]
          this.radioTask = found.id
        }
      },

      fillType: function(newVal) {
        //Re-calculation
        if(newVal === 'calculation') {
          let list = mixing.unique(this.data, ['level'])
          list.sort((a,b)=> - a.level + b.level)
          list.forEach(ele => {
            let filter = this.data.filter(v=>v.level===ele.level && this.$empty(v.formula)===false)
            filter.forEach(item => this.formulaCalc(item))
          })
        } 
        else if (newVal==='fill-all') { //Fill-all
          let listdata = this.datafile.data
          this.data.forEach(ele => {
            let found = listdata.find(v=>v.item===ele.item)
            if(found!==undefined) {
              if(this.$empty(found.input)===false && mixing.isNumber(found.input)===true) {
                Vue.set(this.models, ele.id, mixing.formatNumber(found.input)!==0? mixing.numbertoString(found.input) : undefined)
                ele.item_value = mixing.formatNumber(found.input)!==0? mixing.formatNumber(found.input) : undefined
                ele.error = false
              } else {
                Vue.set(this.models, ele.id, found.input)
                ele.item_value = undefined
                if(this.$empty(found.input)===true) found.error = false
                else ele.error = true
              }
            }
          })
        }
      },

      'task.status': function(newVal) {
        this.taskStatus()
        this.checkRights()
      },

      menuaction: function(newVal) {
        if(newVal===undefined) return
        else if(newVal.action==='download') this.getReport()
        else if(newVal.action==='close-login') {
          this.loginForm = undefined
          this.retype = true
          this.editable = true
          this.msgLocked = []
        }
      },

      media: function(newVal) {
        if(newVal? !newVal.select : 1>0) return
        if(this.componentid!==newVal.component) return
        if(newVal.name==='image') {
          if(!this.images.find(v=>v.imageID===newVal.select.id)) this.images.push({imageID: newVal.select.id, file: newVal.select.file})
        }
        else if(newVal.name==='file') {
          this.file = newVal.select
          this.$store.commit('updateState', {name: 'media', key: 'file', data: this.file})
        }
        this.media = undefined
      },

      quarterly: function(newVal) {
        if(newVal) {
          let found = {name: 'task', url: 'data/Task', params:{sort: 'report_type__code', values: this.values, filter: {year: this.task.year, company: this.task.company, report_name__code__in: [this.task.report_name__code, this.task.report_name__code + '-LK'], status__code: 'approved', report_period__code: (parseInt(this.task.report_period__code) -1)}}}
          this.connection12.getApi([found])
        }
      }
    },

    computed: {
      api: {
        get: function() {return this.$store.state.api},
        set: function(val) {this.$store.commit('updateApi', {api: val})}
      },

      pagetask: {
        get: function() {return this.$store.state.pagetask},
        set: function(val) {this.$store.commit('updatePageTask', {pagetask: val})}
      },

      login: {
        get: function() {return this.$store.state.login},
        set: function(val) {this.$store.commit("updateLogin", {login: val})}
      },

      numberFieldEntered: {
        get:  function() {
          return this.data.filter(v=>v.item_value!==undefined && v.error!==true).length
        },
      },

      numberFieldPending: function() {
        return this.data.length - this.numberFieldEntered
      },

      percentage: function() {
        return (parseInt(this.numberFieldEntered,10)*100 / parseInt((this.numberFieldEntered + this.numberFieldPending),10)).toFixed(1)
      },

      numberFieldLocked: function() {
        return this.data.filter(v=>v.locked===true).length
      },

      numberFieldError: function() {
        return this.data.filter(v=>v.error===true).length
      },

      menuaction: {
        get: function() {return this.$store.state.menuaction},
        set: function(val) {this.$store.commit('updateMenuAction', {menuaction: val})}
      },
      
      media: {
        get: function() {return this.$store.state.media},
        set: function(val) {this.$store.commit("updateMedia", {media: val})}
      },

      openMedia() {
        return this.media? this.media.component : false
      },

      quarterly() {
        return this.task? (parseInt(this.task.report_period__code) >1 &&  parseInt(this.task.report_period__code) <5 && this.editable  && !this.taskRelated 
        && (this.task.report_name__code==='LCTT-TT' || this.task.report_name__code==='LCTT-GT' || this.task.report_name__code==='KQKD')) : false
      }
    },

    methods: {
      closeWindow() {
        window.close()
      },

      getTaskInfo() {
        this.task.assignDate = mixing.yyyymmddhhmm(new Date(this.task.assign_date))
        this.task.dueDate = mixing.yyyymmddhhmm(new Date(this.task.due_date))
        this.task.percentageFormat = this.task.percentage===null? undefined : this.task.percentage + '%'
        this.tophead = this.task.company__name + ' / ' + this.task.report_name__value + ' / ' 
        + this.task.report_type__value + ' / ' + this.task.report_period__value + ' / ' + this.task.year
        this.getTaskHistory()
      },

      getReportData() {
        let connName = mixing.connection(this.$route.query.report.replace('-LK', ''), this.$route.query.type)
        let fields = [{text: 'detail', value: 'Chỉ tiêu', sortable: false, width: "200px",  align: 'center'}]
        let task = this.task //this.task
        let rows = this.connection.getbatchData.find(v=>v.name===connName).data
        let record = rows.length>0? rows[0] : undefined
        this.report = record
        if(record) this.radio = task.accumulate? 'accumulate' : 'quarterly'
        let data = this.$copy(this.reportitem.filter(v=>v.company_type===this.task.company__type__code && v.report_name===this.$route.query.report.replace('-LK', '')))
        let field = {text: 'item_value', value: 'item_value', sortable: false, width: "200px",  align: 'center', type: 'period', period: undefined}
  
        data.forEach(v => {
          v.item_value = record===undefined? undefined : this.$empty(record['f' + v.item])===true? undefined : record['f' + v.item]===0? undefined : record['f' + v.item]
          v.expanded = false 
          v.error = false
          v.locked = false
          v.child = data.find(x=>x.parent===v.item)===undefined? undefined: true

          if(record!==undefined) {
            let found = this.itemchangelist.find(x=>x.report===record.id && x.enable===true && x.item===v.id)
            if(found!==undefined) {
              v.locked = true
              v.edit_note = found.reason
            }
          }
          this.models[v.id] = mixing.numbertoString(v.item_value)
        })
        fields.push(field)
        
        //add fields
        fields.push({text: 'icon', value: '', sortable: false, width: "200px",  align: 'center'})
        data.sort((a,b) => (a.index - b.index))
        this.data = data
        this.fields = fields
        this.dataready = true
        this.expandAll()
      },

      getTaskHistory() {
        if(this.$empty(this.task.history)===true) return
        this.history = JSON.parse(this.task.history)
        this.history.sort((a,b) => (new Date(b.time) - new Date(a.time)))
        this.history.map(v=>v.time=mixing.yyyymmddhhmm(new Date(v.time)))
      },

      checkValue(ele) {
        let val = this.models[ele.id]
        if(this.$empty(val)===false && mixing.isNumber(val)===true) {
            ele.item_value = mixing.formatNumber(val)
            ele.error = false
            Vue.set(this.models, ele.id, mixing.numbertoString(val))
        } else {
            ele.item_value = undefined
            if(this.$empty(val)===true) ele.error = false
            else ele.error = true
        }

        let list = [], isadded = true
        let filter = this.data.filter(v=>v.formula.indexOf(ele.item)>-1)
        list = list.concat(filter)

        while (isadded===true) {
            let count = mixing.unique(list, ['item']).length
            list.forEach(ele => {
                filter = this.data.filter(v=>v.formula.indexOf(ele.item)>-1)
                list = list.concat(filter)
            })
            let countNext = mixing.unique(list, ['item']).length
            if(count===countNext) isadded = false
        }
        let uniqueArr = mixing.unique(list, ['item'])
        uniqueArr.forEach(item => {this.formulaCalc(item)})
      },

      formulaCalc(item) {
        var calc = function(fn) {return new Function('return ' + fn)()}

        if(item.locked===true) return 
        var formula =  JSON.parse(JSON.stringify(item.formula))
        var formula1 = JSON.parse(JSON.stringify(item.formula))
        formula1 = formula1.replace(/-/g, '+')
        var arr = formula1.split('+')
        
        arr.forEach(element => {formula = formula.replace(element, 'f' + element)})
        arr.forEach(element => {
            var value = this.data.find(v=>v.item===element).item_value
            if(this.$empty(value)===true) value = 0
            formula = formula.replace('f' + element, '(' + value + ')')
        })

        item.item_value = calc(formula)===0? undefined: calc(formula)
        item.error = false
        Vue.set(this.models, item.id, mixing.numbertoString(item.item_value))
      },

      uploadFile() {
        var file = document.getElementById("fileUpload");
        if(file.files.length == 0) return
        
        let fileName = file.files[0].name
        let data = new FormData();
        data.append('name', fileName);
        data.append('file', file.files[0]);

        //check file name is valid
        if (!(fileName.search('.xls') > 0 || fileName.search('.xlsx') > 0)) {
          this.msgInfo.push({message: this.api.find3var('inform', 'import', 'file-type-invalid').value, type: 'error'} )
          return
        }

        this.fillType = undefined
        axios.post(this.connection.path + 'upload-file/', data=data)
        .then(response => {
            this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-ok').value, type: 'success'})
            this.getfile(fileName)
            this.dataFile = fileName
            file.value = ''
          }
        )
        .catch(error => {
          this.msgInfo.push({message: this.api.find3var('inform','import','file-upload-fail'), type: 'error'})
          file.value = ''
        })
      },

      getfile(filename) {
        const url = this.connection.path + 'getfile/' + filename
        axios.get(url)
        .then(response => {
          this.datafile = JSON.parse(response.data)
          this.fillData()
        })
        .catch(error => {
          this.msgInfo.push({message: 'Có lỗi khi đọc cấu trúc file', type: 'error'})
        })
      },

      //check require field
      checkfieldlist() {
        //check require fieds
        let requireFields = []
        let found = this.api.find3var('inform','import','cdkt-fields')
        if(found !== undefined) this.requireFields = found.detail.split(',')
        let misslist = []

        //check field list is ok
        this.requireFields.forEach(element => {
            var field = this.datafile.schema.fields.find(v=>v.name===element)
            if(field===undefined) misslist.push(element)
        })

        if(misslist.length>0) {
          this.msgInfo.push({message: this.api.find3var('inform','import','field-list-fail').value, type: 'error'})
          return false
        } else {
          this.msgInfo.push({message: this.api.find3var('inform','import','field-list-ok').value, type: 'success'})
          return true
        }
      },

      fillData() {
        //Check require fields is ok
        if( this.checkfieldlist() === false) return

        //Matching by item
        var count=this.data.length, i=0, j=0
        let listdata = this.datafile.data
        this.data.forEach(ele => {
          let found = listdata.find(v=>v.item===ele.item)
          if(found!==undefined) {
            i = i + 1
            if(this.$empty(found.input)===false && mixing.isNumber(found.input)===true) {
              //check this
              Vue.set(this.models, ele.id, mixing.formatNumber(found.input)!==0? mixing.numbertoString(found.input) : undefined)
              ele.item_value = mixing.formatNumber(found.input)!==0? mixing.formatNumber(found.input) : undefined
              if(mixing.formatNumber(found.input)!==0) j = j + 1
              ele.error = false
            } else {
              Vue.set(this.models, ele.id, found.input)
              ele.item_value = undefined
              if(this.$empty(found.input)===true) found.error = false
              else ele.error = true
            }
          }
        })
        var ele = this.api.find3var('inform','import','fill-fields-ok')
        if(ele !== undefined) {
            ele = this.$copy(ele)
            ele.value = ele.value + ' ' + j.toString() + '/' + count.toString()
            ele.value1 = ele.value + ' ' + j.toString() + '/' + count.toString()
            this.msgInfo.push({message: ele.value, type: 'success'})
        }
        this.fillType = 'calculation'
      },

      getfileTemplate() {
        var _export = new Export()
        let task = this.task
        var filename  = this.task.company__stock_code + '-' + this.task.company__type__code + '-' + task.year + '-Q' + this.task.report_period__code + '-' + this.task.report_type__code + '-' + this.task.report_name__code

        let dataTypes = {
            "item": "String",
            "value": "String",
            "auto_calc": "String",
            "input": "String",
        }
        let fields = []

        _export.set(this.data, filename, dataTypes, fields)
        _export.exportItem()
      },

        getReport() {
          var _export = new Export()
          let task = this.task
          var filename  = this.task.company__stock_code  + '-' + this.task.company__type__code + '-' + task.year + '-Q' + this.task.report_period__code  + '-' + task.report_type__code + '-' + this.task.report_name__code
          let array = this.$copy(this.data)
          array.map(v=>v.input = mixing.numbertoString(v.item_value))
          _export.set(array, filename)
          _export.exportReport()
        },

        validateData() {
          //validate data
          if(this.numberFieldError>0) {
            this.msgInfo.push({message: 'Có lỗi ở ' + this.numberFieldError + ' chỉ tiêu, không thể lưu dữ liệu', type: 'error'})
            return false
          } 
          else if(this.numberFieldEntered===0) {
            this.msgInfo.push({message: 'Bạn chưa nhập báo cáo', type: 'error'})
            return false
          } 
          else if(this.data.filter(v=>v.item_value===0).length>0) {
            this.msgInfo.push({message: 'Có giá trị = 0 trên báo cáo', type: 'error'})
            return false
          }

          /* Blocked
          if(this.radio==='accumulate' && this.taskArr && !this.radioTask) {
            this.msgInfo.push({message: 'Q' + (parseInt(this.task.report_period__code) -1) + ' không có báo cáo thỏa mãn. Hãy nhập báo cáo trước khi lưu.', type: 'error'})
            return false
          } */

          let connName = mixing.connection(this.task.report_name__code, this.task.company__type__code).toLowerCase()
          if(!(connName==='bssx' || connName==='bsnh' || connName==='bsck' || connName==='bsbh')) return true
          var check = function(data, item1, item2) {
            let ele1 = data.find(v=>v.item===item1)
            let ele2 = data.find(v=>v.item===item2)
            if(ele1.item_value===ele2.item_value) return true
            else return false
          }
          var isOK = false
          switch (this.task.company__type__code) {
            case 'SX':
              isOK = check(this.data, '00069', '00133')
              break;

            case 'CK':
              isOK = check(this.data, '01581', '01663')
              break;
                
            case 'BH':
              isOK = check(this.data, '00908', '00991')
              break;

            case 'NH':
              isOK = check(this.data, '00478', '00509')
              break; 
          }

          if(isOK===false) {
            this.msgInfo.push({message: this.api.find3var('inform','balance-sheet','asset-liabilities').value, type: 'error'})
            return false
          }
          return true
        },

        saveData() {
          if(this.validateData()===false) return false
          let data = this.report? this.$copy(this.report) : {task: this.task.id}
          data.update_time = new Date(),
          data.enable = true,
          this.data.forEach((item) => {data['f' + item.item] = item.item_value===undefined? null : item.item_value})

          //insert
          let connName = mixing.connection(this.task.report_name__code.replace('-LK', ''), this.task.company__type__code).toLowerCase()
          connName = connName + 'report'
          if(this.report===undefined) this.connection1.insert(connName, data)
          else this.connection1.update(connName, data)
          this.saveItemChange()
        },

        updateTask() {
          let data = JSON.parse(JSON.stringify(this.task))
          if(data.status__code==='not-yet-entered') {
              data.status = this.api.find3var('list', 'task-status', 'entered').id
              data.entry_time = new Date()
          }
          else if(this.sending===true) {
              data.status = this.api.find3var('list', 'task-status', 'waiting-approve').id
              data.waiting1_time = new Date()
          }
          else if(this.changeStatus!==undefined) {
            data.status = this.changeStatus.id
            if(this.selected.code==='retype') {
              this.msgLocked = [{message: 'Báo cáo được yêu cầu sửa lại với lý do : ' + this.retypeReason, type: 'warning'}]
              let list = data.history===null? [] : JSON.parse(data.history)
              list.push({sender: this.login.id, message: this.retypeReason, time: new Date().toString()})
              data.history = JSON.stringify(list)
              this.selected = undefined
            }
            else if(this.selected.code==='waiting-approve-2') {
                data.waiting2_time = new Date()
            }
            else if(this.selected.code==='approved') {
              this.approve_time = new Date()
              data.approve_time = this.approve_time
            }
          }
          
        data.update_time = new Date()
        data.total_fields = this.numberFieldEntered + this.numberFieldPending,
        data.entered_fields = this.numberFieldEntered,
        data.pending_fields = this.numberFieldPending,
        data.percentage = this.percentage,
        data.marked_fields = this.numberFieldLocked === 0? null : this.numberFieldLocked
        data.file = this.file? this.file.id : null
        if(this.dataFile) data.data_file = this.dataFile
        data.accumulate = this.radio==='accumulate'? 1 : 0
        /* block
        if(this.radio==='accumulate' && this.task.report_name__code.indexOf('-LK')<0) {
          data.report_name = this.api.find3var('list', 'report-name', this.task.report_name__code + '-LK').id
        } else if(this.radio==='quarterly' && this.task.report_name__code.indexOf('-LK')>=0) {
          data.report_name = this.api.find3var('list', 'report-name', this.task.report_name__code).id
        } */
        if(this.$empty(this.retypeReason)===false) data.detail = this.retypeReason
        this.connection2.update('taskobj', data, this.values)
      },

      taskStatus() {
        this.rightApprove = false
        this.result = []
        let list = [{name: 'success', value: 'is-active is-success'},
                    {name: 'error', value: 'is-active is-danger'},
                    {name: 'normal', value: 'is-active is-warning'}]
        let status = this.api.getbyid(this.task.status)
        this.result.push({name: 'assign', value: list.find(v=>v.name==='success').value})
        
        if(status.code==='not-yet-entered' || status.code==='entered')
            this.result.push({name: 'entered', value: list.find(v=>v.name==='normal').value})

        else if(status.code==='waiting-approve') {
            this.rightApprove = true
            this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='normal').value})
        }

        else if(status.code==='waiting-approve-2') {
            this.rightApprove = true
            this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'waiting-approve-2', value: list.find(v=>v.name==='normal').value})
        }

        else if(status.code==='approved') {
            this.result.push({name: 'entered', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'waiting-approve', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'waiting-approve-2', value: list.find(v=>v.name==='success').value})
            this.result.push({name: 'approved', value: list.find(v=>v.name==='success').value})
            let message = 'Báo cáo đã được duyệt. Bạn không thể thay đổi được thông tin.'
            this.msgLocked = [{message: message, type: 'warning'}]
            this.preview = true
            this.editable = false
            if(this.login.type.code==='admin' || this.login.type.code==='manager') this.retype = false
          }

          else if(status.code==='retype') {
              this.msgLocked = [{message: 'Báo cáo được yêu cầu sửa lại với lý do : ' +  this.task.detail, type: 'warning'}]
              this.retypeReason = this.task.detail
          }
          this.selected = this.api.getbyid(this.task.status)
        },

        sendReport() {
          if(this.validateData()===false) return
          if(this.$empty(this.file)) {
            this.msgInfo.push({message: 'Bạn chưa đính kèm file gốc (pdf, word) của báo cáo.', type: 'error'})
            return
          }
          
          this.$buefy.dialog.confirm({
            message: 'Gửi báo cáo đi sẽ không thay đổi được dữ liệu đã nhập nếu không có yêu cầu sửa lại. Bạn có muốn tiếp tục không?',
            type: 'is-warning',
            onConfirm: () => {
              this.sending = true
              this.saveData()
            }
          })
        },

        checkRights() {
          let status = this.api.getbyid(this.task.status)
          let type = this.login.type

          if(type.code==='staff' || type.code==='ctv') {
            this.dldata = false
            if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {   
              this.preview = true
              this.editable = false
              this.rightApprove = false
              let message = 'Báo cáo đang chờ duyệt. Bạn không thể thay đổi được thông tin.'
              this.msgLocked = [{message: message, type: 'warning'}]
            }
          } 
          else {
            if(status.code==='waiting-approve' || status.code==='waiting-approve-2') {
              this.rightApprove = true
              this.approvelist = []
              this.approvelist.push(this.api.find3var('list','task-status','waiting-approve'))
              this.approvelist.push(this.api.find3var('list','task-status','waiting-approve-2'))
              this.approvelist.push(this.api.find3var('list','task-status','retype'))

              if(type.code==='admin' || type.code==='manager') {
                this.approvelist.push(this.api.find3var('list','task-status','approved'))
              }
            }
          }
        },

        approveTask() {
          if(this.selected.code==='retype' && this.$empty(this.retypeReason)===true) {
            this.msgLocked = [{message: 'Lý do sửa lại không được để trống', type: 'warning'}]
            return
          }
          this.changeStatus = {id: this.selected.id, msgSuccess: 'Duyệt công việc thành công.', msgError: 'Duyệt công việc thất bại'}
          this.saveData()
        },

        checkEditValid(element) {
          let isValid = false
          let ele = JSON.parse(JSON.stringify(element))
          if(this.$empty(ele.edit_value)===false && mixing.isNumber(ele.edit_value)===true) isValid = true

          if(isValid===true && this.$empty(ele.edit_note)===false) isValid = true
          else isValid = false

          if(isValid===true) {
              ele.edit_valid = true
              ele.edit_value = mixing.numbertoString(ele.edit_value)
          } else  ele.edit_valid = false

          this.editItem = ele
          return isValid
        },

        openEditForm(ele) {
          this.editItem = JSON.parse(JSON.stringify(ele))
          this.editItem.edit_value =  mixing.numbertoString(ele.item_value)
          this.editItem.edit_note = ele.edit_note
        },

        saveEditItem() {
          if(this.checkEditValid(this.editItem)===false) return
          let ele = this.data.find(v=>v.id===this.editItem.id)
          if(ele.origin_value===undefined) ele.origin_value = JSON.parse(JSON.stringify(ele.item_value))
          ele.locked = true
          ele.edit_note = this.editItem.edit_note
          this.models[ele.id] = this.editItem.edit_value
          ele.item_value = mixing.formatNumber(this.models[ele.id])
          ele.edit_type = 'save'
          this.checkValue(ele)
          this.editItem = undefined
        },

        deleteEditItem() {
          let ele = this.data.find(v=>v.id===this.editItem.id)
          ele.locked = false
          ele.edit_note = undefined
          ele.edit_type = 'delete'
          let list = mixing.unique(this.data, ['level'])
          list.sort((a,b)=> - a.level + b.level)
          list.forEach(ele => {
            let filter = this.data.filter(v=>v.level===ele.level && this.$empty(v.formula)===false)
            filter.forEach(item => this.formulaCalc(item))
          })
          this.editItem = undefined
        },

        saveItemChange() {
          let filter = this.data.filter(v=>v.edit_type!==undefined)
          if(filter.length===0) return
          let list = this.itemchangelist.filter(v=>v.report===this.report.id)

          filter.forEach(element => {
            let data = {
              item: element.id,
              report: this.report.id,
              type: this.task.company__type__code,
              enable: true,
              report_name: this.task.report_name__code,
              task: this.task.id
            }

            let found = list.find(v=>v.item===element.id)
            if(found!==undefined) data = JSON.parse(JSON.stringify(found))
            data.origin_value = this.$empty(element.origin_value)===true? element.item_value : element.origin_value
            data.value = element.item_value
            data.reason = element.edit_note
            data.update_time = new Date()
            
            if(found===undefined) this.connection3.insert('itemchangelist', data)
            else {
              if(element.edit_type==='delete') data.enable = false
              else data.enable = true
              this.connection3.update('itemchangelist', data)
            }
          })
        },

        getTaskRef() {
          if(this.task.report_name__code.indexOf('-LK')>=0) {
            let connName = mixing.connection(this.$route.query.report.replace('-LK', ''), this.$route.query.type)
            let connlist = []
            if(this.taskRelated) {
              connlist.push({name: 'taskref', url: 'data/Task', params: {filter: {id: this.taskRelated.task===this.task.id? this.taskRelated.related : this.taskRelated.task}}})
              connlist.push({name: connName + 'ref', url: 'data/' + connName.toUpperCase(), params: {filter: {task: this.taskRelated.task===this.task.id? this.taskRelated.related : this.taskRelated.task}}})
              if(this.taskRelated.task_prev) {
                connlist.push({name: 'taskprev', url: 'data/Task', params: {values: this.values, filter: {id: this.taskRelated.task_prev}}})
                connlist.push({name: connName + 'prev', url: 'data/' + connName.toUpperCase(), params: {filter: {task: this.taskRelated.task_prev}}})
              }
            }
            this.connection9.getApi(connlist)
          }
        },

        updateTaskRef() {
          //check task related
          let checklist = ['01872', '01873', '01902', '01903', '01968', '01969', '01995']
          let data = this.reportRef? this.$copy(this.reportRef) : 
          {task: this.taskRelated.task===this.task.id? this.taskRelated.related : this.taskRelated.task}
          data.update_time = new Date(),
          data.enable = true,
          this.data.forEach((v) => {
            let found = checklist.find(x=>x===v.item)
            if(found) {
              data['f' + v.item] = this.report['f' + v.item]
            } else {
              data['f' + v.item] = (this.report['f' + v.item]? this.report['f' + v.item] : 0) - (this.reportPrev['f' + v.item]? this.reportPrev['f' + v.item] : 0)
            }
          })
          let connName = mixing.connection(this.task.report_name__code.replace('-LK', ''), this.task.company__type__code).toLowerCase()
          connName = connName + 'report'
          if(data.id) this.connection10.update(connName, data)
          else this.connection10.insert(connName, data)
        },

        toggle(ele) {
          if(ele.child===undefined) return
          ele.expanded =  ele.expanded===true? false : true
          if(ele.expanded===false) {
            let list = this.data.filter(v=>v.expanded===true)
            list.forEach(element => {
              if(element.item===ele.item) element.expanded = false
              else {
                let parent = this.data.find(v=>v.item===element.parent)
                while (parent!==undefined) {
                  if(parent.item===ele.item) element.expanded = false
                  parent = this.data.find(v=>v.item===parent.parent)
                }
              }
            })  
          }
        },

        expandAll() {
          this.expanded = true
          this.data.forEach(element => {
              if(element.child!==undefined) element.expanded = true
          })
          this.expanded = true
        },

        collapseAll() {
          this.data.forEach(element => {if(element.child!==undefined) element.expanded = false})
          this.expanded = false
        },
        
        getstyleicon(item) { 
          var val = 'font-size:28px; color:hsl(0, 0%, 14%)'
          var child = item.child

          switch (item.level) {
            case 0:
              if(item.expanded === true)
                val = child !== undefined?  'font-size:28px; color: rgb(57, 38, 212)' : val
              break;

            case 1:
              if(item.expanded === true)
                val = child !== undefined?  'font-size:28px; color: rgb(57, 38, 212)' : val
              break;

            case 2:
              if(item.expanded === true)
                val = child !== undefined?  'font-size:28px; color: rgb(57, 38, 212)' : val
              break;

            case 3:
              if(item.expanded === true) {
                val = child !== undefined?  'font-size:28px; color:hsl(0, 0%, 14%)': val
              }
              break;
            
            case 4:
              if(item.expanded === true)
                val = child !== undefined?  'font-size:28px; color:hsl(0, 0%, 14%)': val
              break;
                        
            case 5:
              if(item.expanded === true)
                val = child !== undefined?  'font-size:28px; color:hsl(0, 0%, 14%)': val
              break;
            }
          return val
        },

        getstyle(item) {
          let val = 'font-size:13px;color:hsl(0, 0%, 14%)'
          
          switch (item.level) {
            case 0:
              if(item.expanded === true)
                val = 'font-size:16px; color: rgb(57, 38, 212)'
              break;

            case 1:
              if(item.expanded === true)
                val = item.child !== undefined? 'font-size:16px;  color: rgb(57, 38, 212)': 'color: rgb(57, 38, 212)'
              break;

            case 2:
              if(item.expanded === true)
                val = item.child !== undefined? 'font-size:16px; color:rgb(57, 38, 212)': 'color: rgb(57, 38, 212)'
              break;

            case 3:
              if(item.expanded === true)
                val = item.child !== undefined? 'font-size:16px; color:#9C27B0': 'color: rgb(57, 38, 212)'
              break;
          
            case 4:
              if(item.expanded === true)
                val = item.child !== undefined? 'font-size:16px; color:#009688': 'color: rgb(57, 38, 212)'
              break;
                      
            case 5:
              if(item.expanded === true)
                val = item.child !== undefined? 'font-size:16px; color:#FF9100': 'color: rgb(57, 38, 212)'
              break;
          }
          return val
        },

        nextInputfocus(obj) {
          var next = this.nextInputItem(obj.index)
          if(next === undefined) return
      
          //check is same parent
          if(obj.parent === next.parent && this.api1.filter1var('parent', next.item).length === 0) {
              Vue.set(this.form.expand, obj.id, false)
              Vue.set(this.form.expand, next.id, true)
              this.setfocus(next.id)    
              return
          }

          //difference parent
          this.form.watchlist = []
          var nextlist = this.findItemList(next)
          var apix = new Apidata()
          apix.set(nextlist)

          this.form.expand.forEach((element,id) => {
            if(apix.getbyid(id) === undefined) Vue.set(this.form.expand, id, false)
          })

          var i = nextlist.length - 1
          while (i >= 0) {
            this.form.watchlist.push({parent: i === nextlist.length - 1? undefined: nextlist[i+1],item: nextlist[i], value: true, focus: nextlist[i].id === next.id? true: false})
            i = i -1
          }
        },

        informNewItem() {
          if(this.$empty(this.newItem)===true) {
            this.newItemMsg = this.api.getvalue(this.api.find3var('inform','new-item','content-empty'))
            return
          }

          var info = this.task.company__stock_code + '/' + this.task.company__type__code + '/' + this.task.year + '/' + this.task.report_period__value + '/' +  this.task.report_type__code + '/' + this.task.report_name__code
          let data = {
            'subject': this.api.getvalue(this.api.find3var('email','new-item','subject')),
            'content': this.api.getvalue(this.api.find3var('information','report-name','label')) + ': ' + info + '\n\n' + this.api.getvalue(this.api.find3var('information','sender','label')) + ': ' 
            + this.login.name + ' (' + this.login.email + ')' + '\n\n' + this.newItem + '\n\n' + this.api.getvalue(this.api.find3var('footer','company','name')),
            'to': this.api.getvalue(this.api.find3var('email','register-new','receiver'))
          }

          var url = this.connection.path +  'send-email/'
          var  headers = {"Content-Type": "application/json"}
          axios.post(url, data= data, headers=headers)
          .then((response) => {
            this.newItemMsg = this.api.getvalue(this.api.find3var('inform','account','email-sent'))
          })
          .catch(error => {
            this.newItemMsg = this.api.getvalue(this.api.find3var('inform','message','msg3'))
          })
        },

      download() {
        window.open(this.connection.path + 'static/files/' + this.file.file, '_blank')
      },

      removeImage(v, i) {
        this.$delete(this.images, i)
        if(v.id) this.connection6.delete('taskimage', v.id)
      },

      openRelated() {
        let routeData =this.$router.resolve({path: '/finance/data-entry', query: {task: this.task.id===this.taskRelated.task? this.taskRelated.related : this.taskRelated.task,
        type: this.task.company__type__code, company: this.task.company, report: this.taskRelated.related__report_name__code}})
        window.open(routeData.href, '_blank')
      },

      showTime(v) {
        if(!v) return
        return mixing.yyyymmddhhmm(new Date(v))
      },

      downloadDataFile() {
        mixing.download( this.connection.path + 'get-datafile/' + this.task.data_file + '/')
      },

      openReport(v) {
        let routeData =this.$router.resolve({path: '/finance/data-entry', query: {task: v.id, type: v.company__type__code, company: v.company, report: v.report_name__code}})
        window.open(routeData.href, '_blank')
      }
    }
}
</script>

  <style scoped>
    td {
      height: 38px !important;
      padding-top: 3px  !important;
      padding-bottom: 3px  !important;
    }

    input {
      border: 0;
      outline: 0;
      background: transparent;
      border-bottom: 1px solid #7A7A7A;
      -webkit-border-radius: 0;
      border-radius: 0;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
  </style>

  <style scoped
    src="bulma-extensions/bulma-tooltip/dist/css/bulma-tooltip.min.css">
  </style>