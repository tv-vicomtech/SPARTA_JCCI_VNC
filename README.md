# SPARTA JCCI VNC

Sparta JCCI Landing Host guide for Graphical User Interface deployment.

1. Dockerize partner landing host components
2. Clone this repository 
3. Add dockerized services to Dockerfile in repository
4. Build image: $ docker build -t VNClandinghost .
5. Ask for application registration in Keyrock (Sparta ACS) for Landing Host with GUI (fzola@vicomtech.org, jafernandez@vicomtech.org)
6. Configure image to connect with Sparta ACS with credentials created in registration: add client_id, client_secret, public_ip to authentication.py file
7. Start container: $ docker run -d -p host_port:6080 VNClandinghost
8. Service will be reached in URL: public_ip:port/auth/keyrock
