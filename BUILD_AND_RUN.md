# CBS - Build & Run Guide

Complete guide to build and run the Core Banking System locally and with Docker.

## Quick Start (Docker Compose - Recommended)

### Prerequisites
- Docker (v20+)
- Docker Compose (v2+)

### Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/lukasokal/cbs_mockup.git
   cd cbs_mockup
   ```

2. **Build All Services**
   ```bash
   # Option A: Using Maven
   mvn clean package -DskipTests
   
   # Option B: Build Docker images directly
   docker-compose build
   ```

3. **Start All Services**
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**
   - **Frontend**: http://localhost:3000 (React UI)
   - **API Gateway**: http://localhost:8080 (Request entry point)
   - **Kafka UI**: You can use Kafka tools to monitor topics

5. **Stop Services**
   ```bash
   docker-compose down
   ```

6. **View Logs**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f api-gateway
   docker-compose logs -f account-service
   docker-compose logs -f payment-service
   ```

---

## Manual Setup (Local Development)

### Prerequisites
- Java 17+ JDK
- Maven 3.8+
- Node.js 18+ with npm
- Git
- Apache Kafka (local or Docker)

### Step 1: Start Kafka & Zookeeper

**Option A: Using Docker**
```bash
docker-compose up -d kafka zookeeper
```

**Option B: Local Installation**
- Download from https://kafka.apache.org/
- Follow installation guide for your OS

Verify Kafka is running:
```bash
# Test connection
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

### Step 2: Build Maven Projects

```bash
# Navigate to project root
cd cbs_mockup

# Clean and build all modules
mvn clean install -DskipTests

# If you want to run tests as well:
# mvn clean install
```

Build output:
- `cbs-core/target/cbs-core-1.0.0.jar`
- `cbs-api-gateway/target/cbs-api-gateway-1.0.0.jar`
- `cbs-account-service/target/cbs-account-service-1.0.0.jar`
- `cbs-payment-service/target/cbs-payment-service-1.0.0.jar`

### Step 3: Start Backend Services

**Terminal 1: API Gateway (Port 8080)**
```bash
cd cbs-api-gateway
mvn spring-boot:run

# Or run JAR directly:
java -jar target/cbs-api-gateway-1.0.0.jar
```

**Terminal 2: Account Service (Port 8081)**
```bash
cd cbs-account-service
mvn spring-boot:run

# Or:
java -jar target/cbs-account-service-1.0.0.jar
```

**Terminal 3: Payment Service (Port 8082)**
```bash
cd cbs-payment-service
mvn spring-boot:run

# Or:
java -jar target/cbs-payment-service-1.0.0.jar
```

### Step 4: Start Frontend (React)

**Terminal 4: React Frontend (Port 3000)**
```bash
cd cbs-frontend

# Install dependencies
npm install

# Start development server
npm start
```

The browser will automatically open at http://localhost:3000

### Step 5: Verify All Services are Running

```bash
# Check API Gateway
curl http://localhost:8080/api/auth/health

# Check Account Service
curl http://localhost:8081/api/accounts/health

# Check Payment Service
curl http://localhost:8082/api/payments/health

# Check Frontend
curl http://localhost:3000
```

---

## Testing the System

### 1. Create an Account

```bash
curl -X POST http://localhost:8080/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "CUST001",
    "accountType": "CURRENT",
    "currency": "EUR",
    "balance": 1000.00,
    "iban": "SK9212345678901234567890",
    "bic": "FIOBSKBAXXX"
  }'
```

Response:
```json
{
  "code": 200,
  "message": "Account created successfully",
  "data": {
    "accountId": "550e8400-e29b-41d4-a716-446655440000",
    "customerId": "CUST001",
    "accountType": "CURRENT",
    "currency": "EUR",
    "balance": 1000.00,
    "status": "ACTIVE",
    ...
  }
}
```

### 2. Get Account Details

```bash
curl http://localhost:8080/api/accounts/{accountId}
```

### 3. Create a Payment

```bash
curl -X POST http://localhost:8080/api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "initiatorAccountId": "ACC001",
    "beneficiaryIban": "DE89370400440532013000",
    "beneficiaryName": "John Doe",
    "amount": 500.00,
    "currency": "EUR",
    "paymentType": "SEPA_SCT",
    "remittanceInformation": "Invoice #123"
  }'
```

### 4. Check Kafka Topics

List all topics:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Monitor payment events:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic payment-events --from-beginning
```

---

## Environment Configuration

### API Gateway (Port 8080)
`application.yml`:
```yaml
server:
  port: 8080
spring:
  application:
    name: api-gateway
  kafka:
    bootstrap-servers: localhost:9092
```

