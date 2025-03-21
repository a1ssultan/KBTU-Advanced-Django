import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '../views/LoginForm.vue';
import Admin from '../views/AdminPanel.vue';
import store from '../store';
import RegisterForm from '../views/RegisterForm.vue';

const routes = [
    { path: '/register', component: RegisterForm },
    { path: '/', component: LoginForm },
    {
        path: '/admin',
        component: Admin,
        meta: { requiresAdmin: true },
    },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        await store.dispatch('fetchUser');
        if (store.state.user?.role === 'admin') {
            next();
        } else {
            next('/');
        }
    } else {
        next();
    }
});

export default router;