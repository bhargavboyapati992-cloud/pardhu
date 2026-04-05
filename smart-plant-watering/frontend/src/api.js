import axios from 'axios';

const API_URL = '/api';

export const getDashboardData = async () => {
    const response = await axios.get(`${API_URL}/dashboard`);
    return response.data;
};

export const toggleMode = async () => {
    const response = await axios.post(`${API_URL}/toggle-mode`);
    return response.data;
};

export const controlMotor = async (command) => {
    const response = await axios.post(`${API_URL}/motor-control`, { command });
    return response.data;
};
