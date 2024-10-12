require('dotenv').config()

import { fetchPostData } from './src/api/search.js';
// Example usage:
const url = provess.env.BACKEND_URL
const postData = await fetchPostData(url);

if (postData) {
console.log('Received data:', postData);
} else {
console.log('Failed to fetch data');
}