<!-- src/components/UserLogin.vue -->
<template>
  <v-container class="fill-height" fluid>
    <v-parallax
      :src="require('@/assets/background.png')"
      height="100%"
    >
      <v-row
        justify="center"
        align="center"
        class="fill-height"
      >
        <v-col cols="12" sm="8" md="4">
          <v-card elevation="12" class="pa-5">
            <v-card-title class="justify-center">
              <v-avatar size="64">
                <v-img :src="require('@/assets/logo.png')"></v-img>
              </v-avatar>
            </v-card-title>
            <v-card-subtitle class="text-center pb-4">
              Welcome to CUHK(SZ) Library Management System
            </v-card-subtitle>
            <v-card-text>
              <v-form ref="form" @submit.prevent="handleLogin">
                <v-text-field
                  v-model="username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  :error-messages="errors.username"
                  @input="clearError('username')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  prepend-inner-icon="mdi-lock"
                  :error-messages="errors.password"
                  @input="clearError('password')"
                  required
                ></v-text-field>
                <v-card-actions class="justify-center pt-6">
                  <v-btn color="primary" @click="handleLogin">Login</v-btn>
                  <v-spacer></v-spacer>
                  <router-link to="/register">
                    <v-btn text>Register</v-btn>
                  </router-link>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-parallax>

    <!-- Snackbar Component -->
    <v-snackbar
      v-model="snackbar"
      :timeout="3000"
      top
      right
      :color="snackbarColor"
    >
      {{ snackbarMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'UserLogin',
  setup() {
    const username = ref('');
    const password = ref('');
    const form = ref(null);
    const router = useRouter();
    const store = useStore();

    // Reactive object for field-specific errors
    const errors = reactive({});

    // Snackbar state
    const snackbar = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const handleLogin = async () => {
      // Clear previous errors
      Object.keys(errors).forEach((key) => {
        errors[key] = [];
      });

      if (form.value.validate()) {
        try {
          await store.dispatch('login', {
            username: username.value,
            password: password.value,
          });

          // Show success message in Snackbar
          snackbarMessage.value = 'Login successful';
          snackbarColor.value = 'success';
          snackbar.value = true;

          // Redirect after a short delay
          setTimeout(() => {
            if (store.state.user.role === 'librarian') {
              router.push('/librarian');
            } else {
              router.push('/dashboard');
            }
          }, 1500);
        } catch (error) {
          // Handle validation errors
          if (
            error.response &&
            error.response.status === 400 &&
            error.response.data.errors
          ) {
            const serverErrors = error.response.data.errors;
            Object.keys(serverErrors).forEach((field) => {
              errors[field] = serverErrors[field];
            });
          } else if (
            error.response &&
            error.response.status === 401 &&
            error.response.data &&
            error.response.data.message
          ) {
            // Set error message for the password field
            errors.password = [error.response.data.message];
          } else if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            snackbarMessage.value = 'Login failed: ' + error.response.data.message;
            snackbarColor.value = 'error';
            snackbar.value = true;
          } else {
            snackbarMessage.value = 'Login failed: ' + error.message;
            snackbarColor.value = 'error';
            snackbar.value = true;
          }
        }
      }
    };

    // Clear error messages when the user starts typing
    const clearError = (field) => {
      errors[field] = [];
    };

    return {
      username,
      password,
      form,
      handleLogin,
      errors,
      clearError,
      snackbar,
      snackbarMessage,
      snackbarColor,
    };
  },
};
</script>

<style scoped>
/* Custom styles */
.fill-height {
  min-height: 100vh;
}

.v-card {
  border-radius: 12px;
}

.v-text-field {
  margin-bottom: 20px;
}
</style>
