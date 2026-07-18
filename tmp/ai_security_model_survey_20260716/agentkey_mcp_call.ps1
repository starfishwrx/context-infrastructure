param(
    [switch]$List,
    [string]$ToolName,
    [string]$JsonArguments = '{}'
)

$ErrorActionPreference = 'Stop'
$configPath = 'C:\Users\Administrator\.codex\config.toml'
$config = Get-Content -Raw -LiteralPath $configPath
$match = [regex]::Match(
    $config,
    '(?ms)\[mcp_servers\.agentkey\.http_headers\]\s*Authorization\s*=\s*"([^"]+)"'
)
if (-not $match.Success) {
    throw 'AgentKey Authorization header was not found in the Codex config.'
}

$headers = @{
    Authorization = $match.Groups[1].Value
    Accept = 'application/json, text/event-stream'
}
$endpoint = 'https://api.agentkey.app/v1/mcp'

function Invoke-McpRequest {
    param(
        [int]$Id,
        [string]$Method,
        [hashtable]$Params,
        [string]$SessionId
    )

    $requestHeaders = $headers.Clone()
    if ($SessionId) {
        $requestHeaders['Mcp-Session-Id'] = $SessionId
    }
    $payload = @{
        jsonrpc = '2.0'
        id = $Id
        method = $Method
        params = $Params
    } | ConvertTo-Json -Depth 30 -Compress

    Invoke-WebRequest `
        -Uri $endpoint `
        -Method Post `
        -Headers $requestHeaders `
        -ContentType 'application/json' `
        -Body $payload `
        -TimeoutSec 60
}

$initialize = Invoke-McpRequest -Id 1 -Method 'initialize' -Params @{
    protocolVersion = '2025-06-18'
    capabilities = @{}
    clientInfo = @{
        name = 'codex-agentkey-bridge'
        version = '1.0'
    }
}
$sessionId = $initialize.Headers.'Mcp-Session-Id'
if (-not $sessionId) {
    throw 'AgentKey did not return an MCP session ID.'
}

$initializedHeaders = $headers.Clone()
$initializedHeaders['Mcp-Session-Id'] = $sessionId
$initializedPayload = @{
    jsonrpc = '2.0'
    method = 'notifications/initialized'
} | ConvertTo-Json -Compress
Invoke-WebRequest `
    -Uri $endpoint `
    -Method Post `
    -Headers $initializedHeaders `
    -ContentType 'application/json' `
    -Body $initializedPayload `
    -TimeoutSec 60 | Out-Null

if ($List) {
    $response = Invoke-McpRequest -Id 2 -Method 'tools/list' -Params @{} -SessionId $sessionId
} else {
    if (-not $ToolName) {
        throw 'Pass -List or -ToolName.'
    }
    $arguments = $JsonArguments | ConvertFrom-Json -AsHashtable
    $response = Invoke-McpRequest -Id 2 -Method 'tools/call' -Params @{
        name = $ToolName
        arguments = $arguments
    } -SessionId $sessionId
}

$response.Content
