import unittest
from openquery.sql_ast import AST

class TestSqlAST(unittest.TestCase):

    def test_is_query(self):
        self.assertTrue(AST("SELECT * FROM A").is_query())
        self.assertFalse(AST("INSERT INTO A (b, c, d) VALUES ('foo', 'bar', 'baz')").is_query())
        self.assertTrue(AST("""
            SELECT x, y, z
            FROM table_one JOIN table_two ON table_one.a = table_two.b
            WHERE x > 5 AND y < 3
        """).is_query())
        self.assertFalse(AST("INSERT INTO A SELECT * FROM users").is_query())
        self.assertFalse(AST("""
            INSERT INTO agent1
            SELECT * FROM  agents
            WHERE agent_code=ANY(
                SELECT agent_code FROM customer
                WHERE cust_country="UK"
            )
        """).is_query())
        self.assertFalse(AST("DROP TABLE Shippers").is_query())
        self.assertFalse(AST("TRUNCATE TABLE table_name").is_query())
        self.assertFalse(AST("""
            ALTER TABLE Customers
            ADD Email varchar(255)
        """).is_query())
        self.assertFalse(AST("""
            ALTER TABLE Customers
            DROP COLUMN Email
        """).is_query())
        self.assertFalse(AST("""
            CREATE TABLE Persons (
                PersonID int,
                LastName varchar(255),
                FirstName varchar(255),
                Address varchar(255),
                City varchar(255)
            );
        """).is_query())
        self.assertFalse(AST("""
            UPDATE Customers
            SET ContactName = 'Alfred Schmidt', City= 'Frankfurt'
            WHERE CustomerID = 1;
        """).is_query())
        self.assertFalse(AST("""
            DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';
        """).is_query())
