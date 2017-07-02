on EC2 instance:
sudo service docker start


ssh -i "aws-north-virginia-seyedmehdi-key-pair.pem" ubuntu@ec2-52-91-171-139.compute-1.amazonaws.com
 
http://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/

docker build -t temdy/puppyfaceimage ./web_engine/
docker push temdy/puppyfaceimage
