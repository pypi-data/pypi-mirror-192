from .config import welcome , web , android , encryption
from .postdata import http,httpfiles
from .getadress import server_bot
import datetime
from json import dumps, loads
from datetime import datetime
import asyncio
import datetime
from requests import post, get
from random import randint, choice

class client:
    server_Messenger = choice(server_bot.list_servers)
    
    def __init__(self, auth_account: str):
        self.auth = auth_account
        self.enc = encryption(auth_account)

    def requests_method(self, method):
        while 1:
            try:
                loop = asyncio.get_event_loop()
                requests = self.enc.decrypt(loads(loop.run_until_complete(http(client.server_Messenger,self.auth,method))).get("data_enc"))
                return loads(requests)
                break
            except:continue
            
    def send_message(self, chat_id, text, metadata=[],message_id=None):
        method = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "rnd":f"{randint(100000,999999999)}",
                "text":text,
                "reply_to_message_id":message_id
            },
            "client": web
        }
        if metadata != [] : method["input"]["metadata"] = {"meta_data_parts":metadata}
        return self.requests_method(method)
        
    def edit_message(self, chat_id, newText, message_id):
        method = {
            "method":"editMessage",
            "input":{
                "message_id":message_id,
                "object_guid":chat_id,
                "text":newText
            },
            "client": web
        }
        return self.requests_method(method)
        

    def delete_messages(self, chat_id, message_ids):
        method = {
            "method":"deleteMessages",
            "input":{
                "object_guid":chat_id,
                "message_ids":message_ids,
                "type":"Global"
            },
            "client": web
        }
        return self.requests_method(method)
                

    def get_message_filter(self, chat_id, filter_whith):
        method = {
            "method":"getMessages",
            "input":{
                "filter_type":filter_whith,
                "max_id":"NaN",
                "object_guid":chat_id,
                "sort":"FromMax"
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("messages")
        

    def get_message(self, chat_id, min_id):
        method = {
            "method":"getMessagesInterval",
            "input":{
                "object_guid":chat_id,
                "middle_message_id":min_id
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("messages")
        

    def get_chats(self, start_id=None):
        method = {
            "method":"getChats",
            "input":{
                "start_id":start_id
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("chats")

    def delete_user_chat(self, user_guid, last_message):
        method = {
            "method":"deleteUserChat",
            "input":{
                "last_deleted_message_id":last_message,
                "user_guid":user_guid
            },
            "client": web
        }
        return self.requests_method(method)

    def get_Info_by_username(self, username):
        method = {
            "method":"getObjectByUsername",
            "input":{
                "username":username
            },
            "client": web
        }
        return self.requests_method(method)

    def ban_group_member(self, chat_id, user_id):
        method = {
            "method":"banGroupMember",
            "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Set"
            },
            "client": web
        }
        return self.requests_method(method)

    def unban_group_member(self, chat_id, user_id):
        method = {
            "method":"banGroupMember",
            "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Unset"
            },
            "client": android
        }
        return self.requests_method(method)
        
    def get_group_Info(self, chat_id):
        method = {
            "method":"getGroupInfo",
            "input":{
                "group_guid": chat_id
            },
            "client": web
        }
        return self.requests_method(method)

    def add_group_members(self, chat_id, user_ids):
        method = {
            "method":"addGroupMembers",
            "input":{
                "group_guid": chat_id,
                "member_guids": user_ids
            },
            "client": web
        }
        return self.requests_method(method)

    def add_channel_members(self, chat_id, user_ids):
        method = {
            "method":"addChannelMembers",
            "input":{
                "channel_guid": chat_id,
                "member_guids": user_ids
            },
            "client": web
        }
        return self.requests_method(method)

    def get_group_admins(self, chat_id):
        method = {
            "method":"getGroupAdminMembers",
            "input":{
                "group_guid":chat_id
            },
            "client": android
        }
        return self.requests_method(method)
        
    def get_channel_Info(self, channel_guid):
        method = {
            "method":"getChannelInfo",
            "input":{
                "channel_guid":channel_guid
            },
            "client": android
        }
        return self.requests_method(method)

    def get_messages_Info(self, chat_id, message_ids):
        method = {
            "method":"getMessagesByID",
            "input":{
                "object_guid": chat_id,
                "message_ids": message_ids
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("messages")

    def set_members_Access(self, chat_id, access_list):
        method = {
            "method":"setGroupDefaultAccess",
            "input":{
                "access_list": access_list,
                "group_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def get_group_members(self, chat_id, start_id=None):
        method = {
            "method":"getGroupAllMembers",
            "input":{
                "group_guid": chat_id,
                "start_id": start_id
            },
            "client": web
        }
        return self.requests_method(method)

    def get_group_link(self, chat_id):
        method = {
            "method":"getGroupLink",
            "input":{
                "group_guid":chat_id
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("join_link")

    def get_channel_link(self, chat_id):
        method = {
            "method":"getChannelLink",
            "input":{
                "group_guid":chat_id
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("join_link")

    def change_group_link(self, chat_id):
        method = {
            "method":"setGroupLink",
            "input":{
                "group_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("join_link")

    def change_channel_link(self, chat_id):
        method = {
            "method":"setChannelLink",
            "input":{
                "channel_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("join_link")
        
    def set_group_timer(self, chat_id, time):
        method = {
            "method":"editGroupInfo",
            "input":{
                "group_guid": chat_id,
                "slow_mode": time,
                "updated_parameters":["slow_mode"]
            },
            "client": android
        }
        return self.requests_method(method)
        
    def set_group_admin(self, chat_id, user_id):
        method = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": chat_id,
                "access_list":["PinMessages","DeleteGlobalAllMessages","BanMember","SetMemberAccess"],
                "action": "SetAdmin",
                "member_guid": user_id
            },
            "client": android
        }
        return self.requests_method(method)

    def delete_group_admin(self,group_guid,user_id):
        method = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": group_guid,
                "action": "UnsetAdmin",
                "member_guid": user_id
            },
            "client": android
        }
        return self.requests_method(method)

    def set_channel_Admin(self, chat_id, user_id, access_list=[]):
        method = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": chat_id,
                "access_list": access_list,
                "action": "SetAdmin",
                "member_guid": user_id
            },
            "client": android
        }
        return self.requests_method(method)

    def get_stickers_by_emoji(self,emojee):
        method = {
            "method":"getStickersByEmoji",
            "input":{
                "emoji_character": emojee,
                "suggest_by": "All"
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("stickers")

    def send_poll(self,guid,SOAL,LIST):
        method = {
            "method":"createPoll",
            "input":{
                "allows_multiple_answers": "false",
                "is_anonymous": "true",
                "object_guid": guid,
                "options":LIST,
                "question":SOAL,
                "rnd":f"{randint(100000,999999999)}",
                "type":"Regular"
            },
            "client": android
        }
        return self.requests_method(method)

    def forward_messages(self, From, message_ids, to):
        method = {
            "method":"forwardMessages",
            "input":{
                "from_object_guid": From,
                "message_ids": message_ids,
                "rnd": f"{randint(100000,999999999)}",
                "to_object_guid": to
            },
            "client": android
        }
        return self.requests_method(method)

    def chat_group_visit(self,guid,visiblemsg):
        method = {
            "method":"editGroupInfo",
            "input":{
                "chat_history_for_new_members": "Visible",
                "group_guid": guid,
                "updated_parameters": visiblemsg
            },
            "client": android
        }
        return self.requests_method(method)

    def chat_group_hidden(self,guid,hiddenmsg):
        method = {
            "method":"editGroupInfo",
            "input":{
                "chat_history_for_new_members": "Hidden",
                "group_guid": guid,
                "updated_parameters": hiddenmsg
            },
            "client": android
        }
        return self.requests_method(method)

    def pin_message(self, chat_id, message_id):
        method = {
            "method":"setPinMessage",
            "input":{
                "action":"Pin",
                "message_id": message_id,
                "object_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def un_pin_message(self, chat_id, message_id):
        method = {
            "method":"setPinMessage",
            "input":{
                "action":"Unpin",
                "message_id": message_id,
                "object_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def logout_auth(self):
        method = {
            "method":"logout",
            "input":{},
            "client": android
        }
        return self.requests_method(method)

    def join_group(self, link):
        hashLink = link.split("/")[-1]
        method = {
            "method":"joinGroup",
            "input":{
                "hash_link": hashLink
            },
            "client": android
        }
        return self.requests_method(method)

    def join_channel_bylink(self, link):
        hashLink = link.split("/")[-1]
        method = {
            "method":"joinChannelByLink",
            "input":{
                "hash_link": hashLink
            },
            "client": android
        }
        return self.requests_method(method)

    def delete_chat_history(self, chat_id, msg_id):
        method = {
            "method":"deleteChatHistory",
            "input":{
                "last_message_id": msg_id,
                "object_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)
        
    def leave_group(self,chat_id):
        if "https://" in chat_id:
            guid = client.join_group(self,chat_id)["data"]["group"]["group_guid"]
        else:
            guid = chat_id

        method = {
            "method":"leaveGroup",
            "input":{
                "group_guid": guid
            },
            "client": android
        }
        return self.requests_method(method)

    def edit_name_group(self,groupgu,namegp,biogp=None):
        method = {
            "method":"editGroupInfo",
            "input":{
                "description": biogp,
                "group_guid": groupgu,
                "title":namegp,
                "updated_parameters":["title","description"]
            },
            "client": android
        }
        return self.requests_method(method)

    def edit_bio_group(self,groupgu,biogp,namegp=None):
        method = {
            "method":"editGroupInfo",
            "input":{
                "description": biogp,
                "group_guid": groupgu,
                "title":namegp,
                "updated_parameters":["title","description"]
            },
            "client": android
        }
        return self.requests_method(method)

    def join_channel_byid(self, chat_id:str):
        id = chat_id.split("@")[-1]
        guid = client.get_Info_by_username(self,id)["data"]["channel"]["channel_guid"]
        method = {
            "method":"joinChannelAction",
            "input":{
                "action": "Join",
                "channel_guid": guid
            },
            "client": android
        }
        return self.requests_method(method)

    def leave_channel(self,chat_id):
        if "https://" in chat_id:
            guid = client.join_channel_bylink(self,chat_id)["data"]["group"]["channel_guid"]
        else:
            guid = chat_id

        method = {
            "method":"joinChannelAction",
            "input":{
                "action": "Leave",
                "channel_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def set_block_user(self, chat_id):
        method = {
            "method":"setBlockUser",
            "input":{
                "action": "Block",
                "user_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def un_block(self, chat_id):
        method = {
            "method":"setBlockUser",
            "input":{
                "action": "Unblock",
                "user_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def get_channel_members(self, channel_guid, text=None, start_id=None):
        method = {
            "method":"getChannelAllMembers",
            "input":{
                "channel_guid":channel_guid,
                "search_text":text,
                "start_id":start_id,
            },
            "client": android
        }
        return self.requests_method(method)

    def get_link_from_url(self,linkpost):
        method = {
            "method":"getLinkFromAppUrl",
            "input": {
                "app_url": linkpost
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("link").get("open_chat_data")
        
    def start_voice_chat(self, chat_id):
        method = {
            "method":"createGroupVoiceChat",
            "input":{
                "chat_guid":chat_id
            },
            "client": web
        }
        return self.requests_method(method)

    def edit_voice_chat(self,chat_id,voice_chat_id, title):
        method = {
            "method":"setGroupVoiceChatSetting",
            "input":{
                "chat_guid":chat_id,
                "voice_chat_id" : voice_chat_id,
                "title" : title ,
                "updated_parameters": ["title"]
            },
            "client": web
        }
        return self.requests_method(method)
        
    def finish_voice_chat(self, chat_id, voice_chat_id):
        method = {
            "method":"discardGroupVoiceChat",
            "input":{
                "chat_guid":chat_id,
                "voice_chat_id" : voice_chat_id
            },
            "client": web
        }
        return self.requests_method(method)

    def get_chats_update(self):
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        method = {
            "method":"getChatsUpdates",
            "input":{
                "state":time_stamp,
            },
            "client": web
        }
        return self.requests_method(method).get('data').get('chats')

    def ge_messages_chats(self, start_id=None):
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        method = {
            "method":"getChats",
            "input":{
                "start_id":start_id
            },
            "client": web
        }
        return self.requests_method(method).get('data').get('chats')

    def get_preview_link(self,group_link):
        method = {
            "method":"groupPreviewByJoinLink",
            "input":{
                "hash_link": group_link
            },
            "client": web
        }
        return self.requests_method(method).get("data")

    def delete_folder(self,folder_id):
        method = {
            "method":"deleteFolder",
            "input":{
                "folder_id": folder_id
            },
            "client": web
        }
        return self.requests_method(method)

    def create_channel(self,title,typeChannell,bio,guidsUser = None):
        method = {
            "method":"addChannel",
            "input":{
                "addChannel": typeChannell,
                "description": bio,
                "member_guids": guidsUser,
                "title": title,
            },
            "client": web
        }
        return self.requests_method(method)

    def create_group(self,title,guidsUser = None):
        method = {
            "method":"addGroup",
            "input":{
                "member_guids": guidsUser,
                "title": title
            },
            "client": web
        }
        return self.requests_method(method)

    def update_profile(self,first_name = None,last_name = None,bio = None):
        method = {
            "method":"updateProfile",
            "input":{
                "bio": bio,
                "first_name": first_name,
                "last_name": last_name,
                "updated_parameters":["first_name","last_name","bio"]
            },
            "client": web
        }
        return self.requests_method(method)