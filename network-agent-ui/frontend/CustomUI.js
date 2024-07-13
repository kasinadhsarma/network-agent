// First, ensure you have Node.js and npm installed, then create a new React app:
// npx create-react-app network-agent-ui
// cd network-agent-ui

// In your src/App.js file:
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const App = () => {
  const [systemData, setSystemData] = useState({
    cpu: [],
    memory: [],
    network: []
  });

  useEffect(() => {
    // In a real application, you'd fetch data from your backend here
    const fetchData = () => {
      // This is mock data. Replace with actual API calls to your backend.
      const newData = {
        cpu: [...systemData.cpu, { time: new Date().toLocaleTimeString(), usage: Math.random() * 100 }].slice(-10),
        memory: [...systemData.memory, { time: new Date().toLocaleTimeString(), usage: Math.random() * 100 }].slice(-10),
        network: [...systemData.network, { time: new Date().toLocaleTimeString(), traffic: Math.random() * 1000 }].slice(-10)
      };
      setSystemData(newData);
    };

    const interval = setInterval(fetchData, 2000); // Update every 2 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, [systemData]);

  return (
    <div className="App">
      <h1>Network Agent Dashboard</h1>
      <div className="chart-container">
        <h2>CPU Usage</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={systemData.cpu}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="usage" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="chart-container">
        <h2>Memory Usage</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={systemData.memory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="usage" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="chart-container">
        <h2>Network Traffic</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={systemData.network}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="traffic" stroke="#ffc658" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default App;

// In your src/index.css file, add some basic styling:
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.App {
  padding: 20px;
}

.chart-container {
  margin-bottom: 30px;
}

// To run the app:
// npm start