import { Provider } from '@radix-ui/react-toast';
import axios from 'axios';
require('dotenv').config
async function axiosBase(url) {
    try {
      const response = await axios.get(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      // Assuming response.data is an array with a single object containing the string 'q'
      return response.data  // Extract the string you need here
    } catch (error) {
      console.error('Error fetching data:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Status:', error.response.status);
        console.error('Headers:', error.response.headers);
      }
      return "Error fetching data"; // Return a string on error
    }
  }

let url = "http://localhost:8000/"


axiosBase(url)
  .then(data => {
    if (data) {
      console.log('Received data:', data); // data is now a string
    } else {
      console.log('Failed to fetch data');
    }
  });
