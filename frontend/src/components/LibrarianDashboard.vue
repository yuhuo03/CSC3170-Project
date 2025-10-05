<!-- src/components/LibrarianDashboard.vue -->
<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h2>Librarian Dashboard</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Total Books</v-card-title>
          <v-card-text>
            <v-icon color="primary" large>mdi-book</v-icon>
            <span class="headline">{{ reports.total_books }}</span>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Total Loans</v-card-title>
          <v-card-text>
            <v-icon color="primary" large>mdi-book-open</v-icon>
            <span class="headline">{{ reports.total_loans }}</span>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Total Fines Collected</v-card-title>
          <v-card-text>
            <v-icon color="primary" large>mdi-currency-usd</v-icon>
            <span class="headline">
              ${{ (reports.total_fines ?? 0).toFixed(2) }}
            </span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Overdue Loans -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Overdue Loans</v-card-title>
          <v-data-table :headers="overdueHeaders" :items="reports.overdue_loans" class="elevation-1">
            <template v-slot:[`item.user_name`]="{ item }">
              {{ item.user.name }}
            </template>
            <template v-slot:[`item.book_title`]="{ item }">
              {{ item.book_title }}
            </template>
            <template v-slot:[`item.due_date`]="{ item }">
              {{ formatDate(item.due_date) }}
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Unpaid Fines -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Unpaid Fines</v-card-title>
          <v-data-table :headers="fineHeaders" :items="reports.unpaid_fines" class="elevation-1">
            <template v-slot:[`item.user_name`]="{ item }">
              {{ item.user.name }}
            </template>
            <template v-slot:[`item.amount`]="{ item }">
              ${{ item.amount.toFixed(2) }}
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Most Popular Books -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Most Popular Books</v-card-title>
          <v-data-table :headers="popularBookHeaders" :items="reports.most_popular_books" class="elevation-1">
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Existing Buttons and Links -->
    <v-row>
      <v-col cols="12">
        <router-link to="/add-book">
          <v-btn color="primary">Add New Book</v-btn>
        </router-link>
        <router-link to="/librarian/books">
          <v-btn color="primary">Manage Books</v-btn>
        </router-link>
        <router-link to="/librarian/users">
          <v-btn color="primary">Manage Users</v-btn>
        </router-link>
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
import { ref, onMounted } from 'vue';
import axios from '../axios';

export default {
  name: 'LibrarianDashboard',
  setup() {
    const reports = ref({
      total_books: 0,
      total_loans: 0,
      total_fines: 0,
      overdue_loans: [],
      unpaid_fines: [],
      most_popular_books: [],
    });

    const snackbar = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const overdueHeaders = [
      { text: 'Loan ID', value: 'id' },
      { text: 'User', value: 'user_name' },
      { text: 'Book', value: 'book_title' },
      { text: 'Due Date', value: 'due_date' },
    ];

    const fineHeaders = [
      { text: 'Fine ID', value: 'id' },
      { text: 'User', value: 'user_name' },
      { text: 'Amount', value: 'amount' },
      { text: 'Description', value: 'description' },
    ];

    const popularBookHeaders = [
      { text: 'Book Title', value: 'title' },
      { text: 'Borrow Count', value: 'count' },
    ];

    const fetchReports = async () => {
      try {
        const response = await axios.get('/api/reports');
        reports.value = response.data;
      } catch (error) {
        snackbarMessage.value =
          'Failed to fetch reports: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const formatDate = (value) => {
      return new Date(value).toLocaleDateString();
    };

    onMounted(() => {
      fetchReports();
    });

    return {
      reports,
      overdueHeaders,
      fineHeaders,
      popularBookHeaders,
      formatDate,
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