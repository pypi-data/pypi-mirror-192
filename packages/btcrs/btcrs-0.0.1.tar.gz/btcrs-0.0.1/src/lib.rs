use std::str::FromStr;
use {
    pyo3::prelude::*,
    bitcoin::{
        secp256k1::{rand, KeyPair, Secp256k1, XOnlyPublicKey},
        Address, Network,
    },
};

/// Tests that the given string is a valid bitcoin address.
#[pyfunction]
fn is_valid(address: &str, is_testnet: Option<bool>) -> bool {
    let network = match is_testnet {
        Some(true) => Network::Testnet,
        _ => Network::Bitcoin,
    };
    let parsed: Result<Address, _> = Address::from_str(address);

    match parsed {
        Ok(a) => a.is_valid_for_network(network),
        Err(_e) => false,
    }
}


/// Generates a random taproot address.
#[pyfunction]
fn random(is_testnet: Option<bool>) -> String {
    let network = match is_testnet {
        Some(true) => Network::Testnet,
        _ => Network::Bitcoin,
    };
    let secp256k1 = Secp256k1::new();
    let key_pair = KeyPair::new(&secp256k1, &mut rand::thread_rng());
    let (public_key, _parity) = XOnlyPublicKey::from_keypair(&key_pair);
    let address = Address::p2tr(&secp256k1, public_key, None, network);

    address.to_string()
}

/// A small Python wrapper around bitcoin-rust.
#[pymodule]
fn btcrs(py: Python, m: &PyModule) -> PyResult<()> {
    register_address_submodule(py, m)?;
    Ok(())
}

fn register_address_submodule(py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    let child_module = PyModule::new(py, "address")?;
    child_module.add_function(wrap_pyfunction!(is_valid, child_module)?)?;
    child_module.add_function(wrap_pyfunction!(random, child_module)?)?;
    parent_module.add_submodule(child_module)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_valid() {
        //
        // Mainnet
        {
            let some_address = "bc1qv8zhcjzpjw4m4tdyc5zn3dmax0z6rr6l78fevg";
            assert_eq!(is_valid(some_address,   Some(false)), true);
            assert_eq!(is_valid(some_address, Some(true)), false);
        }
        {
            let some_address = "bc1pzwu7ucw9ra9pdcu6h522zcaunz95csa6fl80uq4mun2g27r8zfcqkvnm6w";
            assert_eq!(is_valid(some_address,   Some(false)), true);
            assert_eq!(is_valid(some_address, Some(true)), false);
        }
        {
            let some_address = "bc1pm7lptsa40t6wml9s98erc30kla66z0p25hqppjdgu2h3ghr5nnjqfw9j6s";
            assert_eq!(is_valid(some_address,   Some(false)), true);
            assert_eq!(is_valid(some_address, Some(true)), false);
        }
        {
            let some_address = "bc1paf6hud8ae2e9uqxsfl6t2yf7g869vveqf9ln0scj224pd00cy2ssy8r899";
            assert_eq!(is_valid(some_address,   Some(false)), true);
            assert_eq!(is_valid(some_address, Some(true)), false);
        }
        //
        // Testnet
        {
            let some_address = "tb1pcmpjvdd254j7jf94wu2pk5mxqpsqry524u9q2d9eaza7fx42el2seur6hn";
            assert_eq!(is_valid(some_address, Some(false)), false);
            assert_eq!(is_valid(some_address, Some(true)), true);
        }
        //
        // Bad
        {
            let bad_address = "bc1p55";
            assert_eq!(is_valid(bad_address, Some(false)), false);
            assert_eq!(is_valid(bad_address, Some(true)), false);
        }
    }

    #[test]
    fn test_random() {
        let address = random(None);
        assert!(address.starts_with("bc1p"));
        assert!(is_valid(&address, None));

        let address = random(Some(true));
        assert!(address.starts_with("tb1p"));
        assert!(is_valid(&address, Some(true)));
    }
}
