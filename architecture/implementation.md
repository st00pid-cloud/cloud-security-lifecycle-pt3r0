# The First Version 
  Which you still need since the second architecture is the expansion DLC. 

1. Create a Private S3 Bucket
   Log into AWS S3 and create a bucket > Enable Block all public access, all 4 boxes > Configure the SSE-E3 encryption. Upload your index.html and error.html. Do not enable static website hosting.

2. Configure CloudFront Distribution
   Create distribution in CloudFront > Select S3 bucket as origin > Enable Origin Access Control (OAC) with SigV4 signing > Enforce HTTPS (Redirect HTTP → HTTPS) > Allow only GET, HEAD methods > Set default root object to index.html

3. Attach Least-Privilege Bucket Policy
   Copy CloudFront-generated bucket policy > Paste into S3 bucket policy editor > Replace placeholders with bucket name, account ID, distribution ID > Save.

4. Verify Access Controls
   Test S3 object URL → should return 403 Access Denied > Test CloudFront domain → should render index.html over HTTPS

# The Current Version 
  The current architecture was built in four phases

  ## Edge Perimeter Defense
  This was added to mitigate Layer 7 application attacks, bot traffic, and reconnaissance before requests touch CloudFront or S3. I created a protection pack with the following rules: 
    <br>(1) AWSManagedCommonRuleSet
    <br>(2) AWSManagedRulesKnownBadInputsRuleSet
    <br>(3) AWSManagedRulesAmazonIpReputationList
    <br>(4) Rate Limiting Rule (2000 requests per 5-minute window)

  ## Client Security Headers 
  This is to instruct the end user's browser to enforce strict parsing behaviors and disallow insecure embedding. The following components are added in a custom CloudFront Response Header Policy enforcing: 
    <br>(1)  Strict Transport Security with max-age 2 years (63072000) includeSubDomains and preload. 
    <br>(2) Content-Security-Policy (default-src 'self') 
    <br>(3) X-Frame-Options(DENY) 
    <br>(4) X-Content-Type-Options (no-sniff) 
    <br>(5) 
  
    
