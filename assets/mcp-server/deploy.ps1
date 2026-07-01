<#
.SYNOPSIS
    Deploy the Research Tools MCP server to Azure Container Apps (public HTTPS).

.DESCRIPTION
    Builds the container from ./Dockerfile in the cloud (no local Docker needed) and
    deploys it to Azure Container Apps with an external (public) ingress. Prints the
    MCP endpoint URL that the facilitator shares with participants for Lab 4:

        https://<app-fqdn>/mcp

    Run this ONCE before the workshop. Reuses the workshop resource group by default so
    teardown is a single `az group delete`.

.PREREQUISITES
    * Azure CLI (`az`) signed in:  az login
    * Contributor (or Owner) on the subscription / resource group.
    * The Container Apps extension + providers are registered automatically below.

.EXAMPLE
    ./deploy.ps1
    ./deploy.ps1 -ResourceGroup rg-foundry-workshop -Location swedencentral
#>
[CmdletBinding()]
param(
    [string]$ResourceGroup = "rg-foundry-workshop",
    [string]$Location      = "swedencentral",
    [string]$AppName       = "mcp-research-tools",
    [string]$Environment   = "cae-foundry-workshop"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "==> Registering providers and Container Apps extension (idempotent)..." -ForegroundColor Cyan
az extension add --name containerapp --upgrade --only-show-errors | Out-Null
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait

Write-Host "==> Ensuring resource group '$ResourceGroup' exists in '$Location'..." -ForegroundColor Cyan
az group create --name $ResourceGroup --location $Location --only-show-errors | Out-Null

Write-Host "==> Building from source and deploying '$AppName' to Azure Container Apps..." -ForegroundColor Cyan
Write-Host "    (first run takes a few minutes: it creates an ACR, builds the image, and creates the environment)"
az containerapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --location $Location `
    --environment $Environment `
    --source . `
    --ingress external `
    --target-port 8000 `
    --only-show-errors

Write-Host "==> Pinning scale (min 1 replica so there is no cold start during the workshop)..." -ForegroundColor Cyan
az containerapp update `
    --name $AppName `
    --resource-group $ResourceGroup `
    --min-replicas 1 `
    --max-replicas 3 `
    --only-show-errors | Out-Null

$fqdn = az containerapp show --name $AppName --resource-group $ResourceGroup `
    --query properties.configuration.ingress.fqdn -o tsv

if (-not $fqdn) {
    Write-Error "Could not read the app FQDN. Check the deployment in the Azure portal."
    exit 1
}

$mcpUrl = "https://$fqdn/mcp"

Write-Host ""
Write-Host "==> Validating the deployment..." -ForegroundColor Cyan
try {
    $health = Invoke-WebRequest -Uri "https://$fqdn/healthz" -UseBasicParsing -TimeoutSec 30
    Write-Host "    /healthz -> $($health.StatusCode) $($health.Content)" -ForegroundColor Green
} catch {
    Write-Warning "    /healthz check failed (the app may still be starting): $($_.Exception.Message)"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " MCP server is live. Share this URL with participants (Lab 4):" -ForegroundColor Green
Write-Host ""
Write-Host "   $mcpUrl" -ForegroundColor Yellow
Write-Host ""
Write-Host " Health check:  https://$fqdn/healthz" -ForegroundColor Green
Write-Host " Tear down:     az group delete --name $ResourceGroup --yes --no-wait" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
