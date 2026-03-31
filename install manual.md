# CBS Installation Manual (Azure)

This guide shows how to run the CBS system on Microsoft Azure using a Linux VM and Docker Compose.

## 1. Architecture Used in This Manual

- 1 Azure Linux VM (Ubuntu 22.04 LTS or newer)
- Docker Engine + Docker Compose plugin
- All CBS containers started with `docker compose up`
- Public access to ports:
  - `3000` (Frontend)
  - `8080` (API Gateway)

## 2. Azure Resources and Capacity Planning

Use this sizing as a practical baseline for this repository.

| Environment | Compute Nodes | VM Size | Per-VM Capacity | Recommended Use |
|---|---:|---|---|---|
| Dev / Demo | 1 VM | Standard_D4s_v5 | 4 vCPU, 16 GiB RAM | Team demos, functional testing |
| Staging | 2 VMs | Standard_D4s_v5 | 4 vCPU, 16 GiB RAM each | UAT, pre-production validation |
| Production (small) | 3 VMs | Standard_D8s_v5 | 8 vCPU, 32 GiB RAM each | Initial live traffic with HA |

Recommended Azure resource types:

- Compute: Azure Virtual Machines (Ubuntu)
- Network: Virtual Network, subnets, Network Security Group (NSG)
- Load balancing: Standard Load Balancer (L4)
- Public access: Standard Public IP (Static)
- Storage: Premium SSD managed disks (P20 or higher for production)
- Monitoring: Log Analytics workspace + Azure Monitor

Minimum production-oriented layout:

- 1 Resource Group
- 1 VNet
- 2 subnets (`app-subnet`, `mgmt-subnet`)
- 1 NSG attached to `app-subnet`
- 1 Standard Public IP
- 1 Standard Load Balancer
- 3 application VMs in backend pool

## 3. Prerequisites

- Azure subscription
- Azure CLI installed locally
- SSH key pair available (`~/.ssh/id_rsa.pub`)
- Git installed locally

Login to Azure:

```bash
az login
az account show
```

## 4. Create Azure Resource Group

Choose your own names and region:

```bash
export RG_NAME="rg-cbs-dev"
export LOCATION="westeurope"

az group create \
  --name "$RG_NAME" \
  --location "$LOCATION"
```

## 5. Setup Networking (VNet, Subnets, NSG)

Create dedicated network resources before VM creation.

```bash
export VNET_NAME="vnet-cbs-dev"
export APP_SUBNET="app-subnet"
export MGMT_SUBNET="mgmt-subnet"
export NSG_NAME="nsg-cbs-app"

az network vnet create \
  --resource-group "$RG_NAME" \
  --name "$VNET_NAME" \
  --address-prefixes "10.20.0.0/16" \
  --subnet-name "$APP_SUBNET" \
  --subnet-prefixes "10.20.1.0/24"

az network vnet subnet create \
  --resource-group "$RG_NAME" \
  --vnet-name "$VNET_NAME" \
  --name "$MGMT_SUBNET" \
  --address-prefixes "10.20.2.0/24"

az network nsg create \
  --resource-group "$RG_NAME" \
  --name "$NSG_NAME"

# SSH (restrict source for production)
az network nsg rule create \
  --resource-group "$RG_NAME" \
  --nsg-name "$NSG_NAME" \
  --name "Allow-SSH" \
  --priority 100 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 22

# Frontend
az network nsg rule create \
  --resource-group "$RG_NAME" \
  --nsg-name "$NSG_NAME" \
  --name "Allow-Frontend-3000" \
  --priority 110 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 3000

# API Gateway
az network nsg rule create \
  --resource-group "$RG_NAME" \
  --nsg-name "$NSG_NAME" \
  --name "Allow-API-8080" \
  --priority 120 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 8080

az network vnet subnet update \
  --resource-group "$RG_NAME" \
  --vnet-name "$VNET_NAME" \
  --name "$APP_SUBNET" \
  --network-security-group "$NSG_NAME"
```

## 6. Create Linux VM

Create an Ubuntu VM and open SSH (22), Frontend (3000), and API Gateway (8080):

```bash
export VM_NAME="vm-cbs-dev"
export ADMIN_USER="azureuser"

az vm create \
  --resource-group "$RG_NAME" \
  --name "$VM_NAME" \
  --image "Ubuntu2204" \
  --admin-username "$ADMIN_USER" \
  --authentication-type ssh \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --size "Standard_D4s_v5" \
  --vnet-name "$VNET_NAME" \
  --subnet "$APP_SUBNET"

az vm open-port --resource-group "$RG_NAME" --name "$VM_NAME" --port 22
az vm open-port --resource-group "$RG_NAME" --name "$VM_NAME" --port 3000
az vm open-port --resource-group "$RG_NAME" --name "$VM_NAME" --port 8080
```

