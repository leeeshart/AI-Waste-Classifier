const API_BASE = "http://localhost:5000";

/**
 * Classify an uploaded image file
 * @param {File} file - The image file to classify
 * @returns {Promise<Object>} - Parsed JSON response with label, confidence, and tip
 */
export const classifyImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE}/classify-image`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error classifying image:", error);
    throw error;
  }
};

/**
 * Classify text description of an object
 * @param {string} text - The text description to classify
 * @returns {Promise<Object>} - Parsed JSON response with label, confidence, and tip
 */
export const classifyText = async (text) => {
  try {
    const response = await fetch(`${API_BASE}/classify-text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error classifying text:", error);
    throw error;
  }
};
