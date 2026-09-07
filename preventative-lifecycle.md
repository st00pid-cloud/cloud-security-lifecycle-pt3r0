# Preventative Lifecycle 

## Initial Architecture
The original architecture shown below eliminates public S3 bucket exposure by ensuring that only Amazon CloudFront can access the underlying storage using AWS Origin Access Control (OAC) with modern signature support and server-side encryption compatibility.

<img width="532" height="201" alt="s3-cloudfront-oac drawio" src="https://github.com/user-attachments/assets/77b555b6-7a88-4933-ab81-4cab6e5cef3a" />
<br>*Original Architecture for Testing*

But I decided to move forward and expand the diagram to think more like an actual engineer and align it with the documentation I could find. Instead of just an initial practice on buckets and CDNs I went to a longer route. 

## Second Version of the Architecture
<img width="712" height="362" alt="new-updated-diagram drawio" src="https://github.com/user-attachments/assets/70d74120-9d85-46c3-b624-e0ce6f9be098" />
<br>*Current Version Used* 

The current architecture establishes a hardened content delivery perimeter on AWS. It eliminates direct public exposure of cloud storage by enforcing Amazon CloudFront Origin Access Control (OAC), cryptographic request signing (SigV4), and strict transport layer policies. It also presents a dedicated Logging Bucket. 

## Additional Diagrams and Practices 

### Threat Modelling and Framework Control Mapping
Concurrently with this project, I was writing articles on the AWS Builder Website, focusing on diagrams and such. I decided to add a Threat Modelling Matrix and also a Framework Control Mapping just for the fun of it : D.

#### Threat Modelling Matrix

Core infrastructure threats are addressed by substituting standard configurations with defense-in-depth security controls. (I will still place a "Definition of Terms" section)

| Threat Vector | Unhardened Setup | Architecture Decision |
| -------- | -------- | -------- |
| Public Bucket Leakage | S3 bucket configured as public or enabled with S3 static website hosting mode. | S3 Block Public Access strictly enforced (all 4 flags). Website hosting disabled; REST API endpoint used. |
| Confused Deputy Vulnerability | Open service principals or legacy OAI without IAM condition constraints. | AWS:SourceArn condition restricts bucket access exclusively to the specific CloudFront distribution ARN.|
| Insecure Transport / MitM | Plaintext HTTP allowed in transit between client, CDN, or storage bucket. | CloudFront forces Redirect HTTP to HTTPS; S3 bucket policy enforces explicit deny for unencrypted HTTP. |
| Information Disclosure & Recon | Unauthenticated callers trigger directory indexing or exposed S3 XML errors. | Explicit Default Root Object (index.html) prevents path traversal; s3:ListBucket omitted. |
| Client-Side Vulnerabilities | Missing response headers allowing clickjacking, MIME-sniffing, or XSS execution. | CloudFront Response Headers Policy injects strict HSTS, CSP, X-Frame-Options: DENY, and nosniff. |

#### Framework Control Mapping

| Security Domain | Architectural Addition | CIS AWS Benchmark Control | NIST SP 800-53 (Rev 5) Control | AWS Well-Architected Principle |
| -------- | -------- | -------- | -------- | -------- |
| Edge Defense | AWS WAF attached to CloudFront | CloudFront.1 (WAF attached) | SC-7 (Boundary Protection) | SEC 06: Protect networks & edge boundaries |
| Secure Transport | Minimum TLS 1.2 protocol policy | CloudFront.2 (Viewer TLS 1.2+) | SC-8 / SC-13 (Transmission Confidentiality) | SEC 09: Encrypt data in transit |
| Application Layer | Security Response Headers Policy | N/A (Application Defense) | SI-10 (Information Input Validation / Output Handling) | SEC 06: Harden endpoint configurations |
| Data Protection  | Customer Managed KMS (SSE-KMS) + S3 Versioning | S3.1 / S3.14 (Versioning & KMS Encryption) | SC-28 (Protection at Rest) & CP-9 (Information Backup) | SEC 08: Protect data at rest |
| Audit & Visibility | Dedicated S3 Logging Bucket for Access Logs | S3.9 (S3 Server Access Logging) & CloudFront.5 | AU-2 / AU-3 (Audit Events & Content of Audit Records) | SEC 04: Detect and investigate events |
| Identity / Least Privilege | S3 Bucket Key + Strict SourceArn Condition | S3.5 (Enforce SSL only on bucket policies) | AC-3 / AC-6 (Access Enforcement & Least Privilege) | SEC 03: Manage permissions & reduce blast radius |

Why the diagrams? 
  I wanted to learn the GRC side of creating architectures since there are industry controls : D.

## Definition of Terms
1. Confused Deputy Vulnerability - A security issue where an entity that doesn't have permission to perform an action can coerce a more-privileged entity to perform the action. 






