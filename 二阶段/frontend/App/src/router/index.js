import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminSystem from '../views/AdminSystem.vue'
import UsersManagement from '../views/UsersManagement.vue'
import ExperimentsManagement from '../views/ExperimentsManagement.vue'
import ProjectsManagement from '../views/ProjectsManagement.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
    path: '/admin',
    component: AdminSystem,
    children: [
      {
        path: 'users',
        component: UsersManagement
      },
      {
        path: 'experiments',
        component: ExperimentsManagement
      },
      {
        path: '',
        redirect: '/admin/users'
      }
      ],
    },
    {
        path: '/user',
        component: ProjectsManagement, // 您需要创建的详情页组件
        name: 'ProjectsManagement'
}
  ],
})

export default router
