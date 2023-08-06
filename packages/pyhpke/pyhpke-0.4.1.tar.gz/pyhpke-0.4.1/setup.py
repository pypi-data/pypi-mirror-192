# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhpke', 'pyhpke.kem_primitives', 'pyhpke.keys']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36,<40']

extras_require = \
{'docs': ['Sphinx[docs]>=4.3.2,<6.0.0',
          'sphinx-autodoc-typehints[docs]==1.21.0',
          'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'pyhpke',
    'version': '0.4.1',
    'description': 'A Python implementation of HPKE.',
    'long_description': '# PyHPKE - A Python implementation of HPKE\n\n[![PyPI version](https://badge.fury.io/py/pyhpke.svg)](https://badge.fury.io/py/pyhpke)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyhpke)\n[![Documentation Status](https://readthedocs.org/projects/pyhpke/badge/?version=latest)](https://pyhpke.readthedocs.io/en/latest/?badge=latest)\n![Github CI](https://github.com/dajiaji/pyhpke/actions/workflows/python-package.yml/badge.svg)\n[![codecov](https://codecov.io/gh/dajiaji/pyhpke/branch/main/graph/badge.svg?token=QN8GXEYEP3)](https://codecov.io/gh/dajiaji/pyhpke)\n\n\nPyHPKE is a [HPKE (Hybrid Public Key Encryption)](https://www.rfc-editor.org/rfc/rfc9180.html) implementation written in Python.\n\nYou can install PyHPKE with pip:\n\n```sh\n$ pip install pyhpke\n```\n\nAnd then, you can use it as follows:\n\n\n```py\nfrom pyhpke import AEADId, CipherSuite, KDFId, KEMId, KEMKey\n\n# The sender side:\nsuite_s = CipherSuite.new(KEMId.DHKEM_P256_HKDF_SHA256, KDFId.HKDF_SHA256, AEADId.AES128_GCM)\npkr = KEMKey.from_jwk(  # from_pem is also available.\n    {\n        "kid": "01",\n        "kty": "EC",\n        "crv": "P-256",\n        "x": "Ze2loSV3wrroKUN_4zhwGhCqo3Xhu1td4QjeQ5wIVR0",\n        "y": "HlLtdXARY_f55A3fnzQbPcm6hgr34Mp8p-nuzQCE0Zw",\n    }\n)\nenc, sender = suite_s.create_sender_context(pkr)\nct = sender.seal(b"Hello world!")\n\n# The recipient side:\nsuite_r = CipherSuite.new(KEMId.DHKEM_P256_HKDF_SHA256, KDFId.HKDF_SHA256, AEADId.AES128_GCM)\nskr = KEMKey.from_jwk(\n    {\n        "kid": "01",\n        "kty": "EC",\n        "crv": "P-256",\n        "x": "Ze2loSV3wrroKUN_4zhwGhCqo3Xhu1td4QjeQ5wIVR0",\n        "y": "HlLtdXARY_f55A3fnzQbPcm6hgr34Mp8p-nuzQCE0Zw",\n        "d": "r_kHyZ-a06rmxM3yESK84r1otSg-aQcVStkRhA-iCM8",\n    }\n)\nrecipient = suite_r.create_recipient_context(enc, skr)\npt = recipient.open(ct)\n\nassert pt == b"Hello world!"\n```\n\n## Index\n\n- [Installation](#installation)\n- [Supported HPKE Modes and Cipher Suites](#supported-hpke-modes-and-cipher-suites)\n- [Warnings and Restrictions](#warnings-and-restrictions)\n- [Usage](#usage)\n- [API Reference](#api-reference)\n- [Test](#test)\n- [Contributing](#contributing)\n\n## Installation\n\nYou can install PyHPKE with pip:\n\n```sh\n$ pip install pyhpke\n```\n\n## Supported HPKE Modes and Cipher Suites\n\nPyHPKE supports all of the HPKE modes and cipher suites defined in RFC9180 below.\n\n- modes\n    - ✅ Base\n    - ✅ PSK\n    - ✅ Auth\n    - ✅ AuthPSK\n- KEMs (Key Encapsulation Machanisms)\n    - ✅ DHKEM (P-256, HKDF-SHA256)\n    - ✅ DHKEM (P-384, HKDF-SHA384)\n    - ✅ DHKEM (P-521, HKDF-SHA512)\n    - ✅ DHKEM (X25519, HKDF-SHA256)\n    - ✅ DHKEM (X448, HKDF-SHA512)\n- KDFs (Key Derivation Functions)\n    - ✅ HKDF-SHA256\n    - ✅ HKDF-SHA384\n    - ✅ HKDF-SHA512\n- AEADs (Authenticated Encryption with Associated Data)\n    - ✅ AES-128-GCM\n    - ✅ AES-256-GCM\n    - ✅ ChaCha20Poly1305\n    - ✅ Export Only\n\n## Warnings and Restrictions\n\nAlthough this library has been passed all of the following official test vectors, it has not been formally audited.\n- [RFC9180 official test vectors provided on github.com/cfrg/draft-irtf-cfrg-hpke](https://github.com/cfrg/draft-irtf-cfrg-hpke/blob/5f503c564da00b0687b3de75f1dfbdfc4079ad31/test-vectors.json)\n\n## Usage\n\n```py\nfrom pyhpke import AEADId, CipherSuite, KDFId, KEMId, KEMKey\n\n# The sender side:\nsuite_s = CipherSuite.new(KEMId.DHKEM_P256_HKDF_SHA256, KDFId.HKDF_SHA256, AEADId.AES128_GCM)\npkr = KEMKey.from_jwk(\n    {\n        "kid": "01",\n        "kty": "EC",\n        "crv": "P-256",\n        "x": "Ze2loSV3wrroKUN_4zhwGhCqo3Xhu1td4QjeQ5wIVR0",\n        "y": "HlLtdXARY_f55A3fnzQbPcm6hgr34Mp8p-nuzQCE0Zw",\n    }\n)\nenc, sender = suite_s.create_sender_context(pkr)\nct = sender.seal(b"Hello world!")\n\n# The recipient side:\nsuite_r = CipherSuite.new(KEMId.DHKEM_P256_HKDF_SHA256, KDFId.HKDF_SHA256, AEADId.AES128_GCM)\nskr = KEMKey.from_jwk(\n    {\n        "kid": "01",\n        "kty": "EC",\n        "crv": "P-256",\n        "x": "Ze2loSV3wrroKUN_4zhwGhCqo3Xhu1td4QjeQ5wIVR0",\n        "y": "HlLtdXARY_f55A3fnzQbPcm6hgr34Mp8p-nuzQCE0Zw",\n        "d": "r_kHyZ-a06rmxM3yESK84r1otSg-aQcVStkRhA-iCM8",\n    }\n)\nrecipient = suite_r.create_recipient_context(enc, skr)\npt = recipient.open(ct)\n\nassert pt == b"Hello world!"\n```\n\n## API Reference\n\nSee [Documentation](https://pyhpke.readthedocs.io/en/stable/api.html).\n\n## Test\n\nYou can run tests from the project root after cloning with:\n\n```sh\n$ tox\n```\n\n## Contributing\n\nWe welcome all kind of contributions, filing issues, suggesting new features or sending PRs.\n',
    'author': 'Ajitomi Daisuke',
    'author_email': 'dajiaji@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dajiaji/pyhpke',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
