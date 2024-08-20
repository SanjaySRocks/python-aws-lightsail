import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def remove_all_ports():
    """
    Remove all public ports for an AWS Lightsail instance.

    Parameters:
    - instance_name (str): The name of the Lightsail instance.

    Returns:
    - response: The response from the put_instance_public_ports API call.
    """
    try:
        # Initialize the Lightsail client
        session = boto3.Session(profile_name="daisy", region_name="ap-south-1")
        client = session.client('lightsail')

        # Remove all ports by configuring the instance with no open ports
        response = client.put_instance_public_ports(
            portInfos=[],  # Empty list to close all ports
            instanceName="Debian-1"
        )

        print("All ports configuration removed.")
        return response

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def configure_instance_ports(instance_name, from_port, to_port, protocol, cidrs=None, ipv6_cidrs=None, cidr_list_aliases=None):
    """
    Configure public ports for an AWS Lightsail instance.

    Parameters:
    - instance_name (str): The name of the Lightsail instance.
    - from_port (int): The starting port number.
    - to_port (int): The ending port number.
    - protocol (str): The protocol ('tcp', 'udp', 'icmp', 'icmpv6', or 'all').
    - cidrs (list): List of IPv4 CIDR blocks.
    - ipv6_cidrs (list): List of IPv6 CIDR blocks.
    - cidr_list_aliases (list): List of CIDR list aliases (e.g., 'all').
    
    Returns:
    - response: The response from the put_instance_public_ports API call.
    """

    # Ensure cidrs, ipv6_cidrs, and cidr_list_aliases are lists (or empty lists if not provided)
    cidrs = cidrs or []
    ipv6_cidrs = ipv6_cidrs or []
    cidr_list_aliases = cidr_list_aliases or []

    try:
        # Initialize the Lightsail client
        session = boto3.Session(profile_name="daisy", region_name="ap-south-1")

        client = session.client('lightsail')

        # Configure the public ports
        response = client.put_instance_public_ports(
            portInfos=[
                {
                    'fromPort': from_port,
                    'toPort': to_port,
                    'protocol': protocol,
                    'cidrs': cidrs,
                    'ipv6Cidrs': ipv6_cidrs,
                    'cidrListAliases': cidr_list_aliases,
                },
            ],
            instanceName=instance_name
        )

        print("Port configuration successful.")
        return response

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

# For Test Purpose
import random
import ipaddress
def generate_random_ips(n=60):
    ip_list = []
    for _ in range(n):
        # Generate a random IP address
        ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
        # Append the /32 subnet mask
        ip_list.append(f"{ip}/32")
    return ip_list


# Example usage
if __name__ == "__main__":
    # can take max 60 ips 
    ip_addressx = generate_random_ips()
    instance_name = 'Debian-1'
    from_port = 27015
    to_port = 27015
    protocol = 'tcp'
    cidrs = ip_addressx  # Allow access from any IPv4 address
    ipv6_cidrs = []  # Allow access from any IPv6 address
    cidr_list_aliases = []  # Use 'all' alias

    response = configure_instance_ports(instance_name, from_port, to_port, protocol, cidrs, ipv6_cidrs, cidr_list_aliases)
    # response = remove_all_ports()
    
    if response:
        print(response)
