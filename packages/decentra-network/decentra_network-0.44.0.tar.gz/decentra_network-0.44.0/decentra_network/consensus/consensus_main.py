#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import threading

from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.finished.finished_main import finished_main
from decentra_network.consensus.ongoing.ongoing_main import ongoing_main
from decentra_network.lib.log import get_logger
from decentra_network.lib.perpetualtimer import perpetualTimer
from decentra_network.node.client.client import client
from decentra_network.node.server.server import server
from decentra_network.transactions.cleaner import Cleaner
from decentra_network.transactions.pending.get_pending import GetPending

from decentra_network.consensus.sync.sync import sync

logger = get_logger("CONSENSUS")


def consensus_trigger(
    custom_block: Block = None,
    custom_candidate_class: candidate_block = None,
    custom_unl_nodes: dict = None,
    custom_UNL_NODES_PATH: str = None,
    custom_server: server = None,
    custom_unl: client = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_BLOCKS_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
    pass_sync: bool = False,
) -> Block:
    """
    Consensus process consists of 2 stages. This function makes
    the necessary redirects according to the situation and works
    to shorten the block time.
    """

    block = (GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
             if custom_block is None else custom_block)
    pending_list_txs = GetPending()

    logger.info(
        f"BLOCK#{block.sequence_number}:{block.empty_block_number} Consensus process started"
    )

    logger.info("Consensus Sync process started")
    threading.Thread(
        target=sync,
        args=(
            block,
            pending_list_txs,
            custom_server,
        ),
    ).start()

    if block.validated:
        logger.info("BLOCK is an validated block, consensus process is finished")
        finished_main(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=pass_sync,
        )
    else:
        logger.info("BLOCK is an unvalidated block, consensus process is ongoing")
        ongoing_main(
            block,
            custom_candidate_class=custom_candidate_class,
            custom_unl_nodes=custom_unl_nodes,
            custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
            custom_server=custom_server,
            custom_unl=custom_unl,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=pass_sync,
        )


    logger.info("Consensus process is done")
    return block
