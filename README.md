# Hashcast
_WIP_

## Messages
- stamp
- content
- signature

## Stamps
- verify_key
- time
- nonce


## TODO
- binary serialization for messages/stamps
- readme
- split into libhashcast and hashcast_node_impl repos
  - node will have messaging port and control port
  - control port can mine and broadcast messages that you send it
- create ui
- wifi broadcaster/receiver (looks for HASHCAST_NNNNN SSIDs, connects and connects to gateway ip)
- websocket broadcaster/receiver
- dockerize
- diagrams (TX, RX, clients, relays)
- protopost client that is configured with a list of nodes to spam to
- enforce max message size...
- niceness-based delay
  - niceness based on downstream broadcasters since broadcasting may be expensive (connecting to ssids, setting up BLE, etc)
- save/load keys from env/file