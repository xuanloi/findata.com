<!-- eslint-disable -->
<template>
	<div>   
   <!-- <section class="hero" v-bind:class="api.getvalue(api.find3var('footer','style','style'))" -->
    <section class="hero is-dark is-light"
	:style="'background-color:' + api.getvalue(api.find3var('footer','background','backgroundcolor'))">
  <div class="hero-body pt20 pb20">
	  <div class="columns is-paddingless is-mobile">
		   <div class="column is-4">
				<p class="is-5 has-text-centered" v-html="api.getvalue(api.find3var('footer', 'company','name'))">
				</p>
		  </div>

		<div class="column is-8 has-text-left" v-if="login">
		<p class="is-6 has-text-centered">
		<router-link :to="{	path: '/finance/task-list'}" class="pr30  has-text-white" v-html="api.getval(api.find3var('menu','menu','menu2'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','not-yet-entered'), 'id')}}" class="pr30  has-text-white" v-html="api.getval(api.find3var('menu','menu','menu4'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','entered'), 'id')}}" class="pr30  has-text-white" v-html="api.getval(api.find3var('list','task-status','entered'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','waiting-approve'), 'id') }}" class="pr30  has-text-white" v-html="api.getval(api.find3var('list','task-status','waiting-approve'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','waiting-approve-2'), 'id') }}" class="pr30  has-text-white" v-html="api.getval(api.find3var('list','task-status','waiting-approve-2'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','approved'), 'id') }}" class="pr30  has-text-white" v-html="api.getval(api.find3var('menu','menu','menu3'),'value')"></router-link>
		<router-link :to="{ path: '/finance/task-list', query: {status: api.getval(api.find3var('list','task-status','retype'), 'id') }}" class="has-text-white" v-html="api.getval(api.find3var('list','task-status','retype'),'value')"></router-link>
		</p>
		</div>
	  </div>
  </div>
</section>
</div>
</template>

<script>
/* eslint-disable */
export default {
  	computed: {
		api: {
			get: function() {return this.$store.state.api},
			set: function(val) {this.$store.commit('updateApi', {api: val})}
		},

		login: {
      		get: function() {return this.$store.state.login},
      		set: function(val) {this.$store.commit("updateLogin", { login: val })}
    	}
	},

	methods: {
		chooselangguage: function(val) {
			localStorage.setItem('langguage', val)
			location.reload(false)
		},
	}
}
</script>