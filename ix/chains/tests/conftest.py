import uuid

from ix.chains.fixture_src.lcel import RUNNABLE_BRANCH_CLASS_PATH
from ix.chains.loaders.core import BranchPlaceholder
from ix.chains.models import ChainNode, NodeType
from ix.chains.tests.fake import (
    afake_node_sequence,
    afake_node_map,
    afake_node_branch,
    afake_chain_edge,
    afake_runnable,
)
from ix.task_log.tests.fake import afake_chain
import pytest_asyncio


@pytest_asyncio.fixture
async def lcel_sequence(anode_types) -> dict:
    chain = await afake_chain()
    nodes = await afake_node_sequence(chain=chain)

    return {
        "chain": chain,
        "nodes": nodes,
    }


@pytest_asyncio.fixture
async def lcel_map(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=True)
    map_placeholder = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
            "b": node2,
        },
    )
    return dict(chain=chain, map=map_placeholder, node1=node1, node2=node2)


@pytest_asyncio.fixture
async def lcel_map_with_one_branch(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    map_placeholder = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
        },
    )
    return dict(chain=chain, map=map_placeholder, node1=node1)


@pytest_asyncio.fixture
async def lcel_sequence_in_map_start(anode_types) -> dict:
    """Map contains a sequence and the map is the first node in the chain."""
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_sequence = await afake_node_sequence(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=True)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
            "b": inner_sequence,  # last node in sequence gets edge to map
            "c": node2,
        },
        root=False,
    )
    return {
        "chain": chain,
        "node1": node1,
        "inner_sequence": inner_sequence,
        "node2": node2,
        "map": node_map,
    }


@pytest_asyncio.fixture
async def lcel_sequence_in_map_in_sequence(anode_types) -> dict:
    """Map contains a sequence and the map is the first node in the chain."""
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    inner_sequence = await afake_node_sequence(chain=chain, root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    inner_map = await afake_node_map(
        chain=chain,
        input_node=node1,
        nodes={
            "a": node2,
            "b": inner_sequence[-1],  # last node in sequence gets edge to map
            "c": node3,
        },
        root=False,
    )
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            inner_map,
            node4,
        ],
    )
    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "inner_sequence": inner_sequence,
        "sequence": sequence,
        "map": inner_map,
    }


@pytest_asyncio.fixture
async def lcel_sequence_in_map_in_sequence_n2(anode_types) -> dict:
    """Map contains a sequence and the map is the first node in the chain.

    The sequence ends in n=2 nodes.
    """
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    inner_sequence = await afake_node_sequence(chain=chain, root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    node5 = await afake_runnable(chain=chain, name="node5", root=False)
    inner_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node2,
            "b": inner_sequence[-1],  # last node in sequence gets edge to map
            "c": node3,
        },
        root=False,
    )
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            inner_map,
            node4,
            node5,
        ],
        root=False,
    )
    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
        "inner_sequence": inner_sequence,
        "sequence": sequence,
        "map": inner_map,
    }


@pytest_asyncio.fixture
async def lcel_map_in_sequence(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_map = await afake_node_map(chain=chain, input_node=node1, root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            inner_map,
            node2,
        ],
        root=False,
    )
    return {
        "chain": chain,
        "sequence": sequence,
        "node1": node1,
        "map": inner_map,
        "node2": node2,
    }


@pytest_asyncio.fixture
async def lcel_map_in_sequence_n2(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_map = await afake_node_map(chain=chain, root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            inner_map,
            node2,
            node3,
        ],
        root=False,
    )
    return {
        "chain": chain,
        "sequence": sequence,
        "node1": node1,
        "map": inner_map,
        "node2": node2,
        "node3": node3,
    }


@pytest_asyncio.fixture
async def lcel_map_in_sequence_start(anode_types) -> dict:
    chain = await afake_chain()
    inner_map = await afake_node_map(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            inner_map,
            node2,
        ],
        root=False,
    )
    return {
        "chain": chain,
        "sequence": sequence,
        "map": inner_map,
        "node2": node2,
    }


@pytest_asyncio.fixture
async def lcel_map_in_sequence_start_n2(anode_types) -> dict:
    chain = await afake_chain()
    inner_map = await afake_node_map(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            inner_map,
            node2,
            node3,
        ],
        root=False,
    )
    return {
        "chain": chain,
        "sequence": sequence,
        "map": inner_map,
        "node2": node2,
        "node3": node3,
    }


@pytest_asyncio.fixture
async def lcel_map_in_map(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_map = await afake_node_map(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=True)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
            "b": inner_map,
            "c": node2,
        },
    )
    return {
        "chain": chain,
        "node1": node1,
        "inner_map": inner_map,
        "node2": node2,
        "map": node_map,
    }


