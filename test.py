import slixmpp
import asyncio

class EchoBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        print("Autenticado com sucesso.")
        self.disconnect()

async def main():
    xmpp = EchoBot("lucastt@yax.im", "XMPPpassword")
    await xmpp.start()


if __name__ == "__main__":
    asyncio.run(main())
