
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 431151642822.dkr.ecr.us-east-1.amazonaws.com

docker build --platform linux/amd64 --provenance=false -t sofia_final_so .

docker tag sam_final_so:latest 431151642822.dkr.ecr.us-east-1.amazonaws.com/sofia_final_so:latest

docker push 431151642822.dkr.ecr.us-east-1.amazonaws.com/sofia_final_so:latest