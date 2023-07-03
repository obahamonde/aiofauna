import asyncio
import inspect
import json

from aiohttp.web_exceptions import HTTPException

import models
from aiofauna import FaunaModel
from mixins import app, client, env
from models import *


@app.get("/api/auth")
async def auth(token: str):
    """Authenticates a user"""
    data = await client.fetch(
        f"https://{env.AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    return await User(**data).save()


@app.delete("/api/upload")
async def delete_upload(ref: str):
    """Delete an uploaded file given it's document reference"""
    await Upload.delete(ref)
    return {"message": "Asset deleted successfully", "status": "success"}


@app.get("/api/upload")
async def get_upload(user: str):
    """Fetch Uploaded files for a given user"""
    
    return await Upload.find_many("user", user)


@app.get("/api/users")
async def get_users():
    """Fetch all users"""
    return await User.all()


@app.post("/api/invitations")
async def send_invitation(inv: Invitation):
    """Sends an invitation from one user to another."""
    exists = await Invitation.find_unique("hash", inv.hash)
    if exists:
        raise HTTPException(text=json.dumps({"message": "Invitation already exists"}),content_type="application/json")
    owner, guest = inv.sender, inv.receiver
    hashed = f"{owner}-{guest}"
    conversation = await Conversation.find_unique("name", hashed)
    if isinstance(conversation, Conversation):
        raise HTTPException(text=json.dumps({"message": "Conversation already exists"}),content_type="application/json")
    invitation = await inv.create()
    assert isinstance(invitation, Invitation)
    return invitation

@app.get("/api/invitations/{user_id}")
async def get_invitations(user_id: str):
    """Gets all invitations for a user."""
    return await Invitation.find_many("receiver", user_id)

@app.post("/api/invitations/{invitation_hash}/accept")
async def accept_invitation(invitation_hash: str):
    """Accepts an invitation."""
    invitation = await Invitation.find_unique("hash", invitation_hash)
    assert isinstance(invitation, Invitation)
    # Create a new conversation between the sender and receiver.
    conversation = await Conversation(owner=invitation.sender, guest=invitation.receiver).save()
    assert isinstance(conversation, Conversation)
    return conversation

@app.post("/api/invitations/{invitation_hash}/reject")
async def reject_invitation(invitation_hash: str):
    """Rejects an invitation."""
    invitation = await Invitation.find_unique("hash", invitation_hash)
    assert isinstance(invitation, Invitation)
    invitation.status = "REJECTED"
    await invitation.save()
    return invitation


app.static()


@app.on_event("startup")
async def startup(_) -> None:
    """Runs on startup"""
    await FaunaModel.create_all()