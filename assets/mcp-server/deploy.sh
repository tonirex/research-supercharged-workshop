#!/usr/bin/env bash
# Deploy the Research Tools MCP server to Azure Container Apps (public HTTPS).
#
# Builds the container from ./Dockerfile in the cloud (no local Docker needed) and
# deploys it to Azure Container Apps with an external (public) ingress. Prints the MCP
# endpoint URL that the facilitator shares with participants for Lab 4:
#
#     https://<app-fqdn>/mcp
#
# Run this ONCE before the workshop. Reuses the workshop resource group by default so
# teardown is a single `az group delete`.
#
# Prereqs: `az login` first; Contributor/Owner on the subscription or resource group.
#
# Usage:
#   ./deploy.sh
#   RESOURCE_GROUP=rg-foundry-workshop LOCATION=swedencentral ./deploy.sh
set -euo pipefail
cd "$(dirname "$0")"

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-foundry-workshop}"
LOCATION="${LOCATION:-swedencentral}"
APP_NAME="${APP_NAME:-mcp-research-tools}"
ENVIRONMENT="${ENVIRONMENT:-cae-foundry-workshop}"

echo "==> Registering providers and Container Apps extension (idempotent)..."
az extension add --name containerapp --upgrade --only-show-errors >/dev/null
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait

echo "==> Ensuring resource group '$RESOURCE_GROUP' exists in '$LOCATION'..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --only-show-errors >/dev/null

echo "==> Building from source and deploying '$APP_NAME' to Azure Container Apps..."
echo "    (first run takes a few minutes: it creates an ACR, builds the image, and creates the environment)"
az containerapp up \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --environment "$ENVIRONMENT" \
  --source . \
  --ingress external \
  --target-port 8000 \
  --only-show-errors

echo "==> Pinning scale (min 1 replica so there is no cold start during the workshop)..."
az containerapp update \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --min-replicas 1 \
  --max-replicas 3 \
  --only-show-errors >/dev/null

FQDN=$(az containerapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
  --query properties.configuration.ingress.fqdn -o tsv)

if [[ -z "$FQDN" ]]; then
  echo "ERROR: could not read the app FQDN. Check the deployment in the Azure portal." >&2
  exit 1
fi

MCP_URL="https://${FQDN}/mcp"

echo ""
echo "==> Validating the deployment..."
if curl -fsS "https://${FQDN}/healthz" >/dev/null 2>&1; then
  echo "    /healthz -> ok"
else
  echo "    WARN: /healthz check failed (the app may still be starting)."
fi

echo ""
echo "============================================================"
echo " MCP server is live. Share this URL with participants (Lab 4):"
echo ""
echo "   ${MCP_URL}"
echo ""
echo " Health check:  https://${FQDN}/healthz"
echo " Tear down:     az group delete --name ${RESOURCE_GROUP} --yes --no-wait"
echo "============================================================"