@pytest_asyncio.fixture
async def lcel_map_in_map_in_sequence_start(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_map = await afake_node_map(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=True)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
            "b": inner_map,
            "c": node2,
        },
        root=True,
    )
    node3 = await afake_runnable(chain=chain, name="node3", root=False)

    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node_map,
            node3,
        ],
        root=False,
    )

    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "inner_map": inner_map,
        "map": node_map,
        "sequence": sequence,
    }


@pytest_asyncio.fixture
async def lcel_map_in_map_in_sequence_start_n2(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    inner_map = await afake_node_map(chain=chain, root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=True)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node1,
            "b": inner_map,
            "c": node2,
        },
        root=True,
    )
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)

    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node_map,
            node3,
            node4,
        ],
        root=False,
    )

    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "inner_map": inner_map,
        "map": node_map,
        "sequence": sequence,
    }


@pytest_asyncio.fixture
async def lcel_map_in_map_in_sequence(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    inner_map = await afake_node_map(chain=chain, root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node2,
            "b": inner_map,
            "c": node3,
        },
        root=False,
    )

    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[node1, node_map],
        root=False,
    )

    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "inner_map": inner_map,
        "map": node_map,
        "sequence": sequence,
    }


@pytest_asyncio.fixture
async def lcel_map_in_map_in_sequence_n2(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=True)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    inner_map = await afake_node_map(chain=chain, root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    node5 = await afake_runnable(chain=chain, name="node5", root=False)
    node_map = await afake_node_map(
        chain=chain,
        nodes={
            "a": node2,
            "b": inner_map,
            "c": node3,
        },
        root=False,
    )

    sequence = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            node_map,
            node4,
            node5,
        ],
        root=False,
    )

    return {
        "chain": chain,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
        "inner_map": inner_map,
        "map": node_map,
        "sequence": sequence,
    }


@pytest_asyncio.fixture
async def lcel_branch(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        default=node1,
        branches=[
            ("a", node2),
            ("b", node3),
        ],
    )

    assert await chain.nodes.filter(root=True).acount() == 1
    return {
        "chain": chain,
        "branch": branch,
        "node1": node1,
        "node2": node2,
        "node3": node3,
    }


@pytest_asyncio.fixture
async def lcel_branch_in_branch(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    node5 = await afake_runnable(chain=chain, name="node5", root=False)
    inner_branch = await afake_node_branch(
        chain=chain,
        root=False,
        default=node1,
        branches=[
            ("a", node2),
            ("b", node3),
        ],
    )
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        branches=[
            ("a", inner_branch),
            ("b", node4),
        ],
        default=node5,
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_branch": inner_branch,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
    }


@pytest_asyncio.fixture
async def lcel_branch_in_default_branch(anode_types) -> dict:
    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="inner_default", root=False)
    node2 = await afake_runnable(chain=chain, name="inner_a", root=False)
    node3 = await afake_runnable(chain=chain, name="inner_b", root=False)
    node4 = await afake_runnable(chain=chain, name="a", root=False)
    node5 = await afake_runnable(chain=chain, name="b", root=False)

    inner_branch = await afake_node_branch(
        chain=chain,
        root=False,
        default=node1,
        branches=[
            ("inner_a_in", node2),
            ("inner_b_in", node3),
        ],
    )
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        default=inner_branch,
        branches=[
            ("a_in", node4),
            ("b_in", node5),
        ],
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_branch": inner_branch,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
    }


@pytest_asyncio.fixture
async def lcel_sequence_in_branch(anode_types) -> dict:
    chain = await afake_chain()
    inner_sequence = await afake_node_sequence(chain=chain, root=False)
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        branches=[
            ("a", inner_sequence),
            ("b", node1),
        ],
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_sequence": inner_sequence,
        "node1": node1,
    }


@pytest_asyncio.fixture
async def lcel_sequence_in_default_branch(anode_types) -> dict:
    chain = await afake_chain()
    inner_sequence = await afake_node_sequence(chain=chain, root=False)
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        default=inner_sequence,
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_sequence": inner_sequence,
        "node1": node1,
    }


@pytest_asyncio.fixture
async def lcel_map_in_branch(anode_types) -> dict:
    chain = await afake_chain()
    inner_map = await afake_node_map(chain=chain, root=False)
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    branch = await afake_node_branch(
        root=True,
        chain=chain,
        branches=[
            ("a", node1),
            ("b", inner_map),
        ],
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_map": inner_map,
        "node1": node1,
    }


@pytest_asyncio.fixture
async def lcel_map_in_default_branch(anode_types) -> dict:
    chain = await afake_chain()
    inner_map = await afake_node_map(chain=chain, root=False)
    branch = await afake_node_branch(
        chain=chain,
        root=True,
        default=inner_map,
    )

    return {
        "chain": chain,
        "branch": branch,
        "inner_map": inner_map,
    }


