import requests


class WhatsMate:
    # wrapper around whatsapp cloud api
    def __init__(self, token, phone_number_id):
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v14.0"
        self.v15_base_url = "https://graph.facebook.com/v15.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def say(self, message, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "text",
            "text": {
                "body": message,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_image(self, image_url, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "image",
            "image": {
                "link": image_url,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_video(self, video_url, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "video",
            "video": {
                "link": video_url,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_audio(self, audio_url, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "audio",
            "audio": {
                "link": audio_url,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_file(self, file_url, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "file",
            "file": {
                "link": file_url,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_location(self, latitude, longitude, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_contact(self, contact_name, contact_phone_number, phone_number, recipient_type="individual",
                     preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "contact",
            "contact": {
                "name": contact_name,
                "phone_number": contact_phone_number,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_sticker(self, sticker_id, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "sticker",
            "sticker": {
                "id": sticker_id,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_template(self, template, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "template",
            "template": template,
            "recipient_type": recipient_type,
            "to": phone_number
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    def send_button_template(self, text, buttons, phone_number, recipient_type="individual", preview_url=None):
        template = {
            "type": "button",
            "text": text,
            "buttons": buttons
        }
        return self.send_template(template, phone_number, recipient_type, preview_url)

    def send_list_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None):
        template = {
            "type": "list",
            "elements": elements,
            "buttons": buttons
        }
        return self.send_template(template, phone_number, recipient_type, preview_url)

    def send_media_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None):
        template = {
            "type": "media",
            "elements": elements,
            "buttons": buttons
        }
        return self.send_template(template, phone_number, recipient_type, preview_url)

    def send_open_graph_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None):
        template = {
            "type": "open_graph",
            "elements": elements,
            "buttons": buttons
        }
        return self.send_template(template, phone_number, recipient_type, preview_url)

    def send_receipt_template(self, merchant_name, order_number, currency, payment_method, timestamp, elements, address,
                              summary, adjustments, phone_number, recipient_type="individual", preview_url=None):
        template = {
            "type": "receipt",
            "merchant_name": merchant_name,
            "order_number": order_number,
            "currency": currency,
            "payment_method": payment_method,
            "timestamp": timestamp,
            "elements": elements,
            "address": address,
            "summary": summary,
            "adjustments": adjustments
        }
        return self.send_template(template, phone_number, recipient_type, preview_url)

    # reply to a message
    def reply(self, message_id, text, phone_number, recipient_type="individual", preview_url=None):
        payload = {
            "messaging_product": "whatsapp",
            type: "text",
            "text": {
                "body": text,
                "preview_url": preview_url
            },
            "recipient_type": recipient_type,
            "to": phone_number,
            "message_id": message_id
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()

    # send a message to a group
    def send_to_group(self, group_id, text, preview_url=None):
        return self.say(text, group_id, "group", preview_url)

    # send a message to a broadcast
    def send_to_broadcast(self, broadcast_id, text, preview_url=None):
        return self.say(text, broadcast_id, "broadcast", preview_url)

    # send a message to a contact
    def send_to_contact(self, contact_id, text, preview_url=None):
        return self.say(text, contact_id, "contact", preview_url)

    # mark message as read
    def mark_as_read(self, message_id, recipient_type="individual"):
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "status": "read",
            "message_id": message_id
        }
        response = requests.put(self.url, headers=self.headers, json=payload)
        return response.json()

    # send a message to a contact
