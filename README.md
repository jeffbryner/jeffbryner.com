# jeffbryner.com
da website

Hosted in aws free tier via cloud magic, no servers and s3 buckets. 

If you'd like to do similar:

1) Copy this stuff somewhere (git clone? weird though since you won't be contributing to my homepage)
2) Change all the stuff referencing me to reference you or your site
3) Create an amazon certificate in us-east-1 for your domain (region is important!)
4) Create the s3 buckets you reference
5) Install all the serverless stuff: 
    (serverless itself from serverless.com )
    npm install --save-dev serverless
    npm install --save-dev serverless-apigw-binary
    npm install --save-dev serverless-python-requirements
    npm install --save-dev serverless-wsgi
    npm install --save-dev serverless-api-cloudfront
6) deploy via sls deploy --stage prod (wait patiently.. cloudfront)
7) Add a route53/dns of your choice ALIAS record for your cloudfront distribution name

Unfortunately, this isn't it. You will need to re-deploy one the api gateway has been established since flask needs to know the 'server_name' it is running as. So, once you have a good initial deployment, copy the api gateway name (something like gibberishseriesofcharacters.execute-api.us-west-2.amazonaws.com) into the config.enf.yml file as the SERVER_NAME paramter and redeploy and it should work. 

Voila a python, lambda-based, cloudfront distributed, s3 backed website.