Get VM public IP:

```bash
export VM_IP=$(az vm show -d -g "$RG_NAME" -n "$VM_NAME" --query publicIps -o tsv)
echo "$VM_IP"
```

Create additional VMs for higher-capacity environments:

```bash
# Staging: create VM #2 (same size as primary)
az vm create \
  --resource-group "$RG_NAME" \
  --name "vm-cbs-stg-2" \
  --image "Ubuntu2204" \
  --admin-username "$ADMIN_USER" \
  --authentication-type ssh \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --size "Standard_D4s_v5" \
  --vnet-name "$VNET_NAME" \
  --subnet "$APP_SUBNET"

# Production small: create VM #2 and VM #3 with larger size
az vm create \
  --resource-group "$RG_NAME" \
  --name "vm-cbs-prd-2" \
  --image "Ubuntu2204" \
  --admin-username "$ADMIN_USER" \
  --authentication-type ssh \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --size "Standard_D8s_v5" \
  --vnet-name "$VNET_NAME" \
  --subnet "$APP_SUBNET"

az vm create \
  --resource-group "$RG_NAME" \
  --name "vm-cbs-prd-3" \
  --image "Ubuntu2204" \
  --admin-username "$ADMIN_USER" \
  --authentication-type ssh \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --size "Standard_D8s_v5" \
  --vnet-name "$VNET_NAME" \
  --subnet "$APP_SUBNET"
```

For each extra VM, attach its NIC to the load balancer backend pool using the same method shown in Section 7.

## 7. Setup Load Balancer (Networking + HA Ready)

For production/staging, route traffic through a Standard Load Balancer.

```bash
export PIP_NAME="pip-cbs-lb"
export LB_NAME="lb-cbs"
export FE_NAME="fe-cbs"
export BE_NAME="be-cbs"

az network public-ip create \
  --resource-group "$RG_NAME" \
  --name "$PIP_NAME" \
  --sku Standard \
  --allocation-method Static

az network lb create \
  --resource-group "$RG_NAME" \
  --name "$LB_NAME" \
  --sku Standard \
  --public-ip-address "$PIP_NAME" \
  --frontend-ip-name "$FE_NAME" \
  --backend-pool-name "$BE_NAME"

# Health probes
az network lb probe create \
  --resource-group "$RG_NAME" \
  --lb-name "$LB_NAME" \
  --name "probe-3000" \
  --protocol Tcp \
  --port 3000

az network lb probe create \
  --resource-group "$RG_NAME" \
  --lb-name "$LB_NAME" \
  --name "probe-8080" \
  --protocol Tcp \
  --port 8080

# Load balancer rules
az network lb rule create \
  --resource-group "$RG_NAME" \
  --lb-name "$LB_NAME" \
  --name "rule-frontend-3000" \
  --protocol Tcp \
  --frontend-port 3000 \
  --backend-port 3000 \
  --frontend-ip-name "$FE_NAME" \
  --backend-pool-name "$BE_NAME" \
  --probe-name "probe-3000"

az network lb rule create \
  --resource-group "$RG_NAME" \
  --lb-name "$LB_NAME" \
  --name "rule-api-8080" \
  --protocol Tcp \
  --frontend-port 8080 \
  --backend-port 8080 \
  --frontend-ip-name "$FE_NAME" \
  --backend-pool-name "$BE_NAME" \
  --probe-name "probe-8080"

# Attach VM NIC to backend pool
VM_NIC_ID=$(az vm show -g "$RG_NAME" -n "$VM_NAME" --query "networkProfile.networkInterfaces[0].id" -o tsv)
VM_NIC_NAME=$(basename "$VM_NIC_ID")

az network nic ip-config address-pool add \
  --resource-group "$RG_NAME" \
  --nic-name "$VM_NIC_NAME" \
  --ip-config-name ipconfig1 \
  --lb-name "$LB_NAME" \
  --address-pool "$BE_NAME"

export LB_IP=$(az network public-ip show -g "$RG_NAME" -n "$PIP_NAME" --query ipAddress -o tsv)
echo "$LB_IP"
```

If using 2 or 3 VMs, repeat the NIC attachment step for each VM.

## 8. Connect to VM and Install Dependencies

