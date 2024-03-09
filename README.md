# Rental Car Management System

## Introduction

This project is a Rental Car Management System (RCMS) designed to manage car rentals efficiently. It is built using Python and Streamlit, and connects to a MySQL database hosted on AWS RDS. The system provides an interactive web interface to perform various queries and operations on the rental database.

## Features

- **Database Selection**: Users can select the type of database they want to interact with (currently supports MySQL on AWS RDS).
- **Query Execution**: Users can execute predefined SQL queries to fetch information such as average rental duration, total revenue generated, customer rental details, etc.
- **Dynamic Query Execution**: Users can also run custom SQL queries directly through the interface.
- **Stored Procedures**: The system provides options to execute stored procedures for common tasks like calculating total revenue or fetching customer rental history.

## Setup

### Prerequisites

- Python 3.8 or higher
- Streamlit
- MySQL Connector for Python
- Extra Streamlit Components (optional for additional UI components)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/suryakailash-risk/Rental-Car.git
   ```

2. Navigate to the project directory:
   ```bash
   cd rental-car-management-system
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Update the database connection settings in the code to match your AWS RDS MySQL instance.

2. If you have any additional stored procedures or queries, add them to the `dictionarydata` variable in the code.

## Usage

To run the application, execute the following command in the terminal:

```bash
streamlit run streamlit_app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for any bugs or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

