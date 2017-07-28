### Tutorials:
	Uploading Files to a Database in Flask:
	https://www.youtube.com/watch?v=TLgVEBuQURA

	Returning Files From a Database in Flask:
	https://www.youtube.com/watch?v=QPI3rzZow6k

### Setting up the HTTPS
To make the site secure, a SSL certificate needs to be either self signed or obtained from a certificate authority. Graham Dumpleton has a nice set of instructions on how to [run HTTPS and client authentication with mod_wsgi-express.](https://gist.github.com/GrahamDumpleton/b79d336569054882679e)

However, if using GoDaddy see their help [page](https://ca.godaddy.com/help/apache-generate-csr-certificate-signing-request-5269).

You basically need to generate a private key (.key) file. Then use that to generate a certificate signing request (.csr). Upload the csr file to your certificate authority of choice (GoDaddy in my case), and obtain the .crt file. In my case GoDaddy generates two .crt file. one is *bundle*d and the other one has a long series of meaning less numbers in its name. I use the latter as my *server.crt*.

## Tools

### Docker Visualizer
https://github.com/dockersamples/docker-swarm-visualizer
docker service create \
  --name=visualizer \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer

### sandbox
docker service create --name=sandybox  alpine

## Orchestration 

### Push and pull the Docker image on AWS ECR:
After creating the docker registry repo, go to the [ECS page](https://console.aws.amazon.com/ecs/) >> Repositories >> select your repo >> View Push Commands

 - Retrieve the docker login command that you can use to authenticate your Docker client to your registry:
   `aws ecr get-login --no-include-email --region us-east-1`
   >> USE the output of this get loging command in both the local terminal and EC2 instance to be able to pull the image in the EC2 instance
 - Run the docker login command that was returned in the previous step.
 - Make sure your current directory is the root of this repo.
 - Build your Docker image:
   `docker-compose build`
 - Push the images:
   `docker-compose push`
 - create a `docker-stack.yml` file and put the image name into that file
 - Run the stack on the AWS Docker Swarm manager node: 
   `docker stack deploy --with-registry-auth -c docker-stack.yml a_stack_name` 


## Image processing:
A tutorial on [serving generated images from memory](https://fadeit.dk/blog/2015/04/30/python3-flask-pil-in-memory-image/).

## URL Set Up:
### DNS
It is better to user the Amazon DNS (a.k.a. Route53) instead of the GoDaddy's. To do so:
Create a new hosted zone in AWS Route53 for the website (pairool.com).
Copy the name servers (NS) to GoDaddy's DNS Manager.


### SSL and HTTPS
#### Upload SSL certificates to AWS
First, issue the CSR file for the full address www.example.com not the naked address (example.com).
http://markshust.com/2014/04/13/install-godaddy-ssl-certificate-aws-elb

https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files
aws iam upload-server-certificate --server-certificate-name www.puppymyface.com --certificate-body file://server.crt --private-key file://server.key --certificate-chain file://gd_bundle-g2-g1.crt

### Forced HTTPS:
Want to redirect the traffic from HTTP to HTTPS? Graham Dumpleton has a good Q/A thread with topic [can mod_wsgi-express be used with RewriteRule in the included config?](https://groups.google.com/forum/#!topic/modwsgi/dt2i2syT4uk)
If you google "[How to Force HTTPS Behind AWS ELB](https://www.allcloud.io/how-to/how-to-force-https-behind-aws-elb/)", there are instructions on how to set up the redirection for the Apache
