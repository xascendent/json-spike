import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class TestSQLite {
    public static void main(String[] args) {
        String url = "jdbc:sqlite:./submission_queue.db";

        try (Connection conn = DriverManager.getConnection(url)) {
            if (conn != null) {
                System.out.println("Connection established to SQLite database.");
                
                // Create a test table
                Statement stmt = conn.createStatement();
                stmt.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)");
                System.out.println("Test table created successfully!");
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
