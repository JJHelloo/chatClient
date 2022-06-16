#!/bin/bash

##################################################
# for generating your root CA private key and cert
##################################################

sudo rm -rf /etc/ssl/*CA*
sudo mkdir /etc/ssl/demoCA
sudo mkdir /etc/ssl/demoCA/certs
sudo mkdir /etc/ssl/demoCA/newcerts
sudo mkdir /etc/ssl/demoCA/private

echo "directories created in /etc/ssl/demoCA"
ls /etc/ssl/demoCA
echo ""
echo ""
echo "done creating folders"
echo ""
echo ""

cd /etc/ssl/demoCA

echo ""
echo ""
echo "Generate the CA’s RSA private key of size 2048 bits that will be encrypted by the Advanced Encryption Standard (AES) using a 256-bit key"
echo "[Enter] to continue"
read

# generate new rsa private key for CA
openssl genrsa -aes256 -out cakey.pem 2048

echo ""
echo ""
echo "Now create the root CA certificate"
echo "[Enter] to continue"
read
# create the root CA certificate (this is what you will install in your browser if you are not using intermediary signing keys)
openssl req -x509 -new -nodes -key cakey.pem -sha256 -days 1825 -out cacert.pem

# display  root cert in default form
echo ""
echo ""
echo "ROOT CERT DEFAULT FORMAT"
cat cacert.pem

# Decrypt root Certificate
echo ""
echo ""
echo "DECRYPTED  ROOT CERT"
openssl x509 -text -noout -in /etc/ssl/demoCA/cacert.pem

#move the root key to the private directory
mv ./cakey.pem ./private
echo "moved cakey.pem to private directory"

#copy root CA cert into certs directory using ca-certificates app
sudo cp cacert.pem /usr/local/share/ca-certificates/cacert.crt

ls /usr/local/share/ca-certificates/cacert.crt
echo "copid root CA cert to ca-certificates dir and changed extension"

#RUN CA-CERTIFICATES APP
sudo update-ca-certificates



