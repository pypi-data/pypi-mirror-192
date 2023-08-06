# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smol_evm']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'eth-utils[pycryptodome]>=2.0.0,<3.0.0',
 'pycryptodome>=3.15.0,<4.0.0',
 'tomlkit>=0.11.5,<0.12.0']

entry_points = \
{'console_scripts': ['smol-evm = cli:cli']}

setup_kwargs = {
    'name': 'smol-evm',
    'version': '0.1.0',
    'description': '👨\u200d🔬 An extensible Python implementation of the Ethereum yellow paper from scratch.',
    'long_description': '# smol-evm\n\n👨\u200d🔬 An extensible Python implementation of the Ethereum yellow paper from scratch.\n\nWrite-up with examples:\n\n[Building an EVM from scratch](https://karmacoma.notion.site/Building-an-EVM-from-scratch-series-90ee3c827b314e0599e705a1152eecf9) [karmacoma.notion.so]\n\n# Getting started\n\n> Install smol-evm\n\n```\npip install smol-evm\n```\n\n> Run the CLI\n\n```\n$ smol-evm --help\nUsage: smol-evm [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --debug / --no-debug\n  --help                Show this message and exit.\n\nCommands:\n  disassemble  Disassembles the given bytecode\n  run          Creates an EVM execution context and runs the given bytecode\n\n$ smol-evm run\n````\n\n> Execute bytecode\n\n```bash\n$ smol-evm run --code 602a6000526001601ff3 --no-trace\n0x2a\n```\n\n> Disassemble bytecode\n\n```bash\n$ smol-evm disassemble --code 602a6000526001601ff3\n0000: PUSH1 0x2a\n0002: PUSH1 0x00\n0004: MSTORE\n0005: PUSH1 0x01\n0007: PUSH1 0x1f\n0009: RETURN\n```\n\n> Assemble bytecode\n\n```bash\nsmol-evm disassemble --code 602a6000526001601ff3 | smol-evm assemble -\n602a6000526001601ff3\n```\n\n> Use as a library\n\n⚠️ the interface is very much not stable and is subject to frequent changes\n\n```bash\npython\n>>> from smol_evm.opcodes import *\n>>> code = assemble([PC, DUP1, MSTORE])\n588052\n```\n\n# Developer mode\n\n> Install Poetry\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\n> Install Dependencies\n\n```bash\npoetry install\n```\n\n> Run Tests\n\n```bash\npoetry run pytest -v\n```\n\n> Run the `black` code formatter\n\n```bash\npoetry run black src\n```\n\n# Misc scripts\n\n## raw_deployer.py\n\nTakes the binary representation of a contract and generates the init code that will deploy that contract (Ti in Yellow Paper terminology).\n\nFor instance, let\'s say that you have some Yul code, that when compiled with `solc` has the following binary representation: `602a60205260206020f3`.\n\n```\n> python raw_deployer.py 602a60205260206020f3\n600a8061000d6000396000f3fe602a60205260206020f3\n```\n\nYou can now deploy this code:\n\n```javascript\nweb3.eth.sendTransaction({\n    from: /* your address */,\n    /* no to address as we are creating a contract */\n    data: "600a8061000d6000396000f3fe602a60205260206020f3"\n})\n```\n\nWait for the transaction to be confirmed, and go look at the code of the contract that was deployed, it should match our compiled Yul code `602a60205260206020f3` 🙌\n\n\n## create2.py\nBased on web3.py, this script can find addresses of contracts deployed by the `CREATE2` opcode that satisfy a particular predicate.\n\nUsage: `python3 create2.py deployer_addr <salt | predicate> bytecode`\n\nWhen passing a salt value, this script prints the address of the newly deployed contract based on the deployer address and bytecode hash.\n\nExample: `python3 create2.py Bf6cE3350513EfDcC0d5bd5413F1dE53D0E4f9aE 42 602a60205260206020f3`\n\nWhen passing a predicate, this script will search for a salt value such that the new address satisfies the predicate.\n\nExample: `python3 create2.py Bf6cE3350513EfDcC0d5bd5413F1dE53D0E4f9aE \'lambda addr: "badc0de" in addr.lower()\' 602a60205260206020f3`\n\nAnother predicate that may be useful: `\'lambda addr: addr.startswith("0" * 8)\'`\n\nUse with a deployer contract like this:\n\n```solidity\ncontract Deployer {\n    function deploy(bytes memory code, uint256 salt) public returns(address) {\n        address addr;\n        assembly {\n          addr := create2(0, add(code, 0x20), mload(code), salt)\n          if iszero(extcodesize(addr)) {\n            revert(0, 0)\n          }\n        }\n\n        return addr;\n    }\n}\n```\n',
    'author': 'karmacoma',
    'author_email': 'karma@coma.lol',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/karmacoma-eth/smol-evm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
