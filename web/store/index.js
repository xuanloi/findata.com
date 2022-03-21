/* eslint-disable */

export const state = () => ({
  syspara: undefined,
  api: undefined,
  login: undefined,
  pagefunction: undefined,
  rights: undefined,
  ismobile: undefined,
  pageparam: undefined,
  pagetask: undefined,
  companylist: undefined,
  accountlist: undefined,
  pageaccount: undefined,
  pagecompany: undefined,
  pageitem: undefined,
  leavelist: undefined,
  pageleave: undefined,
  media: undefined,
  menuaction: undefined,
  pageimport: undefined,
  pagehelp: undefined,
  helpcategory: undefined,
  helplist: undefined,
  category: undefined,
  pagenews: undefined,
  newslist: undefined,
  action: undefined,
  hasnews: undefined,
  notification: undefined,
  industry: undefined,
  //datatable
  moneyunit: undefined,
  datatype: undefined,
  filterchoice: undefined,
  colorchoice: undefined,
  textalign: undefined,
  placement: undefined,
  colorscheme: undefined,
  settingtype: undefined,
  filtertype: undefined,
  sorttype: undefined,
  tablesetting: undefined,
  settingchoice: undefined,
  sharechoice: undefined,
  menuchoice: undefined,
  settingclass: undefined,
  textcolor: undefined,
  pagedata: undefined,
  currentsetting: undefined
  //end datatable

})

export const mutations = {
  //datatable
  updateMoneyUnit(state, payload) {state.moneyunit = payload.moneyunit},

  updateDataType (state, payload) { state.datatype = payload.datatype },

  updateFilterChoice (state, payload) { state.filterchoice = payload.filterchoice },

  updateTextAlign (state, payload) { state.textalign = payload.textalign },

  updatePlacement (state, payload) { state.placement = payload.placement },

  updateColorScheme (state, payload) { state.colorscheme = payload.colorscheme },

  updateTextColor (state, payload) { state.textcolor = payload.textcolor },

  updateFilterType (state, payload) { state.filtertype = payload.filtertype },

  updateSortType (state, payload) { state.sorttype = payload.sorttype },

  updateColorChoice (state, payload) { state.colorchoice = payload.colorchoice },

  updateSettingType (state, payload) { state.settingtype = payload.settingtype },

  updateTableSetting (state, payload) { state.tablesetting = payload.tablesetting },

  updateSettingChoice (state, payload) { state.settingchoice = payload.settingchoice },

  updateShareChoice (state, payload) { state.sharechoice = payload.sharechoice },

  updateMenuChoice (state, payload) { state.menuchoice = payload.menuchoice },

  updateSettingClass (state, payload) { state.settingclass = payload.settingclass },

  updatePageData (state, payload) { state.pagedata = payload.pagedata },

  updateCurrentSetting (state, payload) { state.currentsetting = payload.currentsetting },

  //end datatable
  updateState (state, payload) { state[payload.name][payload.key] = payload.data },

  updateStore (state, payload) { state[payload.name] = payload.data},
  
  updateSystemParameter(state, payload) {state.syspara = payload.syspara},

  updateApi (state, payload) { state.api = payload.api },

  updateLogin (state, payload) { state.login = payload.login },

  updatePageFunction (state, payload) { state.pagefunction = payload.pagefunction },

  updateUserRight (state, payload) { state.userright = payload.userright },

  updateIsMobile (state, payload) { state.ismobile = payload.ismobile },

  updateRights (state, payload) { state.rights = payload.rights },

  updatePageParam (state, payload) { state.pageparam = payload.pageparam },

  updatePageTask (state, payload) { state.pagetask = payload.pagetask },

  updateCompanyList (state, payload) { state.companylist = payload.companylist },
  
  updateAccountList (state, payload) { state.accountlist = payload.accountlist },

  updatePageAccount(state, payload) {state.pageaccount = payload.pageaccount},

  updatePageCompany(state, payload) {state.pagecompany = payload.pagecompany},

  updatePageItem(state, payload) {state.pageitem = payload.pageitem},

  updateLeaveList(state, payload) {state.leavelist = payload.leavelist},

  updatePageLeave(state, payload) {state.pageleave = payload.pageleave},

  updateMedia(state, payload) {state.media = payload.media},

  updateMenuAction(state, payload) {state.menuaction = payload.menuaction},

  updatePageImport(state, payload) {state.pageimport = payload.pageimport},

  updatePageHelp(state, payload) {state.pagehelp = payload.pagehelp},

  updateHelpCategory(state, payload) {state.helpcategory = payload.helpcategory},

  updateCategory(state, payload) {state.category = payload.category},

  updatePageNews(state, payload) {state.pagenews = payload.pagenews},

  updateNewsList(state, payload) {state.newslist = payload.newslist},

  updateHelpList(state, payload) {state.helplist = payload.helplist},

  updateAction(state, payload) {state.action = payload.action},

  updateHasNews(state, payload) {state.hasnews = payload.hasnews},

  updateHasNews(state, payload) {state.hasnews = payload.hasnews},

  updateNotification(state, payload) {state.notification = payload.notification},

  updateIndustry(state, payload) {state.industry = payload.industry},
}

export default {state,  mutations}
