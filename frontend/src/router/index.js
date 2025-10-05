// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import SearchBooks from '../components/SearchBooks.vue';
import BookDetails from '../components/BookDetails.vue';
import UserDashboard from '../components/UserDashboard.vue';
import LibrarianDashboard from '../components/LibrarianDashboard.vue';
import AddBook from '../components/AddBook.vue';
import ManageUsers from '../components/ManageUsers.vue';
import EditUser from '../components/EditUser.vue';
import ManageBooks from '../components/ManageBooks.vue';
import EditBook from '../components/EditBook.vue';

const routes = [
  { path: '/', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/search', component: SearchBooks },
  { path: '/book/:id', component: BookDetails },
  { path: '/dashboard', component: UserDashboard },
  { path: '/librarian', component: LibrarianDashboard },
  { path: '/add-book', component: AddBook },
  { path: '/librarian/users', component: ManageUsers },
  { path: '/librarian/users/:id/edit', component: EditUser },
  { path: '/librarian/books', component: ManageBooks },
  { path: '/librarian/books/:id/edit', component: EditBook },
  { path: '/:catchAll(.*)', redirect: '/' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role');
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.path.startsWith('/librarian') && role !== 'librarian') {
    next('/');
  } else if ((to.path === '/dashboard' || to.path === '/search') && !isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;
