<template>
    <div class="admin-container">
      <h2>Admin Panel</h2>
      <button class="logout-btn" @click="logout">Logout</button>

      <table class="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.description }}</td>
            <td>
              <button class="delete-btn" @click="deleteItem(item.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>
  import apiService from '@/services/apiService';

export default {
  data() {
    return {
      items: []
    };
  },
  async mounted() {
    this.items = await apiService.fetchItems();
  },
  methods: {
    async deleteItem(id) {
      await apiService.deleteItem(id);
      this.items = this.items.filter(item => item.id !== id);
    },
    logout() {
      apiService.logout();
      this.$router.push('/login');
    }
  }
};

  </script>

  <style scoped>
  .admin-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    background: #fff;
    text-align: center;
  }

  .logout-btn {
    background-color: red;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    margin-bottom: 10px;
  }

  .admin-table {
    width: 100%;
    border-collapse: collapse;
  }

  .admin-table th, .admin-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  .admin-table th {
    background-color: #f4f4f4;
  }

  .delete-btn {
    background-color: red;
    color: white;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
  }
</style>