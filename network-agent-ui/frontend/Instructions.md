# Full Instructions for React Frontend UI

## 1. Project Setup

1. Ensure you have Node.js and npm installed on your system.
2. Open a terminal and create a new React app:
   ```
   npx create-react-app network-agent-ui
   ```
3. Navigate to the project directory:
   ```
   cd network-agent-ui
   ```
4. Install necessary dependencies:
   ```
   npm install recharts lucide-react tailwindcss@latest postcss@latest autoprefixer@latest
   ```
5. Set up Tailwind CSS:
   - Run: `npx tailwindcss init -p`
   - Open the generated `tailwind.config.js` and replace the content array with:
     ```javascript
     content: [
       "./src/**/*.{js,jsx,ts,tsx}",
     ],
     ```
   - Open `src/index.css` and add these lines at the top:
     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

## 2. Replace App.js Content

Replace the entire content of `src/App.js` with the code provided in the previous message.

## 3. Code Explanation

### Imports
```javascript
import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Cpu, HardDrive, Wifi } from 'lucide-react';
```
- We import necessary React hooks and components from recharts for data visualization.
- Icons are imported from lucide-react.

### Constants
```javascript
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
```
- This array defines colors used in charts.

### DashboardCard Component
```javascript
const DashboardCard = ({ title, icon, children }) => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <div className="flex items-center mb-4">
      {icon}
      <h2 className="text-xl font-semibold ml-2">{title}</h2>
    </div>
    {children}
  </div>
);
```
- This is a reusable component for each dashboard card.
- It takes a title, an icon, and children components as props.

### App Component
```javascript
const App = () => {
  // ... (state and useEffect code)

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">Network Agent Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {/* DashboardCard components */}
      </div>
    </div>
  );
};
```
- This is the main component of our application.
- It uses a grid layout to organize the dashboard cards.

### State Management
```javascript
const [systemData, setSystemData] = useState({
  cpu: [],
  memory: [],
  network: [],
  diskUsage: [
    { name: 'Used', value: 300 },
    { name: 'Free', value: 700 },
  ],
  topProcesses: [
    { name: 'Process 1', cpu: 30 },
    { name: 'Process 2', cpu: 25 },
    { name: 'Process 3', cpu: 20 },
    { name: 'Process 4', cpu: 15 },
    { name: 'Process 5', cpu: 10 },
  ],
});
```
- We use the `useState` hook to manage our application's state.
- The state includes arrays for CPU, memory, and network data, as well as disk usage and top processes.

### Data Fetching Simulation
```javascript
useEffect(() => {
  const fetchData = () => {
    // Simulating real-time data updates
    const newData = {
      ...systemData,
      cpu: [...systemData.cpu, { time: new Date().toLocaleTimeString(), usage: Math.random() * 100 }].slice(-10),
      memory: [...systemData.memory, { time: new Date().toLocaleTimeString(), usage: Math.random() * 100 }].slice(-10),
      network: [...systemData.network, { time: new Date().toLocaleTimeString(), traffic: Math.random() * 1000 }].slice(-10),
    };
    setSystemData(newData);
  };

  const interval = setInterval(fetchData, 2000);
  return () => clearInterval(interval);
}, [systemData]);
```
- The `useEffect` hook is used to simulate real-time data updates.
- It updates the state every 2 seconds with new random data.
- In a real application, you would replace this with actual API calls to your backend.

### Chart Components
Each `DashboardCard` contains a different type of chart:
- Line charts for CPU, Memory, and Network data
- Pie chart for Disk Usage
- Bar chart for Top Processes

Each chart is wrapped in a `ResponsiveContainer` to ensure it resizes properly.

## 4. Running the Application

After setting everything up, you can run the application with:
```
npm start
```

This will start the development server and open the application in your default web browser.

## 5. Next Steps

1. Replace the simulated data in the `useEffect` hook with real API calls to your backend.
2. Add more interactivity, such as the ability to select different time ranges for the data.
3. Implement authentication if required for your application.
4. Add more detailed views or drill-down capabilities for each metric.
5. Optimize performance, especially if dealing with large amounts of real-time data.