SSH into the VM:

```bash
ssh "$ADMIN_USER@$VM_IP"
```

Install Docker Engine and Docker Compose plugin:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git

sudo usermod -aG docker "$USER"
newgrp docker

docker --version
docker compose version
```

## 9. Clone Repository on VM

```bash
git clone https://github.com/lukasokal/cbs_mockup.git
cd cbs_mockup
```

## 10. Run CBS with Docker Compose

Start all services:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Follow logs if needed:

```bash
docker compose logs -f
```

## 11. Validate Deployment

From your local machine (or from VM), verify:

```bash
curl "http://$VM_IP:8080/api/auth/health"
curl "http://$VM_IP:8081/api/accounts/health"
curl "http://$VM_IP:8082/api/payments/health"

# If load balancer is configured, validate via LB endpoint:
curl "http://$LB_IP:8080/api/auth/health"
```

Open in browser:

- Frontend: `http://<VM_PUBLIC_IP>:3000`
- API Gateway: `http://<VM_PUBLIC_IP>:8080`
- Frontend through LB: `http://<LB_PUBLIC_IP>:3000`
- API through LB: `http://<LB_PUBLIC_IP>:8080`

## 12. Operational Commands

Restart all services:

```bash
docker compose restart
```

Stop all services:

```bash
docker compose down
```

Stop and remove images/volumes:

```bash
docker compose down --rmi local --volumes
```

## 13. Troubleshooting

### Containers do not start

```bash
docker compose ps
docker compose logs --tail 200
```

### Port already in use

```bash
sudo lsof -i :3000
sudo lsof -i :8080
sudo lsof -i :8081
sudo lsof -i :8082
```

### Load balancer has no healthy backend

```bash
az network lb show -g "$RG_NAME" -n "$LB_NAME" --query "provisioningState"
az network nic ip-config list -g "$RG_NAME" --nic-name "$VM_NIC_NAME"
```

Check that:

- Docker services are running on backend VM(s)
- LB probe ports (3000 and 8080) are open in NSG
- VM NICs are added to LB backend pool

### Frontend reachable but backend not reachable

- Confirm port 8080 is open in NSG (`az vm open-port ... --port 8080`)
- Confirm API Gateway container is healthy (`docker compose ps`)
- Confirm `REACT_APP_API_URL` points to the gateway endpoint

## 14. Optional: Secure for Non-Dev Use

For staging/production, add:

- HTTPS termination (Nginx or Azure Application Gateway)
- DNS record for stable hostname
- Secrets management (Azure Key Vault)
- Managed database instead of in-memory H2
- Monitoring with Azure Monitor / Log Analytics

For higher security, place only ports 80/443 on the public side and move 3000/8080 to private endpoints behind reverse proxy.

## 15. Alternative Production Architecture: VMSS + Application Gateway (TLS 443)

Use this option when you need autoscaling and TLS termination at the edge.

### 15.1 Recommended Resources and Capacity

| Tier | VMSS Instance Size | Min Instances | Default Instances | Max Instances | Gateway SKU / Capacity |
|---|---|---:|---:|---:|---|
| Staging | Standard_D4s_v5 | 2 | 2 | 4 | WAF_v2 / 1 |
| Production (small) | Standard_D8s_v5 | 3 | 3 | 8 | WAF_v2 / 2 |
| Production (medium) | Standard_D8s_v5 | 4 | 6 | 12 | WAF_v2 / 3 |

Resources created in this pattern:

- 1 VM Scale Set in `app-subnet`
- 1 dedicated subnet for Application Gateway (`appgw-subnet`)
- 1 Public IP for Application Gateway
- 1 Application Gateway WAF_v2 listener on 443
- 1 autoscale policy for VMSS

### 15.2 Create Dedicated Application Gateway Subnet

```bash
export APPGW_SUBNET="appgw-subnet"

az network vnet subnet create \
  --resource-group "$RG_NAME" \
  --vnet-name "$VNET_NAME" \
  --name "$APPGW_SUBNET" \
  --address-prefixes "10.20.3.0/24"
```

### 15.3 Create VM Scale Set (Backend Compute Pool)

```bash
export VMSS_NAME="vmss-cbs-app"

az vmss create \
  --resource-group "$RG_NAME" \
  --name "$VMSS_NAME" \
  --image "Ubuntu2204" \
  --admin-username "$ADMIN_USER" \
  --authentication-type ssh \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --instance-count 3 \
  --vm-sku "Standard_D8s_v5" \
  --orchestration-mode Uniform \
  --upgrade-policy-mode Rolling \
  --vnet-name "$VNET_NAME" \
  --subnet "$APP_SUBNET" \
  --public-ip-address ""
```

