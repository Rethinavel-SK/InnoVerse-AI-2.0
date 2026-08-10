"""
InnoVerse AI 2.0 — Caspian Message Router
============================================
Routes incoming Caspian messages to appropriate handlers:
  - New innovation ideas → full analysis pipeline
  - Task updates → update project state + recalculate
  - Approval responses → process approval
  - General questions → contextual response
"""

import asyncio
import json
import logging
import re
import time
from typing import Any, Optional, Dict

from backend.caspian.channel_formatter import channel_formatter
from backend.database.db import db_manager
from backend.database.models import (
    InnovationProject, InnovationVersion, CommunicationEvent,
    ChannelType, ProjectStatus, TaskStatus, ApprovalStatus,
)

logger = logging.getLogger("CaspianRouter")


class CaspianMessageRouter:
    """
    Routes incoming Caspian messages to InnoVerse handlers.
    """

    def __init__(self):
        self._innovation_handler = None  # Set by main.py after imports

    def set_innovation_handler(self, handler):
        """Set the async function that runs innovation analysis."""
        self._innovation_handler = handler

    async def handle_message(self, message) -> None:
        """
        Main Caspian on_message handler.
        Receives a Caspian Message object and routes to appropriate action.
        """
        text = getattr(message, "text", "") or ""
        channel = getattr(message, "channel", "unknown")
        conversation_id = getattr(message, "conversation_id", "")
        sender = getattr(message, "sender", None)
        text_stripped = text.strip()

        if not text_stripped:
            return

        # Log inbound communication
        try:
            await db_manager.log_communication(CommunicationEvent(
                channel=ChannelType(channel) if channel in ["telegram", "email", "discord"] else ChannelType.TELEGRAM,
                direction="inbound",
                sender=str(sender) if sender else None,
                content=text_stripped[:500],
                message_type="user_message",
                conversation_id=conversation_id,
            ))
        except Exception as e:
            logger.warning("Failed to log inbound message: %s", e)

        # Route based on content
        text_lower = text_stripped.lower()

        # 1. Check for approval responses
        if text_lower in ("approve", "approved", "yes", "confirm"):
            await self._handle_approval(message, "approved")
            return
        if text_lower in ("reject", "rejected", "no", "deny"):
            await self._handle_approval(message, "rejected")
            return

        # 2. Check for task updates (patterns like "task 1 completed", "done", "finished X interviews")
        if self._is_task_update(text_lower):
            await self._handle_task_update(message, text_stripped)
            return

        # 3. Check for status queries
        if any(kw in text_lower for kw in ["status", "progress", "how is", "update on"]):
            await self._handle_status_query(message, text_stripped)
            return

        # 4. Default: Treat as a new innovation idea
        await self._handle_new_innovation(message, text_stripped)

    async def _handle_new_innovation(self, message, text: str):
        """Process a new innovation idea from a channel."""
        channel = getattr(message, "channel", "unknown")
        conversation_id = getattr(message, "conversation_id", "")

        # Create a new innovation project
        project = InnovationProject(
            problem_statement=text,
            title=text[:80] + ("..." if len(text) > 80 else ""),
            status=ProjectStatus.ANALYZING,
        )

        try:
            project = await db_manager.create_project(project)
        except Exception as e:
            logger.error("Failed to create project: %s", e)

        # Create version 1
        version = InnovationVersion(
            project_id=project.id,
            version_number=1,
            problem_statement=text,
        )
        try:
            await db_manager.create_version(version)
        except Exception as e:
            logger.error("Failed to create version: %s", e)

        # Link conversation to project
        from backend.caspian.client import caspian_client
        if conversation_id:
            caspian_client.link_conversation_to_project(conversation_id, project.id)

        # Send acknowledgment
        try:
            message.reply(text=(
                f"🧠 *InnoVerse AI received your innovation idea!*\n\n"
                f"📋 Project ID: `{project.id}`\n"
                f"⏳ Running 11 specialist AI agents...\n\n"
                f"I'll send you the full analysis when complete."
            ))
        except Exception as e:
            logger.error("Failed to send ack: %s", e)

        # Run innovation analysis in background
        if self._innovation_handler:
            try:
                result = await self._innovation_handler(project.id, text)

                # Send results back via channel-appropriate format
                if result:
                    project_data = {
                        "title": project.title,
                        "overall_score": result.get("overall_score", 0),
                        "recommendation": result.get("recommendation", "Pending"),
                        "confidence": result.get("confidence", 0),
                        "executive_summary": result.get("executive_summary", ""),
                        "score_breakdown": result.get("score_breakdown", {}),
                        "top_risks": result.get("top_risks", []),
                        "next_steps": result.get("next_steps", []),
                    }

                    formatted = channel_formatter.format_innovation_summary(channel, project_data)
                    message.reply(**formatted)

                    # If email is connected but this came from Telegram, also send detailed email
                    if channel != "email" and "email" in caspian_client.connected_channels:
                        email_formatted = channel_formatter.format_innovation_summary("email", project_data)
                        # Send via email conversation if we have one
                        # For the demo, reply goes back on source channel
                        logger.info("Detailed email report would be sent for project %s", project.id)

                    # Log outbound communication
                    await db_manager.log_communication(CommunicationEvent(
                        project_id=project.id,
                        channel=ChannelType(channel) if channel in ["telegram", "email", "discord"] else ChannelType.TELEGRAM,
                        direction="outbound",
                        content=f"Innovation analysis complete. Score: {project_data['overall_score']}/100",
                        message_type="report",
                        conversation_id=conversation_id,
                    ))
            except Exception as e:
                logger.error("Innovation analysis failed: %s", e, exc_info=True)
                try:
                    message.reply(text="⚠️ Analysis encountered an error. Our team has been notified.")
                except Exception:
                    pass

    async def _handle_approval(self, message, status: str):
        """Process approval/rejection responses."""
        try:
            pending = await db_manager.get_pending_approvals()
            if pending:
                approval = pending[0]  # Most recent pending
                sender = str(getattr(message, "sender", "user"))
                channel = getattr(message, "channel", "telegram")
                await db_manager.resolve_approval(
                    approval.id, status,
                    approved_by=sender,
                    approved_via=channel,
                )
                emoji = "✅" if status == "approved" else "❌"
                message.reply(text=f"{emoji} Action *{status}*: {approval.action_description}")

                await db_manager.log_communication(CommunicationEvent(
                    project_id=approval.project_id,
                    channel=ChannelType(channel) if channel in ["telegram", "email", "discord"] else ChannelType.TELEGRAM,
                    direction="inbound",
                    content=f"Approval {status}: {approval.action_description}",
                    message_type="approval",
                    conversation_id=getattr(message, "conversation_id", ""),
                ))
            else:
                message.reply(text="ℹ️ No pending approvals found.")
        except Exception as e:
            logger.error("Approval handling error: %s", e)
            message.reply(text="⚠️ Error processing approval.")

    async def _handle_task_update(self, message, text: str):
        """Process task progress updates from users."""
        conversation_id = getattr(message, "conversation_id", "")

        from backend.caspian.client import caspian_client
        project_id = caspian_client.get_project_for_conversation(conversation_id)

        if not project_id:
            message.reply(text="ℹ️ I don't have a project linked to this conversation. Please share your innovation idea first.")
            return

        try:
            tasks = await db_manager.get_tasks(project_id)
            if not tasks:
                message.reply(text="ℹ️ No tasks found for this project.")
                return

            # Try to match and update task
            # Simple heuristic: find first non-completed task
            text_lower = text.lower()
            updated = False

            for task in tasks:
                if task.status == TaskStatus.COMPLETED:
                    continue

                # Check if user mentions this task
                if any(word in text_lower for word in task.title.lower().split()[:3]):
                    # Extract progress numbers if any
                    numbers = re.findall(r'\d+', text)
                    progress = int(numbers[0]) if numbers else 100

                    new_status = "completed" if any(w in text_lower for w in ["done", "completed", "finished", "complete"]) else "in_progress"

                    await db_manager.update_task(
                        task.id,
                        status=new_status,
                        progress=min(progress, 100),
                        progress_detail=text[:200],
                    )
                    updated = True

                    emoji = "✅" if new_status == "completed" else "📊"
                    message.reply(text=f"{emoji} Task updated: *{task.title}*\nStatus: {new_status}\nProgress: {min(progress, 100)}%")
                    break

            if not updated:
                # Update the first pending task
                for task in tasks:
                    if task.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS):
                        await db_manager.update_task(
                            task.id,
                            status="in_progress",
                            progress_detail=text[:200],
                        )
                        message.reply(text=f"📊 Updated task: *{task.title}*\nYour update: {text[:100]}")
                        break

            # Log communication
            await db_manager.log_communication(CommunicationEvent(
                project_id=project_id,
                channel=ChannelType(getattr(message, "channel", "telegram")),
                direction="inbound",
                content=text[:500],
                message_type="update",
                conversation_id=conversation_id,
            ))

        except Exception as e:
            logger.error("Task update error: %s", e)
            message.reply(text="⚠️ Error updating task.")

    async def _handle_status_query(self, message, text: str):
        """Handle status/progress queries."""
        conversation_id = getattr(message, "conversation_id", "")

        from backend.caspian.client import caspian_client
        project_id = caspian_client.get_project_for_conversation(conversation_id)

        if not project_id:
            message.reply(text="ℹ️ No project linked to this conversation. Share an innovation idea to get started!")
            return

        try:
            project = await db_manager.get_project(project_id)
            tasks = await db_manager.get_tasks(project_id)

            if not project:
                message.reply(text="ℹ️ Project not found.")
                return

            completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
            total = len(tasks)

            status_text = (
                f"📊 *Project Status: {project.title}*\n\n"
                f"🎯 Innovation Score: *{project.overall_score or 'N/A'}/100*\n"
                f"📋 Tasks: {completed}/{total} completed\n"
                f"📌 Status: {project.status.value}\n"
            )

            # List pending tasks
            pending = [t for t in tasks if t.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS)]
            if pending:
                status_text += "\n*Pending Tasks:*\n"
                for t in pending[:5]:
                    status_text += f"  • {t.title} ({t.status.value})\n"

            message.reply(text=status_text)

        except Exception as e:
            logger.error("Status query error: %s", e)
            message.reply(text="⚠️ Error fetching status.")

    def _is_task_update(self, text: str) -> bool:
        """Check if message looks like a task update."""
        update_keywords = [
            "completed", "done", "finished", "task", "interview",
            "collected", "built", "validated", "recruited", "tested",
            "progress", "update:", "accomplished",
        ]
        return any(kw in text for kw in update_keywords)


# Singleton
message_router = CaspianMessageRouter()
