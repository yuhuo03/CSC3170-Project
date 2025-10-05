<!-- src/components/EditUser.vue -->
<template>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Edit User</v-card-title>
            <v-card-text>
              <v-form ref="form" @submit.prevent="updateUser">
                <v-text-field
                  v-model="user.name"
                  label="Name"
                  :error-messages="errors.name"
                  @input="clearError('name')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.email"
                  label="Email"
                  :error-messages="errors.email"
                  @input="clearError('email')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.phone"
                  label="Phone"
                  :error-messages="errors.phone"
                  @input="clearError('phone')"
                  required
                ></v-text-field>
                <v-card-actions>
                  <v-btn color="primary" @click="updateUser">Save Changes</v-btn>
                  <v-btn text @click="goBack">Cancel</v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Snackbar Component -->
      <v-snackbar v-model="snackbar" :timeout="3000" top right :color="snackbarColor">
        {{ snackbarMessage }}
        <template v-slot:action="{ attrs }">
          <v-btn text v-bind="attrs" @click="snackbar = false">Close</v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue';
  import axios from '../axios';
  import { useRouter, useRoute } from 'vue-router';
  
  export default {
    name: 'EditUser',
    setup() {
      const user = ref({});
      const router = useRouter();
      const route = useRoute();
      const form = ref(null);
      const errors = reactive({});
  
      const snackbar = ref(false);
      const snackbarMessage = ref('');
      const snackbarColor = ref('');
  
      const fetchUser = async () => {
        try {
          const response = await axios.get(`/api/users/${route.params.id}`);
          user.value = response.data;
        } catch (error) {
          snackbarMessage.value =
            'Failed to fetch user information: ' + (error.response?.data?.message || error.message);
          snackbarColor.value = 'error';
          snackbar.value = true;
          router.push('/librarian/users');
        }
      };
  
      const updateUser = async () => {
        // Clear previous errors
        Object.keys(errors).forEach((key) => {
          errors[key] = [];
        });
  
        if (form.value.validate()) {
          try {
            await axios.put(`/api/users/${route.params.id}`, {
              name: user.value.name,
              email: user.value.email,
              phone: user.value.phone,
            });
            snackbarMessage.value = 'User information updated successfully';
            snackbarColor.value = 'success';
            snackbar.value = true;
            setTimeout(() => {
              router.push('/librarian/users');
            }, 1500);
          } catch (error) {
            if (
              error.response &&
              error.response.status === 400 &&
              error.response.data.errors
            ) {
              const serverErrors = error.response.data.errors;
              Object.keys(serverErrors).forEach((field) => {
                errors[field] = serverErrors[field];
              });
            } else {
              snackbarMessage.value =
                'Failed to update user information: ' + (error.response?.data?.message || error.message);
              snackbarColor.value = 'error';
              snackbar.value = true;
            }
          }
        }
      };
  
      const clearError = (field) => {
        errors[field] = [];
      };
  
      const goBack = () => {
        router.push('/librarian/users');
      };
  
      onMounted(() => {
        fetchUser();
      });
  
      return {
        user,
        updateUser,
        goBack,
        form,
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
  /* Add custom styles if needed */
  </style>
  