@pytest_asyncio.fixture
async def lcel_branch_in_sequence(anode_types) -> dict:
    chain = await afake_chain()
    node0 = await afake_runnable(chain=chain, name="node0", root=True)
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    node5 = await afake_runnable(chain=chain, name="node5", root=False)

    sequence_x = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            node4,
            node5,
        ],
        root=False,
    )
    sequence_a = await afake_node_sequence(
        chain=chain,
        nodes=[
            node2,
            node4,
            node5,
        ],
        root=False,
    )
    sequence_b = await afake_node_sequence(
        chain=chain,
        nodes=[
            node3,
            node4,
            node5,
        ],
        root=False,
    )

    a_uuid = str(uuid.uuid4())
    b_uuid = str(uuid.uuid4())
    branch = await ChainNode.objects.acreate(
        chain=chain,
        class_path=RUNNABLE_BRANCH_CLASS_PATH,
        node_type=await NodeType.objects.aget(class_path=RUNNABLE_BRANCH_CLASS_PATH),
        root=False,
        config={
            "branches": ["a", "b"],
            "branches_hash": [a_uuid, b_uuid],
        },
    )
    branch_placeholder = BranchPlaceholder(
        node=branch,
        default=sequence_x,
        branches=[
            ("a", sequence_a),
            ("b", sequence_b),
        ],
    )

    # edge to branch
    await afake_chain_edge(
        chain=chain,
        source=node0,
        target=branch_placeholder.node,
        source_key="out",
        target_key="in",
    )
    # edge from branch node to sequences
    await afake_chain_edge(
        chain=chain,
        source=branch_placeholder.node,
        target=node1,
        source_key="default",
        target_key="in",
    )
    await afake_chain_edge(
        chain=chain,
        source=branch_placeholder.node,
        target=node2,
        source_key=a_uuid,
        target_key="in",
    )
    await afake_chain_edge(
        chain=chain,
        source=branch_placeholder.node,
        target=node3,
        source_key=b_uuid,
        target_key="in",
    )

    return {
        "chain": chain,
        "sequence": [node0, branch_placeholder],
        "branch": branch,
        "node0": node0,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
    }


@pytest_asyncio.fixture
async def lcel_branch_in_map_in_sequence(anode_types) -> dict:
    """
    This is technically possible but requires wrapping the RunnableBranch into a sequence
    such that the output from any branch is used as input for the next node
    in the sequence.

    Note that this is different from nesting a branch in a sequence. In this case there is
    a common Map Node that turns into a common RunnableMap node. The RunnableMap is what is
    executed. (i.e RunnableBranch -> mapped nodes) It's not possible to create alternate
    sequences when embedding in a sequence.
    """
    raise NotImplementedError("Not supported for now. See code for details.")


@pytest_asyncio.fixture
async def lcel_branch_in_map_start(anode_types) -> dict:
    """
    This is technically possible but requires wrapping the RunnableBranch into a sequence
    such that the output from any branch is used as input for the next node
    in the sequence.

    Note that this is different from nesting a branch in a sequence. In this case there is
    a common Map Node that turns into a common RunnableMap node. The RunnableMap is what is
    executed. (i.e RunnableBranch -> mapped nodes) It's not possible to create alternate
    sequences when embedding in a sequence.
    """
    raise NotImplementedError("Not supported for now. See code for details.")


@pytest_asyncio.fixture
async def lcel_join_after_branch(anode_types) -> dict:
    """Branches can JOIN to a single node after the branch"""

    chain = await afake_chain()
    node1 = await afake_runnable(chain=chain, name="node1", root=False)
    node2 = await afake_runnable(chain=chain, name="node2", root=False)
    node3 = await afake_runnable(chain=chain, name="node3", root=False)
    node4 = await afake_runnable(chain=chain, name="node4", root=False)
    node5 = await afake_runnable(chain=chain, name="node5", root=False)

    sequence_default = await afake_node_sequence(
        chain=chain,
        nodes=[
            node1,
            node4,
            node5,
        ],
    )
    sequence_a = await afake_node_sequence(
        chain=chain,
        nodes=[
            node2,
            node4,
            node5,
        ],
    )
    sequence_b = await afake_node_sequence(
        chain=chain,
        nodes=[
            node3,
            node4,
            node5,
        ],
    )

    branch = await afake_node_branch(
        chain=chain,
        root=True,
        default=sequence_default,
        branches=[
            ("a", sequence_a),
            ("b", sequence_b),
        ],
    )

    return {
        "chain": chain,
        "branch": branch,
        "sequence_default": sequence_default,
        "sequence_a": sequence_a,
        "sequence_b": sequence_b,
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
    }
