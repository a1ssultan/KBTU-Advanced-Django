<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="login-form">
      <input v-model="username" placeholder="Username" required class="input-field" />
      <input v-model="password" type="password" placeholder="Password" required class="input-field" />
      <button type="submit" class="login-button">Login</button>
    </form>

    <!-- Уведомления -->
    <p v-if="success" class="success-message">{{ success }}</p>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import apiService from '@/services/apiService';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      success: ''
    };
  },
  methods: {
    async login() {
      try {
        await apiService.login(this.username, this.password);
        this.success = 'Вход выполнен успешно!';
        setTimeout(() => this.$router.push('/'), 1500);
      } catch {
        this.error = 'Ошибка входа. Проверьте логин и пароль.';
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  background: #fff;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

.login-button:hover {
  background: #0056b3;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>