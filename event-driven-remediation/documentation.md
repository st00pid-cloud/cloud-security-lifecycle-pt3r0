# Architectural Overview
  I like diagrams. I am writing this at 4:00 am cause I just want to. <br> 
<img width="889" height="611" alt="archi-overview" src="https://github.com/user-attachments/assets/9060372a-087c-4790-a1f7-1ce5f5a55c56" />

## Implemented Services 
  I like tables
| Service | Function | Role in Flow |
| --- | --- | --- |
| Amazon S3 | Acts as the protected asset. | Undergoes configuration drift when an actor or process attempts to disable S3 Block Public Access (DeleteBucketPublicAccessBlock) or loosen policies (PutBucketPolicy, PutBucketAcl). It is also the remediation target where the Lambda function enforces full lockout (put_public_access_block). |
| AWS CloudTrail | Provides continuous API auditing and visibility across AWS account resources. | Intercepts control-plane management API calls across all regions. It packages the raw API transaction—including the calling IAM principal identity, source IP, timestamp, and target bucket name—into a standard CloudTrail event format and streams it to EventBridge. |
| Amazon EventBridge | Serves as the central serverless routing engine. | Continuously evaluates incoming events against your custom JSON EventPattern (filtering strictly for aws.s3 management events like DeleteBucketPublicAccessBlock). Once matched, it broadcasts the structured event payload to subscribed targets (AWS Lambda and Amazon SNS) in near real-time. |
| AWS Lambda | Executes automated incident response logic (NIST SP 800-53 IR-4 / CIS AWS Benchmark 2.1.4). | Runs a lightweight Python 3.12 runtime with boto3. It parses the bucket ARN from the event detail, calls s3:PutBucketPublicAccessBlock to enforce all 4 public access block flags within sub-second execution times, and formats a detailed forensic payload. |
| Amazon Simple Notification Service (SNS) | Managed publish/subscribe messaging backbone. | Publishes immediate, human-readable push notifications to security engineers and SecOps endpoints (Email, Slack, or ticketing webhooks). It includes incident context: affected bucket, actor identity, source IP, exact drift event, and remediation confirmation. |
| Amazon CloudWatch Logs | Provides continuous API auditing and visibility across AWS account resources. | viewer |
| AWS CloudTrail |Centralized logging and telemetry store| Captures all standard output (stdout), execution runtimes, memory metrics, and error traces from the Lambda function, creating an auditable execution record to measure Mean Time to Remediate (MTTR). |

## Implementation Process and Documentatin 
1. CloudTrail Checking
   _Just checking if CloudTrail's checking what I do~_
   <img width="1535" height="710" alt="11-cloudtrail-works" src="https://github.com/user-attachments/assets/156268b3-7bc4-4815-ba0e-3a87647791e0" />
   <img width="1532" height="704" alt="image" src="https://github.com/user-attachments/assets/f26963df-76bd-4633-a4ec-7233571bcfc4" />

2. Simple Notification Service
   _Sending the message that "Someone's doing something!"_
   I created a standard topic type, nothing else added.
   <img width="1536" height="761" alt="image" src="https://github.com/user-attachments/assets/7362f52f-ad3d-46e1-8e61-8bfd14326552" />
4. Confirming the subscription
   Under the topic, I created as subscription with email as the protocol. From my personal email, I accepted the subscription. 
   <img width="1535" height="712" alt="image" src="https://github.com/user-attachments/assets/795adb9e-b24e-4a32-b5cd-1f50fdd0b3fd" />
5. Making the IAM Role
   For the Lambda Role, I chose AWS Service as the trusted entity and Lambda as the use case. 
   <img width="1527" height="705" alt="image" src="https://github.com/user-attachments/assets/5cba935e-67ab-4a00-8983-669ad2511cef" />
7. How 'bout the Lambda?
   <img width="1532" height="741" alt="image" src="https://github.com/user-attachments/assets/2cc9e6b7-0a05-48cf-8ee4-a380be841658" />
8. EventBridge Rule Configuration   
    <img width="1242" height="371" alt="image" src="https://github.com/user-attachments/assets/a3cb4a25-6399-4256-8819-c57a242b31df" />
## Testing and Validation
  Thru the cloud shell bby, anyways letsa go

### Drift Simulation
* Creating a dummy test bucket
### Verification and MTTR Measurement
* Heck YEAH EMAILS


   
  
   
## Problems Encountered

## Learnings
### From: Architecture Overview
  Before doing anything else, I visualize how things would work. Looking into the architecture I made, I had to breakdown | recall some concepts. Here ya go: 
  1. Configuration Drift - Modifications not audited or listed.
  2. Asynchronous Invocation - When a service is called asynchronously, the service requester and the service provider run in different threads of execution.
  3. Why does the Amazon EventBridge branch into two?
       This is from the "Fan-Out  Architectural Pattern," where the automated technical response is separated from the human alerting. This means that AWS Lambda focuses entirely on immediate technical containment, while Amazon SNS handles team visibility and paging. Because both services are invoked simultaneously in parallel, Mean Time to Remediate (MTTR) is cut down to milliseconds. Furthermore, this split acts as a critical fail-safe: if the Lambda function times out, crashes, or hits permissions errors, the security team still receives the raw drift notification from SNS. Ultimately, this approach avoids bottlenecks, provides built-in retries for code execution, and guarantees that incident notification never stalls behind script performance.
### From: Implemented Services
1. Wrong ahh region. 
### From: Implementation 
