# MetaTrader 5 Extension

A MT5 extension. This library extension extendsthe features of [MetaTrader5](https://pypi.org/project/MetaTrader5).

## Documentation

### Installation

To install the MetaTrader 5 Adapter, follow these steps:

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

### Usage

To run the MetaTrader 5 Extension, execute the following commands:

```bash
cd examples
```

```bash
cp .env.example .env
```

```bash
python ./examples/mt5_client.py
```

**NOTE:** Make sure to configure the .env file properly before running the script or the docker image.

### Project Structure

The project structure is organized as follows:

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.LICENSE file for details.
