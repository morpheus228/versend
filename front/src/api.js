import axios from 'axios';

// Клиент для обычных API с префиксом /api
const apiClient = axios.create({
  baseURL: 'http://213.171.14.159:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Клиент для авторизации без /api
const authClient = axios.create({
  baseURL: 'http://213.171.14.159:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor для токена
const attachToken = (config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

apiClient.interceptors.request.use(attachToken);
authClient.interceptors.request.use(attachToken);

// Response interceptor для ошибок
apiClient.interceptors.response.use(
  (res) => res,
  (err) => Promise.reject(err)
);

authClient.interceptors.response.use(
  (res) => res,
  (err) => Promise.reject(err)
);

export const api = {
  // обычные ресурсы
  getAccounts: () => apiClient.get('/accounts'),
  createAccount: (payload) => apiClient.post('/accounts', payload),

  getCampaigns: () => apiClient.get('/campaigns'),
  createCampaign: (payload) => apiClient.post('/campaigns', payload),
  getCampaign: (id) => apiClient.get(`/campaigns/${id}`),

  getDialog: (id) => apiClient.get(`/dialogs/${id}`),

  // авторизация
  login: ({ username, password }) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return authClient.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },

  register: (payload) => authClient.post('/auth/register', payload),
};
