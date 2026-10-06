$baseUrl = if ($env:LUGHA_BASE_URL) { $env:LUGHA_BASE_URL } else { "http://localhost:8000" }

if (-not $env:LUGHA_API_KEY) {
    throw "Set LUGHA_API_KEY first"
}

$body = @{
    model      = "lugha-demo-large"
    prompt     = "Explain Kampala to a developer visiting Uganda for the first time."
    language   = "en"
    max_tokens = 64
    region     = "ug"
} | ConvertTo-Json

$data = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/generate" `
    -Headers @{ Authorization = "Bearer $env:LUGHA_API_KEY" } `
    -ContentType "application/json" `
    -Body $body

Write-Output $data.output
Write-Output "Tokens used: $($data.usage.total_tokens)"
