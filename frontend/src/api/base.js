import axios from 'axios';

export async function fetchBase(url) {
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