# Script para compartir el taller en la red local

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TALLER DE PHISHING - Compartir en Clase" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener la IP local
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress

if ($ipAddress) {
    Write-Host "✅ Tu IP en la red local es: " -NoNewline -ForegroundColor Green
    Write-Host $ipAddress -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📱 Comparte esta URL con tus compañeros:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Instagram Clone: " -NoNewline
    Write-Host "http://$ipAddress:5000" -ForegroundColor Green
    Write-Host ""
    Write-Host "   WiFi Portal:     " -NoNewline
    Write-Host "http://$ipAddress:5000/wifi" -ForegroundColor Green
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Verificar si el firewall está bloqueando
    Write-Host "⚠️  IMPORTANTE: Asegúrate de que el puerto 5000 esté abierto" -ForegroundColor Yellow
    Write-Host "   Ejecuta este comando como administrador si tienes problemas:" -ForegroundColor Gray
    Write-Host "   New-NetFirewallRule -DisplayName 'Taller Phishing' -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow" -ForegroundColor DarkGray
    Write-Host ""
    
    # Verificar si el contenedor está corriendo
    $container = docker ps --filter "name=taller-phishing-server" --format "{{.Names}}"
    
    if ($container) {
        Write-Host "✅ El servidor está ejecutándose correctamente" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Para ver los datos capturados en tiempo real:" -ForegroundColor Cyan
        Write-Host "   docker logs -f taller-phishing-server" -ForegroundColor Gray
    } else {
        Write-Host "❌ El contenedor NO está ejecutándose" -ForegroundColor Red
        Write-Host ""
        Write-Host "🚀 Inicia el servidor con:" -ForegroundColor Yellow
        Write-Host "   docker run -d --rm -p 5000:5000 --name taller-phishing-server taller-phishing" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ No se pudo detectar la IP de red local" -ForegroundColor Red
    Write-Host "   Asegúrate de estar conectado a una red WiFi o Ethernet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
