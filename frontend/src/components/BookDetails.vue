<!-- src/components/BookDetails.vue -->
<template>
  <v-container fluid>
    <v-parallax :src="require('@/assets/background.png')" height="100%">
      <v-row class="fill-height" align="center" justify="center">
        <v-col cols="12" md="8">
          <v-card elevation="8" class="pa-5">
            <v-row>
              <!-- Book Cover Image -->
              <v-col cols="12" md="4">
                <v-img
                  :src="book.image || require('@/assets/book-placeholder.jpg')"
                  height="300px"
                  class="rounded-lg"
                ></v-img>
              </v-col>

              <!-- Book Details -->
              <v-col cols="12" md="8">
                <v-card-title class="headline">{{ book.title }}</v-card-title>
                <v-card-subtitle class="mb-3">
                  by {{ book.author }}
                </v-card-subtitle>

                <v-divider class="mb-3"></v-divider>

                <v-list dense>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>ISBN</v-list-item-title>
                      <v-list-item-subtitle>{{ book.isbn }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Publisher</v-list-item-title>
                      <v-list-item-subtitle>{{ book.publisher }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Publication Year</v-list-item-title>
                      <v-list-item-subtitle>{{ book.publication_year }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Available Copies</v-list-item-title>
                      <v-list-item-subtitle>{{ book.copies_available }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Location</v-list-item-title>
                      <v-list-item-subtitle>{{ book.location }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>

                <!-- Action Buttons -->
                <v-card-actions class="mt-4">
                  <v-btn
                    color="primary"
                    large
                    @click="borrowBook"
                    :disabled="book.copies_available === 0"
                  >
                    <v-icon left>mdi-book</v-icon>
                    Borrow Book
                  </v-btn>
                  <v-btn
                    color="secondary"
                    large
                    @click="placeHold"
                  >
                    <v-icon left>mdi-bookmark-plus</v-icon>
                    Place Hold
                  </v-btn>
                  <v-btn
                    text
                    large
                    @click="goBack"
                  >
                    <v-icon left>mdi-arrow-left</v-icon>
                    Back to Search
                  </v-btn>
                </v-card-actions>
              </v-col>
            </v-row>
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
    </v-parallax>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from '../axios';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'BookDetails',
  setup() {
    const book = ref({});
    const route = useRoute();
    const router = useRouter();

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
      }
    };

    const borrowBook = async () => {
      try {
        await axios.post(`/api/borrow/${book.value.id}`);
        snackbarMessage.value = 'Book borrowed successfully';
        snackbarColor.value = 'success';
        snackbar.value = true;
        fetchBook();
      } catch (error) {
        snackbarMessage.value =
          'Failed to borrow book: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const placeHold = async () => {
      try {
        await axios.post(`/api/hold/${book.value.id}`);
        snackbarMessage.value = 'Hold placed successfully';
        snackbarColor.value = 'success';
        snackbar.value = true;
      } catch (error) {
        snackbarMessage.value =
          'Failed to place hold: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const goBack = () => {
      router.push('/search');
    };

    onMounted(() => {
      fetchBook();
    });

    return {
      book,
      borrowBook,
      placeHold,
      goBack,
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

.v-card {
  border-radius: 12px;
}

.v-img {
  border-radius: 12px;
}

.v-card-title,
.v-card-subtitle {
  padding-left: 0;
}

.v-list-item-title {
  font-weight: bold;
}

.v-btn {
  text-transform: none;
}

.pa-5 {
  padding: 32px !important;
}
</style>
