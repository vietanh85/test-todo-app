const axios = require('axios');
const api = axios.create({ baseURL: '/' });
console.log(api.getUri({ url: '/todos' }));
console.log(api.getUri({ url: 'todos' }));
