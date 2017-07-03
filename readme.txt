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
sudo service docker start


ssh -i "aws-north-virginia-seyedmehdi-key-pair.pem" ubuntu@ec2-52-91-171-139.compute-1.amazonaws.com
 
http://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/

docker build -t temdy/puppyfaceimage ./web_engine/
docker push temdy/puppyfaceimage
