# End-to-End Cloud Security Lifecycle: Engineering Defense-in-Depth Across Build, Runtime, and SecOps
**Justine Mae Macario** 

Focuses on engineering a 4-stage cloud security lifecycle pipeline on AWS, establishing enterprise defense-in-depth across pre-commit Infrastructure as Code scanning, perimeter-hardened Cloud Delivery Network Storage architectures, and sub-3 second serverless auto-remediation workflows aligned with NIST, SP 800-53 and CIS Benchmarks.

<br>*Whole repo contains my process* 

### Cloud Security Lifecycle
* a. Preventative Lifecycle
  - Preventative architecture with S3, CloudFront OAC, WAF, and Headers
      - README.md
      - policies/ 
* b. Event-Driven Remediation
  - Automation and Monitoring with CloudTrail, EventBridge, and Lambda
      - README.md
      - lambda/
* c. Shift-Left DevSecOps
  - Shift-Left and Governance with Terraform, Checkov, and GitHub OIDC
      - .github/workflows/
      - terraform/
* d. Continuous Assurance
  - Validation and Assurance with GuardDuty
      - evidence
* e. References and Papers
  - Short reviews on frameworks, documentation, and whitepapers
  - Articles I've written throughout + buncha challenges and all. 
