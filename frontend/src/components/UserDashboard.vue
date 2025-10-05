<!-- src/components/UserDashboard.vue -->
<template>
  <v-container fluid>
    <v-parallax :src="require('@/assets/background.png')" height="100%">
      <v-row class="fill-height" align="center" justify="center">
        <v-col cols="12" md="10">
          <!-- Welcome Banner -->
          <v-card elevation="8" class="mb-6">
            <v-card-title class="headline">
              <v-icon large class="mr-3">mdi-account-circle</v-icon>
              Welcome back, {{ user.name }}!
            </v-card-title>
            <v-card-subtitle>
              Here's a summary of your account activities.
            </v-card-subtitle>
          </v-card>

          <!-- User Loans and Fines -->
          <v-row>
            <!-- Loans Card -->
            <v-col cols="12" md="6">
              <v-card elevation="4">
                <v-card-title>
                  <v-icon class="mr-2">mdi-book-open-variant</v-icon>
                  Your Loans
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list v-if="loans.length">
                    <v-list-item v-for="loan in loans" :key="loan.id">
                      <v-list-item-content>
                        <v-list-item-title>{{ loan.book_title }}</v-list-item-title>
                        <v-list-item-subtitle>
                          Due: {{ formatDate(loan.due_date) }}
                        </v-list-item-subtitle>
                        <v-progress-linear
                          :value="calculateDuePercentage(loan.due_date)"
                          height="7"
                          color="primary"
                          class="mt-2"
                        ></v-progress-linear>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn color="primary" @click="returnBook(loan.id)">Return</v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list>
                  <v-alert type="info" v-else>
                    You have no current loans.
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Fines Card -->
            <v-col cols="12" md="6">
              <v-card elevation="4">
                <v-card-title>
                  <v-icon class="mr-2">mdi-cash-multiple</v-icon>
                  Your Fines
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list v-if="fines.length">
                    <v-list-item v-for="fine in fines" :key="fine.id">
                      <v-list-item-content>
                        <v-list-item-title>{{ fine.description }}</v-list-item-title>
                        <v-list-item-subtitle>
                          Amount: ${{ fine.amount.toFixed(2) }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn color="secondary" @click="payFine(fine.id)" v-if="!fine.paid">Pay</v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list>
                  <v-alert type="success" v-else>
                    You have no unpaid fines.
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Search Books Button -->
          <v-row class="mt-6" justify="center">
            <v-btn color="primary" large @click="goToSearch">
              <v-icon left>mdi-magnify</v-icon>
              Search Books
            </v-btn>
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
  name: 'UserDashboard',
  setup() {
    const user = ref({});
    const loans = ref([]);
    const fines = ref([]);
    const router = useRouter();

    const snackbar = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const fetchDashboard = async () => {
      try {
        const response = await axios.get('/api/dashboard');
        user.value = response.data.user;
        loans.value = response.data.loans;
        fines.value = response.data.fines;
      } catch (error) {
        snackbarMessage.value =
          'Failed to fetch dashboard: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const formatDate = (value) => {
      return new Date(value).toLocaleDateString();
    };

    const returnBook = async (loanId) => {
      try {
        await axios.post(`/api/return/${loanId}`);
        snackbarMessage.value = 'Book returned successfully';
        snackbarColor.value = 'success';
        snackbar.value = true;
        fetchDashboard();
      } catch (error) {
        snackbarMessage.value =
          'Failed to return book: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const payFine = async (fineId) => {
      try {
        await axios.post(`/api/payfine/${fineId}`);
        snackbarMessage.value = 'Fine paid successfully';
        snackbarColor.value = 'success';
        snackbar.value = true;
        fetchDashboard();
      } catch (error) {
        snackbarMessage.value =
          'Failed to pay fine: ' + (error.response?.data?.message || error.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    };

    const calculateDuePercentage = (dueDate) => {
      const now = new Date();
      const due = new Date(dueDate);
      const totalTime = due - now;
      const elapsed = now - new Date(user.value.loan_date);
      const percentage = (elapsed / totalTime) * 100;
      return Math.min(Math.max(percentage, 0), 100);
    };

    const goToSearch = () => {
      router.push('/search');
    };

    onMounted(() => {
      fetchDashboard();
    });

    return {
      user,
      loans,
      fines,
      formatDate,
      returnBook,
      payFine,
      calculateDuePercentage,
      goToSearch,
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

.v-icon {
  color: #1976d2;
}

.v-btn {
  text-transform: none;
}
</style>
