WhatsMate is a class that provides a wrapper around the WhatsApp Cloud API, allowing you to send various types of messages to a phone number using the WhatsApp messaging service.

Here's a brief description of each method in the class:

```python
from whatsmate import WhatsMate
ms = WhatsMate(token='your_whatsapp_token', '+91xxxxxxxxx')

# use methods as 
ms.method() # [pass params as documented]

```

## **`__init__(self, token, phone_number_id)`**

Constructor for the **`WhatsMate`** class. Initializes the **`token`** and **`phone_number_id`** instance variables, which represent the WhatsApp Cloud API token and the phone number ID of the recipient, respectively.

## **`say(self, message, phone_number, recipient_type="individual", preview_url=None)`**

Sends a text message to the recipient.

**Parameters:**

- **`message`** (str): The message to be sent.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Defaults to "individual".
- **`preview_url`** (str, optional): The URL of the preview image to be sent with the message. Defaults to None.

**Returns:**

- A JSON object containing the response from the API.

## **`send_image(self, image_url, phone_number, recipient_type="individual", preview_url=None)`**

Sends an image to the recipient.

**Parameters:**

- **`image_url`** (str): The URL of the image to be sent.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Defaults to "individual".
- **`preview_url`** (str, optional): The URL of the preview image to be sent with the message. Defaults to None.

**Returns:**

- A JSON object containing the response from the API.

## **`send_video(self, video_url, phone_number, recipient_type="individual", preview_url=None)`**

Sends a video to the recipient.

**Parameters:**

- **`video_url`** (str): The URL of the video to be sent.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Defaults to "individual".
- **`preview_url`** (str, optional): The URL of the preview image to be sent with the message. Defaults to None.

**Returns:**

- A JSON object containing the response from the API.

## **`send_audio(self, audio_url, phone_number, recipient_type="individual", preview_url=None)`**

Sends an audio file to the recipient.

**Parameters:**

- **`audio_url`** (str): The URL of the audio file to be sent.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Defaults to "individual".
- **`preview_url`** (str, optional): The URL of the preview image to be sent with the message. Defaults to None.

**Returns:**

- A JSON object containing the response from the API.

## **`send_file(self, file_url, phone_number, recipient_type="individual", preview_url=None)`**

Sends a file to the recipient.

**Parameters:**

- **`file_url`** (str): The URL of the file to be sent.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Defaults to "individual".
- **`preview_url`** (str, optional): The URL of the preview image to be sent with the message. Defaults to None.

**Returns:**

- A JSON object containing the response from the API.

## **`send_location(self, latitude, longitude, phone_number, recipient_type="individual", preview_url=None)`**

Sends a location to the recipient.

### **Method: send_template**

```python
def send_template(self, template, phone_number, recipient_type="individual", preview_url=None):
```

- Sends a WhatsApp message using a custom template.

### Parameters

- **`template`** (dict): The template to use. The format of the template is described in the WhatsApp Business API documentation.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Possible values are "individual" (default) and "group".
- **`preview_url`** (str, optional): The URL of a link to include in the message.

### Returns

- A JSON object containing the response from the WhatsApp server.

### Example

```python
template = {
        "namespace": "your-namespace",
        "name": "your-template-name",
        "language": {
            "policy": "deterministic",
            "code": "en"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": "Hello {{1}}! This is a {{2}} message from {{3}}."
                    }
                ]
            }
        ]
    }
    response = whatsMate.send_template(template, "+14155552671")

```

### **Method: send_button_template**

```python
def send_button_template(self, text, buttons, phone_number, recipient_type="individual", preview_url=None):
```

- Sends a WhatsApp message using a button template.

### Parameters

- **`text`** (str): The text of the message.
- **`buttons`** (list): A list of dictionaries representing the buttons to include in the template. Each button should have a **`type`** and **`title`** field.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Possible values are "individual" (default) and "group".
- **`preview_url`** (str, optional): The URL of a link to include in the message.

### Returns

- A JSON object containing the response from the WhatsApp server.

### Example

```python
buttons = [
        {"type": "url", "title": "Visit Website", "url": "https://example.com"},
        {"type": "text", "title": "More Information", "payload": "more_info"}
    ]
    response = whatsMate.send_button_template("Welcome to our store!", buttons, "+14155552671")

```

