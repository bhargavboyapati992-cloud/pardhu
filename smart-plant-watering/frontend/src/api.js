import axios from 'axios';

const API_URL = '/api';

// --- MOCK FALLBACK STATE FOR DEMONSTRATIONS ---
let mockState = {
    is_on: true,
    mode: "Auto"
};

// Generate realistic looking rough demo values
const mockHistory = Array.from({ length: 20 }).map((_, i) => {
    let date = new Date();
    date.setMinutes(date.getMinutes() - (20 - i));
    const timeStr = date.toLocaleTimeString('en-US', { hour12: false });
    return {
        time: timeStr,
        moisture: Math.max(300, 950 - (i * 25) + (Math.random() * 30 - 15)).toFixed(1),
        temperature: (25 + Math.random() * 5).toFixed(1)
    };
});

const mockLogs = [
    { time: new Date().toLocaleTimeString('en-US', { hour12: false }), action: "ON", reason: "AI Prediction / Threshold" }
];

export const getDashboardData = async () => {
    try {
        const response = await axios.get(`${API_URL}/dashboard`, { timeout: 3500 }); // 3.5s timeout for demo
        return response.data;
    } catch (error) {
        console.warn("Backend asleep or unavailable. Presenting demo rough values.");
        return {
            motor_state: mockState,
            history: mockHistory,
            logs: mockLogs
        };
    }
};

export const toggleMode = async () => {
    try {
        const response = await axios.post(`${API_URL}/toggle-mode`, null, { timeout: 3500 });
        return response.data;
    } catch (error) {
        mockState.mode = mockState.mode === "Auto" ? "Manual" : "Auto";
        return { status: "success", mode: mockState.mode };
    }
};

export const controlMotor = async (command) => {
    try {
        const response = await axios.post(`${API_URL}/motor-control`, { command }, { timeout: 3500 });
        return response.data;
    } catch (error) {
        mockState.is_on = command === "ON";
        mockLogs.unshift({ 
            time: new Date().toLocaleTimeString('en-US', { hour12: false }), 
            action: command, 
            reason: "Manual Toggle (Demo)" 
        });
        return { status: "success", motor_state: mockState.is_on };
    }
};
