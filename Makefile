start-db: docker-compose up
ngrok: ngrok http 8000
server: uvicorn main:app --reload