import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminSystem from '../views/AdminSystem.vue'
import UsersManagement from '../views/UsersManagement.vue'
import ProjectsManagement from '../views/ProjectsManagement.vue'
import UserProjects from '../views/UserProjects.vue'
import ModelsManagement from '../views/ModelsManagement.vue'
import UserSystem from '../views/UserSystem.vue'
import UserExperiment from '../views/UserExperiment.vue'
import UserDataset from "../views/UserDataset.vue";
import UserModels from "../views/UserModels.vue";
import DatasetView from "../views/DatasetView.vue"

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
        path: 'models',
        component: ModelsManagement ,
      },
      {
        path: 'users',
        component: UsersManagement
      },
      {
        path: 'projects',
        component: ProjectsManagement
      },
      {
        path: '',
        redirect: '/admin/users'
      }
      ],
    },
    {
        path: '/user',
        component: UserProjects, // 您需要创建的详情页组件
        name: 'UserProjects'
    },
    {
      path: '/datasets/:dataset_name',
      component: DatasetView,
      name: 'DatasetView',
      props: true

    },
    {
    path: '/projects/:name',
    name: 'UserSystem',
    component: UserSystem,
    props: true ,// 将 :name 自动作为 prop 传入组件
    children: [
      {
        path: 'experiments',
        component: UserExperiment ,
      },
      {
        path: 'datasets',
        component: UserDataset
      },
      {
        path: 'models',
        component: UserModels ,
      },
      {
        path: '',
        redirect: to => {return `${to.path}/experiments`}
      }
    ]
  }
  ],
})

export default router
