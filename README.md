# jeffbryner.com
da website

Hosted in aws free tier via cloud magic, no servers and s3 buckets. 

If you'd like to do similar:

1) Copy this stuff somewhere
2) Change all the stuff referencing me to reference you
3) Create an amazon certificate in us-east-1 for your domain (region is important!)
4) Create the s3 buckets you reference
5) Install all the serverless stuff: 
    (serverless itself from serverless.com )
    npm install --save-dev serverless
    npm install --save-dev serverless-apigw-binary
    npm install --save-dev serverless-python-requirements
    npm install --save-dev serverless-wsgi
    npm install --save-dev serverless-api-cloudfront
6) deploy via sls deploy --stage prod
7) Add a route53/dns of your choice ALIAS record for your cloudfront distribution name

Voila a python, lambda-based, cloudfront distributed, s3 backed website.