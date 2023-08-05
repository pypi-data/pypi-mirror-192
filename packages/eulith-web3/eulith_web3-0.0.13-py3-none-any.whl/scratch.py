import boto3

from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.kms import KmsSigner
from eulith_web3.signing import construct_signing_middleware
from eulith_web3.swap import EulithSwapRequest

if __name__ == '__main__':
    aws_credentials_profile_name = 'kristian'
    key_name = 'SPEED_RACE_COMPETITOR'
    formatted_key_name = f'alias/{key_name}'

    session = boto3.Session(profile_name=aws_credentials_profile_name)
    client = session.client('kms')
    kms_signer = KmsSigner(client, formatted_key_name)

    ew3 = EulithWeb3(eulith_url="https://eth-main.eulithrpc.com/v0",
                     eulith_refresh_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJzdWIiOiJyYWNlciIsImV4cCI6MTcwNzk3OTMyMCwic291cmNlX2hhc2giOiIqIiwic2NvcGUiOiJBUElSZWZyZXNoIn0.18UGdXx-Z5jJYdD5Xy6ZpO-ltebOefcvuURsYFZcXPVJCSbYbH4bD70VDrIHBipiEwwhzp4mEeCKgO40Wt4mPRw",
                     signing_middle_ware=construct_signing_middleware(kms_signer))

    # these are python bindings around the whole ERC20 contract
    weth = ew3.eulith_get_erc_token(TokenSymbol.WETH)
    uni = ew3.eulith_get_erc_token(TokenSymbol.UNI)

    sell_amount = 0.001  # just an arbitrary small number for example

    # set the swap parameters
    swap_params = EulithSwapRequest(
        sell_token=weth,
        buy_token=uni,
        sell_amount=sell_amount)  # quantity; no annoying decimals, 0.001 means 0.001 WETH

    # get a swap quote
    # txs is an array of transactions that make up the swap
    # this array has the necessary ERC20 approvals & swaps
    quote, txs = ew3.eulith_swap_quote(swap_params)

    # convert eth to weth to prepare for the swap
    # we're passing in the gas and from address as override parameters to bypass "pre-tx logic" which would
    # otherwise try to estimate gas and infer the from address from the signer
    # that "pre-tx logic" is a web3py thing that (in our opinion) just gets in the way and slows things down
    eth_to_weth_tx = weth.deposit_eth(sell_amount, override_tx_parameters={'from': kms_signer.address, 'gas': 100000})
    tx_hash = ew3.eth.send_transaction(eth_to_weth_tx).hex()
    print(f"WETH Deposit hash: {tx_hash}")

    # the quote is the price of buy_token denominated in sell_token
    # so cheaper is better
    if quote < 0.005:
        # if you decide you like the quote, send the swap transactions
        # we're doing this in a non-atomic context for this quick start so every since tx has to confirm
        # in order (separately). Later, we'll show you how to bundle this all up into a single tx.
        ew3.eulith_send_multi_transaction(txs)