### Account Service (Port 8081)
`application.yml`:
```yaml
server:
  port: 8081
spring:
  datasource:
    url: jdbc:h2:mem:accountdb
  kafka:
    bootstrap-servers: localhost:9092
```

### Payment Service (Port 8082)
`application.yml`:
```yaml
server:
  port: 8082
spring:
  datasource:
    url: jdbc:h2:mem:paymentdb
  kafka:
    bootstrap-servers: localhost:9092
```

### Frontend
`.env`:
```
REACT_APP_API_URL=http://localhost:8080
```

---

## Troubleshooting

### Issue: Kafka Connection Failed

**Error:**
```
java.lang.Exception: org.apache.kafka.common.errors.BrokerNotAvailableException: 
All brokers are down: [BrokerNotAvailable]
```

**Solution:**
1. Verify Kafka is running:
   ```bash
   docker ps | grep kafka
   # or
   jps | grep Kafka
   ```
2. Check Kafka port:
   ```bash
   netstat -an | grep 9092
   ```
3. Restart Kafka:
   ```bash
   docker-compose restart kafka
   ```

### Issue: Port Already in Use

**Error:**
```
Address already in use: bind
```

**Solution:**
1. Find process using the port:
   ```bash
   lsof -i :8080  # For API Gateway
   lsof -i :8081  # For Account Service
   lsof -i :8082  # For Payment Service
   lsof -i :3000  # For Frontend
   ```
2. Kill the process:
   ```bash
   kill -9 <PID>
   ```
3. Or change the port in `application.yml`

### Issue: Maven Build Fails

**Error:**
```
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin
```

**Solution:**
1. Check Java version:
   ```bash
   java -version  # Should be 17+
   ```
2. Clean and rebuild:
   ```bash
   mvn clean verify
   ```

### Issue: React Frontend Not Loading

**Error:**
```
Cannot GET /
```

**Solution:**
1. Verify React server is running:
   ```bash
   curl http://localhost:3000
   ```
2. Check logs:
   ```bash
   # In the frontend terminal
   npm start
   ```
3. Rebuild frontend:
   ```bash
   cd cbs-frontend
   rm -rf node_modules
   npm install
   npm start
   ```

### Issue: CORS Errors

**Error:**
```
Access to XMLHttpRequest at 'http://localhost:8080/api/...' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
Verify API Gateway CORS configuration in `GatewayConfig.java`:
```java
.corsConfigurations:
  '[/**]':
    allowedOrigins: "*"
    allowedMethods: [GET, POST, PUT, DELETE, OPTIONS]
```

---

## Performance Testing

### Load Test Account Creation

```bash
# Using Apache Bench (ab)
ab -n 1000 -c 10 -p account.json \
  -T application/json \
  http://localhost:8080/api/accounts
```

### Monitor Service Performance

1. **Check memory usage:**
   ```bash
   docker stats
   ```

2. **Monitor Kafka broker:**
   ```bash
   kafka-broker-api-versions.sh --bootstrap-server localhost:9092
   ```

3. **View service logs:**
   ```bash
   docker-compose logs --tail=50 -f account-service
   ```

---

## Production Deployment

### Prerequisites
- Kubernetes cluster (or Docker Swarm)
- PostgreSQL database
- External Kafka cluster
- SSL certificates

### Deployment Steps

1. **Update Configuration**
   - Replace H2 with PostgreSQL
   - Configure external Kafka brokers
   - Set secure JWT secrets

2. **Build Docker Images**
   ```bash
   docker build -t myregistry/cbs-api-gateway:1.0.0 cbs-api-gateway/
   docker build -t myregistry/cbs-account-service:1.0.0 cbs-account-service/
   docker build -t myregistry/cbs-payment-service:1.0.0 cbs-payment-service/
   ```

3. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

See `docs/DEPLOYMENT.md` for detailed production deployment.

---

## Useful Commands

### Maven Commands
```bash
# Build without tests
mvn clean package -DskipTests

# Run single module
mvn -pl cbs-api-gateway spring-boot:run

# Check dependencies
mvn dependency:tree
```

### Docker Commands
```bash
# View running services
docker-compose ps

# View detailed logs
docker-compose logs -f --tail=100

# Rebuild specific service
docker-compose build account-service

# Remove all containers
docker-compose down -v
```

### Kafka Commands
```bash
# List topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Create topic
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1

# Monitor topic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic payment-events --from-beginning
```

---

## Next Steps

1. Review [API Documentation](../docs/API.md)
2. Explore [Database Schema](../docs/DATABASE.md)
3. Check [Development Guide](../docs/DEVELOPMENT.md)
4. Deploy to [Production](../docs/DEPLOYMENT.md)

---

For issues or questions, please create a GitHub issue or check the main README.md.
