<template>
<div id="app">

  <!--<navbar></navbar>-->

  <router-view :key="$route.fullPath"></router-view>  <!-- 2023/04/06, 解決Reload with current path and call data hook again-->
</div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    'navbar': Navbar
  },
  name: 'Menu',
  data() {
    return {

    };
  },
}
</script>

<style scoped lang="scss">
  @media (min-width: 992px) {
    .navbar.custom-nav{
      padding-top:16px;
      padding-bottom:16px;
      background-color: #7DA79D !important;
    }
   }
</style>