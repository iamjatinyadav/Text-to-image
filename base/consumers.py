import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ImageGenerationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("image_generation", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("image_generation", self.channel_name)

    async def image_update(self, event):
        # Handle the message received from the group
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))