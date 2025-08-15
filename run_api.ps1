param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8000
)

$env:UVICORN_WORKERS = "1"
uvicorn app.app:app --host $Host --port $Port --reload
