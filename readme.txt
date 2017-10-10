# Tutorials:
    - [AWS Architecture - tips for creating a VPC, subnets, route tables, and security groups](https://www.youtube.com/watch?v=J64PbhirYS0)
    - [Docker Swarm Mode Walkthrough -- by: ](https://www.youtube.com/watch?v=KC4Ad1DS8xU)
    - [dockersamples/example-voting-app](https://github.com/dockersamples/example-voting-app/blob/master/docker-stack.yml)
    - [Docker for AWS: Orchestration Demo -- by: The Containerizers](https://www.youtube.com/watch?v=0j4Qq13w2pc&t=62s) and the [code playbook](https://gist.github.com/ndemoor/ff0916961ea0cf7e4bd82a9316a6b272) for this video
    - [Get Started with Docker in 6 steps: 1: Orientation 2: Containers 3: Services 4: Swarms 5: Stacks 6: Deploy your app](https://docs.docker.com/get-started/)
    - [Uploading Files to a Database in Flask](https://www.youtube.com/watch?v=TLgVEBuQURA)
    - [Returning Files From a Database in Flask:](https://www.youtube.com/watch?v=QPI3rzZow6k)
    - [Dockerized Nginx+Gunicorn](https://github.com/realpython/dockerizing-django)


# DNS and SSL setup:
### DNS
It is better to user the Amazon DNS (a.k.a. Route53) instead of the GoDaddy's. To do so:
Create a new hosted zone in AWS Route53 for the website (example.com).
Copy the name servers (NS) to GoDaddy's DNS Manager.

### Obtaining the SSL Certificate key files 
To make the site secure, a SSL certificate needs to be either self signed or obtained from a certificate authority. Graham Dumpleton has a nice set of instructions on how to [run HTTPS and client authentication with mod_wsgi-express.](https://gist.github.com/GrahamDumpleton/b79d336569054882679e)
However, if using GoDaddy see their help [page](https://ca.godaddy.com/help/apache-generate-csr-certificate-signing-request-5269).
You basically need to generate a private key (.key) file. Then use that to generate a certificate signing request (.csr). Upload the csr file to your certificate authority of choice (GoDaddy in my case), and obtain the .crt file. In my case GoDaddy generates two .crt file. one is *bundle*d and the other one has a long series of meaning less numbers in its name. I use the latter as my *server.crt*.

### Upload SSL certificates to AWS
First, issue the CSR file for the full address www.example.com, not the naked address (example.com).
http://markshust.com/2014/04/13/install-godaddy-ssl-certificate-aws-elb
https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files
Instructions on how to work with certificates in AWS: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html#delete-server-certificate
aws iam upload-server-certificate --server-certificate-name www.puppymyface.com --certificate-body file://server.crt --private-key file://server.key --certificate-chain file://gd_bundle-g2-g1.crt


# Application Deployment on the Cloud 
## Some handy tools
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
    - On the host machine (your laptob): 
        - [Deploy a Docker Stack on the AWS](https://docs.docker.com/docker-for-aws/#quickstart) 
        - `cd` into the root directory of the application repo
        - `docker login`
        - Build your Docker image:
          `docker-compose build`
        - Push the images:
          `docker-compose push`
    - On the remote machine (AWS EC2, Swarm manager)
        - `docker login`
        - create a `docker-stack.yml` file and copy the content of the docker-stack.yml into it
            * make sure there is no volumes in the file. Docker stack doesn't like volumes.
    - Run the stack on the AWS Docker Swarm manager node: 
        `docker stack deploy --with-registry-auth -c docker-stack.yml a_stack_name` 
    - Settings on the AWS: 
        - Go to Route53 and make an alias from www.example.com to the load balancer of the stack you created. 
          Make sure you can `ping www.example.com` -- don't forget the www in the ping domain address. It's also a good idea to clear the ping cache before doing so. 
        - Go to the load balancer and open port 443 for HTTPS traffic.

# Image processing:
A tutorial on [serving generated images from memory](https://fadeit.dk/blog/2015/04/30/python3-flask-pil-in-memory-image/).

