# btcrs

Needed to use some existing [bitcoin-rust](https://github.com/bitcoin-rust/bitcoin-rust) stuff from python.

For now, just wraps address validation and generation. Will add more as needed.

```python
>>> import btcrs
>>> btcrs.address.is_valid("hello")
False
>>> btcrs.address.is_valid("bc1pzwu7ucw9ra9pdcu6h522zcaunz95csa6fl80uq4mun2g27r8zfcqkvnm6w")
True
>>> some_address = btcrs.address.random()
>>> some_address
'bc1py0sspskhml0t5v6w09pz08wuzyv2fh8q66s0g9vgxdn9qdjdzyfqmj8hvd'
>>> btcrs.address.is_valid(some_address)
True
>>> btcrs.address.is_valid(some_address, is_testnet=True)
False

```