import boto3
from botocore.exceptions import NoCredentialsError, ClientError


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

# Example usage
if __name__ == "__main__":
    # can take max 60 ips 
    ip_addressx = ['176.193.28.232/32', '115.235.198.236/32', '201.47.119.185/32', '122.176.153.64/32', '139.10.160.53/32', '99.58.197.191/32', '47.179.16.36/32', '225.124.48.239/32', '25.102.54.206/32', '96.65.61.56/32', '221.44.26.9/32', '187.206.162.152/32', '213.230.135.82/32', '106.240.15.136/32', '124.10.173.18/32', '236.138.74.100/32', '72.251.205.98/32', '107.226.165.228/32', '240.120.239.166/32', '215.68.159.67/32', '71.240.72.217/32', '210.65.70.195/32', '42.73.99.50/32', '126.10.236.72/32', '42.95.65.223/32', '53.135.252.138/32', '247.186.234.25/32', '206.130.51.217/32', '60.118.9.40/32', '181.86.141.130/32', '252.238.25.147/32', '50.107.180.133/32', '125.230.232.192/32', '153.194.49.255/32', '234.96.104.126/32', '20.187.99.191/32', '90.201.238.125/32', '195.129.59.235/32', '123.247.208.51/32', '225.10.242.220/32', '126.176.183.23/32', '148.106.132.230/32', '222.16.134.122/32', '139.54.119.197/32', '43.218.22.74/32', '125.159.31.48/32', '241.77.100.15/32', '118.187.123.116/32', '250.197.15.34/32', '237.15.176.76/32', '90.27.153.215/32', '214.62.20.117/32', '16.242.184.151/32', '27.205.52.10/32', '154.59.225.3/32', '7.163.31.45/32', '171.191.11.159/32', '34.130.114.235/32', '75.253.97.187/32', '117.229.79.125/32']
    instance_name = 'Debian-1'
    from_port = 27015
    to_port = 27015
    protocol = 'tcp'
    cidrs = ip_addressx  # Allow access from any IPv4 address
    ipv6_cidrs = []  # Allow access from any IPv6 address
    cidr_list_aliases = []  # Use 'all' alias

    response = configure_instance_ports(instance_name, from_port, to_port, protocol, cidrs, ipv6_cidrs, cidr_list_aliases)
    if response:
        print(response)
