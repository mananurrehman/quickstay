#!/bin/bash
# deploy.sh
# Deployment script
# Called by Jenkins pipeline via SSH

set -e

# ========== VARIABLES ==========
APP_DIR="/home/ubuntu/quickstay"
DATA_DIR="/home/ubuntu/quickstay-data"
BRANCH="${1:-develop}"

echo "=========================================="
echo "🚀 QuickStay Deployment Starting..."
echo "📌 Branch: ${BRANCH}"
echo "=========================================="

# ========== STEP 1: CREATE PERSISTENT DIRECTORIES ==========
echo ""
echo "📁 Step 1: Creating persistent data directories..."
mkdir -p ${DATA_DIR}/postgres
mkdir -p ${DATA_DIR}/uploads
echo "✅ Directories ready"

# ========== STEP 2: NAVIGATE TO APP ==========
echo ""
echo "📂 Step 2: Navigating to app directory..."
if [ ! -d "${APP_DIR}" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/mananurrehman/quickstay.git ${APP_DIR}
fi
cd ${APP_DIR}
echo "✅ In ${APP_DIR}"

# ========== STEP 3: PULL LATEST CODE ==========
echo ""
echo "📥 Step 3: Pulling latest code..."
git fetch origin
git checkout ${BRANCH}
git pull origin ${BRANCH}
echo "✅ Code updated to latest ${BRANCH}"

# ========== STEP 4: STOP OLD CONTAINERS ==========
echo ""
echo "🛑 Step 4: Stopping existing containers..."
docker-compose down --remove-orphans || true
echo "✅ Old containers stopped"

# ========== STEP 5: BUILD AND START ==========
echo ""
echo "🔨 Step 5: Building and starting containers..."
docker-compose up -d --build
echo "✅ Containers started"

# ========== STEP 6: VERIFY ==========
echo ""
echo "🔍 Step 6: Waiting for containers to be healthy..."
sleep 30

echo ""
echo "Container Status:"
docker-compose ps

echo ""
echo "=========================================="
echo "🎉 QuickStay Deployed Successfully!"
echo "🌐 Access: http://$(curl -s ifconfig.me):5000"
echo "=========================================="