### **Method: send_list_template**

```python
def send_list_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None):
```

- Sends a WhatsApp message using a list template.

### Parameters

- **`elements`** (list): A list of dictionaries representing the items to include in the list. Each item should have a **`title`**, **`subtitle`**, and **`image_url`** field.
- **`buttons`** (list): A list of dictionaries representing the buttons to include in the template. Each button should have a **`type`** and **`title`** field.
- **`phone_number`** (str): The phone number of the recipient.
- **`recipient_type`** (str, optional): The recipient type. Possible values are "individual" (default) and "group".
- **`preview_url`** (str, optional): The URL of a link to include in the message.

### Returns

- A JSON object containing the response from the WhatsApp server.

**`send_list_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None)`**: Sends a list template message to a phone number.

Example usage:

```python

elements = [
    {
        "title": "Element 1",
        "subtitle": "Subtitle 1",
        "image_url": "https://example.com/image1.jpg",
        "default_action": {
            "type": "web_url",
            "url": "https://example.com/1",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://example.com/fallback"
        }
    },
    {
        "title": "Element 2",
        "subtitle": "Subtitle 2",
        "image_url": "https://example.com/image2.jpg",
        "default_action": {
            "type": "web_url",
            "url": "https://example.com/2",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://example.com/fallback"
        }
    }
]

buttons = [
    {
        "type": "web_url",
        "url": "https://example.com",
        "title": "Button 1"
    },
    {
        "type": "postback",
        "title": "Button 2",
        "payload": "Payload for button 2"
    }
]

response = whatsMate.send_list_template(elements, buttons, "1234567890")

```

**`send_media_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None)`**: Sends a media template message to a phone number.

Example usage:

```python

elements = [
    {
        "media_type": "image",
        "url": "https://example.com/image.jpg",
        "buttons": [
            {
                "type": "web_url",
                "url": "https://example.com",
                "title": "Button 1"
            },
            {
                "type": "postback",
                "title": "Button 2",
                "payload": "Payload for button 2"
            }
        ]
    }
]

buttons = [
    {
        "type": "web_url",
        "url": "https://example.com",
        "title": "Button 1"
    },
    {
        "type": "postback",
        "title": "Button 2",
        "payload": "Payload for button 2"
    }
]

response = whatsMate.send_media_template(elements, buttons, "1234567890")

```

**`send_open_graph_template(self, elements, buttons, phone_number, recipient_type="individual", preview_url=None)`**: Sends an Open Graph template message to a phone number.

**`reply(message_id, text, phone_number, recipient_type="individual", preview_url=None)`**: This method is used to send a reply to a message. The **`message_id`** parameter specifies the ID of the message to which the reply is being sent. The **`text`** parameter is the text of the message being sent as a reply. The **`phone_number`** parameter is the phone number of the recipient of the reply. The **`recipient_type`** parameter specifies the type of recipient, which can be either "individual" or "group". The **`preview_url`** parameter specifies whether to show a preview of any included URL. Returns the response in JSON format.

**`send_to_group(group_id, text, preview_url=None)`**: This method is used to send a message to a group. The **`group_id`** parameter is the ID of the group to which the message is being sent. The **`text`** parameter is the text of the message being sent. The **`preview_url`** parameter specifies whether to show a preview of any included URL. Returns the response in JSON format.

**`send_to_broadcast(broadcast_id, text, preview_url=None)`**: This method is used to send a message to a broadcast. The **`broadcast_id`** parameter is the ID of the broadcast to which the message is being sent. The **`text`** parameter is the text of the message being sent. The **`preview_url`** parameter specifies whether to show a preview of any included URL. Returns the response in JSON format.

**`send_to_contact(contact_id, text, preview_url=None)`**: This method is used to send a message to a contact. The **`contact_id`** parameter is the ID of the contact to which the message is being sent. The **`text`** parameter is the text of the message being sent. The **`preview_url`** parameter specifies whether to show a preview of any included URL. Returns the response in JSON format.

**`mark_as_read(message_id, recipient_type="individual")`**: This method is used to mark a message as read. The **`message_id`** parameter specifies the ID of the message to mark as read. The **`recipient_type`** parameter specifies the type of recipient, which can be either "individual" or "group". Returns the response in JSON format.

I hope this helps! Let me know if you have any further questions.