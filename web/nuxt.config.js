module.exports = {
  server: {
    port: 3000, // default: 3000
    host: 'localhost', // default: localhost
  },
  
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'Frontend',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [
    '~/assets/styles/main.scss',
    '~/assets/styles/style.css',
    '~/node_modules/@mdi/font/css/materialdesignicons.min.css'
  ],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '~/plugins/buefy',
    '~/plugins/gtag',
    '~/plugins/vue-lazyload',
    '~/plugins/lang',
    '~/plugins/components',
    '~/plugins/calculation',
    { src: '~/plugins/vuex-persist', ssr: false }
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    '@nuxtjs/bulma',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '~/io',
    '@nuxtjs/dayjs',
    '@nuxt/image'
  ],

  env: {
    ///WS_URL: process.env.WS_URL || 'http://findata.com.vn'
  },

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {},

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    postcss: {
      preset: {
        features: {
          customProperties: false
        }
      }
    },
    extend(config, { isDev, isClient }) {
      config.resolve.alias["vue"] = "vue/dist/vue.common";
    }
  }
}
