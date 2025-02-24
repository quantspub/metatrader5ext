# MetaTrader 5 Extension 🚀

A powerful extension for MetaTrader 5 that enhances its functionality, enabling advanced trading and market analysis tools. 🛠️

This extension enhances the MetaTrader 5 Python package, introducing advanced tools for trading and market analysis. It simplifies complex tasks such as order management, data retrieval, and strategy automation, while enabling features like custom indicators, advanced charting, and seamless API integrations. Compatible with MetaTrader 5, it supports efficient trading operations and data-driven decision-making for traders and developers alike.

## Installation ⚙️
To install the MetaTrader 5 Extension, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/quantspub/metatrader5ext.git
   ```

2. Navigate to the project directory:
   ```sh
   cd ./metatrader5ext
   ```

3. Install the required Python packages:
   ```sh
   poetry install
   ```

## Usage 🖥️
To run the MetaTrader 5 Extension, execute the following commands:

```sh
cd examples
cp .env.example .env
python ./examples/mt5_client.py
```

**NOTE:** Make sure to configure the `.env` file properly before running the script or the Docker image. ⚠️

## Features ✨
This extension is divided into two parts:

### **MetaTrader5 Module 📦**
- The standard MetaTrader 5 Python module.
- For Linux users, it requires connecting to a Python environment inside Wine using `rpyc`. 🐧
- Provides direct access to MT5's API for trading and data retrieval.

### **EA Module 🤖**
- Enables communication with MetaTrader 5 via sockets.
- Includes a pre-compiled MQL5 server named `MT5Ext.mq5` located in the **Experts** folder within the MQL5 directory. 📂
- Simply attach the server to an MT5 chart to facilitate seamless communication between any client written in any language of choice (e.g., Python, JavaScript, or C++) and MT5. 🌐
- Perfect for building custom trading systems and integrating with external applications. 🔗

## Project Structure 🗂️
The project is organized as follows:

```
metatrader5ext/
├── examples/          # Example scripts for usage
├── metatrader5ext/    # Source code for the extension
├── tests/             # Test cases
├── MQL5/              # MQL5 scripts and EA module
├── docs/              # Documentation files
├── pyproject.toml     # Poetry configuration
├── poetry.lock        # Dependency lock file
├── build.py           # Build script
├── .gitignore         # Git ignore file
├── LICENSE            # License file
├── README.md          # Project documentation
```

## Contributing 🤝
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes. 🐛

1. Fork the repository. 🍴
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes. ✏️
4. Commit your changes:
   ```sh
   git commit -m 'Add some feature'
   ```
5. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
6. Open a pull request. 📥

## License 📄
This project is licensed under the MIT License. See the `LICENSE` file for details.

This extension empowers traders and developers to optimize workflows, automate strategies, and build custom trading solutions. Whether you're a beginner or an expert, it expands the capabilities of the MetaTrader 5 ecosystem, making it a must-have tool for advanced trading automation and analysis. 🚀📈
