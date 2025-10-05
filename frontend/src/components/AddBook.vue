<!-- src/components/AddBook.vue -->
<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="headline">Add New Book</v-card-title>
          <v-card-text>
            <v-form ref="form" @submit.prevent="addBook">
              <v-text-field
                v-model="title"
                label="Title"
                :error-messages="errors.title"
                @input="clearError('title')"
                required
              ></v-text-field>
              <v-text-field
                v-model="author"
                label="Author"
                :error-messages="errors.author"
                @input="clearError('author')"
                required
              ></v-text-field>
              <v-text-field
                v-model="isbn"
                label="ISBN"
                :error-messages="errors.isbn"
                @input="clearError('isbn')"
                required
              ></v-text-field>
              <v-text-field
                v-model="publisher"
                label="Publisher"
                :error-messages="errors.publisher"
                @input="clearError('publisher')"
                required
              ></v-text-field>
              <v-text-field
                v-model="publication_year"
                label="Publication Year"
                type="number"
                :error-messages="errors.publication_year"
                @input="clearError('publication_year')"
                required
              ></v-text-field>
              <v-text-field
                v-model="total_copies"
                label="Total Copies"
                type="number"
                :error-messages="errors.total_copies"
                @input="clearError('total_copies')"
                required
              ></v-text-field>
              <v-text-field
                v-model="location"
                label="Location"
                :error-messages="errors.location"
                @input="clearError('location')"
                required
              ></v-text-field>
              <v-card-actions>
                <v-btn color="primary" @click="addBook">Add Book</v-btn>
                <router-link to="/librarian">
                  <v-btn text>Back to Dashboard</v-btn>
                </router-link>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

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
import axios from '../axios';
import { useRouter } from 'vue-router';

export default {
  name: 'AddBook',
  setup() {
    const title = ref('');
    const author = ref('');
    const isbn = ref('');
    const publisher = ref('');
    const publication_year = ref('');
    const total_copies = ref('');
    const location = ref('');
    const form = ref(null);
    const router = useRouter();

    const errors = reactive({});

    // Snackbar state
    const snackbar = ref(false);
    const snackbarMessage = ref('');

    const addBook = async () => {
      // Clear previous errors
      Object.keys(errors).forEach((key) => {
        errors[key] = [];
      });

      if (form.value.validate()) {
        try {
          const response = await axios.post('/api/books', {
            title: title.value,
            author: author.value,
            isbn: isbn.value,
            publisher: publisher.value,
            publication_year: publication_year.value,
            total_copies: total_copies.value,
            location: location.value,
          });

          if (response && response.data) {
            // Show success message in Snackbar
            snackbarMessage.value = 'Book added successfully';
            snackbar.value = true;

            // Redirect after a short delay
            setTimeout(() => {
              router.push('/librarian');
            }, 1500);
          } else {
            snackbarMessage.value = 'Failed to add book: No response from server';
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
            snackbarMessage.value = 'Failed to add book: ' + error.response.data.message;
            snackbar.value = true;
          } else {
            snackbarMessage.value = 'Failed to add book: ' + error.message;
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
      title,
      author,
      isbn,
      publisher,
      publication_year,
      total_copies,
      location,
      form,
      addBook,
      errors,
      clearError,
      snackbar,
      snackbarMessage,
    };
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
