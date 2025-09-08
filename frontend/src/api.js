import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const predictText = async (text) => {
  const formData = new FormData();
  formData.append("text", text);
  const response = await axios.post(`${BASE_URL}/predict-text`, formData);
  return response.data;
};

export const predictImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${BASE_URL}/predict-image`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

