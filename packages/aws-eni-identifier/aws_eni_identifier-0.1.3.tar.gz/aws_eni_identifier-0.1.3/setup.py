# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_eni_identifier']

package_data = \
{'': ['*']}

install_requires = \
['glom>=23.1.1,<24.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aws-eni-identifier = aws_eni_identifier.cli:app']}

setup_kwargs = {
    'name': 'aws-eni-identifier',
    'version': '0.1.3',
    'description': 'Identify to which AWS service network interface is associated',
    'long_description': '# aws-eni-identifier\nIdentify to which AWS service network interface is associated\n\n![aws-eni-identifier-cli.png](docs/aws-eni-identifier-cli.png?raw=true)\n\n# Installation\n\n```bash\npip install aws-eni-identifier\n```\n\n# Usage\naws-eni-identifier does not connect to AWS by itself, so you will need to load data with aws-cli\n\nLogin to aws:\n```bash\naws sso login --profile my-profile\n```\n\nUse pipe:\n```bash\naws ec2 describe-network-interfaces | aws-eni-identifier\n```\n\nOr save to file with aws-cli and read it:\n```bash\naws ec2 describe-network-interfaces > ni.json\naws-eni-identifier -i ni.json\n```\n\n## Show extra columns\n```bash\naws ec2 describe-network-interfaces | \naws-eni-identifier \\\n    --add-column Attachment.Status \\\n    --add-column AvailabilityZone\n```\n![extra-columns.png](docs/extra-columns.png?raw=true)\n\n## Filter\nFind unused network interfaces:\n```bash \naws ec2 describe-network-interfaces \\\n    --filters "Name=status,Values=available" |\naws-eni-identifier\n```\nFind AWS resource by IP address (you can use public or private IP address)\n```bash \nexport IP=\'51.21.223.193\';\naws ec2 describe-network-interfaces \\\n    --query "NetworkInterfaces[?PrivateIpAddresses[?PrivateIpAddress==\'${IP}\' || Association.PublicIp==\'${IP}\']]" | \naws-eni-identifier\n```\nDetermine what is using specific AWS network interface\n```bash\naws ec2 describe-network-interfaces \\\n    --network-interface-ids eni-0068ac3f8786de59a | \naws-eni-identifier\n```\n\nYou can find more information about filters and queries in [AWS documentation](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-network-interfaces.html#options)\n \n\n# Developing\n\nInstall the package:\n```bash\npoetry install\n```\nRun tests:\n```bash\npoetry run pytest\n```',
    'author': 'Eremin',
    'author_email': 'haru.eaa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fivexl/aws-eni-identifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
