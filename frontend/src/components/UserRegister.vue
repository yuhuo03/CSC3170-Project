<!-- src/components/UserRegister.vue -->
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
        <v-col cols="12" sm="8" md="6">
          <v-card elevation="12" class="pa-5">
            <v-card-title class="justify-center">
              <v-avatar size="64">
                <v-img :src="require('@/assets/logo.png')"></v-img>
              </v-avatar>
            </v-card-title>
            <v-card-subtitle class="text-center pb-4">
              Create Your Account
            </v-card-subtitle>
            <v-card-text>
              <v-form ref="form" @submit.prevent="handleRegister">
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
                <v-text-field
                  v-model="name"
                  label="Full Name"
                  prepend-inner-icon="mdi-account-outline"
                  :error-messages="errors.name"
                  @input="clearError('name')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  prepend-inner-icon="mdi-email"
                  :error-messages="errors.email"
                  @input="clearError('email')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="phone"
                  label="Phone"
                  prepend-inner-icon="mdi-phone"
                  :error-messages="errors.phone"
                  @input="clearError('phone')"
                  required
                ></v-text-field>
                <v-card-actions class="justify-center pt-6">
                  <v-btn color="primary" @click="handleRegister">Register</v-btn>
                  <v-spacer></v-spacer>
                  <router-link to="/">
                    <v-btn text>Back to Login</v-btn>
                  </router-link>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-parallax>

    <!-- Snackbar Component -->
    <v-snackbar v-model="snackbar" :timeout="3000" top right>
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
import axios from '../axios';

export default {
  name: 'UserRegister',
  setup() {
    const username = ref('');
    const password = ref('');
    const name = ref('');
    const email = ref('');
    const phone = ref('');
    const form = ref(null);
    const router = useRouter();
    const errors = reactive({});

    // Snackbar state
    const snackbar = ref(false);
    const snackbarMessage = ref('');

    const handleRegister = async () => {
      // Clear previous errors
      Object.keys(errors).forEach((key) => {
        errors[key] = [];
      });

      if (form.value.validate()) {
        try {
          const response = await axios.post('/api/register', {
            username: username.value,
            password: password.value,
            name: name.value,
            email: email.value,
            phone: phone.value,
          });

          if (response && response.data) {
            // Show success message in Snackbar
            snackbarMessage.value = 'Registration successful';
            snackbar.value = true;

            // Redirect after a short delay
            setTimeout(() => {
              router.push('/');
            }, 1500);
          } else {
            snackbarMessage.value = 'Registration failed: No response from server';
            snackbar.value = true;
          }
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
            error.response.data &&
            error.response.data.message
          ) {
            snackbarMessage.value = 'Registration failed: ' + error.response.data.message;
            snackbar.value = true;
          } else {
            snackbarMessage.value = 'Registration failed: ' + error.message;
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
      name,
      email,
      phone,
      form,
      handleRegister,
      errors,
      clearError,
      snackbar,
      snackbarMessage,
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
