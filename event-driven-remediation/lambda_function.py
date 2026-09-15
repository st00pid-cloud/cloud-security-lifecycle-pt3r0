import json
import logging
import os
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")
sns_client = boto3.client("sns")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    detail = event.get("detail", {})
    event_name = detail.get("eventName", "UnknownEvent")
    event_source = detail.get("eventSource", "UnknownSource")
    event_time = detail.get("eventTime", "UnknownTime")

    # Extract bucket name safely across S3 control plane APIs
    bucket_name = (
        detail.get("requestParameters", {}).get("bucketName")
        or detail.get("requestParameters", {}).get("Bucket")
    )

    # Fallback to responseElements or resources block
    if not bucket_name:
        resources = detail.get("resources", [])
        for resource in resources:
            if resource.get("type") == "AWS::S3::Bucket":
                bucket_name = resource.get("ARN", "").split(":::")[-1]
                break

    if not bucket_name:
        logger.error("Could not extract S3 bucket name from event.")
        return {"status": "FAILED", "reason": "Bucket name missing"}

    iam_principal = detail.get("userIdentity", {}).get("arn", "UnknownPrincipal")
    source_ip = detail.get("sourceIPAddress", "UnknownIP")

    logger.warning(
        "Detected potential drift: Bucket=%s, Action=%s, Principal=%s, IP=%s",
        bucket_name,
        event_name,
        iam_principal,
        source_ip,
    )

    # 1. Execute Remediation: Re-apply full Block Public Access
    remediation_status = "SUCCESS"
    remediation_details = ""

    try:
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        remediation_details = (
            "All 4 S3 Block Public Access configurations enforced successfully."
        )
        logger.info("Remediation completed for bucket: %s", bucket_name)
    except ClientError as err:
        remediation_status = "FAILED"
        remediation_details = str(err)
        logger.error("Remediation failed for %s: %s", bucket_name, err)

    # 2. Dispatch Incident Alert via Amazon SNS
    subject = f"🚨 [SECOP-ALERT] Automated Remediation: S3 Drift on {bucket_name}"
    message = (
        "=== SECURITY OPERATIONS ALERT: INCIDENT DETECTED & REMEDIATED ===\n\n"
        f"Frameworks Aligned : NIST SP 800-53 (SI-4/IR-4), CIS Benchmark 2.1.4\n"
        f"Target Resource     : arn:aws:s3:::{bucket_name}\n"
        f"Triggering API Call : {event_name}\n"
        f"Event Source        : {event_source}\n"
        f"Timestamp (UTC)     : {event_time}\n"
        f"Triggered By (IAM)  : {iam_principal}\n"
        f"Source IP Address   : {source_ip}\n\n"
        "--- ACTION TAKEN ---\n"
        f"Remediation Status  : {remediation_status}\n"
        f"Action Performed    : put_public_access_block (Full Lockout: True)\n"
        f"Remediation Logs    : {remediation_details}\n"
    )

    if SNS_TOPIC_ARN:
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN, Subject=subject[:100], Message=message
            )
            logger.info("SNS notification dispatched.")
        except ClientError as sns_err:
            logger.error("Failed to publish SNS message: %s", sns_err)
    else:
        logger.warning("SNS_TOPIC_ARN environment variable not set.")

    return {
        "statusCode": 200,
        "bucket": bucket_name,
        "remediation": remediation_status,
    }
