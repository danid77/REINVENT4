import pytest
from pathlib import Path

import torch

from reinvent.runmodes.TL.run_transfer_learning import run_transfer_learning
from reinvent.runmodes.utils.helpers import set_torch_device


@pytest.fixture
@pytest.mark.usefixtures("device")
def setup(tmp_path, json_config, pytestconfig):
    device = pytestconfig.getoption("device")
    set_torch_device(device)

    output_model_file = tmp_path / "TL_molformer.model"

    config = {
        "parameters": {
            "input_model_file": json_config["MOLFORMER_PRIOR_PATH"],
            "smiles_file": json_config["TL_MOLFORMER_SMILES_PATH"],
            "output_model_file": output_model_file,
            "save_every_n_epochs": 1,
            "num_epochs": 2,
            "batch_size": 64,
            "sample_batch_size": 10,
            "num_refs": 10,
            "pairs": {
                "type": "tanimoto",
                "lower_threshold": 0.5,
                "upper_threshold": 1.0,
                "min_cardinality": 1,
                "max_cardinality": 100,
            },
        }
    }

    return config


@pytest.mark.integration
def test_transfer_learning(setup, tmp_path, pytestconfig):
    config = setup
    device = pytestconfig.getoption("device")

    run_transfer_learning(config, device)
    model_name = Path(config["parameters"]["output_model_file"]).name
    checkpoint_files = list(Path(tmp_path).glob(f"{model_name}*.chkpt"))

    assert len(checkpoint_files) == config["parameters"]["num_epochs"]

    model = torch.load(checkpoint_files[-1])
    keys = list(model.keys())

    assert keys == [
        "model_type",
        "version",
        "vocabulary",
        "max_sequence_length",
        "network_parameter",
        "network_state",
    ]

    assert model["model_type"] == "Mol2Mol"
