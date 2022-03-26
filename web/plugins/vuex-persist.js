import VuexPersistence from 'vuex-persist'
/** https://github.com/championswimmer/vuex-persist#tips-for-nuxt */

export default ({ store }) => {
  window.onNuxtReady(() => {
    new VuexPersistence({
      key: 'storage',
      storage: window.sessionStorage,
      reducer: state => ({ login: state.login, hasnews: state.hasnews, notification: state.notification })
    }).plugin(store)
  })
}
