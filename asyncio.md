asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
	asyncio.events.get_event_loop()
		get_event_loop_policy().get_event_loop()
		_init_event_loop_policy()
		DefaultEventLoopPolicy()
		DefaultEventLoopPolicy = windows_events._WindowsDefaultEventLoopPolicy{_loop_factory = SelectorEventLoop
			_WindowsSelectorEventLoop
			selector_events.BaseSelectorEventLoop
				selector = selectors.DefaultSelector()
					KqueueSelector/EpollSelector/...
			base_events.BaseEventLoop}
		events.BaseDefaultEventLoopPolicy().get_event_loop()
			self.set_event_loop(self.new_event_loop())
				self._loop_factory()
				base_events.BaseEventLoop()

node = dht.SybilNode
loop.create_task(node.launch(lambda: self, local_addr=address))
	asyncio.get_event_loop().create_datagram_endpoint(protocol_factory = SybilNode)
	protocol = protocol_factory() = SybilNode(asyncio.DatagramProtocol)
	selector_events.BaseSelectorEventLoop._make_datagram_transport
		_SelectorDatagramTransport
			_SelectorTransport.__init__
				self._server._attach()
			self._loop.call_soon(self._protocol.connection_made, self)
				SybilNode.connection_made
					self.tick_periodically()
						self.__bootstrap()
							send self.__build_FIND_NODE_query(self.__true_id) to BOOTSTRAPPING_NODES
							return datagram_received
								self.__on_FIND_NODE_response
									self._routing_table.update
			self._loop.call_soon(self._loop.add_reader, self._sock_fd, self._read_ready)
				self._read_ready
					self._protocol.data_received(data)	
