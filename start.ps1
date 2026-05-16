# start.ps1
Write-Host "🛑 Derrubando containers..." -ForegroundColor Yellow
docker compose down

Write-Host "🧹 Limpando volumes do Kafka/Zookeeper..." -ForegroundColor Yellow
docker volume rm news-pipeline_zookeeper_data news-pipeline_kafka_data 2>$null

Write-Host "🚀 Subindo Zookeeper..." -ForegroundColor Cyan
docker compose up -d zookeeper
Start-Sleep -Seconds 15

Write-Host "🚀 Subindo Kafka..." -ForegroundColor Cyan
docker compose up -d kafka
Start-Sleep -Seconds 20

Write-Host "🚀 Subindo restante..." -ForegroundColor Cyan
docker compose up -d

Write-Host "✅ Status final:" -ForegroundColor Green
docker compose ps
