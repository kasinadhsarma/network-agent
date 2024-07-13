import React, { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  VStack,
  Spinner,
  Alert,
  AlertIcon,
  theme,
} from '@chakra-ui/react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

function App() {
  const [systemData, setSystemData] = useState({
    cpu: [],
    memory: [],
    network: [],
    disk: [],
    load: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const formatTime = () => new Date().toLocaleTimeString();

  const calculateNetworkTraffic = (data) => data.network_info.bytes_sent + data.network_info.bytes_recv;

  const limitDataPoints = (data) => {
    if (data.length > 60) data.shift();
    return data;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        // Placeholder for backend server URL
        const backendServerUrl = 'http://localhost:8000/latest.json'; // Update this URL for production
        const response = await axios.get(backendServerUrl);
        console.log('Fetched data:', response.data); // Log the fetched data
        setSystemData(prevData => {
          const newData = {
            cpu: response.data.data.cpu_usage !== undefined ? limitDataPoints([...prevData.cpu, { time: formatTime(), usage: response.data.data.cpu_usage }]) : prevData.cpu,
            memory: response.data.data.memory_info && response.data.data.memory_info.used !== undefined ? limitDataPoints([...prevData.memory, { time: formatTime(), usage: response.data.data.memory_info.used }]) : prevData.memory,
            network: response.data.data.network_info ? limitDataPoints([...prevData.network, { time: formatTime(), traffic: calculateNetworkTraffic(response.data.data) }]) : prevData.network,
            disk: response.data.data.disk_usage && response.data.data.disk_usage.used !== undefined ? limitDataPoints([...prevData.disk, { time: formatTime(), usage: response.data.data.disk_usage.used }]) : prevData.disk,
            load: response.data.data.load_avg && response.data.data.load_avg.length >= 3 ? limitDataPoints([...prevData.load, { time: formatTime(), load1: response.data.data.load_avg[0], load5: response.data.data.load_avg[1], load15: response.data.data.load_avg[2] }]) : prevData.load
          };
          console.log('Processed data:', newData); // Log the processed data
          return newData;
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to fetch data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    const intervalId = setInterval(fetchData, 60000); // Fetch data every 60 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <VStack spacing={8}>
          <Text fontSize="2xl" fontWeight="bold">Network Agent Dashboard</Text>
          {loading && <Spinner size="xl" />}
          {error && (
            <Alert status="error">
              <AlertIcon />
              {error}
            </Alert>
          )}
          {!loading && !error && (
            <>
              <div className="chart-container">
                <Text fontSize="xl" fontWeight="bold">CPU Usage</Text>
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
                <Text fontSize="xl" fontWeight="bold">Memory Usage</Text>
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
                <Text fontSize="xl" fontWeight="bold">Network Traffic</Text>
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
              <div className="chart-container">
                <Text fontSize="xl" fontWeight="bold">Disk Usage</Text>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={systemData.disk}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="usage" stroke="#ff7300" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="chart-container">
                <Text fontSize="xl" fontWeight="bold">System Load</Text>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={systemData.load}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis label={{ value: 'Load Average', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value, name) => [`${value}`, `${name} (1, 5, 15 min)`]} />
                    <Legend verticalAlign="top" height={36} />
                    <Line type="monotone" dataKey="load1" stroke="#387908" name="1 min" />
                    <Line type="monotone" dataKey="load5" stroke="#ff7300" name="5 min" />
                    <Line type="monotone" dataKey="load15" stroke="#8884d8" name="15 min" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </>
          )}
        </VStack>
      </Box>
    </ChakraProvider>
  );
}

export default App;
