const axios = require('axios');
console.log(axios.getUri({ baseURL: 'https://foo.com', url: '/todos' }));
console.log(axios.getUri({ baseURL: 'https://foo.com/api/v1', url: '/todos' }));