Note: Deploy your CBS containers on VMSS instances using cloud-init or a custom image so each instance runs API Gateway and required services.

### 15.4 Create Public IP and Application Gateway with TLS Listener

```bash
export APPGW_NAME="agw-cbs"
export APPGW_PIP="pip-cbs-agw"

az network public-ip create \
  --resource-group "$RG_NAME" \
  --name "$APPGW_PIP" \
  --sku Standard \
  --allocation-method Static

# Create gateway (initial HTTP backend settings on 8080)
az network application-gateway create \
  --resource-group "$RG_NAME" \
  --name "$APPGW_NAME" \
  --location "$LOCATION" \
  --sku WAF_v2 \
  --capacity 2 \
  --vnet-name "$VNET_NAME" \
  --subnet "$APPGW_SUBNET" \
  --public-ip-address "$APPGW_PIP" \
  --frontend-port 443 \
  --http-settings-protocol Http \
  --http-settings-port 8080 \
  --routing-rule-type Basic
```

### 15.5 Upload TLS Certificate and Bind HTTPS Listener

```bash
export PFX_PATH="/path/to/certificate.pfx"
export PFX_PASSWORD="<strong-password>"

az network application-gateway ssl-cert create \
  --resource-group "$RG_NAME" \
  --gateway-name "$APPGW_NAME" \
  --name "cbs-ssl-cert" \
  --cert-file "$PFX_PATH" \
  --cert-password "$PFX_PASSWORD"

az network application-gateway http-listener create \
  --resource-group "$RG_NAME" \
  --gateway-name "$APPGW_NAME" \
  --name "listener-https" \
  --frontend-port "appGatewayFrontendPort" \
  --frontend-ip "appGatewayFrontendIP" \
  --ssl-cert "cbs-ssl-cert"
```

### 15.6 Configure Backend Pool and Health Probe

```bash
# Collect current VMSS instance private IPs and set them as backend targets
VMSS_IPS=$(az vmss nic list \
  --resource-group "$RG_NAME" \
  --vmss-name "$VMSS_NAME" \
  --query "[].ipConfigurations[0].privateIpAddress" -o tsv | xargs)

az network application-gateway address-pool update \
  --resource-group "$RG_NAME" \
  --gateway-name "$APPGW_NAME" \
  --name "appGatewayBackendPool" \
  --servers $VMSS_IPS

az network application-gateway probe create \
  --resource-group "$RG_NAME" \
  --gateway-name "$APPGW_NAME" \
  --name "probe-api-8080" \
  --protocol Http \
  --path "/api/auth/health" \
  --host "127.0.0.1" \
  --port 8080 \
  --interval 30 \
  --timeout 30 \
  --threshold 3

az network application-gateway http-settings update \
  --resource-group "$RG_NAME" \
  --gateway-name "$APPGW_NAME" \
  --name "appGatewayBackendHttpSettings" \
  --port 8080 \
  --protocol Http \
  --probe "probe-api-8080"
```

When VMSS scales out or in, run the backend pool update command again (or automate this step with deployment pipeline automation).

### 15.7 Configure VMSS Autoscaling

```bash
export AUTOSCALE_NAME="autoscale-cbs-vmss"

az monitor autoscale create \
  --resource-group "$RG_NAME" \
  --resource "$VMSS_NAME" \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --name "$AUTOSCALE_NAME" \
  --min-count 3 \
  --max-count 8 \
  --count 3

az monitor autoscale rule create \
  --resource-group "$RG_NAME" \
  --autoscale-name "$AUTOSCALE_NAME" \
  --condition "Percentage CPU > 70 avg 10m" \
  --scale out 1

az monitor autoscale rule create \
  --resource-group "$RG_NAME" \
  --autoscale-name "$AUTOSCALE_NAME" \
  --condition "Percentage CPU < 35 avg 15m" \
  --scale in 1
```

### 15.8 Validate Endpoint

```bash
APPGW_IP=$(az network public-ip show -g "$RG_NAME" -n "$APPGW_PIP" --query ipAddress -o tsv)
curl -k "https://$APPGW_IP/api/auth/health"
```

If DNS is configured, point your hostname to `APPGW_IP` and test with the DNS name.

## 16. Cleanup Azure Resources

When finished, delete everything to avoid costs:

```bash
az group delete --name "$RG_NAME" --yes --no-wait
```
