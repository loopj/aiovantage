from ssl import SSLContext, PROTOCOL_TLS_CLIENT, CERT_NONE


def create_ssl_context() -> SSLContext:
    """
    Creates a default SSL context that doesn't verify hostname or certificate.

    We don't have a local issuer certificate to check against, and we'll most likely be
    connecting to an IP address, so we can't check the hostname.
    """

    context = SSLContext(PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = CERT_NONE
    return context
