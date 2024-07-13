# network-agent

This repository contains the source code for a secure network agent that collects system and network activity data on Linux. The agent is designed to provide comprehensive monitoring and visualization of system metrics, including CPU usage, memory usage, disk usage, network statistics, and active connections.

## Features

- Collects system and network activity data every 60 seconds.
- Secure data transmission with HMAC authentication.
- Customizable configuration system.
- Detailed error logging.
- Timestamped JSON files for each data collection cycle.
- CVE detection based on open ports and services.

## Setup

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kasinadhsarma/network-agent.git
   cd network-agent/network-agent-backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set the `SECRET_KEY` environment variable for HMAC authentication:
   ```bash
   export SECRET_KEY="your_secret_key"
   ```

4. Run the network agent:
   ```bash
   python network_agent.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../network-agent-ui/frontend
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Build the production version:
   ```bash
   npm run build
   ```

5. Deploy to Netlify:
   - Create a new site on Netlify.
   - Drag and drop the contents of the `build` folder into the Netlify site dashboard.
   - Follow the instructions to complete the deployment.

## Frontend UI

The frontend UI for visualizing the collected data is developed using React and Chakra UI. The UI provides an intuitive dashboard with responsive line charts for CPU usage, memory usage, and network traffic.

### Accessing the Frontend UI

The frontend UI is deployed on Netlify and can be accessed at the following URL:
[Frontend UI on Netlify](http://your-netlify-url)

## Security Measures

- HMAC authentication is used to ensure secure data transmission.
- Best practices for error handling and secure data transmission are followed.
- Timestamped JSON files prevent data overwrites and ensure data integrity.

## CVE Detection

The network agent includes a CVE detection feature that retrieves and displays the CVE count for each detected service based on open ports. The CVE database is parsed and matched with the services to provide relevant security information.

## Prerequisites

- Python 3.6 or higher
- Node.js and npm (for frontend development)
- Internet connection for accessing external resources

## Generating a Secure SECRET_KEY

To generate a secure `SECRET_KEY` for HMAC authentication, you can use the following Python script:

```python
import secrets

def generate_secret_key(length=32):
    return secrets.token_hex(length)

print(generate_secret_key())
```

Run this script to generate a secure `SECRET_KEY` and set it as an environment variable.

## Troubleshooting

- Ensure all dependencies are installed correctly.
- Verify that the `SECRET_KEY` environment variable is set.
- Check the logs for detailed error messages if the network agent fails to run.
- For frontend issues, ensure the development server is running and accessible.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
