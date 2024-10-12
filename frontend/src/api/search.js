import axios from 'axios';


export async function fetchSearchResults(url) {
  try {
    const response = await axios.get(url);
    if (!response.data) {
      throw new Error("No data received from the API.");
    }
    return response.data; 
  } catch (error) {
    console.error("Error fetching search results:", error);
    // Handle error appropriately (e.g., display an error message)
    return []; // Return an empty array on error
  }
}

export async function fetchImage(imageUrl, onError) {
  try {
    const response = await axios.get(imageUrl, { responseType: 'blob' });
    if (!response.data) {
      console.error('No data received from the server.');
      if (typeof onError === 'function') {
        onError("No data received from the server.");
      }
      return null;  // Or throw an error if you prefer.
    }
    const blob = new Blob([response.data]);
    const url = URL.createObjectURL(blob);
    return url;
  } catch (error) {
    console.error('Error fetching image:', error);
    if (typeof onError === 'function') {
      onError(error.message); // Pass the error message to the onError callback
    }
    return null; // Or throw an error, depending on your error handling strategy.
  }
}
