from apps.nem.transactions import *
from apps.nem.layout import *
from trezor.messages.NEMSignTx import NEMSignTx
from trezor.messages.NEMSignedTx import NEMSignedTx


async def nem_sign_tx(ctx, msg: NEMSignTx):
    from ..common import seed
    from trezor.crypto.hashlib import sha3_256
    from trezor.crypto.curve import ed25519

    # if len(msg.transfer.public_key):
        # todo encrypt

    node = await seed.derive_node(ctx, msg.transaction.address_n, NEM_CURVE)

    tx = nem_transaction_create_transfer(
        msg.transaction.network,
        msg.transaction.timestamp,
        node.public_key(),  # todo?
        msg.transaction.fee,
        msg.transaction.deadline,
        msg.transfer.recipient,
        msg.transfer.amount,
        msg.transfer.payload,  # todo might require encryption
        msg.transfer.public_key is not None,
        len(msg.transfer.mosaics)
    )

    for mosaic in msg.transfer.mosaics:
        nem_transaction_write_mosaic(tx, mosaic.namespace, mosaic.mosaic, mosaic.quantity)

    await require_confirm_action(ctx)
    await require_confirm_fee(ctx, msg.transfer.amount, msg.transaction.fee)
    await require_confirm_tx(ctx, msg.transfer.recipient, msg.transfer.amount)

    sha = sha3_256(tx)
    digest = sha.digest(True)

    signature = ed25519.sign(node.private_key(), digest)

    resp = NEMSignedTx()
    resp.signature = signature
    return resp


# async def sign(ctx, msg: NEMSignTx, digest) -> bytes:
#
#     return signature


# def node_derive(root, address_n: list):
#     node = root.clone()
#     node.derive_path(address_n)
#     return node
