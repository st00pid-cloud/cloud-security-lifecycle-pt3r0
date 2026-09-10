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
  Heck yeah
