<!-- src/components/SearchBooks.vue -->
<template>
  <v-container fluid>
    <v-parallax :src="require('@/assets/background.png')" height="100%">
      <v-row class="fill-height" align="center" justify="center">
        <v-col cols="12" md="8">
          <!-- Search Field -->
          <v-text-field
            v-model="query"
            label="Search for books by title or author"
            @input="searchBooks"
            append-icon="mdi-magnify"
            clearable
            outlined
            dense
            class="mt-5"
          ></v-text-field>

          <!-- Books List -->
          <v-row>
            <v-col
              v-for="book in books"
              :key="book.id"
              cols="12"
              sm="6"
              md="4"
              class="d-flex"
            >
              <v-hover v-slot="{ hover }">
                <v-card
                  :elevation="hover ? 12 : 4"
                  class="ma-3"
                  @click="viewBookDetails(book.id)"
                >
                  <v-img
                    :src="book.image || require('@/assets/book-placeholder.jpg')"
                    height="200px"
                  ></v-img>
                  <v-card-title class="text-truncate">{{ book.title }}</v-card-title>
                  <v-card-subtitle class="text-truncate">
                    {{ book.author }}
                  </v-card-subtitle>
                  <v-card-actions>
                    <v-btn text color="primary">View Details</v-btn>
                  </v-card-actions>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Snackbar Component -->
      <v-snackbar v-model="snackbar" :timeout="3000" top right :color="snackbarColor">
        {{ snackbarMessage }}
        <template v-slot:action="{ attrs }">
          <v-btn text v-bind="attrs" @click="snackbar = false">Close</v-btn>
        </template>
      </v-snackbar>
    </v-parallax>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from '../axios';
import { useRouter } from 'vue-router';

export default {
  name: 'SearchBooks',
  setup() {
    const query = ref('');
    const books = ref([]);
    const router = useRouter();

    const snackbar = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const searchBooks = async () => {
      try {
        const response = await axios.get('/api/books', {
          params: { search: query.value },
        });
        books.value = response.data;
      } catch (error) {
        snackbarMessage.value =
          'Failed to fetch books: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const viewBookDetails = (bookId) => {
      router.push(`/book/${bookId}`);
    };

    onMounted(() => {
      searchBooks();
    });

    return {
      query,
      books,
      searchBooks,
      viewBookDetails,
      snackbar,
      snackbarMessage,
      snackbarColor,
    };
  },
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.v-text-field {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
}

.v-card {
  border-radius: 12px;
  cursor: pointer;
}

.v-card-title,
.v-card-subtitle {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ma-3 {
  margin: 16px !important;
}
</style>
