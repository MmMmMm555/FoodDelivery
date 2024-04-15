# Starter

project beginner repo

Certainly! Here's a more comprehensive list covering a wider range of PostgreSQL queries:

1. **SELECT Statement**:

   - Retrieve data from a table.

   ```sql
   SELECT * FROM table_name;
   ```

2. **WHERE Clause**:

   - Filter data based on a condition.

   ```sql
   SELECT * FROM table_name WHERE condition;
   ```

3. **ORDER BY Clause**:

   - Sort the result set.

   ```sql
   SELECT * FROM table_name ORDER BY column_name [ASC|DESC];
   ```

4. **LIMIT Clause**:

   - Limit the number of rows returned.

   ```sql
   SELECT * FROM table_name LIMIT count;
   ```

5. **OFFSET Clause**:

   - Skip a specified number of rows before returning the result set.

   ```sql
   SELECT * FROM table_name OFFSET count;
   ```

6. **INSERT Statement**:

   - Add a new row to a table.

   ```sql
   INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...);
   ```

7. **UPDATE Statement**:

   - Modify existing records in a table.

   ```sql
   UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
   ```

8. **DELETE Statement**:

   - Remove records from a table.

   ```sql
   DELETE FROM table_name WHERE condition;
   ```

9. **JOIN Clause**:

   - Combine rows from two or more tables based on a related column.

   ```sql
   SELECT * FROM table1 INNER JOIN table2 ON table1.column = table2.column;
   ```

10. **LEFT JOIN Clause**:

    - Return all rows from the left table and matching rows from the right table.

    ```sql
    SELECT * FROM table1 LEFT JOIN table2 ON table1.column = table2.column;
    ```

11. **RIGHT JOIN Clause**:

    - Return all rows from the right table and matching rows from the left table.

    ```sql
    SELECT * FROM table1 RIGHT JOIN table2 ON table1.column = table2.column;
    ```

12. **FULL OUTER JOIN Clause**:

    - Return all rows when there is a match in either left or right table.

    ```sql
    SELECT * FROM table1 FULL OUTER JOIN table2 ON table1.column = table2.column;
    ```

13. **UNION Operator**:

    - Combine the result sets of two or more SELECT statements.

    ```sql
    SELECT * FROM table1
    UNION
    SELECT * FROM table2;
    ```

14. **GROUP BY Clause**:

    - Group rows that have the same values into summary rows.

    ```sql
    SELECT column1, aggregate_function(column2) FROM table_name GROUP BY column1;
    ```

15. **HAVING Clause**:

    - Filter groups based on a condition.

    ```sql
    SELECT column1, aggregate_function(column2) FROM table_name GROUP BY column1 HAVING condition;
    ```

16. **Subquery**:

    - A query nested inside another query.

    ```sql
    SELECT column1 FROM table_name WHERE column2 IN (SELECT column2 FROM another_table);
    ```

These are the main SQL queries used in PostgreSQL, covering selection, insertion, updating, deletion, joins, aggregation, and subqueries.

###################################################################
###################################################################
###################################################################
###################################################################
###################################################################

Sure, here's a list of Docker and Docker Compose commands with explanations for Windows Terminal:

**Docker Commands:**

1. **docker version**:

   - Displays the Docker version installed on your system.

   ```bash
   docker version
   ```

2. **docker info**:

   - Provides detailed information about Docker installation, including containers, images, and storage drivers.

   ```bash
   docker info
   ```

3. **docker pull**:

   - Downloads a Docker image from a registry (e.g., Docker Hub).

   ```bash
   docker pull image_name
   ```

4. **docker images**:

   - Lists all Docker images downloaded or created on your system.

   ```bash
   docker images
   ```

5. **docker run**:

   - Creates and starts a Docker container based on a specified image.

   ```bash
   docker run image_name
   ```

6. **docker ps**:

   - Lists all running Docker containers.

   ```bash
   docker ps
   ```

7. **docker ps -a**:

   - Lists all Docker containers, including those that are stopped.

   ```bash
   docker ps -a
   ```

8. **docker stop**:

   - Stops a running Docker container.

   ```bash
   docker stop container_id
   ```

9. **docker start**:

   - Starts a stopped Docker container.

   ```bash
   docker start container_id
   ```

10. **docker rm**:

    - Deletes a Docker container.

    ```bash
    docker rm container_id
    ```

11. **docker rmi**:

    - Deletes a Docker image.

    ```bash
    docker rmi image_name
    ```

12. **docker exec**:

    - Runs a command inside a running Docker container.

    ```bash
    docker exec -it container_id command
    ```

13. **docker build**:
    - Builds a Docker image from a Dockerfile.
    ```bash
    docker build -t image_name .
    ```

**Docker Compose Commands:**

1. **docker-compose version**:

   - Displays the Docker Compose version installed on your system.

   ```bash
   docker-compose version
   ```

2. **docker-compose up**:

   - Builds, (re)creates, starts, and attaches to containers for a service defined in the docker-compose.yml file.

   ```bash
   docker-compose up
   ```

3. **docker-compose down**:

   - Stops and removes containers, networks, volumes, and images created by up.

   ```bash
   docker-compose down
   ```

4. **docker-compose ps**:

   - Lists containers used by the Compose.

   ```bash
   docker-compose ps
   ```

5. **docker-compose logs**:

   - Displays log output from services defined in the docker-compose.yml file.

   ```bash
   docker-compose logs
   ```

6. **docker-compose build**:

   - Builds or rebuilds services defined in the docker-compose.yml file.

   ```bash
   docker-compose build
   ```

7. **docker-compose exec**:

   - Runs a command in a running service container.

   ```bash
   docker-compose exec service_name command
   ```

8. **docker-compose stop**:

   - Stops services defined in the docker-compose.yml file.

   ```bash
   docker-compose stop
   ```

9. **docker-compose start**:

   - Starts services defined in the docker-compose.yml file.

   ```bash
   docker-compose start
   ```

10. **docker-compose restart**:
    - Restarts services defined in the docker-compose.yml file.
    ```bash
    docker-compose restart
    ```

These commands should help you manage your Docker containers and services effectively using Windows Terminal.
