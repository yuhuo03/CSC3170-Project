<!-- src/components/EditBook.vue -->
<template>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="headline">Edit Book</v-card-title>
            <v-card-text>
              <v-form ref="form" @submit.prevent="updateBook">
                <v-text-field
                  v-model="book.title"
                  label="Title"
                  :error-messages="errors.title"
                  @input="clearError('title')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.author"
                  label="Author"
                  :error-messages="errors.author"
                  @input="clearError('author')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.isbn"
                  label="ISBN"
                  :error-messages="errors.isbn"
                  @input="clearError('isbn')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.publisher"
                  label="Publisher"
                  :error-messages="errors.publisher"
                  @input="clearError('publisher')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.publication_year"
                  label="Publication Year"
                  type="number"
                  :error-messages="errors.publication_year"
                  @input="clearError('publication_year')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.total_copies"
                  label="Total Copies"
                  type="number"
                  :error-messages="errors.total_copies"
                  @input="clearError('total_copies')"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="book.location"
                  label="Location"
                  :error-messages="errors.location"
                  @input="clearError('location')"
                  required
                ></v-text-field>
                <v-card-actions>
                  <v-btn color="primary" @click="updateBook">Save Changes</v-btn>
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
    name: 'EditBook',
    setup() {
      const book = ref({});
      const router = useRouter();
      const route = useRoute();
      const form = ref(null);
      const errors = reactive({});
  
      const snackbar = ref(false);
      const snackbarMessage = ref('');
      const snackbarColor = ref('');
  
      const fetchBook = async () => {
        try {
          const response = await axios.get(`/api/books/${route.params.id}`);
          book.value = response.data;
        } catch (error) {
          snackbarMessage.value =
            'Failed to fetch book details: ' + (error.response?.data?.message || error.message);
          snackbarColor.value = 'error';
          snackbar.value = true;
          router.push('/librarian/books');
        }
      };
  
      const updateBook = async () => {
        // Clear previous errors
        Object.keys(errors).forEach((key) => {
          errors[key] = [];
        });
  
        if (form.value.validate()) {
          try {
            await axios.put(`/api/books/${route.params.id}`, {
              title: book.value.title,
              author: book.value.author,
              isbn: book.value.isbn,
              publisher: book.value.publisher,
              publication_year: book.value.publication_year,
              total_copies: book.value.total_copies,
              location: book.value.location,
            });
            snackbarMessage.value = 'Book updated successfully';
            snackbarColor.value = 'success';
            snackbar.value = true;
            setTimeout(() => {
              router.push('/librarian/books');
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
                'Failed to update book: ' + (error.response?.data?.message || error.message);
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
        router.push('/librarian/books');
      };
  
      onMounted(() => {
        fetchBook();
      });
  
      return {
        book,
        updateBook,
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
  