const axios = require('axios');
console.log(axios.getUri({ baseURL: './', url: '/todos' }));
console.log(axios.getUri({ baseURL: './', url: 'todos' }));
