import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Droplet, Power, CheckCircle, AlertTriangle, Activity, Settings } from 'lucide-react';
import { getDashboardData, toggleMode, controlMotor } from './api';

function App() {
  const [data, setData] = useState({
    motor_state: { is_on: false, mode: 'Auto' },
    history: [],
    logs: []
  });

  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await getDashboardData();
      setData(res);
      setLoading(false);
    } catch (e) {
      console.error("Error fetching data", e);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000); // Poll every 3 seconds for real-time feel
    return () => clearInterval(interval);
  }, []);

  const handleToggleMode = async () => {
    await toggleMode();
    fetchData();
  };

  const handleMotorControl = async (cmd) => {
    await controlMotor(cmd);
    fetchData();
  };

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '1.5rem', color: '#8b5cf6' }}>Loading System Data...</div>;
  }

  const latestMoisture = data.history.length > 0 ? data.history[data.history.length - 1].moisture : 0;
  const isWet = latestMoisture > 600;

  return (
    <div>
      <div className="flex-between mb-1">
        <div>
          <h1 style={{ fontSize: '2.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Droplet color="#3b82f6" /> Smart Plant Monitor
          </h1>
          <p className="stat-label mt-1">AI-Powered IoT Dashboard</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div className={`status-indicator ${isWet ? 'status-wet' : 'status-dry'}`}>
            {isWet ? <CheckCircle size={16} /> : <AlertTriangle size={16} />}
            {isWet ? 'Soil is Wet' : 'Soil is Dry'}
          </div>
          <button className="btn btn-outline" onClick={handleToggleMode}>
            <Settings size={18} /> {data.motor_state.mode === 'Auto' ? 'Switch to Manual' : 'Switch to Auto'}
          </button>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* State Panel */}
        <div className="glass-panel">
          <h2 className="mb-1" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={20} color="#8b5cf6"/> Current Status
          </h2>
          <div className="flex-between mt-2">
            <div>
              <div className="stat-label">Soil Moisture</div>
              <div className="stat-value" style={{ color: isWet ? '#10b981' : '#ef4444' }}>
                {latestMoisture.toFixed(1)}
              </div>
            </div>
            <div>
              <div className="stat-label">System Mode</div>
              <div className="stat-value">{data.motor_state.mode}</div>
            </div>
          </div>
        </div>

        {/* Control Panel */}
        <div className="glass-panel">
          <h2 className="mb-1" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Power size={20} color="#3b82f6" /> Motor Control
          </h2>
          <div className="mt-2" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="flex-between">
              <span className="stat-label">Motor Status</span>
              <span className={`status-indicator ${data.motor_state.is_on ? 'status-wet' : 'status-dry'}`} style={{ fontSize: '1rem' }}>
                {data.motor_state.is_on ? 'RUNNING' : 'STOPPED'}
              </span>
            </div>
            
            {data.motor_state.mode === 'Manual' ? (
              <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
                <button 
                  className="btn btn-success" 
                  style={{ flex: 1, justifyContent: 'center' }}
                  onClick={() => handleMotorControl('ON')}
                  disabled={data.motor_state.is_on}
                >
                  Turn ON
                </button>
                <button 
                  className="btn btn-danger" 
                  style={{ flex: 1, justifyContent: 'center' }}
                  onClick={() => handleMotorControl('OFF')}
                  disabled={!data.motor_state.is_on}
                >
                  Turn OFF
                </button>
              </div>
            ) : (
              <div className="stat-label" style={{ textAlign: 'center', marginTop: '1rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                Mode is set to AUTO. The AI Engine controls the motor.
              </div>
            )}
          </div>
        </div>

        {/* Logs Panel */}
        <div className="glass-panel" style={{ maxHeight: '300px', overflowY: 'auto' }}>
          <h2 className="mb-1">Activity Logs</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {data.logs.length === 0 ? <p className="stat-label">No recent logs.</p> : null}
            {data.logs.map((log, i) => (
              <div key={i} style={{ padding: '0.75rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', borderLeft: `3px solid ${log.action === 'ON' ? '#10b981' : log.action === 'OFF' ? '#ef4444' : '#8b5cf6'}`}}>
                <div className="flex-between">
                  <strong>Motor: {log.action}</strong>
                  <span className="stat-label" style={{ fontSize: '0.7rem' }}>{log.time}</span>
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>{log.reason}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Graph Section */}
      <div className="glass-panel mt-2" style={{ height: '400px' }}>
        <h2 className="mb-1">Moisture History</h2>
        {data.history.length > 0 ? (
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={data.history}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} domain={[0, 1023]} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'rgba(30, 41, 59, 0.9)', border: 'none', borderRadius: '8px', color: '#fff' }}
                itemStyle={{ color: '#3b82f6' }}
              />
              <Line type="monotone" dataKey="moisture" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#0f172a', stroke: '#3b82f6', strokeWidth: 2 }} activeDot={{ r: 6 }} />
              <Line type="monotone" dataKey="temperature" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }} className="stat-label">
            Waiting for sensor data...
          </div>
        )}
      </div>

    </div>
  );
}

export default App;
