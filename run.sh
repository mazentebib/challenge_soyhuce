#build image and run
docker build -t movies_db:latest ./database
docker build -t movie_scraper
docker-compose up -d  
