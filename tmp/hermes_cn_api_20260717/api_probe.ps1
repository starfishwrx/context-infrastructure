param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl,

    [Parameter(Mandatory = $true)]
    [string]$Model
)

$ErrorActionPreference = 'Stop'
$BaseUrl = $BaseUrl.TrimEnd('/')

$secureKey = Read-Host 'API Key' -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $apiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
}

$headers = @{
    Authorization = "Bearer $apiKey"
    'Content-Type' = 'application/json'
}

Write-Host "[1/3] Testing $BaseUrl/models"
try {
    $models = Invoke-RestMethod -Method Get -Uri "$BaseUrl/models" -Headers $headers -TimeoutSec 30
    Write-Host 'Models endpoint: OK'
} catch {
    Write-Warning "Models endpoint failed: $($_.Exception.Message)"
    Write-Warning 'Some compatible APIs omit /models. Continue with the configured model name.'
}

Write-Host '[2/3] Testing basic chat completion'
$chatBody = @{
    model = $Model
    messages = @(@{ role = 'user'; content = 'Reply with exactly OK.' })
    stream = $false
} | ConvertTo-Json -Depth 20

$chat = Invoke-RestMethod -Method Post -Uri "$BaseUrl/chat/completions" -Headers $headers -Body $chatBody -TimeoutSec 90
Write-Host "Chat response: $($chat.choices[0].message.content)"

Write-Host '[3/3] Testing OpenAI-style tool calling'
$toolBody = @{
    model = $Model
    messages = @(@{ role = 'user'; content = 'Use the supplied tool to get the current site status.' })
    tools = @(@{
        type = 'function'
        function = @{
            name = 'get_site_status'
            description = 'Return the current site status.'
            parameters = @{
                type = 'object'
                properties = @{}
                required = @()
            }
        }
    })
    tool_choice = 'auto'
    stream = $false
} | ConvertTo-Json -Depth 30

$tool = Invoke-RestMethod -Method Post -Uri "$BaseUrl/chat/completions" -Headers $headers -Body $toolBody -TimeoutSec 90
$toolCalls = $tool.choices[0].message.tool_calls
if ($toolCalls) {
    Write-Host "Tool calling: OK ($($toolCalls[0].function.name))"
} else {
    Write-Warning 'The API returned no tool_calls. Text chat works, but agent compatibility is not yet proven.'
}

$apiKey = $null

