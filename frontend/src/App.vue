<!-- src/App.vue -->
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title> CUHK(SZ) Library Management System </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!isAuthenticated" text to="/">Login</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/register">Register</v-btn>
      <v-btn v-if="isAuthenticated && userRole === 'patron'" text to="/dashboard">Dashboard</v-btn>
      <v-btn v-if="isAuthenticated && userRole === 'librarian'" text to="/librarian">Librarian Dashboard</v-btn>
      <v-btn v-if="isAuthenticated" text @click="logout">Logout</v-btn>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'App',
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole']),
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
  },
};
</script>

<style>
/* Global styles if needed */
</style>
