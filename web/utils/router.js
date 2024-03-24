import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  { path: "/", component: () => import("../src/views/MainView.vue") },
  { path: "/about", component: () => import("../src/views/AboutView.vue") },
  {
    path: "/dashboard",
    component: () => import("../src/views/DashboardView.vue"),
  },
  { path: "/table", component: () => import("../src/views/TableView.vue") },
  { path: "/trace", component: () => import("../src/views/TraceView.vue") },

  // {path: '/login', component: () => import('../src/views/Login.vue')},
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
