import Vue from 'vue'
import VueRouter from 'vue-router'
//import Home from '../views/Home.vue'
import Navbar from '../components/Navbar.vue'
//import App1 from '../views/menu/App1.vue'
//import App2 from '../views/menu/App2.vue'
//import App3 from '../views/menu/App3.vue'
//import App4 from '../views/menu/App4.vue'
import Login from '../views/LoginForm.vue'
import Employer from '../views/menu/Employer.vue'
import Spindle from '../views/menu/Spindle.vue'
import SpindleRunIn from '../views/menu/SpindleRunIn.vue'
import Grids from '../views/menu/SpindleGrids.vue'
//import Grids from '../views/menu/Grids.vue'

//import GridsForLed from '../views/menu/GridsForLed.vue'

//import Department from '../views/menu/Department.vue'
//import Supplier from '../views/menu/Supplier.vue'
//import SupplierForProduct from '../views/menu/SupplierForProduct.vue'
import Permission from '../views/menu/permission.vue'
//import StockInTag from '../views/menu/SpindleStockInTag.vue'
import StockInTag from '../views/menu/SpindleStockInGrid.vue'
//import StockInTagPrint from '../views/menu/StockInTagPrint.vue'
//import StockIn from '../views/menu/StockIn.vue'
import StockOutTag from '../views/menu/SpindleStockOutGrid.vue'
//import StockOutTagPrint from '../views/menu/StockOutTagPrint.vue'
//import StockOut from '../views/menu/SpindleStockOut.vue'
//import BarCode from '../components/BarCode.vue'
//import ReqRecord from '../views/menu/ReqRecord.vue'
import StockRecord from '../views/menu/SpindleStockRecord.vue'
//import Inventory from '../views/menu/Inventory.vue'
//import RePrintTag from '../views/menu/RePrintTag.vue'
//import StorageRecord from '../views/menu/StorageRecord.vue'
//import Correction from '../views/menu/Correction.vue'


Vue.use(VueRouter)

const routes = [
  //{ path: '/',      name: 'Navbar', component: Navbar},
  { path: '/',      name: 'Login', component: Login},
  //{ path: '/about', name: 'About',  component: () => import('../views/About.vue') },
  { path: '/emp',   name: 'Employer', component: Employer},
  { path: '/spindle',  name: 'Spindle', component: Spindle},
  { path: '/runIn',  name: 'SpindleRunIn', component: SpindleRunIn},
  { path: '/grid',  name: 'Grids', component: Grids},

  //{ path: '/gridsForLed',  name: 'GridsForLed', component: GridsForLed},

  //{ path: '/dep',  name: 'Department', component: Department},
  //{ path: '/sup',  name: 'Supplier', component: Supplier},
  //{ path: '/supAndPrd',  name: 'SupplierForProduct', component: SupplierForProduct},
  { path: '/perm',  name: 'Permission', component: Permission},
  //{ path: '/stockIn', name: 'StockIn', component: StockIn},
  { path: '/inTag', name: 'StockInTag', component: StockInTag},
  //{ path: '/inTagPrint',   name: 'StockInTagPrint', component: StockInTagPrint},
  { path: '/outTag', name: 'StockOutTag', component: StockOutTag},
  //{ path: '/outTagPrint',   name: 'StockOutTagPrint', component: StockOutTagPrint},
  //{ path: '/stockOut', name: 'StockOut', component: StockOut},
  //{ path: '/app1', name: 'App1', component: App1},
  //{ path: '/app2', name: 'App2', component: App2},
  //{ path: '/app4', name: 'App4', component: App4},
  { path: '/navbar', name: 'Navbar', component: Navbar,
    //children: [
    //  { path: 'emp',   name: 'Employer', component: Employer},
    //],
  },
  //{ path: '/reqRec', name: 'ReqRecord', component: ReqRecord},
  { path: '/stockRec', name: 'StockRecord', component: StockRecord},
  //{ path: '/invent', name: 'Inventory', component: Inventory},
  //{ path: '/reprintTag', name: 'RePrintTag', component: RePrintTag},
  //{ path: '/storageRec', name: 'StorageRecord', component: StorageRecord},
  //{ path: '/correction', name: 'Correction', component: Correction},
  //{ path: '/barcode', name: 'BarCode', component: BarCode}, //for test
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
