import {createRouter, createWebHashHistory} from "vue-router";

const routes = [
    {path: '/', component: () => import('../src/views/Main.vue')},
    {path: '/about', component: () => import('../src/views/About.vue')},
    {path: '/dashboard', component: () => import('../src/views/Dashboard.vue')},
    {path: '/table', component: () => import('../src/views/Table.vue')},
    {path: '/trace', component: () => import('../src/views/Trace.vue')},

    // {path: '/login', component: () => import('../src/views/Login.vue')},
]


const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router
