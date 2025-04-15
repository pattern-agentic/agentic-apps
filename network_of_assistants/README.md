# Network Of Assistants

## Problem

Each Cisco product has its own specialized agent assistant. It is complex to create
a single assistant that can answer questions on different products. Each question
coming from the users needs to be routed to right agen, and some questions might
require knowledge/collaboration of multiple assistants.

## Solution

Exploit AGP multicast communication to create a “chat room” where multiple assistants
can cooperate. The chat history is visible to all the agents in the chat without requiring
central storage. A moderator agent coordinates the discussion among agents and the user in the chat.
The moderator can discover agents and invite them to join the chat when they are needed.
User and assistants are members of the same chat, instead of a hierarchal structure through
a supervisor, allowing user and product assistants to directly interact.

## Components

- AGP – Used to facilitate communication between the agents
- OASF – Used to declare the Assistants capabilities
- PDF Assistant – A simple assistant which can answer questions on a given set of PDFs, an example of a native NoA assistant.
- Moderator – A agent which moderates the chat between the user and the agents.
- User Proxy – A NoA agent which proxies to the user instead of an LLM

## Communication between Agents

<img width="718" alt="image" src="https://github.com/user-attachments/assets/0b0332d7-b506-42bb-a951-392ebfcd5fb6" />

---

<img width="721" alt="image" src="https://github.com/user-attachments/assets/c2451bca-8fdf-4bba-b68b-77a1beadd94f" />

---

<img width="732" alt="image" src="https://github.com/user-attachments/assets/480bf45e-0b8a-4feb-afb0-aa8c4f45c4a6" />

---

<img width="738" alt="image" src="https://github.com/user-attachments/assets/29d77f25-d0ce-40c9-9ded-b27d314fc62b" />

---

<img width="697" alt="image" src="https://github.com/user-attachments/assets/f786e863-e3bf-4a5a-a9dc-a85fdf1ea88f" />

---

<img width="692" alt="image" src="https://github.com/user-attachments/assets/15032c7c-7129-4d3b-8b58-2b3f979b165a" />

---

<img width="840" alt="image" src="https://github.com/user-attachments/assets/2f600db3-952e-4d41-9d7b-11b74bca091f" />

---

<img width="725" alt="image" src="https://github.com/user-attachments/assets/6ade50e8-dc50-4553-9ce5-82052690f700" />

---

<img width="697" alt="image" src="https://github.com/user-attachments/assets/03c8cac4-0101-40b3-8f92-560102feb12a" />

---

<img width="721" alt="image" src="https://github.com/user-attachments/assets/66dc0796-044e-46d9-b9f1-97665e30f28d" />

---

<img width="789" alt="image" src="https://github.com/user-attachments/assets/0a110b56-283e-4a2c-b671-1a01da041953" />




