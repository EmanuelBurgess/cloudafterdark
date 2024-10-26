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

def extract_ado_from_role(role):
    """Extracts the ADO from the given role string.

    Args:
        role: The role string, e.g., "beneapi-admin"

    Returns:
        The ADO part of the role, e.g., "beneapi"
    """

    return role.split("-")[0]

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
        f"Request is for {subject}, parsed unqualified subject string for auth check is {subject_unqualified_name}")

    # Extract the ADO from the role
    ado = extract_ado_from_role(role)

    # Check if the ADO is in the JWTS_BY_ROLE keys
    if ado not in JWTS_BY_ROLE.keys():
        logging.warning(f"Unauthorized ADO: {ado}")
        return False

    
    parse_role = role.split("-")[2:]
    parse_role = "-".join(parse_role)
    logging.debug(
        f"Request is for {role}, parsed unqualified role string for auth check is {parse_role}"
    )

    if role == OSRE_POWERUSER:
        return True
    elif subject_unqualified_name in JWTS_BY_ROLE[parse_role]:
        return True
    else:
        return False


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
