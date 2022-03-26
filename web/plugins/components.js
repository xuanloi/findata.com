import Vue from 'vue'
import DataTable from '@/components/datatable/DataTable'
import TopMenu from '@/components/TopMenu'
import CompanySearch from '@/components/CompanySearch'
import Editor from '@tinymce/tinymce-vue'
import TableFilter from '@/components/TableFilter.vue'
import Footer from '@/components/Footer'

const components = { DataTable, TopMenu, CompanySearch, Editor, TableFilter, Footer}

Object.entries(components).forEach(([name, component]) => {
  Vue.component(name, component)
})