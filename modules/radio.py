import json
import socket


async def radio(*_args, **kwargs):
    client = kwargs["client"]
    message = kwargs["message"]
    author = kwargs["author"]
    words = kwargs["words"]

    respond = f":musical_note: {client.cfg['radio_url']} :musical_note:"
    if len(words) == 0:
        await client.reply(message, respond)
        return

    user_id = str(author.id)
    target = words[0]

    host = client.cfg["radio_host"]
    port = client.cfg["radio_port"]
    prefix = client.cfg["radio_prefix"]

    instructions = {
        "cmd": "enqueue",
        "target": target,
        "user": user_id
    }

    instruct = f"{prefix}:{json.dumps(instructions)}".encode("utf-8")

    sock = socket.socket()
    try:
        sock.connect((host, port))
        sock.send(instruct)
    except Exception as e:
        await client.reply(message, "Couldn't connect to the Miror Radio service :/")
        raise e from None
    sock.close()

    await client.reply(message, respond)

mb_mod = True
mb_import = True
mb_actions = {
    "on_command": {
        "radio": radio
    }
}
