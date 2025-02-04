import java.io.*;
import java.sql.*;
import java.util.Random;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/vulnerable")
public class app extends HttpServlet {

    // **1. Hardcoded Credentials**
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "password123"; // Hardcoded credentials
    private static final String DB_URL = "jdbc:mysql://localhost:3306/test_db";

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String action = request.getParameter("action");

        if ("cmd".equals(action)) {
            runCommand(request, response);
        } else if ("sql".equals(action)) {
            runSQLQuery(request, response);
        } else if ("file".equals(action)) {
            readFile(request, response);
        } else if ("token".equals(action)) {
            generateToken(response);
        }
    }

    // **2. Command Injection Vulnerability**
    private void runCommand(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String userInput = request.getParameter("cmd"); // User-controlled input
        Process process = Runtime.getRuntime().exec(userInput); // Vulnerable to command injection
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line;
        StringBuilder output = new StringBuilder();
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        response.getWriter().println(output.toString());
    }

    // **3. SQL Injection Vulnerability**
    private void runSQLQuery(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String userId = request.getParameter("id"); // Unsanitized user input
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             Statement stmt = conn.createStatement()) {

            String query = "SELECT * FROM users WHERE id = " + userId; // Vulnerable to SQL injection
            ResultSet rs = stmt.executeQuery(query);

            while (rs.next()) {
                response.getWriter().println("User: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            response.getWriter().println("Database error");
        }
    }

    // **4. Insecure File Handling (Path Traversal)**
    private void readFile(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String fileName = request.getParameter("file"); // User-controlled input
        File file = new File(fileName); // Possible Path Traversal vulnerability
        BufferedReader reader = new BufferedReader(new FileReader(file));
        String line;
        while ((line = reader.readLine()) != null) {
            response.getWriter().println(line);
        }
        reader.close();
    }

    // **5. Weak Cryptographic Randomness**
    private void generateToken(HttpServletResponse response) throws IOException {
        Random random = new Random();
        int token = random.nextInt(1000000); // Not cryptographically secure
        response.getWriter().println("Generated Token: " + token);
    }
}
