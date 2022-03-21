<template>
<div>
  <div class="field is-horizontal" v-for="(v,i) in keys" :key="i">
  <div class="field-body">
    <div class="field is-narrow">
  <div class="control">
    <input class="input fs14" type="text" placeholder="" v-model="keys[i]">
  </div>
</div>
    <div class="field is-grouped">
    <div class="control">
      <input class="input fs14" type="text" placeholder="" v-model="values[i]">
    </div>
    <p class="control">
    <a>
      <span class="icon fs22" @click="addAttr()"><i class="mdi mdi-plus-thick" /></span>
    </a>
    <a class="ml-2">
      <span class="icon has-text-danger fs22" @click="remove(i)"><i class="mdi mdi-minus-thick" /></span>
    </a>
  </p>
  </div>    
  </div>
  </div>
  <div class="buttons mt-5">
    <a class="button is-primary fs14" @click="update()">Cập nhật</a>
    <a class="button is-dark fs14" @click="$emit('close')">Đóng lại</a>
  </div>
</div>
</template>
<script>
export default {
  props: ['field'],

  data() {
    return {
      keys: [],
      values: []
    }
  },

  created() {
    Object.keys(this.field).map(v=>{
      this.keys.push(v)
      if(typeof this.field[v] === 'object' && this.field[v] !== null) {
        this.values.push(JSON.stringify(this.field[v]))
      } else this.values.push(this.field[v])
    })
  },

  methods: {
    addAttr() {
      this.keys.push(undefined)
      this.values.push(undefined)
    },

    remove(i) {
      this.$delete(this.keys, i)
      this.$delete(this.values, i)
    },

    update() {
      let obj = {}
      this.keys.map((v,i)=>{
        if(!this.$empty(v)) obj[v] = this.values[i]
      })
      this.$emit('update', obj)
    }
  }
}
</script>