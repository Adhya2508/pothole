import axios from "axios";

const api = axios.create({
  baseURL: "https://wf78nddt67.execute-api.ap-south-1.amazonaws.com/prod",
});

export default api;