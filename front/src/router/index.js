import Vue from 'vue'
import VueRouter from 'vue-router'
import Navbar from '../components/Navbar.vue'
import Camera from '../components/runVideoMeeting.vue'
import Login from '../views/LoginForm.vue'
import Employer from '../views/menu/Employer.vue'
import Spindle from '../views/menu/Spindle.vue'
import SpindleRunIn from '../views/menu/SpindleRunIn.vue'
import Grids from '../views/menu/SpindleGrids.vue'
import Permission from '../views/menu/permission.vue'
import StockInTag from '../views/menu/SpindleStockInGrid.vue'
import StockOutTag from '../views/menu/SpindleStockOutGrid.vue'
import StockRecord from '../views/menu/SpindleStockRecord.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/',      name: 'Login', component: Login},
  { path: '/emp',   name: 'Employer', component: Employer},
  { path: '/spindle',  name: 'Spindle', component: Spindle},
  { path: '/runIn',  name: 'SpindleRunIn', component: SpindleRunIn},
  { path: '/grid',  name: 'Grids', component: Grids},

  { path: '/perm',  name: 'Permission', component: Permission},
  { path: '/inTag', name: 'StockInTag', component: StockInTag},
  { path: '/outTag', name: 'StockOutTag', component: StockOutTag},
  { path: '/navbar', name: 'Navbar', component: Navbar},
  { path: '/camera', name: 'Camera', component: Camera},
  { path: '/stockRec', name: 'StockRecord', component: StockRecord},
]

const router = new VueRouter({
  mode: 'history',
  // base: process.env.BASE_URL,
  base: '/',
  routes
})

router.beforeEach((to, from, next) => {
  //const isRedirected = from.name === 'Navbar';

  let isAuthenticated=localStorage.getItem('Authenticated');
  if (isAuthenticated == null) {
    isAuthenticated=false;
    localStorage.setItem('Authenticated', isAuthenticated);
  }
  console.log("routing is(to, from, auth):", to.name, from.name, isAuthenticated);

  //if (from.name === 'Navbar' && to.name === 'Login' ) {
//    next()
//  } else {
    //next({ name: 'Navbar' })
  //}

  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login'});
  } else {
    next();
  }
})

export default router
