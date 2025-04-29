# sql-ai-app

Overview

This project enables users to interact with a MySQL database using natural language queries, powered by the Gemini 1.5 Flash model. Instead of writing SQL queries, users can ask questions or give instructions in plain English, and the system will translate them into SQL, execute the queries, and return the results.

#Features





Natural Language Processing: Convert user inputs into SQL queries using Gemini 1.5 Flash.



MySQL Integration: Seamlessly connect to and interact with a MySQL database.



User-Friendly: No SQL knowledge required; interact with the database using everyday language.



Secure: Implements basic security measures to prevent SQL injection and unauthorized access.

Prerequisites





Python 3.8+



MySQL Server



Gemini 1.5 Flash API key



Required Python packages:





mysql-connector-python



google-generativeai



python-dotenv

Installation





Clone the Repository:

git clone https://github.com/aditya0589/sql-ai-app.git
cd sql-ai-app



Install Dependencies:

pip install -r requirements.txt



Set Up Environment Variables: Create a .env file in the project root and add the following:

GEMINI_API_KEY=your_gemini_api_key
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name



Configure MySQL: Ensure your MySQL server is running and the specified database exists.

Usage





Run the Application:

streamlit run app.py



Interact with the Database:





Enter natural language queries like:





"Show me all employees in the marketing department."



"Add a new product with name 'Widget' and price 19.99."



"Update the salary of John Doe to 75000."



The system will process the query, generate the appropriate SQL, execute it, and display the results.

#Example Queries





Retrieve Data: "List all customers who made purchases in 2023."



Insert Data: "Add a new employee named Jane Smith with a salary of 60000."



Update Data: "Change the price of item ID 123 to 29.99."



Delete Data: "Remove all orders older than 2 years."

Project Structure

ai-mysql-nl-interface/
├── main.py              # Entry point for the application
├── query_processor.py   # Handles natural language to SQL conversion
├── database.py          # Manages MySQL connections and query execution
├── .env                # Environment variables (not tracked)
├── requirements.txt     # Python dependencies
└── README.md           # This file

Limitations





The accuracy of SQL generation depends on the Gemini 1.5 Flash model's understanding of the query and database schema.



Complex queries with multiple joins or subqueries may require more precise phrasing.



Currently supports basic CRUD operations; advanced SQL features may not be fully supported.

#Future Improvements





Add support for more complex SQL queries (e.g., joins, aggregations).



Implement a feedback loop to improve query translation accuracy.



Add a web-based interface for easier interaction.



Enhance security with more robust input validation.

#Contributing

Contributions are welcome! Please follow these steps:





Fork the repository.



Create a new branch (git checkout -b feature/your-feature).



Commit your changes (git commit -m 'Add your feature').



Push to the branch (git push origin feature/your-feature).



Open a pull request.

#License

This project is licensed under the MIT License. See the LICENSE file for details.

#Contact

For questions or feedback, please contact yraditya895@gmail.com or open an issue on GitHub.
