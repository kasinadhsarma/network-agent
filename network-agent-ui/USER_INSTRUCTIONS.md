# User Instructions for Network Agent Frontend UI

## Overview
The Network Agent Frontend UI is a web-based interface designed to visualize system and network activity data collected by the network agent. This guide will help you understand how to access and use the dashboard to monitor your system's performance.

## Prerequisites
- Ensure that the backend server is running and accessible at `http://localhost:8000/latest.json`.
- The frontend server should be running on port 3001.

## Accessing the Dashboard
1. Open your web browser.
2. Navigate to `http://localhost:3001` to access the Network Agent Dashboard.

## Features
The dashboard provides real-time visualizations of the following metrics:
- **CPU Usage**: Displays the CPU usage over time.
- **Memory Usage**: Shows the memory usage over time.
- **Network Traffic**: Visualizes the network traffic (bytes sent and received) over time.

## Using the Dashboard
- The dashboard will automatically fetch and update the data every 60 seconds.
- If the data fetch is successful, the charts will be updated with the latest data points.
- If there is an error fetching the data, an error message will be displayed.

## Troubleshooting
- **Error Fetching Data**: If you see an error message indicating that data fetching failed, ensure that the backend server is running and accessible at `http://localhost:8000/latest.json`.
- **No Data Displayed**: If no data is displayed on the charts, check the browser console for any error messages and verify that the backend server is providing the correct data format.

## Additional Information
- The frontend UI is built using React and Chakra UI.
- The data is fetched using the `axios` library.
- The charts are created using the `recharts` library.

For more detailed information about the network agent and its setup, please refer to the main `README.md` file in the repository.

## Contact
If you encounter any issues or have any questions, please contact the project maintainer.

Enjoy monitoring your system with the Network Agent Dashboard!
