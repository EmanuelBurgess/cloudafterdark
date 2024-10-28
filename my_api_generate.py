import datetime
import json
import logging
import mpse_jwt_generator
import os

OSRE_POWERUSER = "ct-ado-mpsm-poweruser"
JWTS_BY_ROLE = {
    "beneapi-admin": ["TEST:BeneMSP"],
    "da-admin": ["TEST:DentalAdju", "TEST:DAManual"],
    "dsbv-admin": ["TEST:DentalBene"],
    "dsi-admin": ["TEST:DentalCI"],
    "dmod-admin": ["TEST:DMODJIT"],
    "mcm-bene-admin": ["TEST:CMMIMCMBene"],
    "mist-admin": ["TEST:MIST", "TEST:Skyward"],
    "pcs-admin": ["TEST:PCS"],
    "rda-admin": ["DEV:RDA"]
}
JWT_ISSUER = 'osre-ops@navapbc.com'
JWT_CONTRACT_MAP_FILE = 'rq2w-contract-id-map.csv'

def handler(event, context):
    loglevel = logging.getLevelNamesMapping()[os.getenv("LOGLEVEL", "INFO")]
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(loglevel)
    else:
        logging.basicConfig(level=loglevel)

    subject = event["pathParameters"]["subject"]

    requester_principal_arn = event["requestContext"]["identity"]["userArn"]
    logging.debug(f"Full requester ARN is {requester_principal_arn}")
    # Example: arn:aws:sts::051277838191:assumed-role/ct-ado-mpsm-poweruser/E33C
    requester_iam_session = requester_principal_arn.split("/")[-1]
    requester_iam_role = requester_principal_arn.split("/")[-2]
    logging.info(
        f"Session {requester_iam_session} as role {requester_iam_role} requesting JWT {subject}")

    authorized = check_authorization(subject, requester_iam_role)
    if not authorized:
        msg = f"Session {requester_iam_session} with assumed-role {requester_iam_role} is not authorized for JWT {subject}"
        logging.error(msg)
        return {
            "isBase64Encoded": False,
            "statusCode": 403,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"status": "403 Forbidden", "message": msg})
        }

    try:
        jwt = generate_jwt(subject)
    except Exception as e:
        msg = f"Error generating JWT: {str(e)}"
        logging.error(msg)
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"status": "400 Bad Request", "message": msg})
        }

    logging.info(f"Returning JWT {subject} to session {requester_iam_session}")
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"jwt": jwt})
    }
def check_authorization(subject: str, role: str) -> bool:
    subject_unqualified_name = subject.rpartition(":")[0]
    logging.debug(
        f"Request is for {subject}, parsed unqualified subject string for auth check is {subject_unqualified_name}"
    )

    if role == OSRE_POWERUSER:
        return True

    # Extract the ADO and environment from the role
    role_parts = role.split("-")
    if len(role_parts) < 3 or not role.startswith('ado-'):
        logging.warning(f"Invalid role format: {role}")
        return False

    env = role_parts[1]
    ado = "-".join(role_parts[2:])
    
   

    # Check if the environment is valid
    if env not in ["dev", "impl", "prod"]:
        logging.warning(f"Unauthorized environment: {env}")
        return False

    # Check if the ADO is in the JWTS_BY_ROLE keys
    if ado not in JWTS_BY_ROLE.keys():
        logging.warning(f"Unauthorized ADO: {ado}")
        return False

    # Check if the subject is authorized for the ADO
    return subject_unqualified_name in JWTS_BY_ROLE[ado]

def generate_jwt(subject: str) -> str:
    environment = os.getenv("ENV", "dev")
    environment = "uat" if environment == "impl" else environment
    expiration = int((datetime.datetime.now(tz=datetime.UTC) +
                      datetime.timedelta(days=1)).timestamp())

    logging.debug(
        f"Creating JWT with subject {subject}, for environment {environment}, expiration {expiration}")

    generator = mpse_jwt_generator.MpseJwtGenerator(issuer=JWT_ISSUER,
                                                    contract_id_filepath=JWT_CONTRACT_MAP_FILE, env=environment)
    jwt = generator.generate_jwt(
        subject, environment, expiration, 'SCRAPER_API')
    return jwt
# Sample event data
event = {
    "pathParameters": {
        "subject": "TEST:DentalAdju:02"
    },
    "requestContext": {
        "identity": {
            "userArn": "arn:aws:blahblah/ado-prod-da-admin/AB23"
        }
    }
}

# Context is usually empty for local testing
context = {}

# Call the handler function
response = handler(event, context)

# Print the response
print(response)
