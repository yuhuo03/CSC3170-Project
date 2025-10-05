<!-- src/components/ManageBooks.vue -->
<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h2>Manage Books</h2>
        <v-data-table
          :headers="headers"
          :items="books"
          :search="search"
          class="elevation-1"
        >
          <template #top>
            <v-toolbar flat>
              <v-toolbar-title>Book List</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-text-field
                v-model="search"
                label="Search"
                solo-inverted
                hide-details
              ></v-text-field>
            </v-toolbar>
          </template>

          <!-- Custom Actions Column -->
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editBook(item.id)">mdi-pencil</v-icon>
            <v-icon small @click="deleteBook(item.id)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Confirm Deletion</v-card-title>
        <v-card-text>Are you sure you want to delete this book?</v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import axios from '../axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'ManageBooks',
  setup() {
    const books = ref([]);
    const search = ref('');
    const headers = [
      { text: 'ID', value: 'id' },
      { text: 'Title', value: 'title' },
      { text: 'Author', value: 'author' },
      { text: 'ISBN', value: 'isbn' },
      { text: 'Available Copies', value: 'copies_available' },
      { text: 'Actions', value: 'actions', sortable: false },
    ];
    const router = useRouter();
    const dialog = ref(false);
    const bookIdToDelete = ref(null);

    const snackbar = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const fetchBooks = async () => {
      try {
        const response = await axios.get('/api/books');
        books.value = response.data;
      } catch (error) {
        snackbarMessage.value =
          'Failed to fetch books: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const editBook = (id) => {
      router.push(`/librarian/books/${id}/edit`);
    };

    const deleteBook = (id) => {
      bookIdToDelete.value = id;
      dialog.value = true;
    };

    const confirmDelete = async () => {
      try {
        await axios.delete(`/api/books/${bookIdToDelete.value}`);
        snackbarMessage.value = 'Book deleted successfully';
        snackbarColor.value = 'success';
        snackbar.value = true;
        dialog.value = false;
        fetchBooks();
      } catch (error) {
        snackbarMessage.value =
          'Failed to delete book: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
        dialog.value = false;
      }
    };

    onMounted(() => {
      fetchBooks();
    });

    return {
      books,
      search,
      headers,
      editBook,
      deleteBook,
      dialog,
      confirmDelete,
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
