<template>
    <div class="register-container">
      <h2 class="register-title">Register</h2>
      <form @submit.prevent="register">
        <input type="text" v-model="username" placeholder="Username" required />
        <input type="email" v-model="email" placeholder="Email" required />
        <select v-model="role" required>
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
        <input type="password" v-model="password" placeholder="Password" required />
        <input type="password" v-model="password2" placeholder="Confirm Password" required />
        <button type="submit">Register</button>
      </form>

      <p v-if="successMessage" class="success">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>

  <script>
  import apiService from '@/services/apiService';

export default {
  data() {
    return {
      username: '',
      email: '',
      role: 'user',
      password: '',
      password2: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    async register() {
      try {
        const success = await apiService.register({
          username: this.username,
          email: this.email,
          role: this.role,
          password: this.password,
          password2: this.password2
        });

        if (success) {
          this.successMessage = 'Регистрация успешна! Перенаправление на вход...';
          setTimeout(() => this.$router.push('/login'), 2000);
        }
      } catch {
        this.errorMessage = 'Ошибка регистрации. Проверьте данные.';
      }
    }
  }
};
  </script>

  <style scoped>
.register-container {
    width: 100%;
  max-width: 400px;
  padding: 20px;
  border-radius: 10px;
  background: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.register-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

input, select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

button {
  background: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.success {
    color: green;
}
.error {
    color: red;
}
</style>