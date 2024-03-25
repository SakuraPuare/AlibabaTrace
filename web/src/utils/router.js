import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  { path: "/", component: () => import("../views/MainView.vue") },
  { path: "/about", component: () => import("../views/AboutView.vue") },
  {
    path: "/dashboard",
    component: () => import("../views/DashboardView.vue"),
  },
  { path: "/table", component: () => import("../views/TableView.vue") },
  { path: "/trace", component: () => import("../views/TraceView.vue") },

  // {path: '/login', component: () => import('../src/views/Login.vue')},
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
