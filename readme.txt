### Tutorials:
	Uploading Files to a Database in Flask:
	https://www.youtube.com/watch?v=TLgVEBuQURA

	Returning Files From a Database in Flask:
	https://www.youtube.com/watch?v=QPI3rzZow6k

### Setting up the HTTPS
To make the site secure, a SSL certificate needs to be either self signed or obtained from a certificate authority. Graham Dumpleton has a nice set of instructions on how to [run HTTPS and client authentication with mod_wsgi-express.](https://gist.github.com/GrahamDumpleton/b79d336569054882679e)

However, if using GoDaddy see their help [page](https://ca.godaddy.com/help/apache-generate-csr-certificate-signing-request-5269).

You basically need to generate a private key (.key) file. Then use that to generate a certificate signing request (.csr). Upload the csr file to your certificate authority of choice (GoDaddy in my case), and obtain the .crt file. In my case GoDaddy generates two .crt file. one is *bundle*d and the other one has a long series of meaning less numbers in its name. I use the latter as my *server.crt*.


### How to run containers on an EC2 instance:
on EC2 instance:
Install Docker:
	Method 1: [AWS documentation](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html#install_docker)
	Method 2: [Yevgeny's tutorial on Running Docker on AWS from the ground up]( http://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/)

sudo service docker start

ssh -i "aws-key-pari-north-viginia.pem" ec2-user@ec2-34-197-42-159.compute-1.amazonaws.com

### Push and pull the Docker image on AWS ECR:
After creating the docker registry repo, go to the [ECS page](https://console.aws.amazon.com/ecs/) >> Repositories >> select your repo >> View Push Commands

 - Retrieve the docker login command that you can use to authenticate your Docker client to your registry:
   `aws ecr get-login --no-include-email --region us-east-1`
   >> USE the output of this get loging command in both the local terminal and EC2 instance to be able to pull the image in the EC2 instance
 - Run the docker login command that was returned in the previous step.
 - Make sure your current directory is the root of this repo.
 - Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here. You can skip this step if your image is already built:
   `docker build -t puppymyface ./web_engine/'
 - After the build completes, tag your image so you can push the image to this repository:
   `docker tag puppymyface:latest 345806756162.dkr.ecr.us-east-1.amazonaws.com/puppymyface:latest`
 - Run the following command to push this image to your newly created AWS repository:
   `docker push 345806756162.dkr.ecr.us-east-1.amazonaws.com/puppymyface:latest`
 - Pull the image on the EC2 instance machine.
   `docker pull 345806756162.dkr.ecr.us-east-1.amazonaws.com/puppymyface`
 - create a `docker-compose.yml` file and put the image name into that file



docker build -t temdy/puppyfaceimage ./web_engine/
docker push temdy/puppyfaceimage
